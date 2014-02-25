'''
Created on 22/08/2013

@author: thiagocastroferreira
'''

import xml.etree.ElementTree as ET
# Formata as expressoes geradas pelos participantes do experimento Stars
def parseDominio(incluirTamanho = False):
    contextos = {}
    atributosRenegados = ["x", "y", "z", "size"]
    
    if incluirTamanho == True:
        atributosRenegados = ["x", "y", "z"]
    
    # WORLD 1
    tree = ET.parse('xmls/atomic-properties-world1.xml') 
    root = tree.getroot()
    
    contextos["1"] = {}
    
    for domain in root:
        domain_id = domain.attrib["ID"]
        contextos["1"][domain_id] = {}
        
        entidades = domain.findall("ENTITY")
        
        for entidade in entidades:
            entidade_id = entidade.attrib["ID"]
            contextos["1"][domain_id][entidade_id] = {}
            
            for atributo in entidade:
                if atributo.attrib["NAME"] not in atributosRenegados:
                    contextos["1"][domain_id][entidade_id][atributo.attrib["NAME"]] = [atributo.attrib["VALUE"]]
                
    tree = ET.parse('xmls/relation-properties-world1.xml') 
    root = tree.getroot()
    
    for domain in root:
        domain_id = domain.attrib["ID"]
        
        relations = domain.findall("RELATION")
        
        for relation in relations:
            target = relation.attrib["TARGET"]
            landmark = relation.attrib["LANDMARK"]
            
            for atributo in relation:
                if atributo.attrib["NAME"] != "distance":
                    if target not in contextos["1"][domain_id].keys():
                        contextos["1"][domain_id][target] = {}
                    contextos["1"][domain_id][target][atributo.attrib["VALUE"]] = [landmark]
                    
                
    # WORLD 2
    tree = ET.parse('xmls/atomic-properties-world2.xml') 
    root = tree.getroot()
    
    contextos["2"] = {}
    
    for domain in root:
        domain_id = domain.attrib["ID"]
        contextos["2"][domain_id] = {}
        
        entidades = domain.findall("ENTITY")
        
        for entidade in entidades:
            entidade_id = entidade.attrib["ID"]
            contextos["2"][domain_id][entidade_id] = {}
            
            for atributo in entidade:
                if atributo.attrib["NAME"] not in atributosRenegados:
                    contextos["2"][domain_id][entidade_id][atributo.attrib["NAME"]] = [atributo.attrib["VALUE"]]
                
    tree = ET.parse('xmls/relation-properties-world2.xml') 
    root = tree.getroot()
    
    for domain in root:
        domain_id = domain.attrib["ID"]
        
        relations = domain.findall("RELATION")
        
        for relation in relations:
            target = relation.attrib["TARGET"]
            landmark = relation.attrib["LANDMARK"]
            
            for atributo in relation:
                if atributo.attrib["NAME"] != "distance":
                    if target not in contextos["2"][domain_id].keys():
                        contextos["2"][domain_id][target] = {}
                    contextos["2"][domain_id][target][atributo.attrib["VALUE"]] = [landmark]
                
    # WORLD 3
    tree = ET.parse('xmls/atomic-properties-world3.xml') 
    root = tree.getroot()
    
    contextos["3"] = {}
    
    for domain in root:
        domain_id = domain.attrib["ID"]
        contextos["3"][domain_id] = {}
        
        entidades = domain.findall("ENTITY")
        
        for entidade in entidades:
            entidade_id = entidade.attrib["ID"]
            contextos["3"][domain_id][entidade_id] = {}
            
            for atributo in entidade:
                if atributo.attrib["NAME"] not in atributosRenegados:
                    contextos["3"][domain_id][entidade_id][atributo.attrib["NAME"]] = [atributo.attrib["VALUE"]]
                
    tree = ET.parse('xmls/relation-properties-world3.xml') 
    root = tree.getroot()
    
    for domain in root:
        domain_id = domain.attrib["ID"]
        
        relations = domain.findall("RELATION")
        
        for relation in relations:
            target = relation.attrib["TARGET"]
            landmark = relation.attrib["LANDMARK"]
            
            for atributo in relation:
                if atributo.attrib["NAME"] != "distance":
                    if target not in contextos["3"][domain_id].keys():
                        contextos["3"][domain_id][target] = {}
                    contextos["3"][domain_id][target][atributo.attrib["VALUE"]] = [landmark]
    
    atributos = ['leftaround', 'right', 'orientation', 'color', 'straight', 'next', 'slightlyleft', 'rightaround', 'left', 'type', 'slightlyright']
    for contexto in contextos:
        for dominio in contextos[contexto].keys():
            for objeto in contextos[contexto][dominio].keys():
                for atributo in atributos:
                    if atributo not in contextos[contexto][dominio][objeto].keys():
                        contextos[contexto][dominio][objeto][atributo] = []
    
    return contextos


