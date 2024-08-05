import scrapy
import os
import pandas as pd
from bs4 import BeautifulSoup

class TerminologyContentSpider(scrapy.Spider):
    name = "artifacts_terminology"
    start_urls = [
        'http://localhost/surpass_fhir/full-ig/site/terminology.html'
    ]

    def parse(self, response):
        # Seleccionamos los enlaces de terminology dentro de Value Sets
        terminology_links = response.css('h3#value-sets + p + ul li a::attr(href)').getall()
        self.log(f'Found {len(terminology_links)} terminology links')

        # Procesar todos los enlaces
        for link in terminology_links:
            yield response.follow(link, callback=self.parse_terminology_content)

    def parse_terminology_content(self, response):
        # Extraemos el título
        title = response.css('title::text').get().strip() if response.css('title::text').get() else 'Untitled'
        self.log(f'Processing terminology content: {title}')

        # Extraemos la descripción (asumimos que es el primer párrafo)
        description = response.css('p::text').get().strip() if response.css('p::text').get() else 'No description found'

        # Extraemos todas las tablas
        tables_html = response.css('table').getall()
        if not tables_html:
            self.log(f'No tables found in {title}')
            return
        
        tables_text = [self.extract_table_text(table_html) for table_html in tables_html]

        # Crear el directorio 'output_content' si no existe
        output_dir = 'output_terminology'
        os.makedirs(output_dir, exist_ok=True)

        # Guardamos las tablas en un fichero TXT en el directorio 'output_content'
        safe_title = "".join(x for x in title if x.isalnum() or x in "._- ")
        filename = os.path.join(output_dir, f"{safe_title}.txt")
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Title: {title}\n\n")
            f.write(f"Description: {description}\n\n")
            for i, table_text in enumerate(tables_text):
                f.write(f"Table {i+1}:\n")
                f.write(table_text)
                f.write("\n\n")

        self.log(f'Saved file {filename}')

    def extract_table_text(self, table_html):
        soup = BeautifulSoup(table_html, 'html.parser')
        table = soup.find('table')

        # Convert the HTML table to a pandas DataFrame
        try:
            df = pd.read_html(str(table))[0]
        except ValueError:
            return "No valid table found"

        # Format the DataFrame into the desired string format
        table_text = df.to_string(index=False)

        return table_text
