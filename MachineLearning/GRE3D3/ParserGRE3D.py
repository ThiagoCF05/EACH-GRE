'''
Created on 22/08/2013

@author: thiagocastroferreira
'''

import numpy as num
import xml.etree.ElementTree as ET
import Utils as utils
        
# Formata as expressoes geradas pelos participantes do experimento Stars
def parseDominio(dir = ''):
    dominios = {}
    
    file = open(dir + "dominios.csv", "r")
    doc = file.readline()
    file.close()
    doc = doc.split('\r')
    
    propriedades = []
    dominios = {}
    
    
    for i in range(0, len(doc)):
        row = doc[i].split(";")
        if i == 0:
            for element in row:
                propriedades.append(element.strip())
        else:
            map = ""
            id = ""
            for j in range(0, len(row)):
                if j == 0:
                    map = str(row[j])
                    if map not in dominios.keys():
                        dominios[map] = {}
                elif j == 1:
                    id = str(row[j])
                    if id not in dominios[map].keys():
                        dominios[map][id] = {}
                else:
                    atributo = propriedades[j]
                    if atributo not in dominios[map][id].keys():
                        dominios[map][id][atributo] = []
                    elements = row[j].split(",")
                    
                    for element in elements:
                        if element != "":
                            dominios[map][id][atributo].append(element.strip())
    
    return dominios


# Formata as descricoes do experimento GRE3D em xml
def parseAnnotation(dir = ''):
    tree = ET.parse(dir + 'gre3d3_descricoes.xml') 
    root = tree.getroot()
    anotacoes = []
    for trial in root:
        anotacao = {}
        anotacao["caracteristicas"] = {}
        anotacao["descricao"] = {}
        
        participante = trial.attrib["p"]
        anotacao["caracteristicas"]["trial"] = participante
        context = trial.attrib["s"]
        anotacao["caracteristicas"]["context"] = context
        
        atributos = trial.find("PATTERN").find("REORDERED_PATTERN").text
        valores = trial.find("STRING-DESCRIPTION").find("CLEANED").text
        
        atributos = atributos.split()
        valores = valores.split()
        
        for i in range(0, len(atributos)):
            atributo = atributos[i].split("_")
            
            if len(atributo) == 1:
                if valores[i] not in anotacao["descricao"]["tg"].keys():
                    anotacao["descricao"]["tg"][valores[i]] = []
                anotacao["descricao"]["tg"][valores[i]].append("lm")
            else:
                if atributo[0] not in anotacao["descricao"].keys():
                    anotacao["descricao"][atributo[0]] = {}
                anotacao["descricao"][atributo[0]][atributo[1]] = [valores[i]]
                
        anotacoes.append(anotacao)
    return anotacoes  

# Formata as expressoes geradas pelos participantes do experimento Stars
def parseParticipantes(dir = ''):
    dominios = {}
    
    file = open(dir + "locutores.csv", "r")
    doc = file.readline()
    file.close()
    doc = doc.split('\r')
    
    propriedades = []
    caracteristicas = {}
    
    row = doc[0].split(",")
    
    for element in row:
        propriedades.append(element.strip())
    
    for i in range(1, len(doc)):
        row = doc[i].split(",")
        
        caracteristicas[row[0]] = {}
        
        if str(row[1]).strip() == "male":
            caracteristicas[row[0]]["genre"] = 0
        else:
            caracteristicas[row[0]]["genre"] = 1
            
        if row[2] == "16-20":
            caracteristicas[row[0]]["age"] = 0
        elif row[2] == "20-25":
            caracteristicas[row[0]]["age"] = 1
        elif row[2] == "26-30":
            caracteristicas[row[0]]["age"] = 2
        elif row[2] == "30-40":
            caracteristicas[row[0]]["age"] = 3
        elif row[2] == "40-50":
            caracteristicas[row[0]]["age"] = 4
        elif row[2] == "50-60":
            caracteristicas[row[0]]["age"] = 5
        else:
            caracteristicas[row[0]]["age"] = 6
    
    return caracteristicas


def parseSVMInput(anotacoes, featureVector, participantes, frequencias, incluiParticipante = True):
    input = []
    
    for anotacao in anotacoes:
        classes = {}
        vetor = []
        participante = anotacao["caracteristicas"]["trial"]
        contexto = anotacao["caracteristicas"]["context"]
        
        if incluiParticipante == True:
            vetor.append(int(participante))
            vetor.append(int(participantes[participante]["genre"]))
            vetor.append(int(participantes[participante]["age"]))
            
            atributos = ["type", "col", "size", "loc", "next-to", "right-of", "left-of", "on-top-of", "in-front-of"]
