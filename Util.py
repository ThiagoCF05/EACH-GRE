'''
Created on 19/02/2014

@author: thiagocastroferreira
'''

import MachineLearning.TUNA_furniture.Parser as parser_furniture
import MachineLearning.TUNA_furniture.CrossValidation as cross_furniture

import MachineLearning.TUNA_people.Parser as parser_people
import MachineLearning.TUNA_people.CrossValidation as cross_people

import MachineLearning.StarsV2.ParserStars as parser_stars
import MachineLearning.StarsV2.CrossValidation as cross_stars

import MachineLearning.Stars2.ParserStars as parser_stars2
import MachineLearning.Stars2.CrossValidation as cross_stars2

import MachineLearning.GRE3D3.ParserGRE3D as parser_gre3d3
import MachineLearning.GRE3D3.CrossValidation as cross_gre3d3

import MachineLearning.GRE3D.ParserGRE3D as parser_gre3d7
import MachineLearning.GRE3D.CrossValidation as cross_gre3d7

import xml.etree.ElementTree as ET
import datetime as date
import numpy as np
import os
from scipy.stats import wilcoxon, chisquare

def initialize_svm_furniture():
    trials = parser_furniture.parse("MachineLearning/TUNA_furniture/")
    atributos = ["type", "colour", "orientation", "size", "x-dimension", "y-dimension"]
    folds = cross_furniture.crossValidation(10, trials)
    return trials, atributos, folds

def initialize_svm_people():
    trials = parser_people.parse("MachineLearning/TUNA_people/")
    atributos = ["type", "orientation", "age", "hairColour", "hasBeard", "hasHair", "hasGlasses", "hasShirt", "hasTie", "hasSuit", "x-dimension", "y-dimension"]
    folds = cross_people.crossValidation(10, trials)
    return trials, atributos, folds

def initialize_stars():
    anotacoes = parser_stars.parseAnnotation("MachineLearning/StarsV2/")
    dominios = parser_stars.parseDominio("MachineLearning/StarsV2/")
    participantes = {}
    atributos = ["type", "colour", "hpos", "vpos", "near", "left", "right", "below", "above"]
    targets = {"abs1":"e2", "abs3":"e2", "abs5":"e3", "proj1":"e2", "proj3":"e4", "proj5":"e2" }
    folds = cross_stars.crossValidation(6, anotacoes)
    return dominios, targets, anotacoes, atributos, participantes, folds

def initialize_stars2():
    anotacoes = parser_stars2.parseAnnotation("MachineLearning/Stars2/")
    dominios = parser_stars2.parseDominio("MachineLearning/Stars2/")
    participantes = {}
    atributos = ["type", "size", "colour", "hpos", "vpos", "near", "left", "right", "below", "above", "in-front-of"]
    targets = {"01f-t1n":"h", "01f-t1r":"h", "01f-t2n":"h", "01f-t2r":"h", "01o-t1n":"h", "01o-t1r":"h", "01o-t2n":"h", "01o-t2r":"h", "02f-t1n":"o", "02f-t1r":"o", "02f-t2n":"o", "02f-t2r":"o", "02o-t1n":"o", "02o-t1r":"o", "02o-t2n":"o", "02o-t2r":"o", "03f-t1n":"m", "03f-t1r":"m", "03f-t2n":"m", "03f-t2r":"m", "03o-t1n":"m", "03o-t1r":"m", "03o-t2n":"m", "03o-t2r":"m", "04f-t1n":"a", "04f-t1r":"a", "04f-t2n":"a", "04f-t2r":"a", "04o-t1n":"a", "04o-t1r":"a", "04o-t2n":"a", "04o-t2r":"a", "05f-t1n":"m", "05f-t2n":"m", "05f-t1r":"m", "05f-t2r":"m", "05o-t1n":"m", "05o-t1r":"m", "05o-t2n":"m", "05o-t2r":"m", "06f-t1n":"h", "06f-t1r":"h", "06f-t2n":"h", "06f-t2r":"h", "06o-t1n":"h", "06o-t1r":"h", "06o-t2n":"h", "06o-t2r":"h", "07f-t1n":"i", "07f-t1r":"i", "07f-t2n":"i", "07f-t2r":"i", "07o-t1n":"i", "07o-t1r":"i", "07o-t2n":"i", "07o-t2r":"i", "08f-t1n":"a", "08f-t1r":"a", "08f-t2n":"a", "08f-t2r":"a", "08o-t1n":"a", "08o-t1r":"a", "08o-t2n":"a", "08o-t2r":"a" }
    folds = cross_stars2.crossValidation(10, anotacoes)
    return dominios, targets, anotacoes, atributos, participantes, folds

