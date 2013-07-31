'''
Created on 19/07/2013

@author: thiagocastroferreira
'''

from Objeto import *

class RelationalAlgorithm(object):
    """docstring for RelationalAlgorithm"""
    def __init__(self, dominio = {}, target = str, distractors = {}, preferred_attributes = []):
        super(RelationalAlgorithm, self).__init__()
        self.dominio = dominio
        self.stack = []
        self.stack.append(target)
        self.distractors = self.findDistractors(target)
        if len(preferred_attributes) == 0:
            self.atributos = dominio[target].keys()
        else:
            self.atributos = preferred_attributes

    def run(self):
        return self.geraResultado({}, self.stack.pop(), None, 1, 1)
                
    def geraResultado(self, descriptionProperties, target, attribute, numeroForInicio, numeroFor):
        
        if attribute != None:
            lista = descriptionProperties[target]
            lista.append(attribute)   
            descriptionProperties[target] = lista  
        else:
            descriptionProperties[target] = []                    
        
        numeroFor = numeroFor - 1
        for atributo in self.atributos:
            if atributo not in descriptionProperties[target] and target != None:   
                if atributo == "type":
                    lista = descriptionProperties[target]
                    lista.append(atributo)   
                    descriptionProperties[target] = lista 
                elif numeroFor == 0:
                    lista = descriptionProperties[target]
                    lista.append(atributo)   
                    descriptionProperties[target] = lista 
                    
                    if self.ruledOut(descriptionProperties[target], target) == True:
                        if self.relationalAttribute(atributo):
                            for element in self.dominio.keys():
                                if element == self.dominio[target][atributo]:
                                    self.stack.insert(0, element)
                                    break
                            
                        if len(self.stack) > 0:
                            target = self.stack.pop()
                            self.distractors = self.findDistractors(target)
                            return self.geraResultado(descriptionProperties, target, None, 1, 1)
                        else:
                            return descriptionProperties                                            
                    
                    lista = descriptionProperties[target]
                    lista.remove(atributo)   
                    descriptionProperties[target] = lista
                    
                else:                    
                    return self.geraResultado(descriptionProperties, target, atributo, numeroForInicio, numeroFor)
                
        if (numeroForInicio < len(self.atributos)):
            return self.geraResultado({}, target, None, numeroForInicio+1, numeroForInicio+1)
        else:
            return []
       
    def relationalAttribute(self, atributo = str):
        lista = atributo.split("_")
        
        if lista[0] != "name" and lista[0] != "type" and lista[0] != "other":
            return True
        else:
            return False
                 
    def ruledOut(self, descriptionProperties = [], target):
        
        for distractor in self.distractors.keys():
            targetDescription = []
            distractorDescription = []
            
            for atributo in descriptionProperties:
                targetDescription.append(self.dominio[target][atributo])
                distractorDescription.append(self.distractors[distractor][atributo])
            
            #print 10 * "-"
            #print "Target: "  + self.target.nome
            #print targetDescription
            #print 10 * "-" 
            #print "Distractor: " + distractor.nome
            #print distractorDescription
            #print 10 * "-" 
            #print "\n\n"
                
            if targetDescription == distractorDescription:
                return False
        
        #print descriptionProperties    
        return True


    def findDistractors(self, target):
        distractors = {}
        for objeto in self.dominio.keys():
            if objeto != target: 
                distractors[objeto] = self.dominio[objeto]

        return distractors

