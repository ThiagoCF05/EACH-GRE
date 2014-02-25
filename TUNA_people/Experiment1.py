'''
Created on 03/09/2013

@author: thiagocastroferreira
'''

import Assurance as ass
from IncrementalAlgorithmRelational2 import *
import numpy as num
import random

def run(trials, atributos):
    
    mediaDice = []
    mediaMasi = []
    acuracia = 0.
    numeroDescricoes = 0.
    
    print 50 * "*"
    print 50 * "-"
    print "Experimento TUNA Furniture Randomico"
    print 50 * "-"
    
    for anotacao in trials:
        targets = anotacao["caracteristicas"]["target"]
        
        A = ass.parse(anotacao["descricao"])
        
        atributos.remove("type")
        random.shuffle(atributos)
        atributos.insert(0, "type")
        descricao = IncrementalAlgorithmRelational2(anotacao["domain"], targets, atributos, False).run()
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
#         print 50 * "*"
        
    print "DICE: ", num.mean(mediaDice)
    print "MASI: ",num.mean(mediaMasi)
    print "ACURACIA: ",acuracia / numeroDescricoes
    print 50 * "*"
    print "\n"
    
    return trials
        