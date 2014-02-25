'''
Created on 12/09/2013

@author: thiagocastroferreira
'''

import Assurance as ass
from IncrementalAlgorithmRelational3 import *
from IncrementalAlgorithmRelational4 import *
from IncrementalAlgorithmRelational5 import *
import numpy as num
from itertools import permutations
import random

def run(dominios, targets, anotacoes, atributos, probabilidade):
        
    frequencia = countAttributeFrequency(anotacoes)
    
    preferencia = getListaPreferencia(frequencia, atributos)
    
    frequencia = countAttributeFrequency(anotacoes)
    print len(frequencia)
    mediaDice = []
    mediaMasi = []
    acuracia = 0.
    numeroDescricoes = 0.
    
    for anotacao in anotacoes:
        contexto = anotacao["caracteristicas"]["context"]
        participante = str(anotacao["caracteristicas"]["trial"])
        
        A = ass.parse(anotacao["descricao"]) 
        
        #random.shuffle(atributos)
        #descricao = IncrementalAlgorithmRelational3(dominios[contexto], targets[contexto], preferencia[participante], False).run()
        descricao = IncrementalAlgorithmRelational5(dominios[contexto], targets[contexto], preferencia[participante],
                                                    frequencia[participante], probabilidade, 0, False).run()
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
    
#     for participante in preferencia:
#         print participante, preferencia[participante]
    file = open("expressoes.txt", "w")
    
    for anotacao in anotacoes:
        file.write(str(anotacao["descricao"]))
        file.write("\n")
        file.write(str(anotacao["algoritmo"]))
        file.write("\n")
        file.write(str(anotacao["caracteristicas"]))
        file.write("\n")
        file.write(str(anotacao["dice"])) 
        file.write("\n")
        file.write(str(anotacao["masi"]))
        file.write("\n")
        file.write(str(100 * "*"))
        file.write("\n")
    
    file.close()

def countAttributeFrequency(anotacoes):
    frequency = {}
    
    for anotacao in anotacoes:
        target = "tg"
        participante = anotacao["caracteristicas"]["trial"]
        
        if participante not in frequency.keys():
            frequency[participante] = {}
            frequency[participante]["target"] = {}
            frequency[participante]["landmark"] = {}
        
        for objeto in anotacao["descricao"]:
            for key in anotacao["descricao"][objeto].keys():
                if objeto == target:
                    if key in frequency[participante]["target"].keys():
                        frequency[participante]["target"][key] = frequency[participante]["target"][key] + 1
                    else:
                        frequency[participante]["target"][key] = 1
                else:
                    if key in frequency[participante]["landmark"].keys():
                        frequency[participante]["landmark"][key] = frequency[participante]["landmark"][key] + 1
                    else:
                        frequency[participante]["landmark"][key] = 1
    #Printar as frequencias do uso de atributos por participante
#     for i in range(1,300):
#         if str(i) in frequency.keys():
#             print str(i), frequency[str(i)]
    return frequency

def getListaPreferencia(frequencia, atributos):
    lista_preferencia = {}
    preferencia = {}
    
    for participante in frequencia.keys():
        if participante not in lista_preferencia.keys():
            lista_preferencia[participante]  = {}
            lista_preferencia[participante]["target"]  = []
            lista_preferencia[participante]["landmark"]  = []
            preferencia[participante]  = {}
            preferencia[participante]["target"]  = []
            preferencia[participante]["landmark"]  = []
        
        frequenciaRelacionais = {}
        frequenciaRel = 0
        if "right-of" in frequencia[participante]["target"].keys():
            frequenciaRelacionais["right-of"] = frequencia[participante]["target"]["right-of"]
            frequenciaRel = frequenciaRel + frequencia[participante]["target"]["right-of"]
            del(frequencia[participante]["target"]["right-of"])
        if "left-of" in frequencia[participante]["target"].keys():
            frequenciaRelacionais["left-of"] = frequencia[participante]["target"]["left-of"]
            frequenciaRel = frequenciaRel + frequencia[participante]["target"]["left-of"]
            del(frequencia[participante]["target"]["left-of"])
        if "on-top-of" in frequencia[participante]["target"].keys():
            frequenciaRelacionais["on-top-of"] = frequencia[participante]["target"]["on-top-of"]
            frequenciaRel = frequenciaRel + frequencia[participante]["target"]["on-top-of"]
            del(frequencia[participante]["target"]["on-top-of"])
        if "next-to" in frequencia[participante]["target"].keys():
            frequenciaRelacionais["next-to"] = frequencia[participante]["target"]["next-to"]
            frequenciaRel = frequenciaRel + frequencia[participante]["target"]["next-to"]
            del(frequencia[participante]["target"]["next-to"])
        if "under" in frequencia[participante]["target"].keys():
            frequenciaRelacionais["under"] = frequencia[participante]["target"]["under"]
            frequenciaRel = frequenciaRel + frequencia[participante]["target"]["under"]
            del(frequencia[participante]["target"]["under"])
        
        while len(frequencia[participante]["target"]) != 0:
            maximo = max(frequencia[participante]["target"].values())
            
            if maximo < frequenciaRel and len(frequenciaRelacionais) != 0:
                while len(frequenciaRelacionais) != 0:
                    maximo1 = max(frequenciaRelacionais.values())
                    
                    for key in frequenciaRelacionais.keys():
                        if frequenciaRelacionais[key] == maximo1:
                            lista_preferencia[participante]["target"].append(key)
                            del(frequenciaRelacionais[key])
            else:
                for key in frequencia[participante]["target"].keys():
                    if frequencia[participante]["target"][key] == maximo:
                        lista_preferencia[participante]["target"].append(key)
                        del(frequencia[participante]["target"][key])
        
        while len(frequenciaRelacionais) != 0:
            maximo1 = max(frequenciaRelacionais.values())
            
            for key in frequenciaRelacionais.keys():
                if frequenciaRelacionais[key] == maximo1:
                    lista_preferencia[participante]["target"].append(key)
                    del(frequenciaRelacionais[key])
                  
        while len(frequencia[participante]["landmark"]) != 0:
            maximo = max(frequencia[participante]["landmark"].values())
            
            for key in frequencia[participante]["landmark"].keys():
                if frequencia[participante]["landmark"][key] == maximo:
                    lista_preferencia[participante]["landmark"].append(key)
                    del(frequencia[participante]["landmark"][key])
    
    
        for atributo in lista_preferencia[participante]["target"]:
            if atributo in atributos:
                preferencia[participante]["target"].append(atributo)
        
        preferencia[participante]["landmark"]  = []
        for atributo in lista_preferencia[participante]["landmark"]:
            if atributo in atributos:
                preferencia[participante]["landmark"].append(atributo)
    return preferencia
