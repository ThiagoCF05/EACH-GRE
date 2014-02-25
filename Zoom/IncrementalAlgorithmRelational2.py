'''
Created on 28/08/2013

@author: thiagocastroferreira
'''

def run(dominio = {}, targets = [], preferred_attributes = [], restricaoContexto = False):
    description = {}
    i = 0
    
    for target in targets:
        distractors = {}
        distractors[target] = initializeDistractors(target, restricaoContexto, dominio)
        
        atributos = {}
        atributos[target] = listaAtributos(target, dominio, preferred_attributes)
        
        i = i + 1
        descricao = {}
        description[str(i)] = searchDescription(target, descricao, atributos, distractors, dominio, preferred_attributes, restricaoContexto)
        
    return description

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
                            
                        atributos[element] = listaAtributos(element, dominio, preferred_attributes)
                        distractors[element] = initializeDistractors(element, restricaoContexto, dominio)
                        description[element] = {}
                        description = searchDescription(element, description, atributos, distractors, dominio, preferred_attributes, restricaoContexto)
                else:
                    description[target][atributo] = [element]
            
            if len(distractors[target]) == 1:
                return description
    if len(distractors[target]) > 1:
        return description

def listaAtributos(target, dominio, preferred_attributes):
    atributos = []
        
    if len(preferred_attributes) == 0:
        atributos = dominio[target].keys()
    else:
        atributos = preferred_attributes

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