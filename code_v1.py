def analyze_sequence(sequence, window_size=3500):
    """
    Analyze the sequence for GC and AT content in sliding windows.

    Parameters:
    - sequence (str): DNA sequence to analyze.
    - window_size (int): Size of the sliding window in base pairs

    Returns:
    - regions (list of tuples): List of tuples containing:
        - Start position of the window.
        - End position of the window.
        - Band type (R band, G band, or Undetermined).
        - GC percentage.
        - AT percentage.
    """
    regions = []  # List to store analysis results for each window
    for i in range(0, len(sequence) - window_size + 1, window_size):
        # Extract a window of the specified size
        window = sequence[i:i + window_size]

        # Calculate GC content as a percentage
        gc_content = (window.count("G") + window.count("C")) / len(window) * 100

        # Calculate AT content as a percentage
        at_content = (window.count("A") + window.count("T")) / len(window) * 100

        # Determine the band type based on GC and AT content
        if gc_content > 50:
            band = "R band"  # High GC content
        elif at_content > 50:
            band = "G band"  # High AT content
        else:
            band = "Undetermined"  # Neither GC nor AT dominates

        # Store the results for this window
        regions.append((i + 1, i + window_size, band, round(gc_content, 2), round(at_content, 2)))
    return regions