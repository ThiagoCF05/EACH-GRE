'''
Created on 20/01/2014

@author: thiagocastroferreira
'''

from sklearn import svm
import numpy as np

def run(inputs = {}, fold = {}):
    CSet = [1.0, 10.0, 100.0, 1000.0]
    gammaSet = [0.1, 0.01, 0.001, 0.0001]
    
    svms = {}
    svmsRelational = {}
    
    resultados = {}
    
    for CI in CSet:
        for gammaI in gammaSet:
            key = str(CI) + "," + str(gammaI)
            
            svms[key] = {}
            svms[key]["type"] = None
            svms[key]["colour"] = None
            svms[key]["size"] = None
            svms[key]["hpos"] = None
            svms[key]["vpos"] = None
            svms[key]["below"] = None
            svms[key]["above"] = None
            svms[key]["in-front-of"] = None
            svms[key]["left"] = None
            svms[key]["right"] = None
            svms[key]["near"] = None
            svms[key]["lm_type"] = None
            svms[key]["lm_colour"] = None
            svms[key]["lm_size"] = None
            svms[key]["lm_hpos"] = None
            svms[key]["lm_vpos"] = None
            svms[key]["lm_below"] = None
            svms[key]["lm_above"] = None
            svms[key]["lm_left"] = None
            svms[key]["lm_right"] = None
            svms[key]["lm_near"] = None
            svms[key]["lm_in-front-of"] = None
            svms[key]["lm2_type"] = None
            svms[key]["lm2_colour"] = None
            svms[key]["lm2_size"] = None
            svms[key]["lm2_hpos"] = None
            svms[key]["lm2_vpos"] = None
            
            #Trained only with relational descriptions
            svmsRelational[key] = {}
            svmsRelational[key]["lm_type"] = None
            svmsRelational[key]["lm_colour"] = None
            svmsRelational[key]["lm_size"] = None
            svmsRelational[key]["lm_hpos"] = None
            svmsRelational[key]["lm_vpos"] = None
            svmsRelational[key]["lm_below"] = None
            svmsRelational[key]["lm_above"] = None
            svmsRelational[key]["lm_in-front-of"] = None
            svmsRelational[key]["lm_left"] = None
            svmsRelational[key]["lm_right"] = None
            svmsRelational[key]["lm_near"] = None
            svmsRelational[key]["lm2_type"] = None
            svmsRelational[key]["lm2_colour"] = None
            svmsRelational[key]["lm2_size"] = None
            svmsRelational[key]["lm2_hpos"] = None
            svmsRelational[key]["lm2_vpos"] = None
    
            treinamento = {}
            for dir in inputs:
                treinamento[dir] = inputs[dir]
                
            teste = treinamento[fold]
            del treinamento[fold]
            
            svms[key] = train(svms[key], treinamento, CI, gammaI, {})
            
            svmsRelational[key] = trainRelationalAttributes(svmsRelational[key], treinamento, CI, gammaI, {})
            
            svms[key]["lm_type"] = svmsRelational[key]["lm_type"]
            svms[key]["lm_colour"] = svmsRelational[key]["lm_colour"]
            svms[key]["lm_size"] = svmsRelational[key]["lm_size"]
            svms[key]["lm_hpos"] = svmsRelational[key]["lm_hpos"]
            svms[key]["lm_vpos"] = svmsRelational[key]["lm_vpos"]
            svms[key]["lm_below"] = svmsRelational[key]["lm_below"]
            svms[key]["lm_above"] = svmsRelational[key]["lm_above"]
            svms[key]["lm_left"] = svmsRelational[key]["lm_left"]
            svms[key]["lm_right"] = svmsRelational[key]["lm_right"]
            svms[key]["lm_near"] = svmsRelational[key]["lm_near"]
            svms[key]["lm_in-front-of"] = svmsRelational[key]["lm_in-front-of"]
            
            svms[key]["lm2_type"] = svmsRelational[key]["lm2_type"]
            svms[key]["lm2_colour"] = svmsRelational[key]["lm2_colour"]
            svms[key]["lm2_size"] = svmsRelational[key]["lm2_size"]
            svms[key]["lm2_hpos"] = svmsRelational[key]["lm2_hpos"]
            svms[key]["lm2_vpos"] = svmsRelational[key]["lm2_vpos"]
    
            resultados[key] = test(svms[key], teste)
    
    return resultados

