'''
Created on 29/01/2014

@author: thiagocastroferreira
'''

import xml.etree.ElementTree as ET
import os
import Utils as utils
import numpy as num

def parse():
    trials = []
    
    files = os.listdir("Corpus")
    
    for file in files:
        if file != ".DS_Store":
            trial = {}
            trial["caracteristicas"] = {}
            
            tree = ET.parse('Corpus/' + file) 
            root = tree.getroot()
            
            id = root.attrib["ID"]
            participante = id.split("t")[1]
            cardinalidade = root.attrib["CARDINALITY"]
            location = root.attrib["CONDITION"]
            similarity = root.attrib["SIMILARITY"]
            
            trial["caracteristicas"]["id"] = id
            trial["caracteristicas"]["cardinality"] = cardinalidade
            trial["caracteristicas"]["location"] = location
            trial["caracteristicas"]["similarity"] = similarity
            trial["caracteristicas"]["participante"] = participante
            
            domain = root.find("DOMAIN")
            
            trial = parseDomain(domain, trial)
            
            attributes = root.find("ATTRIBUTE-SET")
            trial = parseAnnotation(attributes, trial)
            trials.append(trial)
        
    return trials

def parseAnnotation(attributes, trial):
    targets = trial["caracteristicas"]["target"]
    dominio = trial["domain"]
    
    trial["descricao"] = {}
    
    for target in targets:
        trial["descricao"][target] = {}
        for attribute in attributes:
            if trial["caracteristicas"]["cardinality"] != 1:
                if attribute.attrib["NAME"] in dominio[target].keys():
                    if attribute.attrib["VALUE"] in dominio[target][attribute.attrib["NAME"]]:
                        trial["descricao"][target][attribute.attrib["NAME"]] = [attribute.attrib["VALUE"]]
            else:
                trial["descricao"][target][attribute.attrib["NAME"]] = [attribute.attrib["VALUE"]]
        
    return trial

def parseDomain(domain, trial):
    
    trial["domain"] = {}
    trial["caracteristicas"]["target"] = []
    
    for entity in domain:
        id = entity.attrib["ID"]
        type = entity.attrib["TYPE"]
        
        if type == "target":
            trial["caracteristicas"]["target"].append(id)
        
        trial["domain"][id] = {}
        
        for attribute in entity:
            trial["domain"][id][attribute.attrib["NAME"]] = [attribute.attrib["VALUE"]]
        
    return trial

