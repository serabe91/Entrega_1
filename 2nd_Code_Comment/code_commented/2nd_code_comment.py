# The fasta_data class which holds and processes DNA sequences in multi-FASTA format.
class fasta_data:
    # Initializer that takes a file name, reads the file and organizes the data.
    def __init__(self, file_name):
        # Reads the entire file content
        self.f = open(file_name).read()
        self.records = {}
        self.id = ""
        # Processes each line of the file content
        for line in self.f.splitlines():
            # If the line is a header line (starts with ">")
            if line.startswith(">"):
                # If there was a previous sequence, save it to the records
                if self.id != "":
                    self.records[self.id] = self.seq
                # Extracts the identifier from the header line and resets the sequence
                self.id = line.split(" ")[0][1:]
                self.seq = ""
            # If the line is a sequence line, append it to the current sequence
            else:
                self.seq += line.strip()

    # Getter methods for accessing basic data
    def get_records(self):
        return self.records

    def get_id(self):
        return self.records.keys()

    def get_seq(self):
        return self.records.values()

    # Task 1: How many records are in the file?
    def reads_number(self):
        return len(self.records)

    # Task 2: What are the lengths of the sequences in the file?
    def get_lengths(self):
        length = {}
        # Calculate the length for each sequence
        for id, seq in self.records.items():
            length[id] = len(seq)
        # Find the shortest and longest sequences and their identifiers
        min_length = min(length.values())
        max_length = max(length.values())
        min_ids = [id for id, seq_len in length.items() if seq_len == min_length]
        max_ids = [id for id, seq_len in length.items() if seq_len == max_length]
        return length, min_length, max_length, min_ids, max_ids

    # Task 3: Identify all ORFs in each sequence and find the longest one
    def reading_frames(self, frame):
        start_codon = 'ATG'
        stop_codons = ['TAA', 'TAG', 'TGA']
        orfs = {}
        # Process each sequence
        for id, sequence in self.records.items():
            frame_seq = sequence[frame-1:]
            orfs[id] = []
            # Check each codon in the sequence
            for i in range(0, len(frame_seq), 3):
                # If the codon is a start codon
                if frame_seq[i:i+3] == start_codon:
                    # Check the rest codons in the sequence
                    for j in range(i+3, len(frame_seq), 3):
                        # If the codon is a stop codon
                        if frame_seq[j:j+3] in stop_codons:
                            # Record the ORF
                            orfs[id].append((i+1, j+3, frame_seq[i:j+3]))
                            break
        # Find the longest ORF
        longest_orf = max((tuple(list(orf) + [id]) for id, orfs_list in orfs.items() for orf in orfs_list), key=lambda x: x[1] - x[0])
        return orfs, longest_orf

    # Task 4: Identify all repeats of length n in all sequences
    def repeats(self, n):
        repeats = {}
        # Process each sequence
        for sequence in self.records.values():
            # Check each possible repeat in the sequence
            for i in range(len(sequence) - n + 1):
                # If the repeat is already recorded
                if sequence[i:i+n] in repeats:
                    # Increase the count
                    repeats[sequence[i:i+n]] += 1
                else:
                    # Record the repeat
                    repeats[sequence[i:i+n]] = 1
        # Find the most common repeat
        most_common = max(repeats.items(), key=lambda x: x[1])
        return repeats, most_common

# Create an instance of the fasta_data class with the file "dna.example.fasta"
reads = fasta_data("dna.example.fasta")
records = reads.get_records()

# Part 1: Print out the number of records
reads_number = reads.reads_number()
print("number of records: " + str(reads_number))

# Part 2: Print out the minimum and maximum lengths of sequences and their identifiers
records_lengths = reads.get_lengths()
print("minimum length: " + str(records_lengths[1]))
print("maximum length: " + str(records_lengths[2]))
print("minimum ids: " + str(records_lengths[3]))
print("maximum ids: " + str(records_lengths[4]))

# Part 3: Print out the longest ORFs in each frame and their starting positions,
# and the identifier of the sequence containing the longest ORF in frame 1
orfs1, longest_orf1 = reads.reading_frames(1)
orfs2, longest_orf2 = reads.reading_frames(2)
orfs3, longest_orf3 = reads.reading_frames(3)
print("longest ORF in frame 1: " + str(longest_orf1[:2]))
print("longest ORF in frame 2: " + str(longest_orf2[:2]))
print("longest ORF in frame 3: " + str(longest_orf3[:2]))
print("longest ORF in frame 1 id: " + str(longest_orf1[-1]))

# Part 4: Print out the most common repeats of lengths ranging from 5 to 20 in the sequences
for i in range(5,20):
    repeat, most_common = reads.repeats(i)
    print(str(i) + " most common: " + str(most_common))



final_reads = fasta_data("dna2.fasta")
orfs1, longest_orf1 = final_reads.reading_frames(1)
print("longest ORF in frame 1: " + str(longest_orf1[1]-longest_orf1[0] + 1))
orfs2, longest_orf2 = final_reads.reading_frames(2)
print("longest ORF in frame 2: " + str(longest_orf2[1]-longest_orf2[0] + 1))
orfs3, longest_orf3 = final_reads.reading_frames(3)
print("longest ORF in frame 3: " + str(longest_orf3[:2]))
print("longest ORF in frame 3: " + str(longest_orf3[1]-longest_orf3[0] + 1))
lengths = []
lengths.append(max( (repeats[1]-repeats[0] + 1 for repeats in orfs1["gi|142022655|gb|EQ086233.1|16"])))
lengths.append(max( (repeats[1]-repeats[0] + 1 for repeats in orfs2["gi|142022655|gb|EQ086233.1|16"])))
lengths.append(max( (repeats[1]-repeats[0] + 1 for repeats in orfs3["gi|142022655|gb|EQ086233.1|16"])))

orfs4, longest_orf4 = final_reads.reading_frames(2)
print("longest ORF in frame 4: " + str(longest_orf4[:2]))
print(lengths )

repeat, most_common = final_reads.repeats(12)
seqs = []
for seq, reap in repeat.items():
    if reap == most_common[1]:
        seqs.append(seq)
print(seqs)
print(len(seqs))

repeat, most_common = final_reads.repeats(7)
print(most_common)
