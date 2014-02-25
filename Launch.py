'''
Created on 19/02/2014

@author: thiagocastroferreira
'''

import MachineLearning.TUNA_furniture.SVMValidatedExperiment as svm_furniture
import MachineLearning.TUNA_furniture.ExperimentDecisionTree as tree_furniture
import MachineLearning.TUNA_furniture.ValidatedExperimentIndividual as validate_furniture

import MachineLearning.TUNA_people.SVMValidatedExperiment as svm_people
import MachineLearning.TUNA_people.ExperimentDecisionTree as tree_people
import MachineLearning.TUNA_people.ValidatedExperimentIndividual as validate_people

import MachineLearning.StarsV2.SVMValidatedExperiment as svm_stars
import MachineLearning.StarsV2.ExperimentDecisionTree as tree_stars
import MachineLearning.StarsV2.ValidatedExperimentIndividual as validate_stars

import MachineLearning.Stars2.SVMValidatedExperiment as svm_stars2
import MachineLearning.Stars2.ExperimentDecisionTree as tree_stars2
import MachineLearning.Stars2.ValidatedExperimentIndividual as validate_stars2

import MachineLearning.GRE3D3.SVMValidatedExperiment as svm_gre3d3
import MachineLearning.GRE3D3.ExperimentDecisionTree as tree_gre3d3
import MachineLearning.GRE3D3.ValidatedExperimentIndividual as validate_gre3d3

import MachineLearning.GRE3D.SVMValidatedExperiment as svm_gre3d7
import MachineLearning.GRE3D.ExperimentDecisionTree as tree_gre3d7
import MachineLearning.GRE3D.ValidatedExperimentIndividual as validate_gre3d7

import TUNA_furniture.SVMValidatedExperiment as svmie_furniture

import TUNA_people.SVMValidatedExperiment as svmie_people

import StarsV2.SVMValidatedExperiment as svmie_stars

import Stars2.SVMValidatedExperiment as svmie_stars2

import GRE3D3.SVMValidatedExperiment as svmie_gre3d3

import GRE3D.SVMValidatedExperiment as svmie_gre3d7

import Util as utils

if __name__ == '__main__':
    # TUNA
    # FURNITURE
    trials, atributos, folds = utils.initialize_svm_furniture()
    resultados, dices, masis, acertos = validate_furniture.run(trials, atributos, False)
    utils.save_results("tree_validate-furniture_2.xml", resultados, dices, masis, acertos)
     
#     resultados, dices, masis, acertos = validate_furniture.run(trials, atributos, True)
#     utils.save_results("tree_validate-furniture_4.xml", resultados, dices, masis, acertos)
     
#     resultados, dices, masis, acertos = tree_furniture.run(trials, folds, atributos, {}, False)
#     utils.save_results("tree_furniture_7.xml", resultados, dices, masis, acertos)
     
#     resultados, dices, masis, acertos = tree_furniture.run(trials, folds, atributos, {}, True)
#     utils.save_results("tree_furniture_2.xml", resultados, dices, masis, acertos)
     
#     resultados, dices, masis, acertos = svmie_furniture.run(trials, folds, atributos, {}, False)
#     utils.save_results("svmie_furnitureN_7.xml", resultados, dices, masis, acertos)
#       
#     resultados, dices, masis, acertos = svmie_furniture.run(trials, folds, atributos, {}, True)
#     utils.save_results("svmie_furnitureN_8.xml", resultados, dices, masis, acertos)
     
    # PEOPLE
    trials, atributos, folds = utils.initialize_svm_people()
    resultados, dices, masis, acertos = validate_people.run(trials, atributos, False)
    utils.save_results("tree_validate-people_2.xml", resultados, dices, masis, acertos)
     
#     resultados, dices, masis, acertos = validate_people.run(trials, atributos, True)
#     utils.save_results("tree_validate-people_4.xml", resultados, dices, masis, acertos)
     
#     resultados, dices, masis, acertos = tree_people.run(trials, folds, atributos, {}, False)
#     utils.save_results("tree_people_7.xml", resultados, dices, masis, acertos)
     
#     resultados, dices, masis, acertos = tree_people.run(trials, folds, atributos, {}, True)
#     utils.save_results("tree_people_2.xml", resultados, dices, masis, acertos)
     
#     resultados, dices, masis, acertos = svmie_people.run(trials, folds, atributos, {}, False)
#     utils.save_results("svmie_peopleN_7.xml", resultados, dices, masis, acertos)
#       
#     resultados, dices, masis, acertos = svmie_people.run(trials, folds, atributos, {}, True)
#     utils.save_results("svmie_peopleN_8.xml", resultados, dices, masis, acertos)
    
    # STARS
    dominios, targets, anotacoes, atributos, participantes, folds = utils.initialize_stars()
    resultados, dices, masis, acertos = validate_stars.run(dominios, targets, anotacoes, atributos, False)
    utils.save_results("tree_validate-stars_2.xml", resultados, dices, masis, acertos)
     
#     resultados, dices, masis, acertos = validate_stars.run(dominios, targets, anotacoes, atributos, True)
#     utils.save_results("tree_validate-stars_4.xml", resultados, dices, masis, acertos)
     
