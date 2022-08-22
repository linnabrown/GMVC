'''
GMVC:
Genetic Maximum Vertex Cover problem solved by greedy algorithm
==>
Remove individuals via greedy algorithm

Author: Le Huang
July 29, 2022.

write readme
pip install networkx
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
parser.add_argument('--col', type=int, 
                    help='column id of kinship value')
parser.add_argument('--header', type=int, 
                    help='sample file contains header or not')
args = parser.parse_args()

sample_file = args.sample
kinship_file = args.kinship
kinship_thres=args.thres
outputFileRemoved=args.outFR
outputFileUnrelated = args.outFU

#load all sample
all_sample = open(sample_file).readlines() 
all_sample = [int(l.strip()) for l in all_sample] 
#load kinship pairs
df = pd.read_csv(kinship_file, " ", header=0)
# the pairs and nodes that have kinship > kinship_thres
B = df[df['Kinship'] > kinship_thres] 
#Removed the pairs where at least one sample doesn't exist in all_sample
B = B[(B['ID1'].isin(all_sample)) & (B['ID2'].isin(all_sample))]
#construct a graph
G = nx.Graph()
for index,one in B.iterrows():
    ID1 = int(one['ID1'])
    ID2 = int(one['ID2'])
    G.add_edge(ID1, ID2)
G_ori = G.copy()
Bset = list(set(B['ID1'].to_list() + B['ID2'].to_list())) #51849
initial_degree={}
for i in range(len(Bset)):
    initial_degree[Bset[i]]=G.degree[Bset[i]]
#look for the vertex has biggest degree
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


