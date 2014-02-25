'''
Created on 07/02/2014

@author: thiagocastroferreira
'''

import itertools as iter

def isUnderspecified(expressao, dominio):
    properties = expressao["descricao"]["tg"]
    
    distractors = {}
    for property in properties.keys():
        distractors = {}
        for element in properties[property]:
            for object in dominio.keys():
                if property in dominio[object].keys():
                    if element in dominio[object][property]:
                        distractors[object] = dominio[object]
            dominio = distractors
    
    if len(distractors.keys()) > 1:
        return True
    return False
    
def isOverspecified(expressao, dominio):
    properties = expressao["descricao"]["tg"]
    
    permutations = iter.permutations(properties.keys())
    
    for permutation in permutations:
        i = 0
        for property in permutation:
            i = i + 1
            distractors = {}
            for element in properties[property]:
                for object in dominio.keys():
                    if property in dominio[object].keys():
                        if element in dominio[object][property]:
                            distractors[object] = dominio[object]
                dominio = distractors
        
            if len(distractors.keys()) == 1 and i < len(properties.keys()):
                return True
    return False

#contabiliza frequenca dos atributos
def countAttributeFrequencyIndividual(folds, teste):
    foldsAux = {}
    
    for fold in folds:
        if fold != teste:
            foldsAux[fold] = folds[fold]
            
    frequency = {}
    
    for fold in foldsAux:
        for anotacao in folds[fold]:
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
    return frequency

