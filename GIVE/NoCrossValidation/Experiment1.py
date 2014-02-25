'''
Created on 03/09/2013

@author: thiagocastroferreira
'''

import Assurance as ass
from IncrementalAlgorithmRelational2 import *
import numpy as num
import random

# Experimento do corpus GIVE com o Algoritmo Incremental com lista de preferencia aleatoria
def run(contextos, anotacoes, atributos):
    
    mediaDice = []
    mediaMasi = []
    acuracia = 0.
    numeroDescricoes = 0.
    
    print 100 * "*"
    print 100 * "-"
    print "Experimento GIVE Randomico"
    print 100 * "-"
    
    for anotacao in anotacoes:
        contexto = anotacao["caracteristicas"]["context"]
        target = anotacao["caracteristicas"]["target"]
        
        A = ass.parse(anotacao["descricao"])
        
        random.shuffle(atributos)
        descricao = IncrementalAlgorithmRelational2(contextos[contexto], target, atributos, False).run()
        B = ass.parse(descricao)
        
        DICE = ass.dice(A, B)
        MASI = ass.masi(A, B)
        
        if DICE == 1.0:
            acuracia = acuracia + 1
        numeroDescricoes = numeroDescricoes + 1
        
        mediaDice.append(DICE)
        mediaMasi.append(MASI)
        
        anotacao["dice"] = DICE
        anotacao["masi"] = MASI
        anotacao["algoritmo"] = descricao
    
#         print anotacao["descricao"]
#         print anotacao["algoritmo"]
#         print anotacao["caracteristicas"]
#         print anotacao["dice"] 
#         print anotacao["masi"] 
#         print 100 * "*"
        
    print "DICE: ", num.mean(mediaDice)
    print "MASI: ",num.mean(mediaMasi)
    print "ACURACIA: ",acuracia / numeroDescricoes
    print 100 * "*"
    print "\n"
    
    return anotacoes
        