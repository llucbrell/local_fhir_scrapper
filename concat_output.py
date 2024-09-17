import pathlib

def concatenar_txt(directorio_origen, archivo_salida):
    """
    Concatena todos los archivos .txt en el directorio especificado y los guarda en un único archivo de salida.

    :param directorio_origen: Ruta del directorio que contiene los archivos .txt
    :param archivo_salida: Nombre del archivo de salida donde se guardará la concatenación
    """
    # Crear objeto Path para el directorio de origen
    path_origen = pathlib.Path(directorio_origen)
    
    # Verificar que el directorio existe
    if not path_origen.is_dir():
        print(f"El directorio {directorio_origen} no existe.")
        return
    
    # Obtener todos los archivos .txt en el directorio
    archivos_txt = list(path_origen.glob('*.txt'))
    
    if not archivos_txt:
        print(f"No se encontraron archivos .txt en el directorio {directorio_origen}.")
        return
    
    # Ruta completa para el archivo de salida
    ruta_salida = path_origen / archivo_salida
    
    try:
        with ruta_salida.open('w', encoding='utf-8') as salida:
            for archivo in archivos_txt:
                with archivo.open('r', encoding='utf-8') as f:
                    contenido = f.read()
                    salida.write(contenido)
                    salida.write('\n')  # Añadir una nueva línea entre archivos
        print(f"Archivos concatenados exitosamente en {ruta_salida}")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    # Especifica el directorio de origen y el nombre del archivo de salida
    directorio = 'D:/Desarrollo/Web/sandbox/ia/chats-llms/surpass_scrapper/local_scraper/output_partners'  # Reemplaza con la ruta de tu directorio
    salida = 'D:/Desarrollo/Web/sandbox/ia/chats-llms/surpass_scrapper/local_scraper/final_conc_output_data/output_partners_concat.txt'         # Nombre del archivo de salida

    concatenar_txt(directorio, salida)
