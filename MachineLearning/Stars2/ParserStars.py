'''
Created on 22/08/2013

@author: thiagocastroferreira
'''

import xml.etree.ElementTree as ET
import os
import Assurance as ass
import numpy as num
import Utils as utils

# Formata as expressoes geradas pelos participantes do experimento Stars
def parseAnnotation(dir = ""):    
    files = os.listdir(dir + "Corpus/Trials")
    anotacoes = []
    
    for f in files:
        if f != ".DS_Store":
            tree = ET.parse(dir + 'Corpus/Trials/' + f) 
            root = tree.getroot()
            participante = root.attrib["ID"]
            genero = root.attrib["GENDER"]
            idade = root.attrib["AGE"]
            
            for context in root:
                anotacao = {}
                if context.attrib["ID"][0:4] != "fill":
                    anotacao["caracteristicas"] = {}
                    anotacao["descricao"] = {}
                    
                    anotacao["caracteristicas"]["trial"] = participante
                    anotacao["caracteristicas"]["context"] = context.attrib["ID"]
                    anotacao["caracteristicas"]["genre"] = genero
                    anotacao["caracteristicas"]["age"] = idade

                    for entity in context:
                        anotacao["caracteristicas"]["overspec"] = entity.attrib["OVERSPEC"]
                        anotacao["caracteristicas"]["string"] = entity.attrib["STRING"]
                        anotacao["caracteristicas"]["target"] = entity.attrib["TARGET"]
                        
                        anotacao["descricao"][entity.attrib["TARGET"]] = {}
                        
                        if "LANDMARK" in entity.attrib.keys():
                            anotacao["descricao"][entity.attrib["LANDMARK"]] = {}
                            anotacao["caracteristicas"]["landmark"] = entity.attrib["LANDMARK"]
                        
                        if "SECOND-LANDMARK" in entity.attrib.keys():
                            anotacao["descricao"][entity.attrib["SECOND-LANDMARK"]] = {}
                            anotacao["caracteristicas"]["second-landmark"] = entity.attrib["SECOND-LANDMARK"]
                        
                        for attribute in entity:
                            atributo = attribute.attrib["NAME"].split("-")
                            
                            if atributo[0] == "landmark":
                                if attribute.attrib["NAME"] not in anotacao["descricao"][entity.attrib["LANDMARK"]].keys():
                                    anotacao["descricao"][entity.attrib["LANDMARK"]][atributo[1]] = [attribute.attrib["VALUE"]]
                                else:
                                    anotacao["descricao"][entity.attrib["LANDMARK"]][atributo[1]].append(attribute.attrib["VALUE"])
                            elif atributo[0] == "second":
                                if attribute.attrib["NAME"] not in anotacao["descricao"][entity.attrib["SECOND-LANDMARK"]].keys():
                                    anotacao["descricao"][entity.attrib["SECOND-LANDMARK"]][atributo[2]] = [attribute.attrib["VALUE"]]
                                else:
                                    anotacao["descricao"][entity.attrib["SECOND-LANDMARK"]][atributo[2]].append(attribute.attrib["VALUE"])
                            else:
                                if attribute.attrib["NAME"] not in anotacao["descricao"][entity.attrib["TARGET"]].keys():
                                    anotacao["descricao"][entity.attrib["TARGET"]][attribute.attrib["NAME"]] = [attribute.attrib["VALUE"]]
                                else:
                                    anotacao["descricao"][entity.attrib["TARGET"]][attribute.attrib["NAME"]].append(attribute.attrib["VALUE"])
                        anotacoes.append(anotacao)
                
    return anotacoes


# Formata o dominio do experimento Stars em xml
def parseDominio(dir = ""):
    atributos = ["type", "colour", "hpos", "vpos", "size", "near", "left", "right", "below", "above", "in-front-of"]
    tree = ET.parse(dir + 'Corpus/Stars2-context.xml') 
    root = tree.getroot()
    dominios = {}
    for context in root:
        if context.attrib["ID"][0:4] != "fill":
            context_id = context.attrib["ID"]
            dominios[context_id] = {}
            for entity in context:
                entity_id = entity.attrib["ID"]
                dominios[context_id][entity_id] = {}
                #dominios[context_id][entity_id]["function"] = entity.attrib["FUNCTION"]
                for attribute in entity:
                    if attribute.attrib["NAME"] in dominios[context_id][entity_id].keys():
                        dominios[context_id][entity_id][attribute.attrib["NAME"]].append(attribute.attrib["VALUE"])
                    else:
                        dominios[context_id][entity_id][attribute.attrib["NAME"]] = []
                        dominios[context_id][entity_id][attribute.attrib["NAME"]].append(attribute.attrib["VALUE"])
                for atributo in atributos:
                    if atributo not in dominios[context_id][entity_id].keys():
                        dominios[context_id][entity_id][atributo] = []
    return dominios

