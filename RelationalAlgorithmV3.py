'''
Created on 25/07/2013

@author: thiagocastroferreira
'''

#Full Brevity
class RelationalAlgorithmV3(object):


    def __init__(self, dominio = {}, target = str, preferred_attributes = []):
        self.dominio = dominio
        
        ##########################
        for key in self.dominio.keys():
            self.dominio[key]['between'] = []
        ##########################
        
        self.stack = []
        self.stack.append(target)
        self.preferred_attributes = preferred_attributes
        self.atributos = {}
        self.atributos = self.listaAtributos(target)
        # Constraint Network
        self.description = {}
        self.description[target] = {}
        self.distractors = {}
        self.distractors[target] = self.findDistractorsByTarget(target, self.dominio)
            
    def run(self):
        self.checkSuccess()
        return self.description
    
    def checkSuccess(self):
        if len(self.stack) == 0:
            return True
        elif len(self.distractors[self.stack[len(self.stack)-1]]) <= 1:
            self.stack.pop()
            return self.checkSuccess()
        else:
            for key in self.atributos.keys():
                if len(self.atributos[key]) == 0 and key in self.stack:
                    return False
            return self.checkProperty()
    
    def checkProperty(self):
        target = self.stack.pop()
        if self.description[target] == {} and self.dominio[target]['type'] != []:
            self.description[target]['type'] = self.dominio[target]['type'][0]
            properties = {}
            properties['type'] = self.dominio[target]['type'][0]
            self.distractors[target] = self.findDistractorsByProperties(properties)
            self.atributos[target].remove('type')
        else:
            description = self.searchDescription(self.description, target, None, None, 1, 1)
            self.atributos[target] = {}
            
            for key in description.keys():
                self.description[key] = description[key]
            
            for atributo in description[target].keys():
                elemento = description[target][atributo]
                if self.relationalAttribute(atributo):
                    if elemento not in self.description.keys():
                        self.stack.append(elemento)
                        self.atributos = self.listaAtributos(elemento)
                        self.description[elemento] = {}
                        self.distractors[elemento] = self.findDistractorsByTarget(elemento, self.dominio)
                    
        self.stack.append(target)
        return self.checkSuccess()
    
    def searchDescription(self, description, target, atributo, element, loopInicial, loopAtual):
        if atributo != None:
            description[target][atributo] = element  
        
        loopAtual = loopAtual - 1
        for atributo in self.atributos[target]:
            for element in self.dominio[target][atributo]: 
                if loopAtual == 0:
                    properties = {}
                    for key in description[target].keys():
                        properties[key] = description[target][key]
                    properties[atributo] = element
                    
                    distractors = {}
                    distractors = self.findDistractorsByProperties(properties)
                    
                    if len(distractors.keys()) == 1:
                        self.distractors[target] = distractors
                        description[target][atributo] = element   
                        return description                                            
                    
                else:                    
                    return self.searchDescription(description, target, atributo, element, loopInicial, loopAtual)
                
        if (loopInicial < len(self.atributos)):
            return self.searchDescription({}, target, None, None, loopInicial+1, loopInicial+1)
        else:
            return {}
                
    def relationalAttribute(self, atributo = str):
        lista = atributo.split("_")
        
        if lista[0] != "name" and lista[0] != "type" and lista[0] != "other":
            return True
        else:
            return False
           
    def listaAtributos(self, target):
        if len(self.preferred_attributes) == 0:
            aux = self.dominio[target].keys()
            atributos = []
            for atributo in aux:
                if len(self.dominio[target][atributo]) != 0:
                    atributos.append(atributo)
            self.atributos[target] = atributos
        else:
            self.atributos[target] = self.preferred_attributes
        return self.atributos
    
    
    def findDistractorsByTarget(self, target, dominio):
        distractors = {}
        for objeto in dominio.keys():
            if objeto != target: 
                distractors[objeto] = dominio[objeto]

        return distractors
    
    def findDistractorsByProperties(self, properties = {}):
        distractors = {}
        
        dominio = self.dominio
        
        for property in properties.keys():
            distractors = {}
            for object in dominio.keys():
                if properties[property] in dominio[object][property]:
                    distractors[object] = dominio[object]
            dominio = distractors
            
        return distractors
        