def parseFeatureVector(trials):
    featureVector = {}
    attributes_saliencies = {}
    
    for trial in trials:
        contexto = trial["caracteristicas"]["id"]
        dominio = trial["domain"]
        
        attributes_saliencies[contexto] = {}
        
        for element in dominio.keys():
            for atributo in dominio[element].keys():
                if atributo not in attributes_saliencies[contexto].keys():
                    attributes_saliencies[contexto][atributo] = {}
                if dominio[element][atributo][0] not in attributes_saliencies[contexto][atributo].keys():
                    attributes_saliencies[contexto][atributo][dominio[element][atributo][0]] = 1
                else:
                    attributes_saliencies[contexto][atributo][dominio[element][atributo][0]] = attributes_saliencies[contexto][atributo][dominio[element][atributo][0]] + 1
    
    attributes_saliency = {}
    for contexto in attributes_saliencies.keys():
        attributes_saliency[contexto] = {}
        for atributo in attributes_saliencies[contexto].keys():
            attributes_saliency[contexto][atributo] = 0
            for valor in attributes_saliencies[contexto][atributo].keys():
                if attributes_saliencies[contexto][atributo][valor] > attributes_saliency[contexto][atributo]:
                    attributes_saliency[contexto][atributo] = attributes_saliencies[contexto][atributo][valor]
    
    del attributes_saliencies
    
    for trial in trials:
        targets = trial["caracteristicas"]["target"]
        contexto = trial["caracteristicas"]["id"]
        
        featureVector[contexto] = {}
        featureVector[contexto]["dimensions"] = []
        
        for target in targets:
            featureVector[contexto][target] = {}
            featureVector[contexto][target]["num_tg_type"] = 0
            featureVector[contexto][target]["num_tg_age"] = 0
            featureVector[contexto][target]["num_tg_orientation"] = 0
            featureVector[contexto][target]["num_tg_hairColour"] = 0
            featureVector[contexto][target]["num_tg_hasSuit"] = 0
            featureVector[contexto][target]["num_tg_hasShirt"] = 0
            featureVector[contexto][target]["num_tg_hasTie"] = 0
            featureVector[contexto][target]["num_tg_hasBeard"] = 0
            featureVector[contexto][target]["num_tg_hasGlasses"] = 0
            featureVector[contexto][target]["num_tg_hasHair"] = 0
            
            featureVector[contexto][target]["dp_type"] = 0
            featureVector[contexto][target]["dp_age"] = 0
            featureVector[contexto][target]["dp_orientation"] = 0
            featureVector[contexto][target]["dp_hairColour"] = 0
            featureVector[contexto][target]["dp_hasSuit"] = 0
            featureVector[contexto][target]["dp_hasShirt"] = 0
            featureVector[contexto][target]["dp_hasTie"] = 0
            featureVector[contexto][target]["dp_hasBeard"] = 0
            featureVector[contexto][target]["dp_hasGlasses"] = 0
            featureVector[contexto][target]["dp_hasHair"] = 0
            
            featureVector[contexto][target]["saliency_type"] = attributes_saliency[contexto]["type"]
            featureVector[contexto][target]["saliency_age"] = attributes_saliency[contexto]["age"]
            featureVector[contexto][target]["saliency_orientation"] = attributes_saliency[contexto]["orientation"]
            featureVector[contexto][target]["saliency_hairColour"] = attributes_saliency[contexto]["hairColour"]
            featureVector[contexto][target]["saliency_hasSuit"] = attributes_saliency[contexto]["hasSuit"]
            featureVector[contexto][target]["saliency_hasShirt"] = attributes_saliency[contexto]["hasShirt"]
            featureVector[contexto][target]["saliency_hasTie"] = attributes_saliency[contexto]["hasTie"]
            featureVector[contexto][target]["saliency_hasBeard"] = attributes_saliency[contexto]["hasBeard"]
            featureVector[contexto][target]["saliency_hasGlasses"] = attributes_saliency[contexto]["hasGlasses"]
            featureVector[contexto][target]["saliency_hasHair"] = attributes_saliency[contexto]["hasHair"]
            
            if trial["domain"][target]["x-dimension"][0] == "unknown":
                featureVector[contexto][target]["x-dimension"] = 0
                featureVector[contexto]["dimensions"].append(0)
            else:
                featureVector[contexto][target]["x-dimension"] = int(trial["domain"][target]["x-dimension"][0])
                featureVector[contexto]["dimensions"].append(int(trial["domain"][target]["x-dimension"][0]))
                
            if trial["domain"][target]["y-dimension"][0] == "unknown":
                featureVector[contexto][target]["y-dimension"] = 0
                featureVector[contexto]["dimensions"].append(0)
            else:
                featureVector[contexto][target]["y-dimension"] = int(trial["domain"][target]["y-dimension"][0])
                featureVector[contexto]["dimensions"].append(int(trial["domain"][target]["y-dimension"][0]))
            
            for element in trial["domain"].keys():
                if element != target:
                    if trial["domain"][element]["x-dimension"][0] == "unknown":
                        featureVector[contexto]["dimensions"].append(0)
                    else:
                        featureVector[contexto]["dimensions"].append(int(trial["domain"][element]["x-dimension"][0]))
                        
                    if trial["domain"][element]["y-dimension"][0] == "unknown":
                        featureVector[contexto]["dimensions"].append(0)
                    else:
                        featureVector[contexto]["dimensions"].append(int(trial["domain"][element]["y-dimension"][0]))
                    
                    if trial["domain"][target]["age"][0] == trial["domain"][element]["age"][0]:
                        featureVector[contexto][target]["num_tg_age"] = featureVector[contexto][target]["num_tg_age"] + 1
                    else:
                        featureVector[contexto][target]["dp_age"] = featureVector[contexto][target]["dp_age"] + 1
                    
                    if trial["domain"][target]["type"][0] == trial["domain"][element]["type"][0]:
                        featureVector[contexto][target]["num_tg_type"] = featureVector[contexto][target]["num_tg_type"] + 1
                    else:
                        featureVector[contexto][target]["dp_type"] = featureVector[contexto][target]["dp_type"] + 1
                        
                    if trial["domain"][target]["orientation"][0] == trial["domain"][element]["orientation"][0]:
                        featureVector[contexto][target]["num_tg_orientation"] = featureVector[contexto][target]["num_tg_orientation"] + 1
                    else:
                        featureVector[contexto][target]["dp_orientation"] = featureVector[contexto][target]["dp_orientation"] + 1
                    
                    if trial["domain"][target]["hairColour"][0] == trial["domain"][element]["hairColour"][0]:
                        featureVector[contexto][target]["num_tg_hairColour"] = featureVector[contexto][target]["num_tg_hairColour"] + 1
                    else:
                        featureVector[contexto][target]["dp_hairColour"] = featureVector[contexto][target]["dp_hairColour"] + 1
                        
                    if trial["domain"][target]["hasSuit"][0] == trial["domain"][element]["hasSuit"][0]:
                        featureVector[contexto][target]["num_tg_hasSuit"] = featureVector[contexto][target]["num_tg_hasSuit"] + 1
                    else:
                        featureVector[contexto][target]["dp_hasSuit"] = featureVector[contexto][target]["dp_hasSuit"] + 1
                        
                    if trial["domain"][target]["hasShirt"][0] == trial["domain"][element]["hasShirt"][0]:
                        featureVector[contexto][target]["num_tg_hasShirt"] = featureVector[contexto][target]["num_tg_hasShirt"] + 1
                    else:
                        featureVector[contexto][target]["dp_hasShirt"] = featureVector[contexto][target]["dp_hasShirt"] + 1
                        
                    if trial["domain"][target]["hasTie"][0] == trial["domain"][element]["hasTie"][0]:
                        featureVector[contexto][target]["num_tg_hasTie"] = featureVector[contexto][target]["num_tg_hasTie"] + 1
                    else:
                        featureVector[contexto][target]["dp_hasTie"] = featureVector[contexto][target]["dp_hasTie"] + 1
                    
                    if trial["domain"][target]["hasBeard"][0] == trial["domain"][element]["hasBeard"][0]:
                        featureVector[contexto][target]["num_tg_hasBeard"] = featureVector[contexto][target]["num_tg_hasBeard"] + 1
                    else:
                        featureVector[contexto][target]["dp_hasBeard"] = featureVector[contexto][target]["dp_hasBeard"] + 1
                        
                    if trial["domain"][target]["hasGlasses"][0] == trial["domain"][element]["hasGlasses"][0]:
                        featureVector[contexto][target]["num_tg_hasGlasses"] = featureVector[contexto][target]["num_tg_hasGlasses"] + 1
                    else:
                        featureVector[contexto][target]["dp_hasGlasses"] = featureVector[contexto][target]["dp_hasGlasses"] + 1
                        
                    if trial["domain"][target]["hasHair"][0] == trial["domain"][element]["hasHair"][0]:
                        featureVector[contexto][target]["num_tg_hasHair"] = featureVector[contexto][target]["num_tg_hasHair"] + 1
                    else:
                        featureVector[contexto][target]["dp_hasHair"] = featureVector[contexto][target]["dp_hasHair"] + 1
    
    return featureVector

