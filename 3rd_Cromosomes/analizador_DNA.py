import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Función para analizar la secuencia de ADN
def analizar_secuencia(secuencia, tamaño_ventana=10000):
    """
    Divide la secuencia en ventanas de un tamaño dado y calcula los porcentajes de GC y AT para cada ventana.
    """
    regiones = []  # Lista para almacenar los resultados del análisis de ventanas
    for inicio in range(0, len(secuencia) - tamaño_ventana + 1, tamaño_ventana):
        ventana = secuencia[inicio:inicio + tamaño_ventana]
        conteo_g = ventana.count("G")
        conteo_c = ventana.count("C")
        conteo_a = ventana.count("A")
        conteo_t = ventana.count("T")
        contenido_gc = (conteo_g + conteo_c) / len(ventana) * 100
        contenido_at = (conteo_a + conteo_t) / len(ventana) * 100
        regiones.append({"GC%": contenido_gc, "AT%": contenido_at})
    return regiones

# Función para guardar los resultados en un archivo de texto
def guardar_resultados_en_archivo(resultados, nombre_archivo_salida):
    """
    Escribe los resultados del análisis en un archivo de texto, incluyendo la asignación de bandas R o G.
    """
    with open(nombre_archivo_salida, "w") as archivo_salida:
        for secuencia in resultados:
            archivo_salida.write(f"{secuencia['nombre']}\n")
            conteo_bandas_r = 0
            conteo_bandas_g = 0

            for indice_region, region in enumerate(secuencia["regiones"], 1):
                gc = region["GC%"]
                at = region["AT%"]
                tipo_banda = "GC Band" if gc > at else "AT Band"
                banda = "G" if tipo_banda == "GC Band" else "R"
                archivo_salida.write(
                    f"  Región {indice_region} - {tipo_banda}: GC% = {gc:.4f}, AT% = {at:.4f} ----> Banda: {banda}\n"
                )
                if banda == "G":
                    conteo_bandas_g += 1
                else:
                    conteo_bandas_r += 1

            archivo_salida.write(f"  Resumen para {secuencia['nombre']}:\n")
            archivo_salida.write(f"    Total de Bandas G: {conteo_bandas_g}\n")
            archivo_salida.write(f"    Total de Bandas R: {conteo_bandas_r}\n")

# Función para crear un histograma general para cromosomas o plásmidos
def crear_histograma(resultados, titulo, etiqueta_x, etiqueta_y, archivo_salida_pdf):
    """
    Genera gráficos de barras para los porcentajes de GC y AT de cada cromosoma o plásmido y los guarda en un archivo PDF.
    """
    with PdfPages(archivo_salida_pdf) as pdf_pages:
        for secuencia in resultados:
            fig, ax = plt.subplots(figsize=(10, 6))

            porcentajes_gc = [region["GC%"] for region in secuencia["regiones"]]
            porcentajes_at = [region["AT%"] for region in secuencia["regiones"]]

            ancho_barras = 0.35  # Ancho de las barras
            indices_regiones = range(len(porcentajes_gc))
            ax.bar(indices_regiones, porcentajes_gc, ancho_barras, label='GC%', color='green')
            ax.bar(
                [indice + ancho_barras for indice in indices_regiones],
                porcentajes_at,
                ancho_barras,
                label='AT%',
                color='blue',
            )

            ax.set_xlabel(etiqueta_x)
            ax.set_ylabel(etiqueta_y)
            ax.set_title(f'{titulo} - {secuencia["nombre"]}')
            ax.set_xticks([indice + ancho_barras / 2 for indice in indices_regiones])
            ax.set_xticklabels([])  # Eliminar etiquetas en el eje X
            ax.legend()

            pdf_pages.savefig(fig)
            plt.close(fig)

# Función principal
def main():
    archivo_entrada = "Vibrio_Cholerae_Genome.fna"
    archivo_salida_cromosomas = "chromosomes_analysis.txt"
    archivo_salida_plásmidos = "plasmids_analysis.txt"

    resultados_cromosomas = []
    resultados_plásmidos = []

    try:
        with open(archivo_entrada, "r") as archivo:
            secuencia_actual = ""
            nombre_entrada_actual = ""

            for linea in archivo:
                if linea.startswith(">"):
                    if secuencia_actual:
                        secuencia_filtrada = secuencia_actual.upper()  # Convertir a mayúsculas
                        entrada = {
                            "nombre": nombre_entrada_actual,
                            "regiones": analizar_secuencia(secuencia_filtrada),
                        }
                        if "plasmid" in nombre_entrada_actual.lower():
                            resultados_plásmidos.append(entrada)
                        else:
                            resultados_cromosomas.append(entrada)
                    secuencia_actual = ""
                    nombre_entrada_actual = linea.strip()
                else:
                    secuencia_actual += linea.strip()

            if secuencia_actual:
                secuencia_filtrada = secuencia_actual.upper()
                entrada = {
                    "nombre": nombre_entrada_actual,
                    "regiones": analizar_secuencia(secuencia_filtrada),
                }
                if "plasmid" in nombre_entrada_actual.lower():
                    resultados_plásmidos.append(entrada)
                else:
                    resultados_cromosomas.append(entrada)

        guardar_resultados_en_archivo(resultados_cromosomas, archivo_salida_cromosomas)
        guardar_resultados_en_archivo(resultados_plásmidos, archivo_salida_plásmidos)

        crear_histograma(
            resultados_cromosomas,
            "Análisis de Cromosomas",
            "Regiones",
            "Porcentaje",
            "chromosomes_histogram.pdf",
        )
        crear_histograma(
            resultados_plásmidos,
            "Análisis de Plásmidos",
            "Regiones",
            "Porcentaje",
            "plasmids_histogram.pdf",
        )

        print(f"Análisis completado. Resultados guardados en {archivo_salida_cromosomas} y {archivo_salida_plásmidos}")

    except FileNotFoundError:
        print("Error: El archivo de entrada no fue encontrado. Por favor verifica la ruta y vuelve a intentarlo.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

# Ejecutar el programa principal
if __name__ == "__main__":
    main()