#     resultados, dices, masis, acertos = tree_stars.run(dominios, targets, folds, atributos, {}, False)
#     utils.save_results("tree_stars_7.xml", resultados, dices, masis, acertos)
     
#     resultados, dices, masis, acertos = tree_stars.run(dominios, targets, folds, atributos, {}, True)
#     utils.save_results("tree_stars_2.xml", resultados, dices, masis, acertos)
     
#     resultados, dices, masis, acertos = svmie_stars.run(dominios, targets, folds, atributos, {}, False)
#     utils.save_results("svmie_starsN_7.xml", resultados, dices, masis, acertos)
#       
#     resultados, dices, masis, acertos = svmie_stars.run(dominios, targets, folds, atributos, {}, True)
#     utils.save_results("svmie_starsN_8.xml", resultados, dices, masis, acertos)
    
    # STARS 2
    dominios, targets, anotacoes, atributos, participantes, folds = utils.initialize_stars2()
    resultados, dices, masis, acertos = validate_stars2.run(dominios, targets, anotacoes, atributos, False)
    utils.save_results("tree_validate-stars2_2.xml", resultados, dices, masis, acertos)
     
#     resultados, dices, masis, acertos = validate_stars2.run(dominios, targets, anotacoes, atributos, True)
#     utils.save_results("tree_validate-stars2_4.xml", resultados, dices, masis, acertos)
     
#     resultados, dices, masis, acertos = tree_stars2.run(dominios, targets, folds, atributos, {}, False)
#     utils.save_results("tree_stars2_7.xml", resultados, dices, masis, acertos)
     
#     resultados, dices, masis, acertos = tree_stars2.run(dominios, targets, folds, atributos, {}, True)
#     utils.save_results("tree_stars2_2.xml", resultados, dices, masis, acertos)
     
#     resultados, dices, masis, acertos = svmie_stars2.run(dominios, targets, folds, atributos, {}, False)
#     utils.save_results("svmie_stars2N_7.xml", resultados, dices, masis, acertos)
#       
#     resultados, dices, masis, acertos = svmie_stars2.run(dominios, targets, folds, atributos, {}, True)
#     utils.save_results("svmie_stars2N_8.xml", resultados, dices, masis, acertos)
    
    # GRE3D3
    dominios, targets, anotacoes, atributos, participantes, folds = utils.initialize_gre3d3()
    resultados, dices, masis, acertos = validate_gre3d3.run(dominios, targets, anotacoes, atributos, participantes, False)
    utils.save_results("tree_validate-gre3d3_2.xml", resultados, dices, masis, acertos)
     
#     resultados, dices, masis, acertos = validate_gre3d3.run(dominios, targets, anotacoes, atributos, participantes, True)
#     utils.save_results("tree_validate-gre3d3_4.xml", resultados, dices, masis, acertos)
     
#     resultados, dices, masis, acertos = tree_gre3d3.run(dominios, targets, folds, atributos, participantes, False)
#     utils.save_results("tree_gre3d3_7.xml", resultados, dices, masis, acertos)
     
#     resultados, dices, masis, acertos = tree_gre3d3.run(dominios, targets, folds, atributos, participantes, True)
#     utils.save_results("tree_gre3d3_2.xml", resultados, dices, masis, acertos)
     
#     resultados, dices, masis, acertos = svmie_gre3d3.run(dominios, targets, folds, atributos, participantes, False)
#     utils.save_results("svmie_gre3d3N_7.xml", resultados, dices, masis, acertos)
#       
#     resultados, dices, masis, acertos = svmie_gre3d3.run(dominios, targets, folds, atributos, participantes, True)
#     utils.save_results("svmie_gre3d3N_8.xml", resultados, dices, masis, acertos)
    
    # GRE3D7
    dominios, targets, anotacoes, atributos, participantes, folds = utils.initialize_gre3d7()
    resultados, dices, masis, acertos = validate_gre3d7.run(dominios, targets, anotacoes, atributos, participantes, False)
    utils.save_results("tree_validate-gre3d7_2.xml", resultados, dices, masis, acertos)
     
#     resultados, dices, masis, acertos = validate_gre3d7.run(dominios, targets, anotacoes, atributos, participantes, True)
#     utils.save_results("tree_validate-gre3d7_4.xml", resultados, dices, masis, acertos)
     
#     resultados, dices, masis, acertos = tree_gre3d7.run(dominios, targets, folds, atributos, participantes, False)
#     utils.save_results("tree_gre3d7_7.xml", resultados, dices, masis, acertos)
     
#     resultados, dices, masis, acertos = tree_gre3d7.run(dominios, targets, folds, atributos, participantes, True)
#     utils.save_results("tree_gre3d7_2.xml", resultados, dices, masis, acertos)
    
#     resultados, dices, masis, acertos = svmie_gre3d7.run(dominios, targets, folds, atributos, participantes, False)
#     utils.save_results("svmie_gre3d7N_7.xml", resultados, dices, masis, acertos)
#      
#     resultados, dices, masis, acertos = svmie_gre3d7.run(dominios, targets, folds, atributos, participantes, True)
#     utils.save_results("svmie_gre3d7N_8.xml", resultados, dices, masis, acertos)
    
    