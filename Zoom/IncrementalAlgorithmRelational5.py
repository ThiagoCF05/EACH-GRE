'''
Created on 13/09/2013

@author: thiagocastroferreira
'''

def run(dominio = {}, targets = [], preferred_attributes = [], restricaoContexto = False):
    descricao = {}
    i = 0
    for target in targets:
        i = i + 1
        
        distractors = {}
        distractors[target] = initializeDistractors(target, restricaoContexto, dominio)
        
        atributos = {}
        atributos[target] = listaAtributos(target, True, preferred_attributes, dominio)
        
        description = {}
        descricao[str(i)] = searchDescription(target, description, atributos, distractors, dominio, preferred_attributes, restricaoContexto)
    
    return descricao

def searchDescription(target, description, atributos, distractors, dominio, preferred_attributes, restricaoContexto):
    description[target] = {}
    
    for atributo in atributos[target]:
        for element in dominio[target][atributo]:
            
            properties = {}
            for key in description[target].keys():
                properties[key] = description[target][key]
            if atributo in properties.keys():
                aux = []
                for row in properties[atributo]:
                    aux.append(row)
                aux.append(element)
                properties[atributo] = aux
            else:
                properties[atributo] = [element]  
            
            previousDistractor = {}
            for distractor in distractors[target].keys():
                previousDistractor[distractor] = distractors[target][distractor]
            
            distractors[target] = findDistractorsByProperties(properties, target, distractors)
            
            if len(distractors[target]) < len(previousDistractor):
                if relationalAttribute(atributo):
                    if element not in description.keys():
                        if atributo in description[target].keys():
                            description[target][atributo].append(element)
                        else:
                            description[target][atributo] = [element]
                        atributos[element] = listaAtributos(element, False, preferred_attributes, dominio)
                        distractors[element] = initializeDistractors(element, restricaoContexto, dominio)
                        description[element] = {}
                        description = searchDescription(element, description, atributos, distractors, dominio, preferred_attributes, restricaoContexto)
                    else:
                        distractors[target] = previousDistractor
                else:
                    description[target][atributo] = [element]
                    
            if len(distractors[target]) == 1:
                return description
            
    return description

def listaAtributos(target, ehAlvo, preferred_attributes, dominio):
    atributos = []
    
    if ehAlvo:
        if len(preferred_attributes["target"]) == 0:
            atributos = dominio[target].keys()
        else:
            atributos = preferred_attributes["target"]
    else:
        if len(preferred_attributes["landmark"]) == 0:
            atributos = dominio[target].keys()
        else:
            atributos = preferred_attributes["landmark"]
    
    if "between" in atributos:
        atributos.remove("between")
    if "id" in atributos:
        atributos.remove("between")
    return atributos

def relationalAttribute(atributo = str):
    lista = atributo.split("_")
    
    if lista[0] != "type" and lista[0] != "name" and lista[0] != "other":
        return True
    else:
        return False

def initializeDistractors(target, contextRestriction, dominio = {}):
    distractors = {}
    if contextRestriction:
        for element in dominio[target]['near-to']:
            distractors[element] = dominio[element]
        distractors[target] = dominio[target]
    else:
        distractors = dominio
    
    return distractors
        
def findDistractorsByProperties(properties = {}, target = str, distract = {}):
    distractors = {}
    dominio = distract[target]
    for property in properties.keys():
        distractors = {}
        for element in properties[property]:
            for object in dominio.keys():
                if element in dominio[object][property]:
                    distractors[object] = dominio[object]
            dominio = distractors
            
    return distractors