#             for atributo in atributos:
#                 if atributo in frequencias[participante]["target"].keys():
#                     vetor.append(frequencias[participante]["target"][atributo])
#                 else:
#                     vetor.append(0)
#                      
#             for atributo in atributos:
#                 if atributo in frequencias[participante]["landmark"].keys():
#                     vetor.append(frequencias[participante]["landmark"][atributo])
#                 else:
#                     vetor.append(0)
        
        vetor.append(participantes[participante]["tg_description_size"])
        vetor.append(participantes[participante]["lm_description_size"])
        vetor.append(participantes[participante]["num_relations"])
#             vetor.append(participantes[participante]["overspecified_mean"])
#             vetor.append(participantes[participante]["underspecified_mean"])
#             vetor.append(participantes[participante]["minimal_mean"])
        
        if featureVector[contexto]["tg_size"] == "small":
            vetor.append(0)
        else:
            vetor.append(1)
        
        if featureVector[contexto]["lm_size"] == "small":
            vetor.append(0)
        else:
            vetor.append(1)
            
        if featureVector[contexto]["relation"] == "none":
            vetor.append(0)
        elif featureVector[contexto]["relation"] == "horizontal":
            vetor.append(0)
        else:
            vetor.append(1)
        
        vetor.append(featureVector[contexto]["num_tg_size"])
        vetor.append(featureVector[contexto]["num_lm_size"])
        vetor.append(featureVector[contexto]["num_tg_col"])
        vetor.append(featureVector[contexto]["num_lm_col"])
        vetor.append(featureVector[contexto]["num_tg_type"])
        vetor.append(featureVector[contexto]["num_lm_type"])
        vetor.append(featureVector[contexto]["tg_lm_size"])
        vetor.append(featureVector[contexto]["tg_lm_col"])
        vetor.append(featureVector[contexto]["tg_lm_type"])
        
#         vetor.append(featureVector[contexto]["dp_tg_col"])
#         vetor.append(featureVector[contexto]["dp_lm_col"])
#         vetor.append(featureVector[contexto]["dp_tg_type"])
#         vetor.append(featureVector[contexto]["dp_lm_type"])
#         vetor.append(featureVector[contexto]["dp_tg_size"])
#         vetor.append(featureVector[contexto]["dp_lm_size"])
#         vetor.append(featureVector[contexto]["dp_tg_loc"])
#         vetor.append(featureVector[contexto]["dp_lm_loc"])
#              
#         vetor.append(featureVector[contexto]["saliency_col"])
#         vetor.append(featureVector[contexto]["saliency_type"])
#         vetor.append(featureVector[contexto]["saliency_size"])
#         vetor.append(featureVector[contexto]["saliency_loc"])
        
        if "type" in anotacao["descricao"]["tg"].keys():
            classes["type"] = 1
        else:
            classes["type"] = 0
        
        if "col" in anotacao["descricao"]["tg"].keys():
            classes["col"] = 1
        else:
            classes["col"] = 0
        
        if "size" in anotacao["descricao"]["tg"].keys():
            classes["size"] = 1
        else:
            classes["size"] = 0
            
        if "loc" in anotacao["descricao"]["tg"].keys():
            classes["loc"] = 1
        else:
            classes["loc"] = 0
            
        if "on-top-of" in anotacao["descricao"]["tg"].keys():
            classes["relation"] = 1
        elif "next-to" in anotacao["descricao"]["tg"].keys():
            classes["relation"] = 2
        elif "left-of" in anotacao["descricao"]["tg"].keys():
            classes["relation"] = 4
        elif "right-of" in anotacao["descricao"]["tg"].keys():
            classes["relation"] = 3
        elif "in-front-of" in anotacao["descricao"]["tg"].keys():
            classes["relation"] = 5
        else:
            classes["relation"] = 0
            
        if classes["relation"] > 0:
            if "type" in anotacao["descricao"]["lm"].keys():
                classes["lm_type"] = 1
            else:
                classes["lm_type"] = 0
            
            if "col" in anotacao["descricao"]["lm"].keys():
                classes["lm_col"] = 1
            else:
                classes["lm_col"] = 0
            
            if "size" in anotacao["descricao"]["lm"].keys():
                classes["lm_size"] = 1
            else:
                classes["lm_size"] = 0
                
            if "loc" in anotacao["descricao"]["lm"].keys():
                classes["lm_loc"] = 1
            else:
                classes["lm_loc"] = 0
        else:
            classes["lm_type"] = 0
            classes["lm_col"] = 0
            classes["lm_size"] = 0
            classes["lm_loc"] = 0
                
        data = {}
        data["data"] = vetor
        data["classes"] = classes
        data["anotacao"] = anotacao
        input.append(data)
    
    return input

