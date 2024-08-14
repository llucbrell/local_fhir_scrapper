# FHIR SurPass IG Scrapers

This repo contains some scrapers used locally to get info from the FHIR IG due to feed some Language Models with data. The objective of this code is to get data in plain text format to work with some LMs within some experimental contexts. Aslo this repo contains a spider to extract partner info data from surpass website.

## Download and Server Installation

To begin, you need to download the complete FHIR Implementation Guide and set up an Apache HTTP server to serve the files locally. Here are the detailed steps:

1. **Download the FHIR Implementation Guide**: You can download the complete guide from the following link:
   [FHIR Implementation Guide](https://build.fhir.org/ig/hl7-eu/pcsp/downloads.html#full-ig)

2. **Install Apache HTTP Server**: We recommend using XAMPP, which is an easy-to-install and configure solution. You can download XAMPP from the following link:
   [XAMPP](https://www.apachefriends.org/index.html)

3. **Configure the Server**:
   - Once you have installed XAMPP, place the implementation guide files in the `htdocs` folder of the XAMPP installation directory.
   - Ensure that the Apache server is running. You can do this through the XAMPP control panel.


## Spider use
There are 3 scrappy spiders, to run you have to use this commands.

To install dependencies

```shell
pip install -r requirements.txt
```

To run one spider and get the info.

```shell
scrapy crawl <spider_name>
```

## Scraper Descriptions

Below are the descriptions of the various scrapers developed to extract information from the FHIR Implementation Guide:

### Artifacts Scraper

This scraper extracts all data related to tables containing information on resource construction from all links on the `artifacts.html` page.

### Detailed Descriptions Scraper

This scraper extracts all information from the detailed descriptions (`detailed descriptions`) on the `artifacts.html` page.

### Logical Models Scraper

This scraper extracts the detailed description of all logical models present in the implementation guide.

### Terminology Scraper

This scraper extracts tables and information related to the terminology used in the implementation guide.

## Output Directories

Each of the scrapers saves the extracted data in different directories as text files. These directories are automatically created in the root of the project and are named according to the type of information extracted.

## Responsible Use

These scrapers should not be used to scrape any website without permission. If you decide to use them, make sure to enable appropriate measures in the `settings.py` file to respect the site's policies and avoid overloading the servers.

# Scrapers de la Guía de Implementación FHIR del proyecto SurPass

Este repositorio contiene algunos scrapers utilizados localmente para obtener información de la Guía de Implementación FHIR con el fin de alimentar algunos Modelos de Lenguaje con datos. El objetivo de este código es obtener datos en formato de texto plano para trabajar con algunos ML en contextos experimentales.

## Descarga e Instalación del Servidor

Para empezar, necesitas descargar la guía de implementación FHIR completa y configurar un servidor Apache HTTP para servir los archivos localmente. Aquí te dejamos los pasos detallados:

1. **Descargar la Guía de Implementación FHIR**: Puedes descargar la guía completa desde el siguiente enlace:
   [Guía de Implementación FHIR](https://build.fhir.org/ig/hl7-eu/pcsp/downloads.html#full-ig)

2. **Instalar Servidor Apache HTTP**: Nosotros recomendamos usar XAMPP, que es una solución fácil de instalar y configurar. Puedes descargar XAMPP desde el siguiente enlace:
   [XAMPP](https://www.apachefriends.org/index.html)

3. **Configurar el Servidor**:
   - Una vez que hayas instalado XAMPP, coloca los archivos de la guía de implementación en la carpeta `htdocs` del directorio de instalación de XAMPP.
   - Asegúrate de que el servidor Apache esté en ejecución. Puedes hacerlo a través del panel de control de XAMPP.

## Uso
Hay 3 spiders de scrapy, para ejecutarlos tienes que hacer.

Para instalar las dependencias

```shell
pip install -r requirements.txt
```

Para ejecutar un spider en concreto.

```shell
scrapy crawl <spider_name>
```

## Descripción de los Scrapers

A continuación, se detallan los diferentes scrapers desarrollados para extraer la información de la guía de implementación FHIR:

### Scraper de Artifacts

Este scraper extrae todos los datos relativos a las tablas con la información de la construcción de los recursos de todos los enlaces en la página `artifacts.html`.

### Scraper de Detailed Descriptions

Este scraper extrae toda la información de las descripciones detalladas (`detailed descriptions`) de la página `artifacts.html`.

### Scraper de Logical Models

Este scraper extrae la descripción detallada de todos los modelos lógicos (`logical models`) presentes en la guía de implementación.

### Scraper de Terminología

Este scraper extrae las tablas y la información relativa a la terminología usada en la guía de implementación.

## Directorios de Salida

Cada uno de los scrapers guarda los datos extraídos en diferentes directorios como archivos de texto. Estos directorios se crean automáticamente en la raíz del proyecto y se nombran de acuerdo al tipo de información extraída.

## Uso Responsable

Estos scrapers no deben ser utilizados para scrapear ninguna web sin permiso. Si decides usarlos, asegúrate de activar las medidas apropiadas en el archivo `settings.py` para respetar las políticas del sitio web y evitar sobrecargar los servidores.