def parseSVMInput(anotacoes, featureVector, participantes, frequencias, incluiParticipante = True):
    input = []
    
    for participante in anotacoes:
        for anotacao in anotacoes[participante]:
            contexto = anotacao["caracteristicas"]["id"]
            participante = anotacao["caracteristicas"]["participante"]
            targets = anotacao["caracteristicas"]["target"]
            
            data = {}
            for target in targets:
                classes = {}
                vetor = []
                
                if incluiParticipante == True:
                    vetor.append(int(participante))
                    
                    atributos = ["type", "orientation", "age", "hairColour", "hasBeard", "hasHair", "hasGlasses", "hasShirt", "hasTie", "hasSuit", "x-dimension", "y-dimension"]
                    for atributo in atributos:
                        if atributo in frequencias[participante]["target"].keys():
                            vetor.append(frequencias[participante]["target"][atributo])
                        else:
                            vetor.append(0)
                        
                    vetor.append(participantes[participante]["tg_description_size"])
                    vetor.append(participantes[participante]["overspecified_mean"])
                    vetor.append(participantes[participante]["underspecified_mean"])
                    vetor.append(participantes[participante]["minimal_mean"])
                
                vetor.append(anotacao["caracteristicas"]["cardinality"])
                if anotacao["caracteristicas"]["location"] == "+LOC":
                    vetor.append(1)
                else:
                    vetor.append(0)
                
                if anotacao["caracteristicas"]["similarity"] == "similar":
                    vetor.append(1)
                else:
                    vetor.append(0)
                
                vetor.append(featureVector[contexto][target]["num_tg_type"])
                vetor.append(featureVector[contexto][target]["num_tg_age"])
                vetor.append(featureVector[contexto][target]["num_tg_orientation"])
                vetor.append(featureVector[contexto][target]["num_tg_hairColour"])
                vetor.append(featureVector[contexto][target]["num_tg_hasSuit"])
                vetor.append(featureVector[contexto][target]["num_tg_hasShirt"])
                vetor.append(featureVector[contexto][target]["num_tg_hasTie"])
                vetor.append(featureVector[contexto][target]["num_tg_hasBeard"])
                vetor.append(featureVector[contexto][target]["num_tg_hasGlasses"])
                vetor.append(featureVector[contexto][target]["num_tg_hasHair"])
                
                vetor.append(featureVector[contexto][target]["dp_type"])
                vetor.append(featureVector[contexto][target]["dp_age"])
                vetor.append(featureVector[contexto][target]["dp_orientation"])
                vetor.append(featureVector[contexto][target]["dp_hairColour"])
                vetor.append(featureVector[contexto][target]["dp_hasSuit"])
                vetor.append(featureVector[contexto][target]["dp_hasShirt"])
                vetor.append(featureVector[contexto][target]["dp_hasTie"])
                vetor.append(featureVector[contexto][target]["dp_hasBeard"])
                vetor.append(featureVector[contexto][target]["dp_hasGlasses"])
                vetor.append(featureVector[contexto][target]["dp_hasHair"])
                 
                vetor.append(featureVector[contexto][target]["saliency_type"])
                vetor.append(featureVector[contexto][target]["saliency_age"])
                vetor.append(featureVector[contexto][target]["saliency_orientation"])
                vetor.append(featureVector[contexto][target]["saliency_hairColour"])
                vetor.append(featureVector[contexto][target]["saliency_hasSuit"])
                vetor.append(featureVector[contexto][target]["saliency_hasShirt"])
                vetor.append(featureVector[contexto][target]["saliency_hasTie"])
                vetor.append(featureVector[contexto][target]["saliency_hasBeard"])
                vetor.append(featureVector[contexto][target]["saliency_hasGlasses"])
                vetor.append(featureVector[contexto][target]["saliency_hasHair"])
                