def run2(inputs = {}, teste = [], combinacoes = {}):
            
    svms = {}
    svms["type"] = None
    svms["colour"] = None
    svms["size"] = None
    svms["hpos"] = None
    svms["vpos"] = None
    svms["below"] = None
    svms["above"] = None
    svms["left"] = None
    svms["right"] = None
    svms["near"] = None
    svms["in-front-of"] = None
    svms["lm_type"] = None
    svms["lm_colour"] = None
    svms["lm_size"] = None
    svms["lm_hpos"] = None
    svms["lm_vpos"] = None
    svms["lm_below"] = None
    svms["lm_above"] = None
    svms["lm_left"] = None
    svms["lm_right"] = None
    svms["lm_near"] = None
    svms["lm_in-front-of"] = None
    svms["lm2_type"] = None
    svms["lm2_colour"] = None
    svms["lm2_size"] = None
    svms["lm2_hpos"] = None
    svms["lm2_vpos"] = None
    
    #Trained only with relational descriptions
    svmsRelational = {}
    svmsRelational["lm_type"] = None
    svmsRelational["lm_colour"] = None
    svmsRelational["lm_size"] = None
    svmsRelational["lm_hpos"] = None
    svmsRelational["lm_vpos"] = None
    svmsRelational["lm_below"] = None
    svmsRelational["lm_above"] = None
    svmsRelational["lm_left"] = None
    svmsRelational["lm_right"] = None
    svmsRelational["lm_near"] = None
    svmsRelational["lm_in-front-of"] = None
    svmsRelational["lm2_type"] = None
    svmsRelational["lm2_colour"] = None
    svmsRelational["lm2_size"] = None
    svmsRelational["lm2_hpos"] = None
    svmsRelational["lm2_vpos"] = None
    
    svms = train(svms, inputs, 0.0, 0.0, combinacoes)
    
    svmsRelational = trainRelationalAttributes(svmsRelational, inputs, 0.0, 0.0, combinacoes)
    
    svms["lm_type"] = svmsRelational["lm_type"]
    svms["lm_colour"] = svmsRelational["lm_colour"]
    svms["lm_size"] = svmsRelational["lm_size"]
    svms["lm_hpos"] = svmsRelational["lm_hpos"]
    svms["lm_vpos"] = svmsRelational["lm_vpos"]
    svms["lm_below"] = svmsRelational["lm_below"]
    svms["lm_above"] = svmsRelational["lm_above"]
    svms["lm_left"] = svmsRelational["lm_left"]
    svms["lm_right"] = svmsRelational["lm_right"]
    svms["lm_near"] = svmsRelational["lm_near"]
    svms["lm_in-front-of"] = svmsRelational["lm_in-front-of"]
    
    svms["lm2_type"] = svmsRelational["lm2_type"]
    svms["lm2_colour"] = svmsRelational["lm2_colour"]
    svms["lm2_size"] = svmsRelational["lm2_size"]
    svms["lm2_hpos"] = svmsRelational["lm2_hpos"]
    svms["lm2_vpos"] = svmsRelational["lm2_vpos"]

    resultados = test(svms, teste)
    
    return resultados

def train(svms, treinamento, CI, gammaI, combinacoes):
    for svm1 in svms:
        data = []
        classe = []
        
        for fold in treinamento:
            for anotacao in treinamento[fold]:
                data.append(anotacao["data"])
                classe.append(anotacao["classes"][svm1])
        
        list = np.unique(classe)
        
        if len(list) == 1:
            if classe[0] == 0:
                classe[0] = 1
            else:
                classe[0] = 0
        
        if combinacoes != {}:
            svms[svm1] = svm.SVC(kernel = "rbf", C = combinacoes[svm1]["C"], gamma = combinacoes[svm1]["gamma"])
        else:
            svms[svm1] = svm.SVC(kernel = "rbf", C = CI, gamma = gammaI)
        svms[svm1].fit(data, classe)
    return svms

