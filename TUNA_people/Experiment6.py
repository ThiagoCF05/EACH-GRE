'''
Created on 03/09/2013

@author: thiagocastroferreira
'''

import Assurance as ass
from IncrementalAlgorithmRelational5 import *
from IncrementalAlgorithmRelationalOverspecified import *
import numpy as num
import CrossValidation as cross

def toList(folds, teste):
    treinamentoSet = []
    testeSet = []
    for fold in folds:
        if fold == teste:
            for participante in folds[fold].keys():
                for anotacao in folds[fold][participante]:
                    testeSet.append(anotacao)
        else:
            for participante in folds[fold].keys():
                for anotacao in folds[fold][participante]:
                    treinamentoSet.append(anotacao)
        
    return [treinamentoSet, testeSet]

def countAttributeFrequency(anotacoes):
    frequency = {}
    
    for anotacao in anotacoes:
        participante = str(anotacao["caracteristicas"]["participante"])
        targets = anotacao["caracteristicas"]["target"]
        if participante not in frequency.keys():
            frequency[participante] = {}
            frequency[participante]["target"] = {}
        
        for objeto in anotacao["descricao"]:
            for key in anotacao["descricao"][objeto].keys():
                if objeto in targets:
                    if key in frequency[participante]["target"].keys():
                        frequency[participante]["target"][key] = frequency[participante]["target"][key] + 1
                    else:
                        frequency[participante]["target"][key] = 1
    return frequency

def run(folds, atributos, probabilidade):
    
    diceGeral = []
    masiGeral = []
    acuraciaGeral = []
    diceGeralSuperespecificada = []
    masiGeralSuperespecificada = []
    acuraciaGeralSuperespecificada = []
    
    anotacoes = {}
    
    print 50 * "*"
    print 50 * "-"
    print "Experimento TUNA Furniture Personalizado"
    print 50 * "-"
    
    for fold in folds:
        print 50 * "-"
        print "FOLD: ", fold
        print 50 * "-"
        [treinamento, teste] = toList(folds, fold)
        
        anotacoes[fold] = {}
    
        frequencia = countAttributeFrequency(treinamento)
    
        preferencia = getListaPreferencia(frequencia, atributos)
        
        frequencia = countAttributeFrequency(treinamento)
            
            # inclui os atributos nao mencionados no final da lista de preferencia
#             random.shuffle(atributos)
#             for atributo in atributos:
#                 if atributo not in lista_preferencia[participante]["target"]:
#                     lista_preferencia[participante]["target"].append(atributo)
#                    
#                 if atributo not in lista_preferencia[participante]["landmark"]:
#                     lista_preferencia[participante]["landmark"].append(atributo)
        
        mediaDice = []
        mediaMasi = []
        acuracia = 0.
        numeroDescricoes = 0. 
        mediaDiceSuperespecificada = []
        mediaMasiSuperespecificada = []
        acuraciaSuperespecificada = 0.
        numeroDescricoesSuperespecificada = 0.  
        
        for anotacao in teste:
            participante = str(anotacao["caracteristicas"]["participante"])
            target = anotacao["caracteristicas"]["target"]
            
            numeroExpressoesParticipante = 0
            for annotation in treinamento:
                if annotation["caracteristicas"]["participante"] == participante:
                    numeroExpressoesParticipante = numeroExpressoesParticipante + 1
            
            A = ass.parse(anotacao["descricao"])
            
            descricao = IncrementalAlgorithmRelational5(anotacao["domain"], target, preferencia[participante], 
                                            frequencia[participante], probabilidade, numeroExpressoesParticipante, False).run()
            B = ass.parse(descricao)
                
            DICE = ass.dice(A, B)
            MASI = ass.masi(A, B)
            
            if DICE == 1.0:
                acuracia = acuracia + 1
            numeroDescricoes = numeroDescricoes + 1
            
            mediaDice.append(DICE)
            mediaMasi.append(MASI)
            
            anotacao["dice_personalizado"] = DICE
            anotacao["masi_personalizado"] = MASI
            anotacao["algoritmo_personalizado"] = descricao
            
            descricao = IncrementalAlgorithmRelationalOverspecified(anotacao["domain"], target, preferencia[participante], 
                                            frequencia[participante], probabilidade, numeroExpressoesParticipante, False).run()
            B = ass.parse(descricao)
                
            DICE = ass.dice(A, B)
            MASI = ass.masi(A, B)
            
            if DICE == 1.0:
                acuraciaSuperespecificada = acuraciaSuperespecificada + 1
            numeroDescricoesSuperespecificada = numeroDescricoesSuperespecificada + 1
            
            mediaDiceSuperespecificada.append(DICE)
            mediaMasiSuperespecificada.append(MASI)
            
            anotacao["dice_personalizado_superespecificado"] = DICE
            anotacao["masi_personalizado_superespecificado"] = MASI
            anotacao["algoritmo_personalizado_superespecificado"] = descricao
            
            #anotacoes[fold][participante] = anotacao
            
#             print anotacao["descricao"]
#             print anotacao["algoritmo_personalizado"]
#             print anotacao["caracteristicas"]
#             print anotacao["dice_personalizado"] 
#             print anotacao["masi_personalizado"] 
#             print 50 * "*"
            
        print "DICE: ", num.mean(mediaDice)
        print "MASI: ", num.mean(mediaMasi)
        print "ACURACIA: ", acuracia / numeroDescricoes
        print "\n"
        
        diceGeral.append(num.mean(mediaDice))
        masiGeral.append(num.mean(mediaMasi))
        acuraciaGeral.append(acuracia / numeroDescricoes)
        diceGeralSuperespecificada.append(num.mean(mediaDiceSuperespecificada))
        masiGeralSuperespecificada.append(num.mean(mediaMasiSuperespecificada))
        acuraciaGeralSuperespecificada.append(acuraciaSuperespecificada / numeroDescricoesSuperespecificada)
#         for participante in lista_preferencia:
#             print participante, lista_preferencia[participante]

    print 50 * "-"
    print "GERAL: "
    print 50 * "-"
    print "DICE: ", num.mean(diceGeral)
    print "MASI: ", num.mean(masiGeral)
    print "ACURACIA: ", num.mean(acuraciaGeral)
    print "DICE SUPERESPECIFICADO: ", num.mean(diceGeralSuperespecificada)
    print "MASI SUPERESPECIFICADO: ", num.mean(masiGeralSuperespecificada)
    print "ACURACIA SUPERESPECIFICADA: ", num.mean(acuraciaGeralSuperespecificada)
    print 50 * "*"
    print "\n"
    return folds

def getListaPreferencia(frequencia, atributos):
    lista_preferencia = {}
    preferencia = {}
    
    for participante in frequencia.keys():
        if participante not in lista_preferencia.keys():
            lista_preferencia[participante]  = {}
            lista_preferencia[participante]["target"]  = []
            preferencia[participante]  = {}
            preferencia[participante]["target"]  = []
        
        while len(frequencia[participante]["target"]) != 0:
            maximo = max(frequencia[participante]["target"].values())
            
            for key in frequencia[participante]["target"].keys():
                if frequencia[participante]["target"][key] == maximo:
                    lista_preferencia[participante]["target"].append(key)
                    del(frequencia[participante]["target"][key])
                  
    
    
        for atributo in lista_preferencia[participante]["target"]:
            if atributo in atributos:
                preferencia[participante]["target"].append(atributo)
        
    return preferencia