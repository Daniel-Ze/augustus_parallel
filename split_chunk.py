from __future__ import print_function
import sys, os, datetime, time
import cProfile

def convFasta(x):
    new_file = ''
    lines_1 = ''
    a = 0
    count_l = len(x)
    for lines in x:
        if lines != "" and lines[:1] == '>':
            lines_1 = lines.split(' ')
            new_file = new_file + lines_1[0] + "\n"
            a = a + 1
            while a < count_l and '>' not in x[a]:
                new_file = new_file + x[a].rstrip().upper()
                a = a + 1
            new_file = new_file + "\n"
    new_file = new_file.split()
    return new_file

def main():
    if len(sys.argv) == 5:
        with open(sys.argv[1], 'r') as f:
            fasta_file = f.readlines()
        chunck = sys.argv[2]
        desc = sys.argv[3]
        output = sys.argv[4]
    #2. If none of the above works quit.
    else:
        exit("[info]\t\tpython find_gc.py fasta.fa description")

    gc = ''
    new_file_gene = ''
    c = ''
    l = 0
    i = 0
    chunck_size_part = 0
    chunck_seq = ''
    missing_1 = 0

    abs_path = os.path.abspath(sys.argv[1])
    cwd = os.path.dirname(abs_path)

    fasta = convFasta(fasta_file)

    chunck_size = int((len(fasta)) / int(chunck))

    if (chunck_size % 2 == 0):
        missing_1 = len(fasta) - (int(chunck) * chunck_size)
    else:
        chunck_size = chunck_size + 1

    chunck_size_part = missing_1

    num_fasta = len(fasta) / 2

    print("[info]\t\tNumber of sequences in file:        " + str(num_fasta))
    print("[info]\t\tNumber of sequences in split files: " + str(chunck_size / 2))

    while i < int(chunck):
        print("[info]\t\t\tGenerating chunck number: " + str(i + 1))
        chunck_size_part = chunck_size_part + chunck_size
        while l < chunck_size_part:
            try:
                chunck_seq = chunck_seq + str(fasta[l]) + "\n"
                l = l + 1
            except IndexError:
                l = l + 1
                continue
        if output == '':
            out = open(cwd+'/tmp/'+desc+'_chunck'+str(i)+'.fa', 'w')
            out.write(chunck_seq)
            out.close()
        else:
            out = open(output+'/tmp/'+desc+'_chunck'+str(i)+'.fa', 'w')
            out.write(chunck_seq)
            out.close()
        i = i + 1
        chunck_seq = ''

if __name__ == "__main__":
    main()