def parseFeatureVector(dominios, targets):
    featureVector = {}
    attributes_saliencies = {}
    
    for contexto in dominios.keys():
        
        attributes_saliencies[contexto] = {}
        
        for element in dominios[contexto].keys():
            for atributo in ["type", "size", "col", "loc"]:
                if atributo not in attributes_saliencies[contexto].keys():
                    attributes_saliencies[contexto][atributo] = {}
                if dominios[contexto][element][atributo][0] not in attributes_saliencies[contexto][atributo].keys():
                    attributes_saliencies[contexto][atributo][dominios[contexto][element][atributo][0]] = 1
                else:
                    attributes_saliencies[contexto][atributo][dominios[contexto][element][atributo][0]] = attributes_saliencies[contexto][atributo][dominios[contexto][element][atributo][0]] + 1
    
    attributes_saliency = {}
    for contexto in attributes_saliencies.keys():
        attributes_saliency[contexto] = {}
        for atributo in ["type", "size", "col", "loc"]:
            attributes_saliency[contexto][atributo] = 0
            for valor in attributes_saliencies[contexto][atributo].keys():
                if attributes_saliencies[contexto][atributo][valor] > attributes_saliency[contexto][atributo]:
                    attributes_saliency[contexto][atributo] = attributes_saliencies[contexto][atributo][valor]
    
    del attributes_saliencies
    
    for contexto in dominios.keys():
        target = targets[contexto]
        landmark = str
        relation = "none"
        
        # define o landmark do objeto mapeado
        if len(dominios[contexto][target]["next-to"]) > 0:
            landmark = dominios[contexto][target]["next-to"][0]
        
        # define a orientacao do objeto  
        if len(dominios[contexto][target]["right-of"]) > 0:
            relation = "horizontal"
        elif len(dominios[contexto][target]["left-of"]) > 0:
            relation = "horizontal"
        elif len(dominios[contexto][target]["in-front-of"]) > 0:
            relation = "horizontal"
        elif len(dominios[contexto][target]["on-top-of"]) > 0:
            relation = "vertical"
        
        if contexto not in featureVector.keys():
            featureVector[contexto] = {}
        
        featureVector[contexto]["tg_size"] = dominios[contexto][target]["size"][0]
        featureVector[contexto]["lm_size"] = dominios[contexto][landmark]["size"][0]
        featureVector[contexto]["relation"] = relation
        
        # define se o landmark e objeto-alvo possuem o mesmo tamanho
        if dominios[contexto][target]["size"][0] == dominios[contexto][landmark]["size"][0]:
            featureVector[contexto]["tg_lm_size"] = 1
        else:
            featureVector[contexto]["tg_lm_size"] = 0
        
        # define se o landmark e objeto-alvo possuem a mesma cor
        if dominios[contexto][target]["col"][0] == dominios[contexto][landmark]["col"][0]:
            featureVector[contexto]["tg_lm_col"] = 1
        else:
            featureVector[contexto]["tg_lm_col"] = 0
        
        # define se o landmark e objeto-alvo possuem o mesmo tipo
        if dominios[contexto][target]["type"][0] == dominios[contexto][landmark]["type"][0]:
            featureVector[contexto]["tg_lm_type"] = 1
        else:
            featureVector[contexto]["tg_lm_type"] = 0
        
        featureVector[contexto]["num_tg_size"] = 0
        featureVector[contexto]["num_lm_size"] = 0
        featureVector[contexto]["num_tg_col"] = 0
        featureVector[contexto]["num_lm_col"] = 0
        featureVector[contexto]["num_tg_type"] = 0
        featureVector[contexto]["num_lm_type"] = 0
        
        featureVector[contexto]["dp_tg_col"] = 0
        featureVector[contexto]["dp_lm_col"] = 0
        featureVector[contexto]["dp_tg_type"] = 0
        featureVector[contexto]["dp_lm_type"] = 0
        featureVector[contexto]["dp_tg_size"] = 0
        featureVector[contexto]["dp_lm_size"] = 0
        featureVector[contexto]["dp_tg_loc"] = 0
        featureVector[contexto]["dp_lm_loc"] = 0
        
        featureVector[contexto]["saliency_col"] = attributes_saliency[contexto]["col"]
        featureVector[contexto]["saliency_type"] = attributes_saliency[contexto]["type"]
        featureVector[contexto]["saliency_size"] = attributes_saliency[contexto]["size"]
        featureVector[contexto]["saliency_loc"] = attributes_saliency[contexto]["loc"]
        
        for element in dominios[contexto].keys():
            if element != target:
                if dominios[contexto][target]["size"][0] == dominios[contexto][element]["size"][0]:
                    featureVector[contexto]["num_tg_size"] = featureVector[contexto]["num_tg_size"] + 1
                else:
                    featureVector[contexto]["dp_tg_size"] = featureVector[contexto]["dp_tg_size"] + 1
                
                if dominios[contexto][target]["col"][0] == dominios[contexto][element]["col"][0]:
                    featureVector[contexto]["num_tg_col"] = featureVector[contexto]["num_tg_col"] + 1
                else:
                    featureVector[contexto]["dp_tg_col"] = featureVector[contexto]["dp_tg_col"] + 1
                
                if dominios[contexto][target]["type"][0] == dominios[contexto][element]["type"][0]:
                    featureVector[contexto]["num_tg_type"] = featureVector[contexto]["num_tg_type"] + 1
                else:
                    featureVector[contexto]["dp_tg_type"] = featureVector[contexto]["dp_tg_type"] + 1
                    
                if dominios[contexto][target]["loc"][0] != dominios[contexto][element]["loc"][0]:
                    featureVector[contexto]["dp_tg_loc"] = featureVector[contexto]["dp_tg_loc"] + 1
                    
            if element != landmark:
                if dominios[contexto][landmark]["size"][0] == dominios[contexto][element]["size"][0]:
                    featureVector[contexto]["num_lm_size"] = featureVector[contexto]["num_lm_size"] + 1
                else:
                    featureVector[contexto]["dp_lm_size"] = featureVector[contexto]["dp_lm_size"] + 1
                
                if dominios[contexto][landmark]["col"][0] == dominios[contexto][element]["col"][0]:
                    featureVector[contexto]["num_lm_col"] = featureVector[contexto]["num_lm_col"] + 1
                else:
                    featureVector[contexto]["dp_lm_col"] = featureVector[contexto]["dp_lm_col"] + 1
                
                if dominios[contexto][landmark]["type"][0] == dominios[contexto][element]["type"][0]:
                    featureVector[contexto]["num_lm_type"] = featureVector[contexto]["num_lm_type"] + 1
                else:
                    featureVector[contexto]["dp_lm_col"] = featureVector[contexto]["dp_lm_col"] + 1
                    
                if dominios[contexto][landmark]["loc"][0] != dominios[contexto][element]["loc"][0]:
                    featureVector[contexto]["dp_lm_loc"] = featureVector[contexto]["dp_lm_loc"] + 1
    
    return featureVector

