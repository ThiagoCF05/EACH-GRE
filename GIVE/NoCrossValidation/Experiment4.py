'''
Created on 11/11/2013

@author: thiagocastroferreira
'''

import Assurance as ass
from IncrementalAlgorithmRelational5 import *
import numpy as num
import random

# Experimento no corpus GIVE com o algoritmo IA superespecificado
# e a lista de preferencia ordenada pela frequencia de atributos
def run(contextos, anotacoes, atributos):
        
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
    
    preferencia = {}
    preferencia["target"]  = []
    for atributo in lista_preferencia["target"]:
        if atributo in atributos:
            preferencia["target"].append(atributo)
    
    preferencia["landmark"]  = []
    for atributo in lista_preferencia["landmark"]:
        if atributo in atributos:
            preferencia["landmark"].append(atributo)
        
    mediaDice = []
    mediaMasi = []
    acuracia = 0.
    numeroDescricoes = 0.
    
    frequencia = countAttributeFrequency(anotacoes)
    for anotacao in anotacoes:
        contexto = anotacao["caracteristicas"]["context"]
        participante = str(anotacao["caracteristicas"]["trial"])
        target = anotacao["caracteristicas"]["target"]
        
        A = ass.parse(anotacao["descricao"]) 
        
        #random.shuffle(atributos)
        descricao = IncrementalAlgorithmRelational5(contextos[contexto], target, preferencia,
                                                    frequencia, 0.7, len(anotacoes), True).run()
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
        
    print "DICE: " + str(num.mean(mediaDice))
    print "MASI: " + str(num.mean(mediaMasi))
    print "Acuracia: " + str(acuracia / numeroDescricoes)
    print "\n"
    
#     print lista_preferencia

def countAttributeFrequency(anotacoes):
    frequency = {}
    frequency["target"] = {}
    frequency["landmark"] = {}
    
    for anotacao in anotacoes:
        target = anotacao["caracteristicas"]["target"]
        
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