# Formata as descricoes do experimento GRE3D em xml
def parseAnnotation():
    tree = ET.parse('xmls/descriptions.xml') 
    root = tree.getroot()
    anotacoes = []
    for trial in root:
        anotacao = {}
        anotacao["caracteristicas"] = {}
        anotacao["descricao"] = {}
        
        anotacao["caracteristicas"]["trial"] = trial.attrib["PLAYER_ID"]
        anotacao["caracteristicas"]["context"] = trial.attrib["WORLD_ID"]
        anotacao["caracteristicas"]["target"] = trial.attrib["TAGERT_ID"]
        
        entidade = trial.find("ENTITY")
        target = entidade.attrib["ID"]
        anotacao["descricao"][target] = {}
        
        for atributo in entidade:
            anotacao["descricao"][target][atributo.attrib["NAME"]] = [atributo.attrib["VALUE"]]
        
        relacionamentos = trial.findall("RELATIONSHIP")
        
        for relacionamento in relacionamentos:
            relacao = relacionamento.find("RELATION")
            tg = relacao.attrib["TARGET"]
            landmark = relacao.attrib["LANDMARK"]
            
            for atributo in relacao:
                anotacao["descricao"][tg][atributo.attrib["VALUE"]] = [landmark]
            
            lm = relacionamento.find("ENTITY")
            anotacao["descricao"][lm.attrib["ID"]] = {}
            
            for atributo in lm:
                anotacao["descricao"][lm.attrib["ID"]][atributo.attrib["NAME"]] = [atributo.attrib["VALUE"]]
        
        anotacoes.append(anotacao)
        
    return anotacoes  

def parseFeatureVector():
    contextos = parseDominio(True)
    
    featureVector = {}
    
    for contexto in contextos.keys():
        featureVector[contexto] = {}
        for dominio in contextos[contexto].keys():
            featureVector[contexto][dominio] = {}
            
            for target in contextos[contexto][dominio].keys():
                featureVector[contexto][dominio][target] = {}
                
                relation = "none"
                
                # define a orientacao do objeto  
                if len(contextos[contexto][dominio][target]["orientation"]) > 0:
                    if contextos[contexto][dominio][target]["orientation"][0].strip() == "up" or contextos[contexto][dominio][target]["orientation"][0].strip() == "down":
                        relation = "vertical"
                    else:
                        relation = "horizontal"
                
                featureVector[contexto][dominio][target]["tg_size"] = "small"
                
                if "size" in contextos[contexto][dominio][target]:
                    if float(contextos[contexto][dominio][target]["size"][0]) <= 5:
                        featureVector[contexto][dominio][target]["tg_size"] = "small"
                    else:
                        featureVector[contexto][dominio][target]["tg_size"] = "large"
                    
                featureVector[contexto][dominio][target]["relation"] = relation
                
                
                featureVector[contexto][dominio][target]["num_tg_size"] = 0
                featureVector[contexto][dominio][target]["num_tg_col"] = 0
                featureVector[contexto][dominio][target]["num_tg_type"] = 0
                
                for element in contextos[contexto][dominio].keys():
                    
                    if element != target:
                        if "size" in contextos[contexto][dominio][element] and "size" in contextos[contexto][dominio][target]:
                            if float(contextos[contexto][dominio][target]["size"][0]) <= 5 and float(contextos[contexto][dominio][element]["size"][0]) <= 5:
                                featureVector[contexto][dominio][target]["num_tg_size"] = featureVector[contexto][dominio][target]["num_tg_size"] + 1
                            
                            if float(contextos[contexto][dominio][target]["size"][0]) > 5 and float(contextos[contexto][dominio][element]["size"][0]) > 5:
                                featureVector[contexto][dominio][target]["num_tg_size"] = featureVector[contexto][dominio][target]["num_tg_size"] + 1
                        
                        if len(contextos[contexto][dominio][target]["color"]) > 0 and len(contextos[contexto][dominio][element]["color"]) > 0:
                            if contextos[contexto][dominio][target]["color"][0] == contextos[contexto][dominio][element]["color"][0]:
                                featureVector[contexto][dominio][target]["num_tg_col"] = featureVector[contexto][dominio][target]["num_tg_col"] + 1
                        
                        if len(contextos[contexto][dominio][target]["type"]) > 0 and len(contextos[contexto][dominio][element]["type"]) > 0:
                            if contextos[contexto][dominio][target]["type"][0] == contextos[contexto][dominio][element]["type"][0]:
                                featureVector[contexto][dominio][target]["num_tg_type"] = featureVector[contexto][dominio][target]["num_tg_type"] + 1
    
    return featureVector