def descriptionsMeans(folds, teste, participantes, dominios):
    foldsAux = {}
    
    for fold in folds:
        if fold != teste:
            foldsAux[fold] = folds[fold]
    
    tg_description_size = {}
    lm_description_size = {}
    num_relations = {}  
    overspecified_description = {}
    underspecified_description = {}
    minimal_description = {}
        
    for fold in foldsAux:
        for anotacao in foldsAux[fold]:
            participante = anotacao["caracteristicas"]["trial"]
            
            if participante not in tg_description_size.keys():
                tg_description_size[participante] = []
                lm_description_size[participante] = []
                num_relations[participante] = []
                overspecified_description[participante] = 0
                underspecified_description[participante] = 0
                minimal_description[participante] = 0
            
            overspecified = utils.isOverspecified(anotacao, dominios[anotacao["caracteristicas"]["context"]])
            underspecified = utils.isUnderspecified(anotacao, dominios[anotacao["caracteristicas"]["context"]])
            
            if overspecified == True:
                overspecified_description[participante] = overspecified_description[participante] + 1
            if underspecified == True:
                underspecified_description[participante] = underspecified_description[participante] + 1
            if overspecified == False and underspecified == False:
                minimal_description[participante] = minimal_description[participante] + 1
            
            tg_description = len(anotacao["descricao"]["tg"].keys())
            lm_description = 0
            relations = 0
            
            if "lm" in anotacao["descricao"].keys():
                lm_description = len(anotacao["descricao"]["lm"].keys())
            
                for objeto in anotacao["descricao"].keys():
                    for atributo in anotacao["descricao"][objeto].keys():
                        if atributo in ["next-to", "right-of", "left-of", "on-top-of", "in-front-of"]:
                            relations = relations + 1
            
            tg_description_size[participante].append(tg_description)
            lm_description_size[participante].append(lm_description)
            num_relations[participante].append(relations)
    
    for participante in participantes.keys(): 
        if participante in tg_description_size.keys():      
            participantes[participante]["tg_description_size"] = num.mean(tg_description_size[participante])
            participantes[participante]["lm_description_size"] = num.mean(lm_description_size[participante])
            participantes[participante]["num_relations"] = num.mean(num_relations[participante])
            participantes[participante]["overspecified_mean"] = float(overspecified_description[participante]) / len(tg_description_size[participante])
            participantes[participante]["underspecified_mean"] = float(underspecified_description[participante]) / len(tg_description_size[participante])
            participantes[participante]["minimal_mean"] = float(minimal_description[participante]) / len(tg_description_size[participante])
        
    return participantes