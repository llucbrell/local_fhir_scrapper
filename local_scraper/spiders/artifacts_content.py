import scrapy
import os
from bs4 import BeautifulSoup
import pandas as pd

class ArtifactsContentSpider(scrapy.Spider):
    name = "artifacts_content"
    start_urls = [
        #'https://build.fhir.org/ig/hl7-eu/pcsp/artifacts.html',
        'http://localhost/surpass_fhir/full-ig/site/artifacts.html'
    ]

    def parse(self, response):
        # Seleccionamos los enlaces de los artifacts
        artifact_links = response.css('tr td:first-child a::attr(href)').getall()
        self.log(f'Found {len(artifact_links)} artifact links')

        # Procesar todos los enlaces
        for link in artifact_links:  # Para pruebas, limitamos a los primeros 2 enlaces
            yield response.follow(link, callback=self.parse_artifact_content)

    def parse_artifact_content(self, response):
        # Extraemos el título
        title = response.css('title::text').get().strip() if response.css('title::text').get() else 'Untitled'
        self.log(f'Processing artifact content: {title}')

        # Extraemos la tabla con clase 'colsd'
        table_html = response.css('table.colsd').get()
        table_text = self.extract_table_text(table_html)

        # Extraemos el texto del tercer párrafo en el contexto correcto
        third_paragraph_text = self.extract_third_paragraph_text(response)

        # Seguimos el enlace de definición para extraer la tabla 'dict'
        definitions_link = response.url.replace('.html', '-definitions.html')
        request = scrapy.Request(definitions_link, callback=self.parse_definitions)
        request.meta['title'] = title
        request.meta['table_text'] = table_text
        request.meta['third_paragraph_text'] = third_paragraph_text

        yield request

    def parse_definitions(self, response):
        title = response.meta['title']
        table_text = response.meta['table_text']
        third_paragraph_text = response.meta['third_paragraph_text']

        # Extraemos la tabla con clase 'dict'
        dict_table_html = response.css('table.dict').get()
        dict_table_text = self.extract_dict_table_text(dict_table_html)

        # Crear el directorio 'output_content' si no existe
        output_dir = 'output_content'
        os.makedirs(output_dir, exist_ok=True)

        # Guardamos los datos en un fichero TXT en el directorio 'output_content'
        safe_title = "".join(x for x in title if x.isalnum() or x in "._- ")
        filename = os.path.join(output_dir, f"{safe_title}.txt")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Title: {title}\n\n")
            f.write("Header Table:\n")
            f.write(table_text)
            f.write("\n\nThird Paragraph:\n")
            f.write(third_paragraph_text)
            f.write("\n\nDict Table:\n")
            f.write(dict_table_text)
        
        self.log(f'Saved file {filename}')

    def extract_table_text(self, table_html):
        if not table_html:
            return "No table found"

        soup = BeautifulSoup(table_html, 'html.parser')
        table = soup.find('table')
        
        # Convert the HTML table to a pandas DataFrame
        df = pd.read_html(str(table))[0]

        # Format the DataFrame into the desired string format
        table_text = ""
        for index, row in df.iterrows():
            for col in df.columns:
                table_text += f"- {col} : {row[col]}\n"

        return table_text

    def extract_third_paragraph_text(self, response):
        paragraphs = response.css('p').getall()
        if len(paragraphs) >= 4:
            third_paragraph_html = paragraphs[3]
            soup = BeautifulSoup(third_paragraph_html, 'html.parser')
            third_paragraph_text = soup.get_text()
        else:
            third_paragraph_text = "No third paragraph found"
        return third_paragraph_text

    def extract_dict_table_text(self, dict_table_html):
        if not dict_table_html:
            return "No dict table found"

        soup = BeautifulSoup(dict_table_html, 'html.parser')
        table = soup.find('table')
        
        # Convert the HTML table to a pandas DataFrame
        df = pd.read_html(str(table))[0]

        # Format the DataFrame into the desired string format
        dict_table_text = df.to_string(index=False)
        
        return dict_table_text
