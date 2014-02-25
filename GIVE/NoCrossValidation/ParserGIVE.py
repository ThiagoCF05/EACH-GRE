'''
Created on 22/08/2013

@author: thiagocastroferreira
'''

import xml.etree.ElementTree as ET
# Formata as expressoes geradas pelos participantes do experimento Stars
def parseDominio():
    contextos = {}
    
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
                if atributo.attrib["NAME"] not in ["x", "y", "z", "size"]:
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
                if atributo.attrib["NAME"] not in ["x", "y", "z", "size"]:
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
                if atributo.attrib["NAME"] not in ["x", "y", "z", "size"]:
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
        
    