'''
Created on 19/12/2012

@author: thiagocastroferreira
'''
from numpy import *
from scipy import *
import matplotlib.pyplot as plt
from hcluster import *
import Assurance as ass
from Parser import *

if __name__ == '__main__':

    anotacaoes = test()
    #anotacoes = parseAnnotation()
    
#     conjuntos = []
#     aux = {}
#     id = 0
#     for entidade in anotacoes.keys():
#         for anotacao in anotacoes[entidade]:
#             aux[id] = anotacao
#             conjuntos.append(ass.parseProperty(anotacao))
#             id = id + 1
#     
#     valores = []
#     for i in range(0, len(conjuntos)):
#         for j in range(0, len(conjuntos)):
#             valueDice = ass.dice(conjuntos[i], conjuntos[j])
#             valores.append(valueDice)
#     matriz = array(valores).reshape(len(conjuntos), len(conjuntos))
#     
#     Z = linkage(matriz)
#     
#     T = fcluster(Z, t=0.8)
#     print 'Single'
#     print T
#     
#     plt.figure(figsize=(20,12))
#     dendrogram(Z)
#     plt.savefig('single_0.8.png')
#     
#     ##################################
#     raw_input()
#     
#     Z = linkage(matriz, 'complete')
#     
#     T = fcluster(Z, t=1.1)
#     print 'Complete'
#     print T
#     
#     plt.figure(figsize=(20,12))
#     dendrogram(Z)
#     plt.savefig('complete_1.1.png')
#     
#     ##################################
#     raw_input()
#     
#     Z = linkage(matriz, 'average')
#     
#     T = fcluster(Z, t=1.1)
#     print 'Average'
#     print T
#     
#     plt.figure(figsize=(20,12))
#     dendrogram(Z)
#     plt.savefig('average_1.1.png')
#     
#     ##################################
#     raw_input()
#     
#     Z = linkage(matriz, 'weighted')
#     
#     T = fcluster(Z, t=1.1)
#     print 'Weighted'
#     print T
#     
#     plt.figure(figsize=(20,12))
#     dendrogram(Z)
#     plt.savefig('weighted_1.1.png')
#     
#     ##################################
#     raw_input()
#     
#     Z = linkage(matriz, 'median')
#     
#     T = fcluster(Z, t=1.1)
#     print 'Median'
#     print T
#     
#     plt.figure(figsize=(20,12))
#     dendrogram(Z)
#     plt.savefig('median_1.1.png')
#     
#     ##################################
#     raw_input()
#     
#     Z = linkage(matriz, 'ward')
#     
#     T = fcluster(Z, t=1.1)
#     print 'Ward'
#     print T
#     
#     plt.figure(figsize=(20,12))
#     dendrogram(Z)
#     plt.savefig('ward_1.1.png')
    
    
    