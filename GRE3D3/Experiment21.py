'''
Created on 13/09/2013

@author: thiagocastroferreira
'''

import ParserGRE3D as parser
import Assurance as ass
from IncrementalAlgorithmRelational2 import *
from IncrementalAlgorithmRelational3 import *
from IncrementalAlgorithmRelational4 import *
from IncrementalAlgorithmRelational5 import *
import numpy as num
from itertools import permutations
import random

def run(dominios, targets, anotacoes, atributos, probabilidade):
        
    frequencia = countAttributeFrequency(anotacoes)
    
    lista_preferencia = getListaPreferencia(frequencia, atributos)
    
    frequencia = countAttributeFrequency(anotacoes)
    
    mediaDice = []
    mediaMasi = []
    acuracia = 0.
    numeroDescricoes = 0.
    
    for anotacao in anotacoes:
        contexto = anotacao["caracteristicas"]["context"]
        participante = str(anotacao["caracteristicas"]["trial"])
        
        A = ass.parse(anotacao["descricao"])
        
        #random.shuffle(atributos)
        descricao = IncrementalAlgorithmRelational5(dominios[contexto], targets[contexto], lista_preferencia, frequencia, probabilidade, 4480, False).run()
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
        
    print "Dice: ", num.mean(mediaDice)
    print "Masi: ",num.mean(mediaMasi)
    print "Acuracia: ",acuracia / numeroDescricoes
    print "\n"
    
    #print lista_preferencia

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

def getListaPreferencia(frequencia, atributos):
    lista_preferencia  = {}
    lista_preferencia["target"]  = []
    lista_preferencia["landmark"]  = []
    preferencia  = {}
    preferencia["target"]  = []
    preferencia["landmark"]  = []
    
    frequenciaRelacionais = {}
    frequenciaRel = 0
    if "right-of" in frequencia["target"].keys():
        frequenciaRelacionais["right-of"] = frequencia["target"]["right-of"]
        frequenciaRel = frequenciaRel + frequencia["target"]["right-of"]
        del(frequencia["target"]["right-of"])
    if "left-of" in frequencia["target"].keys():
        frequenciaRelacionais["left-of"] = frequencia["target"]["left-of"]
        frequenciaRel = frequenciaRel + frequencia["target"]["left-of"]
        del(frequencia["target"]["left-of"])
    if "on-top-of" in frequencia["target"].keys():
        frequenciaRelacionais["on-top-of"] = frequencia["target"]["on-top-of"]
        frequenciaRel = frequenciaRel + frequencia["target"]["on-top-of"]
        del(frequencia["target"]["on-top-of"])
    if "next-to" in frequencia["target"].keys():
        frequenciaRelacionais["next-to"] = frequencia["target"]["next-to"]
        frequenciaRel = frequenciaRel + frequencia["target"]["next-to"]
        del(frequencia["target"]["next-to"])
    if "under" in frequencia["target"].keys():
        frequenciaRelacionais["under"] = frequencia["target"]["under"]
        frequenciaRel = frequenciaRel + frequencia["target"]["under"]
        del(frequencia["target"]["under"])
    
    while len(frequencia["target"]) != 0:
        maximo = max(frequencia["target"].values())
        
        if maximo < frequenciaRel and len(frequenciaRelacionais) != 0:
            while len(frequenciaRelacionais) != 0:
                maximo1 = max(frequenciaRelacionais.values())
                
                for key in frequenciaRelacionais.keys():
                    if frequenciaRelacionais[key] == maximo1:
                        lista_preferencia["target"].append(key)
                        del(frequenciaRelacionais[key])
        else:
            for key in frequencia["target"].keys():
                if frequencia["target"][key] == maximo:
                    lista_preferencia["target"].append(key)
                    del(frequencia["target"][key])
    
    while len(frequenciaRelacionais) != 0:
        maximo1 = max(frequenciaRelacionais.values())
        
        for key in frequenciaRelacionais.keys():
            if frequenciaRelacionais[key] == maximo1:
                lista_preferencia["target"].append(key)
                del(frequenciaRelacionais[key])      
              
    while len(frequencia["landmark"]) != 0:
        maximo = max(frequencia["landmark"].values())
        
        for key in frequencia["landmark"].keys():
            if frequencia["landmark"][key] == maximo:
                lista_preferencia["landmark"].append(key)
                del(frequencia["landmark"][key])


    for atributo in lista_preferencia["target"]:
        if atributo in atributos:
            preferencia["target"].append(atributo)
    
    preferencia["landmark"]  = []
    for atributo in lista_preferencia["landmark"]:
        if atributo in atributos:
            preferencia["landmark"].append(atributo)
    return preferencia