def test(svms, teste):
    acertos = {}
    total = {}
    expressoes = []
    
    #matriz de confusao
    tp = {}
    tn = {}
    fp = {}
    fn = {}
    
    for anotacao in teste:
        anotacao["previsoes"] = {}
        for svm1 in svms:
            if svm1 not in acertos.keys():
                acertos[svm1] = 0.0
                total[svm1] = 0.0
                tp[svm1] = 0
                tn[svm1] = 0
                fp[svm1] = 0
                fn[svm1] = 0
            
            resultado = svms[svm1].predict([anotacao["data"]])
            real = anotacao["classes"][str(svm1)]
            
            anotacao["previsoes"][str(svm1)] = resultado[0]
            
            if svm1 in ["lm_type", "lm_colour", "lm_size", "lm_vpos", "lm_hpos"] and (anotacao["classes"]["in-front-of"] > 0 or anotacao["classes"]["above"] > 0 or anotacao["classes"]["below"] > 0 or anotacao["classes"]["near"] > 0 or anotacao["classes"]["right"] > 0 or anotacao["classes"]["left"] > 0):
                if real == resultado[0]:
                    acertos[svm1] = acertos[svm1] + 1.0
                
                total[svm1] = total[svm1] + 1.0
                
                if real == 0 and resultado[0] == 0:
                    tn[svm1] = tn[svm1] + 1
                elif real != 0 and resultado[0] != 0:
                    tp[svm1] = tp[svm1] + 1
                elif real != 0 and resultado[0] == 0:
                    fn[svm1] = fn[svm1] + 1
                elif real == 0 and resultado[0] != 0:
                    fp[svm1] = fp[svm1] + 1
            elif svm1 in ["lm2_type", "lm2_colour", "lm2_size", "lm2_vpos", "lm2_hpos"] and (anotacao["classes"]["lm_in-front-of"] > 0 or anotacao["classes"]["lm_above"] > 0 or anotacao["classes"]["lm_below"] > 0 or anotacao["classes"]["lm_near"] > 0 or anotacao["classes"]["lm_right"] > 0 or anotacao["classes"]["lm_left"] > 0):
                if real == resultado[0]:
                    acertos[svm1] = acertos[svm1] + 1.0
                
                total[svm1] = total[svm1] + 1.0
                
                if real == 0 and resultado[0] == 0:
                    tn[svm1] = tn[svm1] + 1
                elif real != 0 and resultado[0] != 0:
                    tp[svm1] = tp[svm1] + 1
                elif real != 0 and resultado[0] == 0:
                    fn[svm1] = fn[svm1] + 1
                elif real == 0 and resultado[0] != 0:
                    fp[svm1] = fp[svm1] + 1
            elif svm1 not in ["lm_type", "lm_colour", "lm_size", "lm_vpos", "lm_hpos", "lm2_type", "lm2_colour", "lm2_size", "lm2_vpos", "lm2_hpos"]:
                if real == resultado[0]:
                    acertos[svm1] = acertos[svm1] + 1.0
                
                total[svm1] = total[svm1] + 1.0
                
                if real == 0 and resultado[0] == 0:
                    tn[svm1] = tn[svm1] + 1
                elif real != 0 and resultado[0] != 0:
                    tp[svm1] = tp[svm1] + 1
                elif real != 0 and resultado[0] == 0:
                    fn[svm1] = fn[svm1] + 1
                elif real == 0 and resultado[0] != 0:
                    fp[svm1] = fp[svm1] + 1
            
        expressoes.append(anotacao)
        
    return [acertos, total, expressoes, tp, tn, fp, fn]
        
def trainRelationalAttributes(svms, treinamento, CI, gammaI, combinacoes):
    for svm1 in svms:
        data = []
        classe = []
        
        for fold in treinamento:
            for anotacao in treinamento[fold]:
                if anotacao["classes"]["lm_in-front-of"] > 0 or anotacao["classes"]["lm_above"] > 0 or anotacao["classes"]["lm_below"] > 0 or anotacao["classes"]["lm_near"] > 0 or anotacao["classes"]["lm_right"] > 0 or anotacao["classes"]["lm_left"] > 0:
                    data.append(anotacao["data"])
                    classe.append(anotacao["classes"][svm1])
        
        list = np.unique(classe)
        
        if len(list) == 1:
            if classe[0] == 0:
                classe[0] = 1
            else:
                classe[0] = 0
            
        if combinacoes != {}:
            svms[svm1] = svm.SVC(kernel = "rbf", C = combinacoes[svm1]["C"], gamma = combinacoes[svm1]["gamma"])
        else:
            svms[svm1] = svm.SVC(kernel = "rbf", C = CI, gamma = gammaI)
        svms[svm1].fit(data, classe)
    return svms   