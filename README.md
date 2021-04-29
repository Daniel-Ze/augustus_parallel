# AUGUSTUS parallel execution

AUGUSTUS gene prediction with a defined species model can't be executed by default in a parallel fashion to speed up the process of gene prediction. This script is intended for multifasta files like genomes. It will take the multifasta file and according to the supplied number of jobs it will chop the file in several multifasta files and run several AUGUSTUS instances in parallel. Using GNU parallel (Tange et al., 2020) AUGUSTUS will be run in parallel on the choped multifasta files. The generated annotation files (gff3) are merged at the end. Therefore, the option --uniqueGeneId is set to true by default to ensure unique gene ids for all predicted genes. The perl script 'getAnnoFast.pl' (supplied with AUGUSTUS) is run at the end.

### What you need

To run the script you will need the following programs:
  - GNU parallel
  - Python > 3.6
  - Perl
  - AUGUSTUS

### How to install it

Install GNU parallel on Ubuntu:

```bash
sudo apt install parallel
```

It is assumed you have conda installed on your system.
For people without unlimited power install GNU parallel into your conda base:
```bash
mamba install parallel=20201122
```
Install AUGUSTUS in a conda environment:
```bash
mamba create -n augustus augustus
```
Copy the folder containing run_augustus_parallel and split_chunk.py to your
desired directory. After that edit line nr. 13 in run_augustus_parallel:
```bash
cd ~/augustus_parallel
nano run_augustus_parallel
...
  13  home=/home/username/augustus_parallel/
...
```
Put the augustus_parallel directory in your $PATH. The bash script run_augustus_parallel
needs to be executable:
```bash
chmod a+x run_augustus_parallel
```
## How to run it

The script can be executed from anywhere:

```
user@computer$ run_augustus_parallel
/home/daniel/miniconda3/etc/profile.d/conda.sh exists.
[error]	No fasta file supplied.

Run AUGUSTUS in parallel.
The AUGUSTUS parameter --uniqueGeneId is set to true by default (necessary).

Usage: run_augustus_parallel -f fasta.file.fa -j n -c n -s suffix -p AUGUSTUS_parameters

    -f Path to fasta file.fa (mandatory)
    -j N chunks to generate from the multifasta file
    -c Number of CPUs to use (careful with the memomry consumption of AUGUSTUS)
    -s Suffix (defaulting to Aug_parallel)
    -p AUGUSTUS parameters: e.g. '--species=arabidopsis,--gff3=on,--UTR=on,--progress=true'
    -o Output path (full): /home/user/analysis
```

The python script split_chunk.py will split the multifasta file into equal indicated parts. For highly fragmented genomes it might be good to first check the total number of sequences in the file:
```bash
grep -E '^>' multifasta.fa | wc -l
```

If you want to create a single file per sequence in list just use the number from the command above for the -j flag.
The number of CPUs (the number of AUGUSTUS instances) is controlled with the -c flag.
An run example would be:

```bash
grep -E '^>' genome.fa | wc -l
19
run_augustus_parallel -i genome.fa -j 19 -c 8 -s OrganismX -p '--species=Your_specie_of_choice,--gff3=on,--progress=true'
```
The above is a minmal working example. The script will split the multifasta file into 19 single files(-j 19). With GNU parallel 8 instances of AUGUSTUS will be run in parallel (-c 8). The -p flag can be populated with many more parameters. For a complete overview of AUGUSTUS parameters please use:
```bash
augustus
augustus --species=help
augustus --paramlist
```
For further documentation of augustus please visit: https://github.com/Gaius-Augustus/Augustus

All temporay files are stored in the folder tmp/. The generated .gff3 files are combined in one and the augustus script getAnnoFasta.pl is run on the final annotation file.

## References

Tange, O. - GNU Parallel 20201122 ('Biden'), Nov 2020, Zendoo, https://doi.org/10.5281/zenodo.4284075

Stanke M, Keller O, Gunduz I, Hayes A, Waack S, Morgenstern B. AUGUSTUS: ab initio prediction of alternative transcripts. Nucleic Acids Res. 2006;34(Web Server issue):W435-W439. https://doi.10.1093/nar/gkl200
