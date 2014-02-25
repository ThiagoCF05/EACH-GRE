'''
Created on 14/09/2013

@author: thiagocastroferreira
'''

import Assurance as ass
import IncrementalAlgorithmRelational5 as ie5
import IncrementalAlgorithmRelationalOverspecified as ieo
import numpy as num

def run(dominios, targets, folds, atributos, probabilidade):
    
    mediaDice = []
    mediaMasi = []
    acuracia = 0.
    numeroDescricoes = 0.
    mediaDiceSuperespecificada = []
    mediaMasiSuperespecificada = []
    acuraciaSuperespecificada = 0.
    numeroDescricoesSuperespecificada = 0.
    
    for i in range(1, len(folds)+1):
        fold = str(i)
        print "Fold: ", fold
        print 50 * "-"
        
        [treinamento, teste] = toList(folds, fold)
        frequencia = countAttributeFrequency(treinamento)
    
        preferencia = getListaPreferencia(frequencia, atributos)
        
        frequencia = countAttributeFrequency(treinamento)
        
        mediaFoldDice = []
        mediaFoldMasi = []
        acuraciaFold = 0.
        numeroDescricoesFold = 0.
        mediaFoldDiceSuperespecificada = []
        mediaFoldMasiSuperespecificada = []
        acuraciaFoldSuperespecificada = 0.
        numeroDescricoesFoldSuperespecificada = 0.
    
        for anotacao in teste:
            contexto = anotacao["caracteristicas"]["context"]
            participante = str(anotacao["caracteristicas"]["trial"])
            
            numeroExpressoesParticipante = 0
            for annotation in treinamento:
                if annotation["caracteristicas"]["trial"] == participante:
                    numeroExpressoesParticipante = numeroExpressoesParticipante + 1
            
            A = []
            for expressao in anotacao["anotacoes"].keys():
                A.extend(ass.parse(anotacao["anotacoes"][expressao]))
            A = set(A)
            
            #random.shuffle(atributos)
            #descricao = IncrementalAlgorithmRelational3(dominios[contexto], targets[contexto], preferencia[participante], False).run()
            descricao = ie5.run(dominios[contexto], targets[contexto], preferencia[participante], False)
            
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
                acuraciaFold = acuraciaFold + 1
            numeroDescricoes = numeroDescricoes + 1
            numeroDescricoesFold = numeroDescricoesFold + 1
            
            mediaDice.append(DICE)
            mediaMasi.append(MASI)
            
            mediaFoldDice.append(DICE)
            mediaFoldMasi.append(MASI)
            
            anotacao["dice_personalizado"] = DICE
            anotacao["masi_personalizado"] = MASI
            anotacao["algoritmo_personalizado"] = descricao
            
            descricao = ieo.run(dominios[contexto], targets[contexto], preferencia[participante],frequencia[participante], probabilidade, numeroExpressoesParticipante, False)

            B = []
            i = 0
            for expressao in descricao.keys():
                B.extend(ass.parse(descricao[expressao], targets[contexto][i]))
                i = i + 1
            B = set(B)
            
            DICE = ass.dice(A, B)
            MASI = ass.masi(A, B)
            
            if DICE == 1.0:
                acuraciaSuperespecificada = acuraciaSuperespecificada + 1
                acuraciaFoldSuperespecificada = acuraciaFoldSuperespecificada + 1
            numeroDescricoesSuperespecificada = numeroDescricoesSuperespecificada + 1
            numeroDescricoesFoldSuperespecificada = numeroDescricoesFoldSuperespecificada + 1
            
            mediaDiceSuperespecificada.append(DICE)
            mediaMasiSuperespecificada.append(MASI)
            
            mediaFoldDiceSuperespecificada.append(DICE)
            mediaFoldMasiSuperespecificada.append(MASI)
            
            anotacao["dice_personalizado_superespecificado"] = DICE
            anotacao["masi_personalizado_superespecificado"] = MASI
            anotacao["algoritmo_personalizado_superespecificado"] = descricao
