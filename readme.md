### GMVC: Genetic Minimum Vertex Cover problem solved by greedy algorithm



Setup & Run an example
----
    #Setup
    module load python/3.8.8
    pip install networkx pandas numpy --user
    git clone https://github.com/linnabrown/GMVC.git
    cd GMVC
    #Run an example
    python main.py \
    --sample example/sample.txt \
    --kinship example/kinship.txt \
    --thres 0.2 \
    --outFR example/removed_sample.txt \
    --outFU example/unrelated_sample.txt \
    --has_header True \
    --sep="\t"

Params
----

```
  -h, --help            show this help message and exit
  --sample SAMPLE       File path of sample file
  --kinship KINSHIP     File path of kinship file
  --thres THRES         Threshold of kinship.
  --outFR OUTFR         output file path of removed sample IDs
  --outFU OUTFU         output file path of unrelated samples
  --has_header HAS_HEADER
                        Whether sample file has header or not. Default=True.
  --kinship_col_index KINSHIP_COL_INDEX
                        The column index of kinship values. Default=5
  --sep SEP             Delimiter to use. Default=" "
```

Results
---
-unrelated_sample.txt (name can be customized by you). The unrelated sample kept by GMVC algorithm.

-removed_sample.txt (name can be customized by you). The sample which are removed by GMVC algorithm. Column 1 is sampleID. Column 2 degreeWhenRmv means the count of neighbour (kinship>0.2) of this sample when performing removing from the graph. Column 3 means the count of neighbours of this sample in the `--kinship` file.



FAQ
----
Q: What does my input `--kinship` file look like?

A: Kinship file is a table that quantifies the relationship of each pair of individuals. This file always contain at least three columns generated: `ID1, ID2, Kinship`. ID1 represents the ID of first individual, ID2 represents the ID of second individual, and kinship represents the relationship degree between ID1 and ID2, which can be estimated by GATK software and so on.

Since the input kinship file can be generated by different softwares, we provide customized parameters for you. 

1. `--has_header` indicates whether the input kinship file has header or not. If the kinship file has header, add `--has_header True`, otherwise, add `--has_header False`. 
2. `--kinship_col_index` indicates the index of the kinship column in the file. For example, if the kinship column is 5th column in the file, you ned to add `--kinship_col_index 5`. Remember, individual 1 and individual 2 are always in column 1 and column 2. Also, the index starts from 1 not 0.
3. `--sep` indicates the dilimiter of kinship file. If you use tab seperated file, you can indicate `--sep "\t"`.
