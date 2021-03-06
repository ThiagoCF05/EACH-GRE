'''
Created on 29/07/2013

@author: thiagocastroferreira
'''

class IncrementalAlgorithmRelational(object):


    def __init__(self, dominio = {}, target = str, preferred_attributes = [], restricaoContexto = False):
        self.dominio = dominio
        self.target = target
        self.preferred_attributes = preferred_attributes
        self.distractors = {}
        self.restricaoContexto = restricaoContexto
        # restricao de contexto
        self.distractors[target] = self.initializeDistractors(target, restricaoContexto, self.dominio)
        
        self.atributos = {}
        self.atributosRelacionais = {}
        [self.atributos[target], self.atributosRelacionais[target]] = self.listaAtributos(target)
        
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
                    self.description[target][atributo] = [element]
                
                if len(self.distractors[target]) == 1:
                    return self.description
        if len(self.distractors[target]) > 1:
            return self.searchRelationalDescription(target)

    def searchRelationalDescription(self, target):
        candidateLandmarks = self.setCandidateLandmarks(target)
        
        for landmark in candidateLandmarks:
            atributo = landmark[0]
            element = landmark[1]
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
                if element not in self.description.keys():
                    if atributo in self.description[target].keys():
                        self.description[target][atributo].append(element)
                    else:
                        self.description[target][atributo] = [element]
                    [self.atributos[element], self.atributosRelacionais[element]] = self.listaAtributos(element)
                    self.distractors[element] = self.initializeDistractors(element, self.restricaoContexto, self.dominio)
                    self.description[element] = {}
                    self.description = self.searchDescription(element)
            
            
            if len(self.distractors[target]) == 1:
                return self.description
        return self.description
            
            
    def setCandidateLandmarks(self, target):
        candidateLandmarks = []
        
        
        for atributo in self.atributosRelacionais[target]:
            for element in self.dominio[target][atributo]:
                candidateLandmarks.append([atributo, element])
        
        return candidateLandmarks
    
    def listaAtributos(self, target):
        atributos = []
        atributosRelacionais = []
            
        if len(self.preferred_attributes) == 0:
            aux = self.dominio[target].keys()
            
            for atributo in aux:
                if len(self.dominio[target][atributo]) != 0:
                    if self.relationalAttribute(atributo):
                        atributosRelacionais.append(atributo)
                    else:
                        atributos.append(atributo)
        else:
            for atributo in self.preferred_attributes:
                if len(self.dominio[target][atributo]) != 0:
                    if self.relationalAttribute(atributo):
                        atributosRelacionais.append(atributo)
                    else:
                        atributos.append(atributo)
        

        return [atributos, atributosRelacionais]
    
    def relationalAttribute(self, atributo = str):
        lista = atributo.split("_")
        
        if lista[0] != "others" and lista[0] != "type" and lista[0] != "hpos" and lista[0] != "vpos":
            return True
        else:
            return False
    
    def initializeDistractors(self, target, contextRestriction, dominio = {}):
        distractors = {}
        if contextRestriction:
            for element in dominio[target]['near-to']:
                distractors[element] = dominio[element]
            distractors[target] = dominio[target]
        else:
            distractors = dominio
        
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

        
        