#                 for dimension in featureVector[contexto]["dimensions"]:
#                     vetor.append(dimension)
                
                if "type" in anotacao["descricao"][target].keys():
                    classes["type"] = 1
                else:
                    classes["type"] = 0
                
                if "orientation" in anotacao["descricao"][target].keys():
                    classes["orientation"] = 1
                else:
                    classes["orientation"] = 0
                    
                if "age" in anotacao["descricao"][target].keys():
                    classes["age"] = 1
                else:
                    classes["age"] = 0
                    
                if "hairColour" in anotacao["descricao"][target].keys():
                    classes["hairColour"] = 1
                else:
                    classes["hairColour"] = 0
                
                if "hasBeard" in anotacao["descricao"][target].keys():
                    classes["hasBeard"] = 1
                else:
                    classes["hasBeard"] = 0
                    
                if "hasHair" in anotacao["descricao"][target].keys():
                    classes["hasHair"] = 1
                else:
                    classes["hasHair"] = 0
                    
                if "hasGlasses" in anotacao["descricao"][target].keys():
                    classes["hasGlasses"] = 1
                else:
                    classes["hasGlasses"] = 0
                    
                if "hasShirt" in anotacao["descricao"][target].keys():
                    classes["hasShirt"] = 1
                else:
                    classes["hasShirt"] = 0
                    
                if "hasTie" in anotacao["descricao"][target].keys():
                    classes["hasTie"] = 1
                else:
                    classes["hasTie"] = 0
                    
                if "hasSuit" in anotacao["descricao"][target].keys():
                    classes["hasSuit"] = 1
                else:
                    classes["hasSuit"] = 0
                    
                if "x-dimension" in anotacao["descricao"][target].keys():
                    classes["x-dimension"] = 1
                else:
                    classes["x-dimension"] = 0
                    
                if "y-dimension" in anotacao["descricao"][target].keys():
                    classes["y-dimension"] = 1
                else:
                    classes["y-dimension"] = 0
                
                data[target] = {}
                data[target]["data"] = vetor
                data[target]["classes"] = classes
                data[target]["anotacao"] = anotacao
            input.append(data)
    
    return input

