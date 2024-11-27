def leer_fasta(archivo_fasta):
    """
    Lee un archivo FASTA y devuelve un diccionario con las secuencias.
    Clave: ID de la secuencia.
    Valor: Secuencia nucleotídica.
    """
    secuencias = {}
    with open(archivo_fasta, "r") as archivo:
        id_secuencia = ""
        secuencia = []
        for linea in archivo:
            if linea.startswith(">"):  # Identificador de secuencia
                if id_secuencia:
                    secuencias[id_secuencia] = "".join(secuencia)
                id_secuencia = linea[1:].strip()
                secuencia = []
            else:
                secuencia.append(linea.strip())
        if id_secuencia:
            secuencias[id_secuencia] = "".join(secuencia)
    return secuencias


def contenido_gc(secuencia):
    """
    Calcula el porcentaje de GC de una secuencia.
    """
    g = secuencia.count("G")
    c = secuencia.count("C")
    total = len(secuencia)
    return (g + c) / total * 100 if total > 0 else 0


def identificar_regiones(secuencia, tam_bloque=1000, tam_cds=500):
    """
    Divide la secuencia en bloques de regiones codificantes y no codificantes.
    Alterna bloques codificantes y no codificantes, y devuelve el rango de posiciones.
    """
    regiones_codificantes = []
    regiones_no_codificantes = []

    for i in range(0, len(secuencia), tam_bloque):
        if (i // tam_bloque) % 2 == 0:  # Cada dos bloques, se asume codificante
            fin = i + tam_cds
            regiones_codificantes.append((i + 1, fin))
        else:
            fin = i + tam_bloque
            regiones_no_codificantes.append((i + 1, fin))

    return regiones_codificantes, regiones_no_codificantes


def analizar_genoma(archivo_fasta, archivo_salida):
    """
    Analiza el genoma en un archivo FASTA, identifica las regiones codificantes y no codificantes,
    y guarda el resultado en un archivo de salida.
    """
    secuencias = leer_fasta(archivo_fasta)

    with open(archivo_salida, "w") as salida:
        for id_secuencia, secuencia in secuencias.items():
            longitud_total = len(secuencia)
            gc_total = contenido_gc(secuencia)

            salida.write(f"Analizando secuencia: {id_secuencia}\n")
            salida.write(f"Longitud total: {longitud_total} bases\n")
            salida.write(f"Contenido GC: {gc_total:.2f}%\n")

            # Identificar regiones codificantes y no codificantes
            regiones_codificantes, regiones_no_codificantes = identificar_regiones(secuencia)

            salida.write("\n--- Análisis de regiones ---\n")

            salida.write(f"Regiones codificantes: {len(regiones_codificantes)}\n")
            for idx, (inicio, fin) in enumerate(regiones_codificantes, 1):
                salida.write(f"  Región codificante {idx}: Desde {inicio} hasta {fin}\n")

            salida.write(f"\nRegiones no codificantes: {len(regiones_no_codificantes)}\n")
            for idx, (inicio, fin) in enumerate(regiones_no_codificantes, 1):
                salida.write(f"  Región no codificante {idx}: Desde {inicio} hasta {fin}\n")
            salida.write("\n")


# Archivo FASTA de entrada y archivo de salida
fasta_file = "Vibrio_Cholerae_Genome.fna"
archivo_salida = "analisis_genoma.txt"
analizar_genoma(fasta_file, archivo_salida)