def parseFeatureVector(dominios, targets):
    featureVector = {}
    attributes_saliencies = {}
    
    for contexto in dominios.keys():
        
        attributes_saliencies[contexto] = {}
        
        for element in dominios[contexto].keys():
            for atributo in ["type", "size", "colour", "hpos", "vpos"]:
                if atributo not in attributes_saliencies[contexto].keys():
                    attributes_saliencies[contexto][atributo] = {}
                if dominios[contexto][element][atributo][0] not in attributes_saliencies[contexto][atributo].keys():
                    attributes_saliencies[contexto][atributo][dominios[contexto][element][atributo][0]] = 1
                else:
                    attributes_saliencies[contexto][atributo][dominios[contexto][element][atributo][0]] = attributes_saliencies[contexto][atributo][dominios[contexto][element][atributo][0]] + 1
    
    attributes_saliency = {}
    for contexto in attributes_saliencies.keys():
        attributes_saliency[contexto] = {}
        for atributo in ["type", "size", "colour", "hpos", "vpos"]:
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
        if len(dominios[contexto][target]["near"]) > 0:
            landmark = dominios[contexto][target]["near"][0]
        
        # define a orientacao do objeto  
        if len(dominios[contexto][target]["right"]) > 0:
            relation = "horizontal"
        elif len(dominios[contexto][target]["left"]) > 0:
            relation = "horizontal"
        elif len(dominios[contexto][target]["above"]) > 0:
            relation = "vertical"
        elif len(dominios[contexto][target]["below"]) > 0:
            relation = "vertical"
        
        if contexto not in featureVector.keys():
            featureVector[contexto] = {}
        
        featureVector[contexto]["tg_size"] = dominios[contexto][target]["size"][0]
        featureVector[contexto]["lm_size"] = dominios[contexto][landmark]["size"][0]
        featureVector[contexto]["relation"] = relation
        
        # define se o landmark e objeto-alvo possuem a mesma cor
        if dominios[contexto][target]["colour"][0] == dominios[contexto][landmark]["colour"][0]:
            featureVector[contexto]["tg_lm_col"] = 1
        else:
            featureVector[contexto]["tg_lm_col"] = 0
        
        # define se o landmark e objeto-alvo possuem o mesmo tipo
        if dominios[contexto][target]["type"][0] == dominios[contexto][landmark]["type"][0]:
            featureVector[contexto]["tg_lm_type"] = 1
        else:
            featureVector[contexto]["tg_lm_type"] = 0
        
        featureVector[contexto]["num_tg_col"] = 0
        featureVector[contexto]["num_lm_col"] = 0
        featureVector[contexto]["num_tg_type"] = 0
        featureVector[contexto]["num_lm_type"] = 0
        
        featureVector[contexto]["dp_tg_col"] = 0
        featureVector[contexto]["dp_lm_col"] = 0
        featureVector[contexto]["dp_tg_type"] = 0
        featureVector[contexto]["dp_lm_type"] = 0
        featureVector[contexto]["dp_tg_hpos"] = 0
        featureVector[contexto]["dp_lm_hpos"] = 0
        featureVector[contexto]["dp_tg_vpos"] = 0
        featureVector[contexto]["dp_lm_vpos"] = 0
        featureVector[contexto]["dp_tg_size"] = 0
        featureVector[contexto]["dp_lm_size"] = 0
        
        featureVector[contexto]["saliency_col"] = attributes_saliency[contexto]["colour"]
        featureVector[contexto]["saliency_type"] = attributes_saliency[contexto]["type"]
        featureVector[contexto]["saliency_size"] = attributes_saliency[contexto]["size"]
        featureVector[contexto]["saliency_hpos"] = attributes_saliency[contexto]["hpos"]
        featureVector[contexto]["saliency_vpos"] = attributes_saliency[contexto]["vpos"]
        
        for element in dominios[contexto].keys():
            if element != target:
                if dominios[contexto][target]["colour"][0] == dominios[contexto][element]["colour"][0]:
                    featureVector[contexto]["num_tg_col"] = featureVector[contexto]["num_tg_col"] + 1
                else:
                    featureVector[contexto]["dp_tg_col"] = featureVector[contexto]["dp_tg_col"] + 1
                
                if dominios[contexto][target]["type"][0] == dominios[contexto][element]["type"][0]:
                    featureVector[contexto]["num_tg_type"] = featureVector[contexto]["num_tg_type"] + 1
                else:
                    featureVector[contexto]["dp_tg_type"] = featureVector[contexto]["dp_tg_type"] + 1
                    
                if dominios[contexto][target]["hpos"][0] != dominios[contexto][element]["hpos"][0]:
                    featureVector[contexto]["dp_tg_hpos"] = featureVector[contexto]["dp_tg_hpos"] + 1
                
                if dominios[contexto][target]["vpos"][0] != dominios[contexto][element]["vpos"][0]:
                    featureVector[contexto]["dp_tg_vpos"] = featureVector[contexto]["dp_tg_vpos"] + 1
                    
                if dominios[contexto][target]["size"][0] != dominios[contexto][element]["size"][0]:
                    featureVector[contexto]["dp_tg_size"] = featureVector[contexto]["dp_tg_size"] + 1
                    
            if element != landmark:
                if dominios[contexto][landmark]["colour"][0] == dominios[contexto][element]["colour"][0]:
                    featureVector[contexto]["num_lm_col"] = featureVector[contexto]["num_lm_col"] + 1
                else:
                    featureVector[contexto]["dp_lm_col"] = featureVector[contexto]["dp_lm_col"] + 1
                
                if dominios[contexto][landmark]["type"][0] == dominios[contexto][element]["type"][0]:
                    featureVector[contexto]["num_lm_type"] = featureVector[contexto]["num_lm_type"] + 1
                else:
                    featureVector[contexto]["dp_lm_col"] = featureVector[contexto]["dp_lm_col"] + 1
                    
                if dominios[contexto][landmark]["hpos"][0] != dominios[contexto][element]["hpos"][0]:
                    featureVector[contexto]["dp_lm_hpos"] = featureVector[contexto]["dp_lm_hpos"] + 1
                
                if dominios[contexto][landmark]["vpos"][0] != dominios[contexto][element]["vpos"][0]:
                    featureVector[contexto]["dp_lm_vpos"] = featureVector[contexto]["dp_lm_vpos"] + 1
                    
                if dominios[contexto][landmark]["size"][0] != dominios[contexto][element]["size"][0]:
                    featureVector[contexto]["dp_lm_size"] = featureVector[contexto]["dp_lm_size"] + 1
    
    return featureVector