#             print "Descricao: " + str(anotacao["anotacoes"])
#             print "Anotacao: " + str(anotacao["algoritmo_personalizado"])
#             print "Anotacao Superespecificado: " + str(anotacao["algoritmo_personalizado_superespecificado"])
#             print anotacao["caracteristicas"]
#             print anotacao["dice_personalizado_superespecificado"] 
#             print anotacao["masi"] 
#             print "\n"
            
        print "Dice: ", num.mean(mediaFoldDice)
        print "Masi: ",num.mean(mediaFoldMasi)
        print "Acuracia: ",acuraciaFold / numeroDescricoesFold
        print "Dice Superespecificado: ", num.mean(mediaFoldDiceSuperespecificada)
        print "Masi Superespecificado: ",num.mean(mediaFoldMasiSuperespecificada)
        print "Acuracia Superespecificado: ",acuraciaFoldSuperespecificada / numeroDescricoesFoldSuperespecificada
        print "\n"
        
    print "Dice: ", num.mean(mediaDice)
    print "Masi: ",num.mean(mediaMasi)
    print "Acuracia: ",acuracia / numeroDescricoes
    print "Dice Superespecificado: ", num.mean(mediaDiceSuperespecificada)
    print "Masi Superespecificado: ",num.mean(mediaMasiSuperespecificada)
    print "Acuracia Superespecificado: ",acuraciaSuperespecificada / numeroDescricoesSuperespecificada
    print "\n"
    
    return folds
    
#     for participante in preferencia:
#         print participante, preferencia[participante]
#     file = open("expressoes.txt", "w")
#     
#     for anotacao in anotacoes:
#         file.write(str(anotacao["descricao"]))
#         file.write("\n")
#         file.write(str(anotacao["algoritmo"]))
#         file.write("\n")
#         file.write(str(anotacao["caracteristicas"]))
#         file.write("\n")
#         file.write(str(anotacao["dice"])) 
#         file.write("\n")
#         file.write(str(anotacao["masi"]))
#         file.write("\n")
#         file.write(str(50 * "*"))
#         file.write("\n")
#     
#     file.close()

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
        target = "tg"
        participante = anotacao["caracteristicas"]["trial"]
        
        if participante not in frequency.keys():
            frequency[participante] = {}
            frequency[participante]["target"] = {}
            frequency[participante]["landmark"] = {}
        
        for descricao in anotacao["anotacoes"]:
            for objeto in anotacao["anotacoes"][descricao]:
                for key in anotacao["anotacoes"][descricao][objeto].keys():
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
        if "right-to" in frequencia[participante]["target"].keys():
            frequenciaRelacionais["right-to"] = frequencia[participante]["target"]["right-to"]
            frequenciaRel = frequenciaRel + frequencia[participante]["target"]["right-to"]
            del(frequencia[participante]["target"]["right-to"])
        if "left-to" in frequencia[participante]["target"].keys():
            frequenciaRelacionais["left-to"] = frequencia[participante]["target"]["left-to"]
            frequenciaRel = frequenciaRel + frequencia[participante]["target"]["left-to"]
            del(frequencia[participante]["target"]["left-to"])
        if "in-front-of" in frequencia[participante]["target"].keys():
            frequenciaRelacionais["in-front-of"] = frequencia[participante]["target"]["in-front-of"]
            frequenciaRel = frequenciaRel + frequencia[participante]["target"]["in-front-of"]
            del(frequencia[participante]["target"]["in-front-of"])
        if "next-to" in frequencia[participante]["target"].keys():
            frequenciaRelacionais["next-to"] = frequencia[participante]["target"]["next-to"]
            frequenciaRel = frequenciaRel + frequencia[participante]["target"]["next-to"]
            del(frequencia[participante]["target"]["next-to"])
        if "behind" in frequencia[participante]["target"].keys():
            frequenciaRelacionais["behind"] = frequencia[participante]["target"]["behind"]
            frequenciaRel = frequenciaRel + frequencia[participante]["target"]["behind"]
            del(frequencia[participante]["target"]["behind"])
        
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
