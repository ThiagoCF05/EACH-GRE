'''
Created on 03/09/2013

@author: thiagocastroferreira
'''

import ParserGRE3D as parser
import Assurance as ass
from IncrementalAlgorithmRelational2 import *
from IncrementalAlgorithmRelational3 import *
import numpy as num
from itertools import permutations
import random

def countAttributeFrequency(anotacoes):
    frequency = {}
    frequency["target"] = {}
    frequency["landmark"] = {}
    
    for anotacao in anotacoes:
        target = "tg"
        
        for objeto in anotacao["descricao"]:
            for key in anotacao["descricao"][objeto].keys():
                if objeto == target:
                    if key in frequency["target"].keys():
                        frequency["target"][key] = frequency["target"][key] + 1
                    else:
                        frequency["target"][key] = 1
                else:
                    if key in frequency["landmark"].keys():
                        frequency["landmark"][key] = frequency["landmark"][key] + 1
                    else:
                        frequency["landmark"][key] = 1
    return frequency

def run(dominios, targets, anotacoes, atributos):
        
    frequencia = countAttributeFrequency(anotacoes)
    
    lista_preferencia = {}
    
    
    lista_preferencia["target"]  = []
    while len(frequencia["target"]) != 0:
        maximo = max(frequencia["target"].values())
        
        for key in frequencia["target"].keys():
            if frequencia["target"][key] == maximo:
                lista_preferencia["target"].append(key)
                del(frequencia["target"][key])
       
    lista_preferencia["landmark"]  = []         
    while len(frequencia["landmark"]) != 0:
        maximo = max(frequencia["landmark"].values())
        
        for key in frequencia["landmark"].keys():
            if frequencia["landmark"][key] == maximo:
                lista_preferencia["landmark"].append(key)
                del(frequencia["landmark"][key])
    
    mediaDice = []
    mediaMasi = []
    acuracia = 0.
    numeroDescricoes = 0.
    
    for anotacao in anotacoes:
        contexto = anotacao["caracteristicas"]["context"]
        participante = str(anotacao["caracteristicas"]["trial"])
        
        A = ass.parse(anotacao["descricao"])
        
        #random.shuffle(atributos)
        descricao = IncrementalAlgorithmRelational3(dominios[contexto], targets[contexto], lista_preferencia, False).run()
        B = ass.parse(descricao, targets[contexto])
        
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
        
    print num.mean(mediaDice)
    print num.mean(mediaMasi)
    print acuracia / numeroDescricoes
    print "\n"
    
    print lista_preferencia