def defineExpressao(previsoes, dominio, target):
    #descricao prevista pela svm
    descricao = {}
    
    descricao[target] = {}
    
    for atributo in dominio[target].keys():
        descricao[target][atributo] = dominio[target][atributo]
    
    if "under" in descricao[target].keys():
        del descricao[target]["under"]
    if "behind" in descricao[target].keys():
        del descricao[target]["behind"]
    
    relacional = False
    landmark = str
    for atributo in ["type","col","size","loc","relation","lm_type","lm_col","lm_size","lm_loc"]:
        element = atributo.split("_")
        
        if len(element) == 1 and atributo != "relation":
            if previsoes[atributo] == 0:
                if atributo in descricao[target].keys():
                    del descricao[target][atributo]
        
        elif len(element) == 2 and relacional == True:
            if previsoes[atributo] == 0:
                del descricao[landmark][element[1]]
        
        elif len(element) == 1 and atributo == "relation":
            if previsoes[atributo] == 0:
                if "in-front-of" in descricao[target].keys():
                    del descricao[target]["in-front-of"]
                del descricao[target]["on-top-of"]
                del descricao[target]["next-to"]
                del descricao[target]["right-of"]
                del descricao[target]["left-of"]
            else:
                if previsoes[atributo] == 1:
                    if "in-front-of" in descricao[target].keys():
                        del descricao[target]["in-front-of"]
                    del descricao[target]["next-to"]
                    del descricao[target]["right-of"]
                    del descricao[target]["left-of"]
                    
                    if len(descricao[target]["on-top-of"]) == 0:
                        del descricao[target]["on-top-of"]
                    else:
                        landmark = descricao[target]["on-top-of"][0]
                        descricao[landmark] = {}
                        relacional = True
                        
                        for key in dominio[landmark].keys():
                            descricao[landmark][key] = dominio[landmark][key]
                        
                        if "in-front-of" in descricao[landmark].keys():
                            del descricao[landmark]["in-front-of"]
                        del descricao[landmark]["on-top-of"]
                        del descricao[landmark]["next-to"]
                        del descricao[landmark]["right-of"]
                        del descricao[landmark]["left-of"]
                        del descricao[landmark]["under"]
                        if "behind" in descricao[landmark].keys():
                            del descricao[landmark]["behind"]
                
                elif previsoes[atributo] == 2:
                    if "in-front-of" in descricao[target].keys():
                        del descricao[target]["in-front-of"]
                    del descricao[target]["on-top-of"]
                    del descricao[target]["right-of"]
                    del descricao[target]["left-of"]
                    
                    if len(descricao[target]["next-to"]) == 0:
                        del descricao[target]["next-to"]
                    else:
                        landmark = descricao[target]["next-to"][0]
                        descricao[landmark] = {}
                        relacional = True
                        
                        for key in dominio[landmark].keys():
                            descricao[landmark][key] = dominio[landmark][key]
                        
                        if "in-front-of" in descricao[landmark].keys():
                            del descricao[landmark]["in-front-of"]
                        del descricao[landmark]["on-top-of"]
                        del descricao[landmark]["next-to"]
                        del descricao[landmark]["right-of"]
                        del descricao[landmark]["left-of"]
                        del descricao[landmark]["under"]
                        if "behind" in descricao[landmark].keys():
                            del descricao[landmark]["behind"]
                
                elif previsoes[atributo] == 3:
                    if "in-front-of" in descricao[target].keys():
                        del descricao[target]["in-front-of"]
                    del descricao[target]["on-top-of"]
                    del descricao[target]["next-to"]
                    del descricao[target]["left-of"]
                    
                    if len(descricao[target]["right-of"]) == 0:
                        del descricao[target]["right-of"]
                    else:
                        landmark = descricao[target]["right-of"][0]
                        descricao[landmark] = {}
                        relacional = True
                        
                        for key in dominio[landmark].keys():
                            descricao[landmark][key] = dominio[landmark][key]
                        
                        if "in-front-of" in descricao[landmark].keys():
                            del descricao[landmark]["in-front-of"]
                        del descricao[landmark]["on-top-of"]
                        del descricao[landmark]["next-to"]
                        del descricao[landmark]["right-of"]
                        del descricao[landmark]["left-of"]
                        del descricao[landmark]["under"]
                        if "behind" in descricao[landmark].keys():
                            del descricao[landmark]["behind"]
                
                elif previsoes[atributo] == 4:
                    if "in-front-of" in descricao[target].keys():
                        del descricao[target]["in-front-of"]
                    del descricao[target]["on-top-of"]
                    del descricao[target]["next-to"]
                    del descricao[target]["right-of"]
                    
                    if len(descricao[target]["left-of"]) == 0:
                        del descricao[target]["left-of"]
                    else:
                        landmark = descricao[target]["left-of"][0]
                        descricao[landmark] = {}
                        relacional = True
                        
                        for key in dominio[landmark].keys():
                            descricao[landmark][key] = dominio[landmark][key]
                        
                        if "in-front-of" in descricao[landmark].keys():
                            del descricao[landmark]["in-front-of"]
                        del descricao[landmark]["on-top-of"]
                        del descricao[landmark]["next-to"]
                        del descricao[landmark]["right-of"]
                        del descricao[landmark]["left-of"]
                        del descricao[landmark]["under"]
                        if "behind" in descricao[landmark].keys():
                            del descricao[landmark]["behind"]
                
                elif previsoes[atributo] == 5 and "in-front-of" in descricao[target].keys():
                    del descricao[target]["on-top-of"]
                    del descricao[target]["next-to"]
                    del descricao[target]["right-of"]
                    del descricao[target]["left-of"]
                    
                    if len(descricao[target]["in-front-of"]) == 0:
                        del descricao[target]["in-front-of"]
                    else:
                        landmark = descricao[target]["in-front-of"][0]
                        descricao[landmark] = {}
                        relacional = True
                        
                        for key in dominio[landmark].keys():
                            descricao[landmark][key] = dominio[landmark][key]
                        
                        if "in-front-of" in descricao[landmark].keys():
                            del descricao[landmark]["in-front-of"]
                        del descricao[landmark]["on-top-of"]
                        del descricao[landmark]["next-to"]
                        del descricao[landmark]["right-of"]
                        del descricao[landmark]["left-of"]
                        del descricao[landmark]["under"]
                        if "behind" in descricao[landmark].keys():
                            del descricao[landmark]["behind"]
    return descricao