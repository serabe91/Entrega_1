# Function to analyze GC and AT content in sequence windows
def analyze_sequence(sequence, window_size=10000):
    """
    Analyze the sequence for GC and AT content in fixed-size windows.

    Parameters:
    - sequence (str): DNA sequence to analyze.
    - window_size (int): Size of the sliding window in base pairs.

    Returns:
    - regions (list of tuples): Each tuple contains:
        - Start position of the window.
        - End position of the window.
        - Band type (R band, G band, or Undetermined).
        - GC percentage.
        - AT percentage.
    """
    regions = []  # List to store results for each window.

    # Loop through the sequence in chunks of `window_size`
    for i in range(0, len(sequence), window_size):
        # Extract a slice of the sequence for this window
        window = sequence[i:i + window_size]

        # Calculate GC content percentage
        gc_content = (window.count("G") + window.count("C")) / len(window) * 100

        # Calculate AT content percentage
        at_content = (window.count("A") + window.count("T")) / len(window) * 100

        # Determine band type based on GC and AT content
        if gc_content > 50:
            band = "R band"  # High GC content
        elif at_content > 50:
            band = "G band"  # High AT content
        else:
            band = "Undetermined"  # Neither dominates

        # Save the results for this window
        regions.append((i + 1, i + len(window), band, round(gc_content, 2), round(at_content, 2)))

    return regions


# Function to read sequences from an input FASTA file
def read_sequences(file_path):
    """
    Reads sequences from a FASTA file, separating chromosomes and plasmids.

    Parameters:
    - file_path (str): Path to the input .fna file.

    Returns:
    - chrom_sequences (list of tuples): Chromosome names and sequences.
    - plasmid_sequences (list of tuples): Plasmid names and sequences.
    """
    chrom_sequences = []  # List to store chromosome names and sequences.
    plasmid_sequences = []  # List to store plasmid names and sequences.

    with open(file_path, "r") as file:
        sequence = ""  # Variable to build the current sequence.
        entry_name = ""  # Variable to store the current entry name.

        # Read the file line by line
        for line in file:
            if line.startswith(">"):  # Line indicates a new entry
                # Save the previous sequence before moving to the next
                if sequence:
                    if "plasmid" in entry_name.lower():
                        plasmid_sequences.append((entry_name, sequence))
                    else:
                        chrom_sequences.append((entry_name, sequence))
                    sequence = ""  # Reset for the next entry
                entry_name = line.strip()  # Save the entry name
            else:
                sequence += line.strip()  # Append sequence data

        # Save the last sequence in the file
        if sequence:
            if "plasmid" in entry_name.lower():
                plasmid_sequences.append((entry_name, sequence))
            else:
                chrom_sequences.append((entry_name, sequence))

    return chrom_sequences, plasmid_sequences


# Function to save analysis results to an output file
def save_results(results, output_file):
    """
    Saves GC/AT analysis results to a file.

    Parameters:
    - results (list of tuples): Analysis results, including regions and content.
    - output_file (str): Path to the output file.
    """
    with open(output_file, "w") as out:
        for name, regions in results:
            out.write(f"{name}\n")
            for start, end, band, gc, at in regions:
                out.write(f"  Start: {start}, End: {end}, {band}, GC%: {gc}, AT%: {at}\n")


# Main script to perform the analysis
try:
    # File paths
    input_file = "Vibrio_Cholerae_Genome.fna"  # Input file path
    output_chromosomes = "chromosomes_analysis.txt"  # Output for chromosomes
    output_plasmids = "plasmids_analysis.txt"  # Output for plasmids

    # Read the sequences
    chromosomes, plasmids = read_sequences(input_file)

    # Analyze chromosomes
    chrom_results = [(name, analyze_sequence(seq)) for name, seq in chromosomes]

    # Analyze plasmids
    plasmid_results = [(name, analyze_sequence(seq)) for name, seq in plasmids]

    # Save results to files
    save_results(chrom_results, output_chromosomes)
    save_results(plasmid_results, output_plasmids)

    print(f"Analysis completed! Results saved to {output_chromosomes} and {output_plasmids}.")

# Handle errors if the input file is missing
except FileNotFoundError:
    print("Error: Input file not found. Please check the file path and try again.")

# Catch any unexpected errors
except Exception as e:
    print(f"An error occurred: {e}")