def parseSVMInput(anotacoes, featureVector, participantes, frequencias, incluiParticipante = True):
    input = []
    
    for participante in anotacoes:
        for anotacao in anotacoes[participante]:
            classes = {}
            vetor = []
            participante = anotacao["caracteristicas"]["trial"]
            contexto = anotacao["caracteristicas"]["context"]
            target = anotacao["caracteristicas"]["target"]
            
            if incluiParticipante == True:
                vetor.append(int(participante))
                
                genero = anotacao["caracteristicas"]["genre"]
                if genero == "m":
                    vetor.append(0)
                else:
                    vetor.append(1)
                    
                idade = int(anotacao["caracteristicas"]["age"])
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
                
                atributos = ["type", "size", "colour", "hpos", "vpos", "near", "left", "right", "below", "above", "in-front-of"]
#                 for atributo in atributos:
#                     if atributo in frequencias[participante]["target"].keys():
#                         vetor.append(frequencias[participante]["target"][atributo])
#                     else:
#                         vetor.append(0)
#                                  
#                 for atributo in atributos:
#                     if atributo in frequencias[participante]["landmark"].keys():
#                         vetor.append(frequencias[participante]["landmark"][atributo])
#                     else:
#                         vetor.append(0)
            
            vetor.append(participantes[participante]["overspecification"])
            vetor.append(participantes[participante]["tg_description_size"])
            vetor.append(participantes[participante]["lm_description_size"])
            vetor.append(participantes[participante]["lm2_description_size"])
            vetor.append(participantes[participante]["num_relations"])
