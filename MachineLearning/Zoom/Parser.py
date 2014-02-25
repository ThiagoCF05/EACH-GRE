'''
Created on 03/01/2014

@author: thiagocastroferreira
'''

import os
import xml.etree.ElementTree as ET

def parseMapas():
    maps = {}
    
    files = os.listdir("Mapas/")

    for f in files:
        if f != ".DS_Store":
            map = f.split()[1].split(".")[0]
            file = open("Mapas/" + f, "r")
            doc = file.readline()
            file.close()
            doc = doc.split('\r')
            maps[map] = doc
    
    for map in ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20"]:
        linha = 0
        propriedades = []
        
        doc = maps[map]
        maps[map] = {}
        
        for row in doc:
            linha = linha + 1
            elements = row.split(';')
            if linha == 1:
                for element in elements:
                    propriedades.append(element.strip())
            else:
                objeto = {}
                objeto_id = str
                
                for i in range(0, len(elements)):
                    if i == 0:
                        objeto_id = elements[i].strip()
                    
                    elif propriedades[i] == "between":
                        elementos = elements[i].split("-")
                        
                        valores = []
                        for elemento in elementos:
                            valores.append(elemento.strip("[]").split(","))
                        
                        if [''] in valores:
                            valores.remove([''])
                        objeto[propriedades[i]] = valores
                    else:
                        valores = elements[i].split(',')
                        for j in range(0, len(valores)):
                            valores[j] = valores[j].strip()
                        
                        if valores[0] == '':
                            objeto[propriedades[i]] = []
                        else:
                            if '' in valores:
                                valores.remove('')
                            objeto[propriedades[i]] = valores
                maps[map][objeto_id] = objeto
    
    return maps
    
def parseAnnotation():
    expressoes = []
    
    participantes = {}
    files = os.listdir("Expressoes/")
    for f in files:
        if f != ".DS_Store":
            tree = ET.parse("Expressoes/" + f)
            root = tree.getroot()
            
            participantes[root.attrib["ID"]] = root.attrib
            
            participante_id = root.attrib["ID"]
            
            del participantes[root.attrib["ID"]]["ID"]
            
            for contexto in root.findall("CONTEXT"):
                expressao = {}
                expressao["caracteristicas"] = {}
                expressao["caracteristicas"]["context"] = contexto.attrib["ID"]
                expressao["caracteristicas"]["trial"] = participante_id
                expressao["caracteristicas"]["string"] = contexto.attrib["WORD-STRING"]
                
                expressao["anotacoes"] = {}
                
                for child in contexto:
                    target = child.attrib["TARGET.ID"]
                    
                    expressao["anotacoes"][target] = {}
                    expressao["anotacoes"][target]["tg"] = {}
                    
                    for atributo in child:
                        aux = atributo.attrib["NAME"].split(".")
                        
                        if aux[0] in ["d1", "d2", "d3", "d4"]:
                            if aux[0] not in expressao["anotacoes"][target].keys():
                                expressao["anotacoes"][target][aux[0]] = {}
                                
                            expressao["anotacoes"][target][aux[0]][aux[1]] = [atributo.attrib["VALUE"]]
                        else:
                            expressao["anotacoes"][target]["tg"][atributo.attrib["NAME"]] = atributo.attrib["VALUE"].strip("[]").split(",")
                expressoes.append(expressao)
    
    return [expressoes, participantes]

def parseFeatureVector(dominios, targets):
    featureVector = {}
    
    for contexto in dominios.keys():
        targetSet = targets[contexto]
        
        for target in targetSet:
            if contexto not in featureVector.keys():
                featureVector[contexto] = {}
                
            featureVector[contexto][target] = {}
            featureVector[contexto][target]["num_tg_type"] = 0
            featureVector[contexto][target]["num_tg_next"] = len(dominios[contexto][target]["next-to"])
            
            for element in dominios[contexto].keys():
                if element != target:
                    if dominios[contexto][target]["type"][0] == dominios[contexto][element]["type"][0]:
                        featureVector[contexto][target]["num_tg_type"] = featureVector[contexto][target]["num_tg_type"] + 1
    
    return featureVector

