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
    
    resultados = {}
    
    for CI in CSet:
        for gammaI in gammaSet:
            key = str(CI) + "," + str(gammaI)
            
            svms[key] = {}
            svms[key]["type"] = None
            svms[key]["col"] = None
            svms[key]["size"] = None
            svms[key]["loc"] = None
            svms[key]["relation"] = None
            
            #Trained only with relational descriptions
            svmsRelational[key] = {}
            svmsRelational[key]["lm_type"] = None
            svmsRelational[key]["lm_col"] = None
            svmsRelational[key]["lm_size"] = None
            svmsRelational[key]["lm_loc"] = None
    
            treinamento = {}
            for dir in inputs:
                treinamento[dir] = inputs[dir]
                
            teste = treinamento[fold]
            del treinamento[fold]
            
            svms[key] = train(svms[key], treinamento, CI, gammaI, {})
            
            svmsRelational[key] = trainRelationalAttributes(svmsRelational[key], treinamento, CI, gammaI, {})
            
            svms[key]["lm_type"] = svmsRelational[key]["lm_type"]
            svms[key]["lm_col"] = svmsRelational[key]["lm_col"]
            svms[key]["lm_size"] = svmsRelational[key]["lm_size"]
            svms[key]["lm_loc"] = svmsRelational[key]["lm_loc"]
    
            resultados[key] = test(svms[key], teste)
    
    return resultados

def run2(inputs = {}, teste = [], combinacoes = {}):
            
    svms = {}
    svms["type"] = None
    svms["col"] = None
    svms["size"] = None
    svms["loc"] = None
    svms["relation"] = None
    
    #Trained only with relational descriptions
    svmsRelational = {}
    svmsRelational["lm_type"] = None
    svmsRelational["lm_col"] = None
    svmsRelational["lm_size"] = None
    svmsRelational["lm_loc"] = None
    
    svms = train(svms, inputs, 0.0, 0.0, combinacoes)
    
    svmsRelational = trainRelationalAttributes(svmsRelational, inputs, 0.0, 0.0, combinacoes)
    
    svms["lm_type"] = svmsRelational["lm_type"]
    svms["lm_col"] = svmsRelational["lm_col"]
    svms["lm_size"] = svmsRelational["lm_size"]
    svms["lm_loc"] = svmsRelational["lm_loc"]

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
            
            if svms[svm1] == None:
                resultado = [0]
            else:
                resultado = svms[svm1].predict([anotacao["data"]])
            real = anotacao["classes"][str(svm1)]
            
            anotacao["previsoes"][str(svm1)] = resultado[0]
            
            if svm1 in ["lm_type", "lm_col", "lm_size", "lm_loc"] and anotacao["classes"]["relation"] > 0:
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
            elif svm1 not in ["lm_type", "lm_col", "lm_size", "lm_loc"]:
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
                if anotacao["classes"]["relation"] > 0:
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