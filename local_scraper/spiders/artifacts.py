import scrapy
import os
import pandas as pd
from io import StringIO

class ArtifactsSpider(scrapy.Spider):
    name = "artifacts"
    start_urls = [
        #'https://build.fhir.org/ig/hl7-eu/pcsp/artifacts.html',
        'http://localhost/surpass_fhir/full-ig/site/artifacts.html',
    ]

    def parse(self, response):
        # Seleccionamos los enlaces de los artifacts
        artifact_links = response.css('tr td:first-child a::attr(href)').getall()
        self.log(f'Found {len(artifact_links)} artifact links')

        # Procesar solo los primeros 10 enlaces para pruebas
        for link in artifact_links:
            yield response.follow(link, callback=self.parse_artifact)

    def parse_artifact(self, response):
        # Extraemos el título
        title = response.css('title::text').get().strip() if response.css('title::text').get() else 'Untitled'
        self.log(f'Processing artifact: {title}')

        # Extraemos todas las tablas en formato HTML
        tables = response.css('table').getall()
        self.log(f'Found {len(tables)} tables in {title}')

        # Crear el directorio 'output' si no existe
        output_dir = 'output'
        os.makedirs(output_dir, exist_ok=True)

        # Guardamos los datos en un fichero TXT en el directorio 'output'
        if tables:
            safe_title = "".join(x for x in title if x.isalnum() or x in "._- ")
            filename = os.path.join(output_dir, f"{safe_title}_tables.txt")
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Title: {title}\n\n")
                for table_html in tables:
                    df = pd.read_html(StringIO(table_html))[0]
                    table_str = df.to_string(index=False)
                    f.write(table_str)
                    f.write("\n\n")
            self.log(f'Saved file {filename}')
        else:
            self.log(f'No tables found for {title}')