def initialize_gre3d3():
    anotacoes = parser_gre3d3.parseAnnotation("MachineLearning/GRE3D3/")
    dominios = parser_gre3d3.parseDominio("MachineLearning/GRE3D3/")
    participantes = parser_gre3d3.parseParticipantes("MachineLearning/GRE3D3/")
    targets = {"1":"b1","2":"b1","3":"b1","4":"c2","5":"c1","6":"b1","7":"b1","8":"b1","9":"c1","10":"c2","11":"b1","12":"b1","13":"b1","14":"c2","15":"c1","16":"b1","17":"b1","18":"b1","19":"c1","20":"c1"}
    atributos = ['loc', 'left-of', 'next-to', 'on-top-of', 'right-of', 'type', 'col', 'size', 'in-front-of']
    folds = cross_gre3d3.crossValidation(10, anotacoes)
    return dominios, targets, anotacoes, atributos, participantes, folds

def initialize_gre3d7():
    anotacoes = parser_gre3d7.parseAnnotation("MachineLearning/GRE3D/")
    dominios = parser_gre3d7.parseDominio("MachineLearning/GRE3D/")
    participantes = parser_gre3d7.parseParticipantes("MachineLearning/GRE3D/")
    targets = {"1":"b3","2":"b2","3":"b3","4":"b2","5":"b3","6":"b1","7":"b3","8":"b1","9":"b2","10":"b1","11":"b2","12":"b1","13":"b3","14":"b1","15":"b3","16":"b1","17":"b1","18":"b1","19":"b1","20":"b1","21":"b1","22":"b1","23":"b1","24":"b1","25":"b4","26":"b3","27":"b4","28":"b3","29":"b3","30":"b3","31":"b3","32":"b3"}
    atributos = ['loc', 'left-of', 'next-to', 'on-top-of', 'right-of', 'type', 'col', 'size']
    folds = cross_gre3d7.crossValidation(10, anotacoes)
    return dominios, targets, anotacoes, atributos, participantes, folds

def validate_results(corpus = "", printResults = False):
    results = load_results(corpus, printResults)
    
    for exp1 in results.keys():
        for exp2 in results.keys():
            if exp1 != exp2:
                T, p = wilcoxon(results[exp1]["dice"], results[exp2]["dice"])
                print "Wilcoxon: " + exp1 + " X " + exp2
                print "T: ", T, " p-value: ", p
                print 50 * "-"

def load_results(corpus = "", printResults = True):
    files = os.listdir("Resultados/")
    results = {}
    for file in files:
        
        f = file.split("_")
        if f[1] == corpus or corpus == "":
            
            root = ET.parse("Resultados/" + file).getroot()
            dices = [float(dice) for dice in list(root.find("dice").text.replace('[', '').replace(']', '').split(','))]
            masis = [float(masi) for masi in list(root.find("masi").text.replace('[', '').replace(']', '').split(','))]
            accepts = float(root.find("accepts").text)
            folds = root.find("folds")    
            
            acertosT = {}
            totalT = {}
            for fold in folds:
                for attribute in fold:
                    atributo = attribute.attrib["id"]
                    if atributo not in acertosT:
                        acertosT[atributo] = 0.0
                        totalT[atributo] = 0.0
                    acertosT[atributo] = acertosT[atributo] + float(attribute.attrib["accepts"])
                    totalT[atributo] = totalT[atributo] + float(attribute.attrib["total"])
            
            if printResults == True:
                print "\n"
                print file
                print "General:"
                print 50 * "*"
                print "Expressions: "
                print "Dice: " + str(np.mean(dices))
                print "Masi: " + str(np.mean(masis))
                print "Accuracy: " + str(accepts / len(dices))
                print "\n" 
                  
                print "Attributes:"
                print 15 * "-"     
                for atributo in acertosT.keys():
                    print "Attribute: " + str(atributo)
                    print "Accuracy: " + str(acertosT[atributo] / totalT[atributo])
                    print 10 * "-" 
            
            results[file.split(".")[0]] = {}
            results[file.split(".")[0]]["dice"] = dices
            results[file.split(".")[0]]["accepts"] = accepts
    return results

def save_results(nomeArquivo, resultados, dices, masis, acertos):
    results = ET.Element('results')
    
    results.set("data", date.datetime.now().strftime('%d/%m/%Y - %H:%M:%S'))
    
    dice = ET.SubElement(results, 'dice')
    dice.text = str(dices)
    
    masi = ET.SubElement(results, 'masi')
    masi.text = str(masis)
    
    accepts = ET.SubElement(results, 'accepts')
    accepts.text = str(acertos)
    
    folds = ET.SubElement(results, 'folds')
    i = 1
    
    for resultado in resultados:
        fold = ET.SubElement(folds, 'fold')
        fold.set('id', str(i))
        i = i + 1
        
        acertosAtributos = resultado[0]
        totalAtributos = resultado[1]
        
        for atributo in acertosAtributos.keys():
            attribute = ET.SubElement(fold, 'attribute')
            attribute.set('id', str(atributo))
            attribute.set('accepts', str(acertosAtributos[atributo]))
            attribute.set('total', str(totalAtributos[atributo]))
            
    tree = ET.ElementTree(results)
    tree.write("Resultados/" + nomeArquivo)
    
validate_results("stars2")