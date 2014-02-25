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
    
    resultados = {}
    
    for CI in CSet:
        for gammaI in gammaSet:
            key = str(CI) + "," + str(gammaI)
            
            svms[key] = {}
            svms[key]["type"] = None
            svms[key]["size"] = None
            svms[key]["orientation"] = None
            svms[key]["colour"] = None
            svms[key]["x-dimension"] = None
            svms[key]["y-dimension"] = None
    
            treinamento = {}
            for dir in inputs:
                treinamento[dir] = inputs[dir]
                
            teste = treinamento[fold]
            del treinamento[fold]
            
            svms[key] = train(svms[key], treinamento, CI, gammaI, {})
    
            resultados[key] = test(svms[key], teste)
    
    return resultados

def run2(inputs = {}, teste = [], combinacoes = {}):
            
    svms = {}
    svms["type"] = None
    svms["size"] = None
    svms["orientation"] = None
    svms["colour"] = None
    svms["x-dimension"] = None
    svms["y-dimension"] = None
    
    svms = train(svms, inputs, 0.0, 0.0, combinacoes)

    resultados = test(svms, teste)
    
    return resultados

def train(svms, treinamento, CI, gammaI, combinacoes):
    for svm1 in svms:
        data = []
        classe = []
        
        for fold in treinamento:
            for anotacao in treinamento[fold]:
                for target in anotacao.keys():
                    data.append(anotacao[target]["data"])
                    classe.append(anotacao[target]["classes"][svm1])
        
        list = np.unique(classe)
        
        if len(list) == 1:
            if classe[0] == 0:
                classe[0] = 1
            else:
                classe[0] = 0
        
        if combinacoes != {}:
            svms[svm1] = svm.SVC(kernel = "rbf", C = combinacoes[svm1]["C"], gamma = combinacoes[svm1]["gamma"], probability = True)
        else:
            svms[svm1] = svm.SVC(kernel = "rbf", C = CI, gamma = gammaI, probability = True)
        svms[svm1].fit(data, classe)
    return svms

def test(svms, teste):
    acertos = {}
    total = {}
    expressoes = []
    
    for anotacao in teste:
        for target in anotacao.keys():
            anotacao[target]["previsoes"] = {}
            
            for svm1 in svms:
                if svm1 not in acertos.keys():
                    acertos[svm1] = 0.0
                    total[svm1] = 0.0
                
                resultado = svms[svm1].predict_proba([anotacao[target]["data"]])
                real = anotacao[target]["classes"][str(svm1)]
                
                anotacao[target]["previsoes"][str(svm1)] = resultado[0][1]
                
                if real == int(resultado[0][1]):
                    acertos[svm1] = acertos[svm1] + 1.0
                
                total[svm1] = total[svm1] + 1.0
            
        expressoes.append(anotacao)
        
    return [acertos, total, expressoes]