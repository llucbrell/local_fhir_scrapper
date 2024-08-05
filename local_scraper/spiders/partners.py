import scrapy
import os

class PartnersSpider(scrapy.Spider):
    name = "partners"
    start_urls = [
        'https://www.pancaresurpass.eu/'
    ]

    def parse(self, response):
        # Seleccionamos los enlaces del navbar
        navbar_links = response.css('.fusion-main-menu a::attr(href)').getall()
        self.log(f'Found {len(navbar_links)} navbar links')

        # Procesar los enlaces del navbar
        for link in navbar_links:
            yield response.follow(link, callback=self.parse_navbar_page)

    def parse_navbar_page(self, response):
        # Extraemos el título
        title = response.css('title::text').get().strip() if response.css('title::text').get() else 'Untitled'
        self.log(f'Processing page: {title}')

        # Extraer el contenido específico del div 'fusion-content-tb fusion-content-tb-1'
        content_div = response.css('div.fusion-content-tb.fusion-content-tb-1')
        header = content_div.css('h2::text').get()
        paragraphs = content_div.xpath('.//text()[not(ancestor::h2)]').getall()

        page_text = [header.strip()] if header else []
        page_text.extend([p.strip() for p in paragraphs if p.strip()])
        page_text = "\n".join(page_text)

        # Crear el directorio 'output_partners' si no existe
        output_dir = 'output_partners'
        os.makedirs(output_dir, exist_ok=True)

        # Guardar el texto de la página en un fichero TXT en el directorio 'output_partners'
        safe_title = "".join(x for x in title if x.isalnum() or x in "._- ")
        filename = os.path.join(output_dir, f"{safe_title}.txt")
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Title: {title}\n\n")
            f.write(page_text)
        
        self.log(f'Saved file {filename}')

        # Si la página es la de partners, extraemos los enlaces de los partners
        if "partners" in response.url:
            partner_links = response.css('ul.sub-menu a::attr(href)').getall()
            self.log(f'Found {len(partner_links)} partner links on {title}')
            for link in partner_links:
                yield response.follow(link, callback=self.parse_partner_page)

    def parse_partner_page(self, response):
        # Extraemos el título
        title = response.css('title::text').get().strip() if response.css('title::text').get() else 'Untitled'
        self.log(f'Processing partner page: {title}')

        # Extraer el contenido específico del div 'fusion-content-tb fusion-content-tb-1'
        content_div = response.css('div.fusion-content-tb.fusion-content-tb-1')
        header = content_div.css('h2::text').get()
        paragraphs = content_div.xpath('.//text()[not(ancestor::h2)]').getall()

        page_text = [header.strip()] if header else []
        page_text.extend([p.strip() for p in paragraphs if p.strip()])
        page_text = "\n".join(page_text)

        # Crear el directorio 'output_partners' si no existe
        output_dir = 'output_partners'
        os.makedirs(output_dir, exist_ok=True)

        # Guardar el texto de la página en un fichero TXT en el directorio 'output_partners'
        safe_title = "".join(x for x in title if x.isalnum() or x in "._- ")
        filename = os.path.join(output_dir, f"{safe_title}.txt")
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Title: {title}\n\n")
            f.write(page_text)
        
        self.log(f'Saved file {filename}')