def descriptionsMeans(folds, teste):
    foldsAux = {}
    
    participantes = {}
    
    for fold in folds:
        if fold != teste:
            foldsAux[fold] = folds[fold]
    
    tg_description_size = {} 
    overspecified_description = {}
    underspecified_description = {}
    minimal_description = {}
        
    for fold in foldsAux:
        for participante in foldsAux[fold].keys():
            for anotacao in foldsAux[fold][participante]:
                participante = anotacao["caracteristicas"]["participante"]
                
                if participante not in tg_description_size.keys():
                    tg_description_size[participante] = []
                    overspecified_description[participante] = 0
                    underspecified_description[participante] = 0
                    minimal_description[participante] = 0
                
                if participante not in participantes.keys():
                    participantes[participante] = {}
                
                if "numeroExpressoes" not in participantes[participante].keys():
                    participantes[participante]["numeroExpressoes"] = 1
                else:
                    participantes[participante]["numeroExpressoes"] = participantes[participante]["numeroExpressoes"] + 1
                
                overspecified = utils.isOverspecified(anotacao)
                underspecified = utils.isUnderspecified(anotacao)
                
                if overspecified == True:
                    overspecified_description[participante] = overspecified_description[participante] + 1
                if underspecified == True:
                    underspecified_description[participante] = underspecified_description[participante] + 1
                if overspecified == False and underspecified == False:
                    minimal_description[participante] = minimal_description[participante] + 1
                
                for target in anotacao["descricao"].keys():
                    tg_description = len(anotacao["descricao"][target].keys())
                    tg_description_size[participante].append(tg_description)
    
    for participante in participantes.keys():       
        participantes[participante]["tg_description_size"] = num.mean(tg_description_size[participante])
        participantes[participante]["overspecified_mean"] = float(overspecified_description[participante]) / len(tg_description_size[participante])
        participantes[participante]["underspecified_mean"] = float(underspecified_description[participante]) / len(tg_description_size[participante])
        participantes[participante]["minimal_mean"] = float(minimal_description[participante]) / len(tg_description_size[participante])
        
    return participantes