'''
Created on 03/09/2013

@author: thiagocastroferreira
'''

import Assurance as ass
import IncrementalAlgorithmRelational2 as ie
import numpy as num
import random

def run(dominios, targets, anotacoes, atributos):
    
    mediaDice = []
    mediaMasi = []
    acuracia = 0.
    numeroDescricoes = 0.
    
    print 50 * "*"
    print 50 * "-"
    print "Experimento Zoom Randomico"
    print 50 * "-"
    
    for anotacao in anotacoes:
        contexto = anotacao["caracteristicas"]["context"]
        target = targets[contexto]
        
        A = []
        for expressao in anotacao["anotacoes"].keys():
            A.extend(ass.parse(anotacao["anotacoes"][expressao]))
        A = set(A)
        
        atributos.remove("type")
        random.shuffle(atributos)
        atributos.insert(0, "type")
        
        descricao = ie.run(dominios[contexto], target, atributos, False)
        
        B = []
        i = 0
        for expressao in descricao.keys():
            B.extend(ass.parse(descricao[expressao], targets[contexto][i]))
            i = i + 1
        B = set(B)
        
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
    
    return anotacoes
        