def parseSVMInput(contextos, anotacoes, featureVectors):
    input = []
    for anotacao in anotacoes:
        classes = {}
        vetor = []
        participante = anotacao["caracteristicas"]["trial"]
        contexto = anotacao["caracteristicas"]["context"]
        target = anotacao["caracteristicas"]["target"]
        
        dominio = str
        achou = False
        for dom in contextos[contexto].keys():
            for objeto in contextos[contexto][dom].keys():
                if target == objeto:
                    dominio = dom
                    achou = True
                    break
            if achou == True:
                break
        
        featureVector = featureVectors[contexto][dominio][target]
        
        vetor.append(int(participante))
        if featureVector["tg_size"] == "small":
            vetor.append(0)
        else:
            vetor.append(1)
            
        if featureVector["relation"] == "none":
            vetor.append(0)
        elif featureVector["relation"] == "horizontal":
            vetor.append(0)
        else:
            vetor.append(1)
        
        vetor.append(featureVector["num_tg_size"])
        vetor.append(featureVector["num_tg_col"])
        vetor.append(featureVector["num_tg_type"])
        
        if "type" in anotacao["descricao"][target].keys():
            classes["type"] = 1
        else:
            classes["type"] = 0
        
        if "color" in anotacao["descricao"][target].keys():
            classes["col"] = 1
        else:
            classes["col"] = 0
        
        relacao = str
        if "in front of" in anotacao["descricao"][target].keys():
            classes["relation"] = 1
            relacao = "in front of"
        elif "next" in anotacao["descricao"][target].keys():
            classes["relation"] = 2
            relacao = "next"
        elif "right" in anotacao["descricao"][target].keys():
            classes["relation"] = 3
            relacao = "right"
        elif "left" in anotacao["descricao"][target].keys():
            classes["relation"] = 4
            relacao = "left"
        elif "behind" in anotacao["descricao"][target].keys():
            classes["relation"] = 5
            relacao = "behind"
        elif "up" in anotacao["descricao"][target].keys():
            classes["relation"] = 6
            relacao = "up"
        elif "corner" in anotacao["descricao"][target].keys():
            classes["relation"] = 7
            relacao = "corner"
        else:
            classes["relation"] = 0
            relacao = "none"
            
        if classes["relation"] > 0:
            landmark = anotacao["descricao"][target][relacao][0]
            if "type" in anotacao["descricao"][landmark].keys():
                classes["lm_type"] = 1
            else:
                classes["lm_type"] = 0
            
            if "color" in anotacao["descricao"][landmark].keys():
                classes["lm_col"] = 1
            else:
                classes["lm_col"] = 0
            
        else:
            classes["lm_type"] = 0
            classes["lm_col"] = 0
                
        data = {}
        data["data"] = vetor
        data["classes"] = classes
        data["anotacao"] = anotacao
        input.append(data)
    
    return input
    