#                 vetor.append(participantes[participante]["overspecified_mean"])
#                 vetor.append(participantes[participante]["underspecified_mean"])
#                 vetor.append(participantes[participante]["minimal_mean"])
                
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
            
            vetor.append(featureVector[contexto]["num_tg_col"])
            vetor.append(featureVector[contexto]["num_lm_col"])
            vetor.append(featureVector[contexto]["num_tg_type"])
            vetor.append(featureVector[contexto]["num_lm_type"])
            vetor.append(featureVector[contexto]["tg_lm_col"])
            vetor.append(featureVector[contexto]["tg_lm_type"])
            
#             vetor.append(featureVector[contexto]["dp_tg_col"])
#             vetor.append(featureVector[contexto]["dp_lm_col"])
#             vetor.append(featureVector[contexto]["dp_tg_type"])
#             vetor.append(featureVector[contexto]["dp_lm_type"])
#             vetor.append(featureVector[contexto]["dp_tg_size"])
#             vetor.append(featureVector[contexto]["dp_lm_size"])
#             vetor.append(featureVector[contexto]["dp_tg_hpos"])
#             vetor.append(featureVector[contexto]["dp_lm_hpos"])
#             vetor.append(featureVector[contexto]["dp_tg_vpos"])
#             vetor.append(featureVector[contexto]["dp_lm_vpos"])
#        
#             vetor.append(featureVector[contexto]["saliency_col"])
#             vetor.append(featureVector[contexto]["saliency_type"])
#             vetor.append(featureVector[contexto]["saliency_hpos"])
#             vetor.append(featureVector[contexto]["saliency_vpos"])
#             vetor.append(featureVector[contexto]["saliency_size"])
            
            if "type" in anotacao["descricao"][target].keys():
                classes["type"] = 1
            else:
                classes["type"] = 0
            
            if "colour" in anotacao["descricao"][target].keys():
                classes["colour"] = 1
            else:
                classes["colour"] = 0
                
            if "hpos" in anotacao["descricao"][target].keys():
                classes["hpos"] = 1
            else:
                classes["hpos"] = 0
                
            if "vpos" in anotacao["descricao"][target].keys():
                classes["vpos"] = 1
            else:
                classes["vpos"] = 0
            
            if "size" in anotacao["descricao"][target].keys():
                classes["size"] = 1
            else:
                classes["size"] = 0
                
            if "near" in anotacao["descricao"][target].keys():
                classes["relation"] = 1
            elif "left" in anotacao["descricao"][target].keys():
                classes["relation"] = 2
            elif "right" in anotacao["descricao"][target].keys():
                classes["relation"] = 4
            elif "above" in anotacao["descricao"][target].keys():
                classes["relation"] = 3
            elif "below" in anotacao["descricao"][target].keys():
                classes["relation"] = 5
            elif "in-front-of" in anotacao["descricao"][target].keys():
                classes["relation"] = 6
            else:
                classes["relation"] = 0
                
            if "landmark" in anotacao["caracteristicas"].keys():
                landmark = anotacao["caracteristicas"]["landmark"]
                
                if "type" in anotacao["descricao"][landmark].keys():
                    classes["lm_type"] = 1
                else:
                    classes["lm_type"] = 0
                
                if "colour" in anotacao["descricao"][landmark].keys():
                    classes["lm_colour"] = 1
                else:
                    classes["lm_colour"] = 0
                
                if "vpos" in anotacao["descricao"][landmark].keys():
                    classes["lm_vpos"] = 1
                else:
                    classes["lm_vpos"] = 0
                    
                if "hpos" in anotacao["descricao"][landmark].keys():
                    classes["lm_hpos"] = 1
                else:
                    classes["lm_hpos"] = 0
                
                if "size" in anotacao["descricao"][landmark].keys():
                    classes["lm_size"] = 1
                else:
                    classes["lm_size"] = 0
                    
                if "near" in anotacao["descricao"][landmark].keys():
                    classes["lm_relation"] = 1
                elif "left" in anotacao["descricao"][landmark].keys():
                    classes["lm_relation"] = 2
                elif "right" in anotacao["descricao"][landmark].keys():
                    classes["lm_relation"] = 4
                elif "above" in anotacao["descricao"][landmark].keys():
                    classes["lm_relation"] = 3
                elif "below" in anotacao["descricao"][landmark].keys():
                    classes["lm_relation"] = 5
                elif "in-front-of" in anotacao["descricao"][landmark].keys():
                    classes["lm_relation"] = 6
                else:
                    classes["lm_relation"] = 0
            else:
                classes["lm_type"] = 0
                classes["lm_colour"] = 0
                classes["lm_vpos"] = 0
                classes["lm_hpos"] = 0
                classes["lm_size"] = 0
                classes["lm_relation"] = 0
                
            if "second-landmark" in anotacao["caracteristicas"].keys():
                landmark = anotacao["caracteristicas"]["second-landmark"]
                
                if "type" in anotacao["descricao"][landmark].keys():
                    classes["lm2_type"] = 1
                else:
                    classes["lm2_type"] = 0
                
                if "colour" in anotacao["descricao"][landmark].keys():
                    classes["lm2_colour"] = 1
                else:
                    classes["lm2_colour"] = 0
                
                if "vpos" in anotacao["descricao"][landmark].keys():
                    classes["lm2_vpos"] = 1
                else:
                    classes["lm2_vpos"] = 0
                    
                if "hpos" in anotacao["descricao"][landmark].keys():
                    classes["lm2_hpos"] = 1
                else:
                    classes["lm2_hpos"] = 0
                    
                if "size" in anotacao["descricao"][landmark].keys():
                    classes["lm2_size"] = 1
                else:
                    classes["lm2_size"] = 0
            else:
                classes["lm2_type"] = 0
                classes["lm2_colour"] = 0
                classes["lm2_vpos"] = 0
                classes["lm2_hpos"] = 0
                classes["lm2_size"] = 0
                
            classes["description_size"] = len(ass.parse(anotacao["descricao"])) / 2
               
            data = {}
            data["data"] = vetor
            data["classes"] = classes
            data["anotacao"] = anotacao
            input.append(data)
    
    return input

