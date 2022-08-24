'''
GMVC:
Genetic Minimum Vertex Cover problem solved by greedy algorithm
==>
Remove individuals via greedy algorithm

Author: Le Huang
July 29, 2022.
'''
import pandas as pd
import networkx as nx
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--sample', type=str,
                    help='File path of sample file')
parser.add_argument('--kinship', type=str, 
                    help='File path of kinship file')
parser.add_argument('--thres', type=float, default=0.2,
                    help='Threshold of kinship.')
parser.add_argument('--outFR', type=str, 
                    help='output file path of removed sample IDs')
parser.add_argument('--outFU', type=str, 
                    help='output file path of unrelated samples')
parser.add_argument('--has_header', type=bool, default=True,
                    help='Whether sample file has header or not. Default=True.')
parser.add_argument('--kinship_col_index', type=int, default=5, 
                    help='The column index of kinship values. Default=5')
parser.add_argument('--sep', type=str, default=" ", 
                    help='Delimiter to use. Default=" "')                    
args = parser.parse_args()

sample_file = args.sample
kinship_file = args.kinship
kinship_thres=args.thres
outputFileRemoved=args.outFR
outputFileUnrelated = args.outFU
has_header=args.has_header
kinship_col_index=args.kinship_col_index


#load all sample
all_sample = open(sample_file).readlines() 
all_sample = [int(l.strip()) for l in all_sample] 
#load kinship pairs
if has_header:
    df = pd.read_csv(kinship_file, sep=args.sep, header=0, engine="python")
else:
    df = pd.read_csv(kinship_file,sep=args.sep, header=None, engine="python")
kinship_table_cols=df.columns
sample1_col=kinship_table_cols[0]
sample2_col=kinship_table_cols[1]
kinship_col=kinship_table_cols[kinship_col_index-1]

# the pairs and nodes that have kinship > kinship_thres
B = df[df[kinship_col] > kinship_thres] 
#Removed the pairs where at least one sample doesn't exist in all_sample
B = B[(B[sample1_col].isin(all_sample)) & (B[sample2_col].isin(all_sample))]
if len(B)==0:
    exit("Your all of individuals of kinship file do not exists in your sample file. Program quit.")
#construct a graph
G = nx.Graph()
for index,one in B.iterrows():
    ID1 = int(one[sample1_col])
    ID2 = int(one[sample2_col])
    G.add_edge(ID1, ID2)
G_ori = G.copy()
Bset = list(set(B[sample1_col].to_list() + B[sample2_col].to_list()))
initial_degree={}
for i in range(len(Bset)):
    initial_degree[Bset[i]]=G.degree[Bset[i]]
#look for the vertex which has largest degree
removed_sample = [] # sample IDs removed from graph
neighboursInB=[]# num of neighbors in B for a removed sample ID
neighborsWhenRemoved=[]
degree_list = [G.degree[Bset[i]] for i in range(len(Bset))]
#greedy algorithm
while(max(degree_list)>0):
    maxDegree=0
    maxVertex=0
    index=-1
    for i in range(len(Bset)):
        if degree_list[i] > maxDegree:
            maxDegree = degree_list[i]
            maxVertex = Bset[i]
            index=i
    neighborsWhenRemoved.append(G.degree[maxVertex])
    neighboursInB.append(G_ori.degree[maxVertex])
    removed_sample.append(maxVertex)
    G.remove_node(maxVertex)
    Bset = list(G.nodes)
    degree_list = [G.degree[Bset[i]] for i in range(len(Bset))]
# Then we can just remove the sample from the all sample.
left_sample=set(all_sample) - set(removed_sample)

#Output
fw=open(outputFileUnrelated, 'w')
for one in left_sample:
    fw.write(str(one)+"\n")
fw.close()
new_df= pd.DataFrame(columns=['sampleID','degreeWhenRmv','degreeOri'])
new_df['sampleID'] = removed_sample
new_df['degreeWhenRmv'] = neighborsWhenRemoved
new_df['degreeOri'] = neighboursInB
new_df.to_csv(outputFileRemoved,'\t', index=False)
print("Finished.")

