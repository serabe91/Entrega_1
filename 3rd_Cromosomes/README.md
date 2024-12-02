# Análisis de Secuencias de ADN en Bandas Cromosómicas

Este proyecto realiza un análisis de secuencias de ADN, calculando los porcentajes de contenido GC (guanina + citosina) y AT (adenina + timina) en regiones específicas y catalogando como bandas G y R, respectivamente. Los resultados se dividen entre cromosomas y plásmidos, se guardan en archivos de texto y se generan histogramas en formato PDF.

![Flujograma_code](https://github.com/serabe91/Entrega_1/blob/master/3rd_Cromosomes/document_pfuncion/diagrama_flujo_codigo.png)

## Características

- **Análisis por ventanas**: Divide las secuencias en ventanas de tamaño fijo y calcula el porcentaje de GC y AT en cada una.
- **Clasificación por tipo**: Diferencia entre cromosomas y plásmidos según los nombres de las secuencias.
- **Asignación de bandas**: Determina si cada ventana pertenece a una banda GC ("G") o AT ("R").
- **Visualización**: Genera gráficos en formato PDF para analizar los porcentajes.

## Requisitos

- **Python 3.12**
- Librería **matplotlib**:
  ```bash
  pip install matplotlib
  ```

## Archivos del Proyecto

- **`analizador_DNA.py`**: Código principal del programa.
- **`Vibrio_Cholerae_Genome.fna`**: Archivo de entrada con las secuencias de ADN (en formato FASTA).
Se usó este genoma de poco tamaño para fácil testeo del código, pero se adjunta también otro genoma de mayor extensión (*Saccharomyces cerevisiae S288C*) para una prueba más extensiva
(Extraídos de GenBank, NCBI; Accesion codes: GCF_008369605.1, GCF_000146045.2)
- **`chromosomes_analysis.txt`**: Resultados del análisis de los cromosomas.
- **`plasmids_analysis.txt`**: Resultados del análisis de los plásmidos.
- **`chromosomes_histogram.pdf`**: Histogramas de porcentajes GC y AT para los cromosomas.
- **`plasmids_histogram.pdf`**: Histogramas de porcentajes GC y AT para los plásmidos.

## Uso

1. Coloca el archivo `Vibrio_Cholerae_Genome.fna` en el mismo directorio que el script.
   (o el archivo que se desee analizar, reemplazando su nombre y su extensión pero teniendo en cuenta la ubicación correcta del archivo)
3. Ejecuta el programa principal:
   ```bash
   python analizador_adn.py
   ```
4. Los resultados se guardarán en archivos de texto y se generarán gráficos en PDF.

## Funciones del Código
En caso de querer una explicación más extensa de las partes de cada función, esto se encuentra adjunto en: [documentación funciones](https://github.com/serabe91/Entrega_1/tree/752cd09941b5a62d27f2935e16b6c6ef0da55204/3rd_Cromosomes/document_pfuncion)

### `analizar_secuencia(secuencia, tamaño_ventana=10000)`
- Divide la secuencia en ventanas y calcula el porcentaje de GC y AT por ventana (tamaño predeterminado 10.000 nt, se ajustará de acuerdo al genoma por analizar).
- **Entrada**:
  - `secuencia`: Secuencia de ADN a analizar.
  - `tamaño_ventana`: Tamaño de cada ventana.
- **Salida**: Lista con porcentajes de GC y AT para cada ventana.

### `guardar_resultados_en_archivo(resultados, nombre_archivo_salida)`
- Guarda los resultados en un archivo de texto, incluyendo la asignación de bandas GC y AT.
- **Entrada**:
  - `resultados`: Datos analizados de las secuencias.
  - `nombre_archivo_salida`: Nombre del archivo de salida.

### `crear_histograma(resultados, titulo, etiqueta_x, etiqueta_y, archivo_salida_pdf)`
- Genera histogramas para los porcentajes de GC y AT y los guarda en un PDF.
- **Entrada**:
  - `resultados`: Resultados del análisis.
  - `titulo`: Título del gráfico.
  - `etiqueta_x`: Etiqueta del eje X.
  - `etiqueta_y`: Etiqueta del eje Y.
  - `archivo_salida_pdf`: Nombre del archivo PDF.

### `main()`
- Función principal que coordina el análisis, guarda los resultados y genera gráficos.

## Archivos de Salida

- **`chromosomes_analysis.txt`**:
  - Contiene el análisis de las regiones de los cromosomas, indicando porcentajes de GC y AT por ventana y el número de bandas GC ("G") y AT ("R").
- **`plasmids_analysis.txt`**:
  - Contiene el análisis de las regiones de los plásmidos con el mismo formato.
- **`chromosomes_histogram.pdf`**:
  - Archivo PDF con gráficos de barras de los porcentajes de GC y AT para cada región de los cromosomas.
- **`plasmids_histogram.pdf`**:
  - Archivo PDF con gráficos de barras de los porcentajes de GC y AT para cada región de los plásmidos.
 

### Ejemplo de Resultados
```
>Cromosoma 1
  Región 1 - GC Band: GC% = 53.4567, AT% = 46.5433 ----> Banda: G
  Región 2 - AT Band: GC% = 45.6789, AT% = 54.3211 ----> Banda: R
  Resumen para Cromosoma 1:
    Total de Bandas G: 1
    Total de Bandas R: 1
```

## Manejo de Errores

- **Archivo no encontrado**: Si el archivo de entrada no existe, se muestra un mensaje de error.
- **Errores generales**: Muestra detalles del error para facilitar su resolución.

## Licencia

Este proyecto está licenciado bajo la [Licencia MIT](https://github.com/serabe91/Entrega_1/blob/e8ebc72b33d53a0c5004afce9b42a501bd7a674a/3rd_Cromosomes/LICENSE).