def descriptionsMeans(folds, teste, dominios):
    foldsAux = {}
    participantes = {}
    
    for fold in folds:
        if fold != teste:
            foldsAux[fold] = folds[fold]
    
    tg_description_size = {}
    lm_description_size = {}
    lm2_description_size = {}
    overspecification = {}
    num_relations = {}  
    overspecified_description = {}
    underspecified_description = {}
    minimal_description = {}
        
    for fold in foldsAux:
        for participante in foldsAux[fold].keys():
            for anotacao in foldsAux[fold][participante]:
                participante = anotacao["caracteristicas"]["trial"]
                
                if participante not in tg_description_size.keys():
                    tg_description_size[participante] = []
                    lm_description_size[participante] = []
                    lm2_description_size[participante] = []
                    num_relations[participante] = []
                    overspecification[participante] = []
                    overspecified_description[participante] = 0
                    underspecified_description[participante] = 0
                    minimal_description[participante] = 0
                
                if participante not in participantes.keys():
                    participantes[participante] = {}
                
                overspecified = utils.isOverspecified(anotacao, dominios[anotacao["caracteristicas"]["context"]])
                underspecified = utils.isUnderspecified(anotacao, dominios[anotacao["caracteristicas"]["context"]])
                
                if overspecified == True:
                    overspecified_description[participante] = overspecified_description[participante] + 1
                if underspecified == True:
                    underspecified_description[participante] = underspecified_description[participante] + 1
                if overspecified == False and underspecified == False:
                    minimal_description[participante] = minimal_description[participante] + 1
                
                tg_description = len(anotacao["descricao"][anotacao["caracteristicas"]["target"]].keys())
                lm_description = 0
                lm2_description = 0
                relations = 0
                
                if "landmark" in anotacao["caracteristicas"].keys():
                    lm_description = len(anotacao["descricao"][anotacao["caracteristicas"]["landmark"]].keys())
                    relations = relations + 1
                    
                if "second_landmark" in anotacao["caracteristicas"].keys():
                    lm2_description = len(anotacao["descricao"][anotacao["caracteristicas"]["second_landmark"]].keys())
                    relations = relations + 1
                
                overspecification[participante].append(int(anotacao["caracteristicas"]["overspec"]))
                tg_description_size[participante].append(tg_description)
                lm_description_size[participante].append(lm_description)
                lm2_description_size[participante].append(lm2_description)
                num_relations[participante].append(relations)
    
    for participante in participantes.keys():       
        participantes[participante]["tg_description_size"] = num.mean(tg_description_size[participante])
        participantes[participante]["lm_description_size"] = num.mean(lm_description_size[participante])
        participantes[participante]["lm2_description_size"] = num.mean(lm2_description_size[participante])
        participantes[participante]["num_relations"] = num.mean(num_relations[participante])
        participantes[participante]["overspecification"] = num.mean(overspecification[participante])
        participantes[participante]["overspecified_mean"] = float(overspecified_description[participante]) / len(tg_description_size[participante])
        participantes[participante]["underspecified_mean"] = float(underspecified_description[participante]) / len(tg_description_size[participante])
        participantes[participante]["minimal_mean"] = float(minimal_description[participante]) / len(tg_description_size[participante])
        
    return participantes

