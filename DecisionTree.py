#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 12:12:42 2018

@author: jigar
"""

import sys
import math
import random

#node class to create tree structure
class TreeNode:
    #initialize instance variables
    def __init__(self,col=-1, value=0.0,measure=0.0):
        self.attributeColumn = col
        self.attributeSplitValue = value
        self.nodeMeasure = measure
        self.left = None
        self.right = None
        self.categoryValue = ''

#get data from file
def getDataSet(filename):
    dataSet = []
    data = open(filename,'r')
    with data:
        line = data.readline()
        while line:
            row = str(line).rstrip().split(',')
            dataSet.append(row)
            line = data.readline()
    data.close()
    return dataSet

#Split dataset into 2 parts based on attribute values
def splitDataSet(dataSet, attributeColumn, attributeSplitValue):
    leftDataSet = []
    rightDataSet = []

    for row in dataSet:
        if float(row[attributeColumn]) <= attributeSplitValue:
            leftDataSet.append(row)
        else:
            rightDataSet.append(row)

    return[leftDataSet,rightDataSet]

#check if node needs to be split; stopping condition
def checkNodeSplitRequired(dataSet,categoryIndex):
    if len(dataSet) < 5:
        return False
    else:
        categoryValues = getColumnValues(dataSet,categoryIndex,False)
        if len(categoryValues) == 1:
            return False
        elif len(categoryValues) > 1:
            return True

#given the dataset find the category value in majority and return it
def getDataSetCategory(dataSet,categoryIndex):
    categoryCount = {}
    dataSetCategory = ['',0]
    for row in dataSet:
        if row[categoryIndex] not in categoryCount:
            categoryCount[row[categoryIndex]] = 0
        count = categoryCount[row[categoryIndex]]
        count = count + 1
        categoryCount[row[categoryIndex]] = count
        if dataSetCategory[1] < count:
            dataSetCategory[0] = row[categoryIndex]
            dataSetCategory[1] = count
    return dataSetCategory[0]

#Get unique column values from dataset
def getColumnValues(dataSet,index,toFloat):

    columnValues = []
    for row in dataSet:
        value = row[index]
        if toFloat is True:
            value = float(value)
        if value not in columnValues:
            columnValues.append(value)
    return columnValues

#given a set of category value counts calculate its gini index
def calculateGini(splitStats):

    less_count = 0
    more_count = 0
    for categoryValueKey in splitStats:
        less_count = less_count + splitStats[categoryValueKey][0]
        more_count = more_count + splitStats[categoryValueKey][1]

    less_gini = 1
    more_gini = 1
    for categoryValueKey in splitStats:
        if less_count != 0:
            less_gini = less_gini - (splitStats[categoryValueKey][0]/less_count)**2
        if more_count != 0:
            more_gini = more_gini - (splitStats[categoryValueKey][1]/more_count)**2

    total_count = less_count + more_count

    if total_count != 0:
        return ((less_count/total_count)*less_gini) + ((more_count/total_count)*more_gini)
    else:
        return 0.5

#given a set of category value counts, calculate its information gain
def calculateInformationGain(splitStats,parentMeasure):

    less_count = 0
    more_count = 0
    for categoryValueKey in splitStats:
        less_count = less_count + splitStats[categoryValueKey][0]
        more_count = more_count + splitStats[categoryValueKey][1]

    less_entropy = 0.0
    more_entropy = 0.0
    for categoryValueKey in splitStats:
        if less_count != 0:
            probability = splitStats[categoryValueKey][0]/less_count
            if probability != 0.0:
                less_entropy = less_entropy + probability*math.log2(probability)
        if more_count != 0:
            probability = splitStats[categoryValueKey][1]/more_count
            if probability != 0.0:
                more_entropy = more_entropy + probability*math.log2(probability)

    less_entropy = less_entropy*(-1)
    more_entropy = more_entropy*(-1)

    total_count = less_count + more_count

    entropy = ((less_count/total_count)*less_entropy) + ((more_count/total_count)*more_entropy)

    return [( parentMeasure - entropy),entropy]

#based on gini index find best possible split attribute and its valve
def getSplitAttribute(dataSet,categoryIndex,skipIndex,measureType,parentMeasure):

    num_cols = len(dataSet[0])

    splitAttributeIndex = -1
    splitAttributeMeasure = 1
    splitAttributeGain = 0
    splitAttributePosition = 0

    for i in range(num_cols):
        if i != categoryIndex and i != skipIndex:

            attrValues = getColumnValues(dataSet,i,True)
            attrValues.sort()

            split_stats = {}

            for j in range(len(attrValues)):

                if j == 0 or j == len(attrValues) - 1:
                    splitPosition = float(attrValues[j])
                else:
                    splitPosition = (float(attrValues[j])+float(attrValues[j+1]))/2
                position_stats= {}

                for row in dataSet:

                    if float(row[i]) <= splitPosition:
                        cls = 0
                    else:
                        cls = 1

                    if row[categoryIndex] not in position_stats:
                        position_stats[row[categoryIndex]] = [0,0]

                    stats = position_stats[row[categoryIndex]]
                    stats[cls] = stats[cls] + 1
                    position_stats[row[categoryIndex]] = stats

                split_stats[splitPosition] = position_stats

            for splitPosition in split_stats:
                if measureType == 'gini':
                    measure_value = calculateGini(split_stats[splitPosition])
                    if measure_value < splitAttributeMeasure:
                        splitAttributeMeasure = measure_value
                        splitAttributeIndex = i
                        splitAttributePosition = splitPosition
                else:
                    measure_values = calculateInformationGain(split_stats[splitPosition],parentMeasure)
                    if parentMeasure == 0.0:
                        if measure_values[1] < splitAttributeMeasure:
                            splitAttributeMeasure = measure_values[1]
                            splitAttributeIndex = i
                            splitAttributePosition = splitPosition
                    else:
                        if measure_values[0] > splitAttributeGain:
                            splitAttributeMeasure = measure_values[1]
                            splitAttributeIndex = i
                            splitAttributePosition = splitPosition
                            splitAttributeGain = measure_values[0]

    return [splitAttributeIndex,splitAttributePosition,splitAttributeMeasure]

#create nodes recursively to get full tree
def createTree(dataSet,categoryIndex,skipIndex,measure,parentMeasure):

    node = None

    if checkNodeSplitRequired(dataSet,categoryIndex):

        splitAttribute = getSplitAttribute(dataSet,categoryIndex,skipIndex,measure,parentMeasure)

        if splitAttribute[0] == -1:
            node = TreeNode()
            node.categoryValue = getDataSetCategory(dataSet,categoryIndex)

        else :
            node = TreeNode(splitAttribute[0],splitAttribute[1],splitAttribute[2])

            splitDataSets = splitDataSet(dataSet,splitAttribute[0],splitAttribute[1])
            node.left = createTree(splitDataSets[0],categoryIndex,skipIndex,measure,splitAttribute[2])
            node.right = createTree(splitDataSets[1],categoryIndex,skipIndex,measure,splitAttribute[2])

    else:

        node = TreeNode()
        node.categoryValue = getDataSetCategory(dataSet,categoryIndex)

    return node

#display tree by traversing nodes recursively
def display_tree(node,level):

    tabs = ''
    for i in range(level):
        tabs = tabs + '\t'
    if node.categoryValue != '':
        print(''+tabs+'-> Category Value : '+str(node.categoryValue))
    else:
        print(''+tabs+'-> Split Column : '+str(node.attributeColumn)+' | Split Value : '+str(node.attributeSplitValue)+' | Node Measure : '+str(node.nodeMeasure))
        display_tree(node.left,level+1)
        display_tree(node.right,level+1)

#split train and test data randomly in 1:1 ratio
def splitTrainTestData(dataSet):
    rows = len(dataSet)
    trainDataRows = []
    while float(len(trainDataRows)) < rows/2:
        row = random.randint(0,rows)
        if row not in trainDataRows:
            trainDataRows.append(row)

    trainData = []
    testData = []

    for i in range(rows):
        if i in trainDataRows:
            trainData.append(dataSet[i])
        else:
            testData.append(dataSet[i])

    return(trainData,testData)

#get the category of row by traversing tree and checking conditions of row values
def getRowCategory(node,row):
    categoryValue = ''
    if node.categoryValue != '':
        categoryValue = node.categoryValue
    else:
        if float(row[node.attributeColumn]) <= node.attributeSplitValue:
            categoryValue = getRowCategory(node.left,row)
        else:
            categoryValue = getRowCategory(node.right,row)
    return categoryValue

#test decision tree on test data and calculate accuracy
def checkDecisionTree(node,dataSet,categoryIndex):
    rows = len(dataSet)
    correctPrediction = 0

    for row in dataSet:
        categoryPrediction = getRowCategory(node,row)
        if categoryPrediction == row[categoryIndex]:
            correctPrediction = correctPrediction + 1

    return correctPrediction/rows

def main():
    #Set command line parameter values
    filename = ''
    measure = ''
    categoryIndex = -1
    skipIndex = -1
    displayTree = ''

    cnt = 0
    for p in sys.argv:
        if p == '-m':
            measure = sys.argv[cnt+1]
        elif p == '-i':
            filename = sys.argv[cnt+1]
        elif p == '-c':
            categoryIndex = int(sys.argv[cnt+1])
        elif p == '-s':
            skipIndex = int(sys.argv[cnt+1])
        elif p == '-d':
            displayTree = sys.argv[cnt+1]
        cnt = cnt + 1

    if categoryIndex == -1 or filename == '' or measure == '':
        print('Incorrect Parameters. Try Again.')
        sys.exit()

    dataSet = getDataSet(filename)

    overallTrainAccuracy = 0.0
    overallTestAccuracy = 0.0

    for i in range(1,6):

        randomDataSets = splitTrainTestData(dataSet)

        root_node = createTree(randomDataSets[0],categoryIndex,skipIndex,measure,0.0)

        if displayTree == 'X':
            display_tree(root_node,0)

        print('Case '+str(i))
        trainAccuracy = checkDecisionTree(root_node,randomDataSets[0],categoryIndex)
        print('Training Accuracy : '+str(round(trainAccuracy,3)))

        testAccuracy = checkDecisionTree(root_node,randomDataSets[1],categoryIndex)
        print('Testing Accuracy : '+str(round(testAccuracy,3)))

        overallTrainAccuracy = ((overallTrainAccuracy*(i-1)) + trainAccuracy)/i
        overallTestAccuracy = ((overallTestAccuracy*(i-1)) + testAccuracy)/i

    print('Overall Results:')
    print('Overall Training Accuracy : '+str(round(overallTrainAccuracy,3)))
    print('Overall Testing Accuracy : '+str(round(overallTestAccuracy,3)))

if __name__ == "__main__":
    main()