def parseSVMInput(anotacoes, targets, featureVector, participantes, frequencias, incluiParticipante = True):
    input = []
    
    for anotacao in anotacoes:
        classes = {}
        participante = anotacao["caracteristicas"]["trial"]
        contexto = anotacao["caracteristicas"]["context"]
        targetSet = targets[contexto]
        
        for target in targetSet:
            vetor = []
            
            # Expressao composta ou nao?
            if len(targetSet) > 1:
                vetor.append(1)
            else:
                vetor.append(0)
            
            if incluiParticipante == True:
                useRelation = 0
                
                vetor.append(int(participante))
                if participantes[participante]["GENDER"] == "m":
                    vetor.append(0)
                else:
                    vetor.append(1)
                    
                idade = int(participantes[participante]["AGE"])
                if idade <= 20:
                    vetor.append(0)
                elif idade > 20 and idade <= 25:
                    vetor.append(1)
                elif idade >= 26 and idade <= 30:
                    vetor.append(2)
                elif idade > 30 and idade <= 40:
                    vetor.append(3)
                elif idade > 40 and idade <= 50:
                    vetor.append(4)
                elif idade > 50 and idade <= 60:
                    vetor.append(5)
                else:
                    vetor.append(6)

                
                atributos = ["type","in","name","next-to","in-front-of","other","right-to","left-to","behind", "between"]
                for atributo in atributos:
                    if atributo in frequencias[participante]["target"].keys():
                        vetor.append(frequencias[participante]["target"][atributo])
                        
                        if atributo in ["next-to", "right-to", "left-to", "behind", "in-front-of", "in", "between"]:
                            useRelation = 1
    #                 else:
    #                     vetor.append(0)
                    
    #             for atributo in atributos:
    #                 if atributo in frequencias[participante]["landmark"].keys():
    #                     vetor.append(frequencias[participante]["landmark"][atributo])
    #                 else:
    #                     vetor.append(0)
                vetor.append(useRelation)
            
            vetor.append(featureVector[contexto][target]["num_tg_type"])
            vetor.append(featureVector[contexto][target]["num_tg_next"])
            
            if target in anotacao["anotacoes"].keys():
                vetor.append(len(anotacao["anotacoes"][target].keys()) - 1)
                
                if "type" in anotacao["anotacoes"][target]["tg"].keys():
                    classes["type"] = 1
                else:
                    classes["type"] = 0
                
                if "name" in anotacao["anotacoes"][target]["tg"].keys():
                    classes["name"] = 1
                else:
                    classes["name"] = 0
                
                if "other" in anotacao["anotacoes"][target]["tg"].keys():
                    classes["other"] = 1
                else:
                    classes["other"] = 0
                
                if "in" in anotacao["anotacoes"][target]["tg"].keys():
                    classes["in"] = 1
                else:
                    classes["in"] = 0
                    
                if "between" in anotacao["anotacoes"][target]["tg"].keys():
                    classes["between"] = 1
                else:
                    classes["between"] = 0
                    
                if "behind" in anotacao["anotacoes"][target]["tg"].keys():
                    classes["behind"] = 1
                else:
                    classes["behind"] = 0
                
                if "next-to" in anotacao["anotacoes"][target]["tg"].keys():
                    classes["next-to"] = 1
                else:
                    classes["next-to"] = 0
                
                if "right-to" in anotacao["anotacoes"][target]["tg"].keys():
                    classes["right-to"] = 1
                else:
                    classes["right-to"] = 0
                
                if "left-to" in anotacao["anotacoes"][target]["tg"].keys():
                    classes["left-to"] = 1
                else:
                    classes["left-to"] = 0
                    
                if "in-front-of" in anotacao["anotacoes"][target]["tg"].keys():
                    classes["in-front-of"] = 1
                else:
                    classes["in-front-of"] = 0
            else:
                vetor.append(0)
                classes["type"] = 0
                classes["name"] = 0
                classes["other"] = 0
                classes["in"] = 0
                classes["left-to"] = 0
                classes["right-to"] = 0
                classes["next-to"] = 0
                classes["in-front-of"] = 0
                classes["behind"] = 0
                classes["between"] = 0
            
            
#             for landmark in anotacao["anotacoes"][target].keys():
#                 if landmark != "tg":
#                     if "type" in anotacao["descricao"][target][landmark].keys():
#                         classes[landmark + "_type"] = 1
#                     else:
#                         classes[landmark + "_type"] = 0
#                     
#                     if "name" in anotacao["descricao"][target][landmark].keys():
#                         classes[landmark + "_name"] = 1
#                     else:
#                         classes[landmark + "_name"] = 0
#                     
#                     if "other" in anotacao["descricao"][target][landmark].keys():
#                         classes[landmark + "_other"] = 1
#                     else:
#                         classes[landmark + "_other"] = 0
                    
            data = {}
            data["data"] = vetor
            data["classes"] = classes
            data["anotacao"] = anotacao
            input.append(data)
    
    return input