def parseSVMInputSecondVersion(anotacoes, featureVector, participantes, frequencias, incluiParticipante = True):
    input = []
    
    for participante in anotacoes:
        for anotacao in anotacoes[participante]:
            classes = {}
            vetor = []
            participante = anotacao["caracteristicas"]["trial"]
            contexto = anotacao["caracteristicas"]["context"]
            target = anotacao["caracteristicas"]["target"]
            
            if incluiParticipante == True:
                vetor.append(int(participante))
                
                genero = anotacao["caracteristicas"]["genre"]
                if genero == "m":
                    vetor.append(0)
                else:
                    vetor.append(1)
                    
                idade = int(anotacao["caracteristicas"]["age"])
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
                
                atributos = ["type", "colour", "size", "hpos", "vpos", "near", "left", "right", "below", "above", "in-front-of"]
                for atributo in atributos:
                    if atributo in frequencias[participante]["target"].keys():
                        vetor.append(frequencias[participante]["target"][atributo])
                    else:
                        vetor.append(0)
                      
                for atributo in atributos:
                    if atributo in frequencias[participante]["landmark"].keys():
                        vetor.append(frequencias[participante]["landmark"][atributo])
                    else:
                        vetor.append(0)
            
            tg_description_size = len(anotacao["descricao"][anotacao["caracteristicas"]["target"]].keys())
            lm_description_size = 0
            lm2_description_size = 0
            num_relations = 0
            
            if "landmark" in anotacao["caracteristicas"].keys():
                lm_description_size = len(anotacao["descricao"][anotacao["caracteristicas"]["landmark"]].keys())
                relations = relations + 1
                
            if "second_landmark" in anotacao["caracteristicas"].keys():
                lm2_description_size = len(anotacao["descricao"][anotacao["caracteristicas"]["second_landmark"]].keys())
                relations = relations + 1
            
            vetor.append(int(anotacao["caracteristicas"]["overspec"]))
            vetor.append(tg_description_size)
            vetor.append(lm_description_size)
            vetor.append(lm2_description_size)
                       
            if featureVector[contexto]["relation"] == "none":
                vetor.append(0)
            elif featureVector[contexto]["relation"] == "horizontal":
                vetor.append(0)
            else:
                vetor.append(1)
            
            vetor.append(featureVector[contexto]["num_tg_col"])
            vetor.append(featureVector[contexto]["num_lm_col"])
            vetor.append(featureVector[contexto]["num_tg_type"])
            vetor.append(featureVector[contexto]["num_lm_type"])
            vetor.append(featureVector[contexto]["tg_lm_col"])
            vetor.append(featureVector[contexto]["tg_lm_type"])
            
            if "type" in anotacao["descricao"][target].keys():
                classes["type"] = 1
            else:
                classes["type"] = 0
            
            if "colour" in anotacao["descricao"][target].keys():
                classes["colour"] = 1
            else:
                classes["colour"] = 0
                
            if "size" in anotacao["descricao"][target].keys():
                classes["size"] = 1
            else:
                classes["size"] = 0
                
            if "hpos" in anotacao["descricao"][target].keys():
                classes["hpos"] = 1
            else:
                classes["hpos"] = 0
                
            if "vpos" in anotacao["descricao"][target].keys():
                classes["vpos"] = 1
            else:
                classes["vpos"] = 0
            
            if "near" in anotacao["descricao"][target].keys():
                classes["near"] = 1
            else:
                classes["near"] = 0
            
            if "left" in anotacao["descricao"][target].keys():
                classes["left"] = 1
            else:
                classes["left"] = 0
            
            if "right" in anotacao["descricao"][target].keys():
                classes["right"] = 1
            else:
                classes["right"] = 0
            
            if "above" in anotacao["descricao"][target].keys():
                classes["above"] = 1
            else:
                classes["above"] = 0
            
            if "below" in anotacao["descricao"][target].keys():
                classes["below"] = 1
            else:
                classes["below"] = 0
                
            if "in-front-of" in anotacao["descricao"][target].keys():
                classes["in-front-of"] = 1
            else:
                classes["in-front-of"] = 0
            
                
            if "landmark" in anotacao["caracteristicas"].keys():
                landmark = anotacao["caracteristicas"]["landmark"]
                
                if "type" in anotacao["descricao"][landmark].keys():
                    classes["lm_type"] = 1
                else:
                    classes["lm_type"] = 0
                
                if "colour" in anotacao["descricao"][landmark].keys():
                    classes["lm_colour"] = 1
                else:
                    classes["lm_colour"] = 0
                    
                if "size" in anotacao["descricao"][landmark].keys():
                    classes["lm_size"] = 1
                else:
                    classes["lm_size"] = 0
                
                if "vpos" in anotacao["descricao"][landmark].keys():
                    classes["lm_vpos"] = 1
                else:
                    classes["lm_vpos"] = 0
                    
                if "hpos" in anotacao["descricao"][landmark].keys():
                    classes["lm_hpos"] = 1
                else:
                    classes["lm_hpos"] = 0
                
                if "near" in anotacao["descricao"][landmark].keys():
                    classes["lm_near"] = 1
                else:
                    classes["lm_near"] = 0
                    
                if "left" in anotacao["descricao"][landmark].keys():
                    classes["lm_left"] = 1
                else:
                    classes["lm_left"] = 0
                
                if "right" in anotacao["descricao"][landmark].keys():
                    classes["lm_right"] = 1
                else:
                    classes["lm_right"] = 0
                
                if "above" in anotacao["descricao"][landmark].keys():
                    classes["lm_above"] = 1
                else:
                    classes["lm_above"] = 0
                
                if "below" in anotacao["descricao"][landmark].keys():
                    classes["lm_below"] = 1
                else:
                    classes["lm_below"] = 0
                    
                if "in-front-of" in anotacao["descricao"][landmark].keys():
                    classes["lm_in-front-of"] = 1
                else:
                    classes["lm_in-front-of"] = 0
                
            else:
                classes["lm_type"] = 0
                classes["lm_colour"] = 0
                classes["lm_size"] = 0
                classes["lm_vpos"] = 0
                classes["lm_hpos"] = 0
                classes["lm_near"] = 0
                classes["lm_left"] = 0
                classes["lm_right"] = 0
                classes["lm_above"] = 0
                classes["lm_below"] = 0
                classes["lm_in-front-of"] = 0
                
            if "second-landmark" in anotacao["caracteristicas"].keys():
                landmark = anotacao["caracteristicas"]["second-landmark"]
                
                if "type" in anotacao["descricao"][landmark].keys():
                    classes["lm2_type"] = 1
                else:
                    classes["lm2_type"] = 0
                
                if "colour" in anotacao["descricao"][landmark].keys():
                    classes["lm2_colour"] = 1
                else:
                    classes["lm2_colour"] = 0
                    
                if "size" in anotacao["descricao"][landmark].keys():
                    classes["lm2_size"] = 1
                else:
                    classes["lm2_size"] = 0
                
                if "vpos" in anotacao["descricao"][landmark].keys():
                    classes["lm2_vpos"] = 1
                else:
                    classes["lm2_vpos"] = 0
                    
                if "hpos" in anotacao["descricao"][landmark].keys():
                    classes["lm2_hpos"] = 1
                else:
                    classes["lm2_hpos"] = 0
                    
            else:
                classes["lm2_type"] = 0
                classes["lm2_colour"] = 0
                classes["lm2_size"] = 0
                classes["lm2_vpos"] = 0
                classes["lm2_hpos"] = 0
                    
            data = {}
            data["data"] = vetor
            data["classes"] = classes
            data["anotacao"] = anotacao
            input.append(data)
    
    return input