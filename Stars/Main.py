'''
Created on 19/12/2012

@author: thiagocastroferreira
'''
# from numpy import *
# from scipy import *
# import matplotlib.pyplot as plt
# from hcluster import *
import Assurance as ass
from ParserStars import *
from IncrementalAlgorithmRelational import *

if __name__ == '__main__':
    dominio = parseDominio()
    
    lista_preferencia = ["type", "others", "hpos", "vpos", "next", "left", "right", "below", "above"]
    
    incremental = IncrementalAlgorithmRelational(dominio["abs1"], "e2", lista_preferencia, False)
    list = incremental.run()
    
    print list