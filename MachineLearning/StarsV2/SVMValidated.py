'''
Created on 31/10/2013

@author: thiagocastroferreira
'''
from sklearn import svm
import numpy as np

def run(inputs = {}, fold = {}):
    CSet = [1.0, 10.0, 100.0, 1000.0]
    gammaSet = [0.1, 0.01, 0.001, 0.0001]
    
    svms = {}
    svmsRelational = {}
    svmsRelational2 = {}
    
    resultados = {}
    
    for CI in CSet:
        for gammaI in gammaSet:
            key = str(CI) + "," + str(gammaI)
            
            svms[key] = {}
            svms[key]["type"] = None
            svms[key]["colour"] = None
            svms[key]["hpos"] = None
            svms[key]["vpos"] = None
            svms[key]["relation"] = None
            
            svms[key]["description_size"] = None
            
            #Trained only with relational descriptions
            svmsRelational[key] = {}
            svmsRelational[key]["lm_type"] = None
            svmsRelational[key]["lm_colour"] = None
            svmsRelational[key]["lm_hpos"] = None
            svmsRelational[key]["lm_vpos"] = None
            svmsRelational[key]["lm_relation"] = None
            
            svmsRelational2[key] = {}
            svmsRelational2[key]["lm2_type"] = None
            svmsRelational2[key]["lm2_colour"] = None
            svmsRelational2[key]["lm2_hpos"] = None
            svmsRelational2[key]["lm2_vpos"] = None
    
            treinamento = {}
            for dir in inputs:
                treinamento[dir] = inputs[dir]
                
            teste = treinamento[fold]
            del treinamento[fold]
            
            svms[key] = train(svms[key], treinamento, CI, gammaI, {})
            
            svmsRelational[key] = trainRelationalAttributes(svmsRelational[key], treinamento, CI, gammaI, {})
            
            svms[key]["lm_type"] = svmsRelational[key]["lm_type"]
            svms[key]["lm_colour"] = svmsRelational[key]["lm_colour"]
            svms[key]["lm_hpos"] = svmsRelational[key]["lm_hpos"]
            svms[key]["lm_vpos"] = svmsRelational[key]["lm_vpos"]
            svms[key]["lm_relation"] = svmsRelational[key]["lm_relation"]
            
            svmsRelational2[key] = trainRelationalAttributes(svmsRelational2[key], treinamento, CI, gammaI, {}, True)
            svms[key]["lm2_type"] = svmsRelational2[key]["lm2_type"]
            svms[key]["lm2_colour"] = svmsRelational2[key]["lm2_colour"]
            svms[key]["lm2_hpos"] = svmsRelational2[key]["lm2_hpos"]
            svms[key]["lm2_vpos"] = svmsRelational2[key]["lm2_vpos"]
    
            resultados[key] = test(svms[key], teste)
    
    return resultados

def run2(inputs = {}, teste = [], combinacoes = {}):
            
    svms = {}
    svms["type"] = None
    svms["colour"] = None
    svms["hpos"] = None
    svms["vpos"] = None
    svms["relation"] = None
    
    svms["description_size"] = None
    
    #Trained only with relational descriptions
    svmsRelational = {}
    svmsRelational["lm_type"] = None
    svmsRelational["lm_colour"] = None
    svmsRelational["lm_hpos"] = None
    svmsRelational["lm_vpos"] = None
    svmsRelational["lm_relation"] = None
    
    svmsRelational2 = {}
    svmsRelational2["lm2_type"] = None
    svmsRelational2["lm2_colour"] = None
    svmsRelational2["lm2_hpos"] = None
    svmsRelational2["lm2_vpos"] = None
    
    svms = train(svms, inputs, 0.0, 0.0, combinacoes)
    
    svmsRelational = trainRelationalAttributes(svmsRelational, inputs, 0.0, 0.0, combinacoes)
    
    svms["lm_type"] = svmsRelational["lm_type"]
    svms["lm_colour"] = svmsRelational["lm_colour"]
    svms["lm_hpos"] = svmsRelational["lm_hpos"]
    svms["lm_vpos"] = svmsRelational["lm_vpos"]
    svms["lm_relation"] = svmsRelational["lm_relation"]
    
    svmsRelational2 = trainRelationalAttributes(svmsRelational2, inputs, 0.0, 0.0, combinacoes, True)
    svms["lm2_type"] = svmsRelational2["lm2_type"]
    svms["lm2_colour"] = svmsRelational2["lm2_colour"]
    svms["lm2_hpos"] = svmsRelational2["lm2_hpos"]
    svms["lm2_vpos"] = svmsRelational2["lm2_vpos"]

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
            if svm1 == "description_size":
                svms[svm1] = svm.SVR(kernel = "rbf", C = combinacoes[svm1]["C"], gamma = combinacoes[svm1]["gamma"])
            else:
                svms[svm1] = svm.SVC(kernel = "rbf", C = combinacoes[svm1]["C"], gamma = combinacoes[svm1]["gamma"])
        else:
            if svm1 == "description_size":
                svms[svm1] = svm.SVR(kernel = "rbf", C = CI, gamma = gammaI)
            else:
                svms[svm1] = svm.SVC(kernel = "rbf", C = CI, gamma = gammaI)
        svms[svm1].fit(data, classe)
    return svms

def trainRelationalAttributes(svms, treinamento, CI, gammaI, combinacoes, landmark = False):
    for svm1 in svms:
        data = []
        classe = []
        
        for fold in treinamento:
            for anotacao in treinamento[fold]:
                if landmark == False:
                    if anotacao["classes"]["relation"] > 0:
                        data.append(anotacao["data"])
                        classe.append(anotacao["classes"][svm1])
                else:
                    if anotacao["classes"]["lm_relation"] > 0:
                        data.append(anotacao["data"])
                        classe.append(anotacao["classes"][svm1])
                    
        list = np.unique(classe)
        
        if len(classe) <= 1:
            svms[svm1] = None
        
        else:
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
            
            if svms[svm1] == None:
                resultado = [0]
            else:
                resultado = svms[svm1].predict([anotacao["data"]])
            real = anotacao["classes"][str(svm1)]
            
            anotacao["previsoes"][str(svm1)] = resultado[0]
            
            if svm1 in ["lm_type", "lm_colour", "lm_vpos", "lm_hpos"] and anotacao["classes"]["relation"] > 0:
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
                    
            elif svm1 in ["lm2_type", "lm2_colour", "lm2_vpos", "lm2_hpos"] and anotacao["classes"]["lm_relation"] > 0:
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
            elif svm1 not in ["lm_type", "lm_colour", "lm_vpos", "lm_hpos", "lm2_type", "lm2_colour", "lm2_vpos", "lm2_hpos"]:
                if real == int(resultado[0]):
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