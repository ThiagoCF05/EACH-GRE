'''
Created on 03/09/2013

@author: thiagocastroferreira
'''

class IncrementalAlgorithmRelational3(object):
    def __init__(self, context = {}, target = str, preferred_attributes = [], restricaoContexto = False):
        self.context = context
        self.dominio = self.initializeDominio(self.context)
        self.target = target
        self.preferred_attributes = preferred_attributes
        self.distractors = {}
        self.restricaoContexto = restricaoContexto
        # restricao de contexto
        self.distractors[target] = self.initializeDistractors(target, restricaoContexto, self.context)
        
        self.atributos = {}
        self.atributos[target] = self.listaAtributos(target, True)
        
        self.description = {}
        self.description[self.target] = {}

    def run(self):
        return self.searchDescription(self.target)

    def searchDescription(self, target):
        for atributo in self.atributos[target]:
            for element in self.dominio[target][atributo]:
                properties = {}
                for key in self.description[target].keys():
                    properties[key] = self.description[target][key]
                if atributo in properties.keys():
                    aux = []
                    for row in properties[atributo]:
                        aux.append(row)
                    aux.append(element)
                    properties[atributo] = aux
                else:
                    properties[atributo] = [element]  
                
                previousDistractor = {}
                for distractor in self.distractors[target].keys():
                    previousDistractor[distractor] = self.distractors[target][distractor]
                
                self.distractors[target] = self.findDistractorsByProperties(properties, target, self.distractors)
                
                if len(self.distractors[target]) < len(previousDistractor):
                    if self.relationalAttribute(atributo):
                        if element not in self.description.keys():
                            if atributo in self.description[target].keys():
                                self.description[target][atributo].append(element)
                            else:
                                self.description[target][atributo] = [element]
                            self.atributos[element] = self.listaAtributos(element, False)
                            self.distractors[element] = self.initializeDistractors(element, self.restricaoContexto, self.context)
                            self.description[element] = {}
                            self.description = self.searchDescription(element)
                    else:
                        self.description[target][atributo] = [element]
                
                if len(self.distractors[target]) == 1:
                    return self.description
        if len(self.distractors[target]) > 1:
            return self.description
    
    def listaAtributos(self, target, ehAlvo):
        atributos = []
        
        if ehAlvo:
            if len(self.preferred_attributes["target"]) == 0:
                atributos = self.context[target].keys()
            else:
                atributos = self.preferred_attributes["target"]
        else:
            if len(self.preferred_attributes["landmark"]) == 0:
                atributos = self.context[target].keys()
            else:
                atributos = self.preferred_attributes["landmark"]
        
        return atributos
    
    def relationalAttribute(self, atributo = str):
        lista = atributo.split("_")
        
        if lista[0] != "color" and lista[0] != "type" and lista[0] != "orientation":
            return True
        else:
            return False
    
    def initializeDominio(self, context = {}):
        dominio = {}
        
        for domain in context.keys():
            for objeto in context[domain].keys():
                if objeto not in dominio.keys():
                    dominio[objeto] = context[domain][objeto]
        
        return dominio
    
    def initializeDistractors(self, target, contextRestriction, context = {}):
        distractors = {}
        if contextRestriction:
            for dominio in context.keys():
                for objeto in context[dominio].keys():
                    if objeto == target:
                        distractors = context[dominio]
                        return distractors
        else:
            for dominio in context.keys():
                for objeto in context[dominio].keys():
                    if objeto not in distractors.keys():
                        distractors[objeto] = context[dominio][objeto]
        
        return distractors
            
    
    def findDistractorsByProperties(self, properties = {}, target = str, distract = {}):
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