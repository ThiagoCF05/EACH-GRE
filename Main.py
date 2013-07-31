'''
Created on 19/12/2012

@author: thiagocastroferreira
'''

import sys
from graph import *
from MapParser import *
from RelationalAlgorithmV3 import *
from IncrementalAlgorithmRelational import *

if __name__ == '__main__':
    dominio = parse()
#    for target in dominio.keys():
#        print target
#        print "\n"
#        sys.argv = []
#        sys.argv.append("")
#        sys.argv.append("mapa.json")
#        sys.argv.append(target)
#        sys.argv.append("custos.txt")
#        sys.argv.append(target)
#        sys.argv.append("all")
#        sys.argv.append("4")
#        main(sys.argv)
#        print '\n'
    
    preferenced_attributes = ['type','name','other','in','right-of','left-of','near-to',
                              'in-front-of','behind',
                              'have','northeast','northwest','southeast','southwest']
    
    for entidade in dominio.keys():
        if entidade[0:3] != "str" and entidade[0:3] != "pos":
            print entidade
            relational = IncrementalAlgorithmRelational(dominio, entidade, preferenced_attributes)
            list = relational.run()
            print list
            print '\n'
    
        
    
    
    
    