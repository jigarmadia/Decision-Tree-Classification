# Decision-Tree-Classification
Implementation of Decision Tree Classification Technique in Python 
Author : Jigar Madia
Date : 02/03/2018


Decision Tree

Program Name : DecisionTree.py

Programming Language : Python 3

Additional Packages : sys, random

Execution Details : This program can be run from command line as below

$ python3 DecisionTree.py -m <measure> -i <inputFile> -c <categoryColumnIndex> -s <skipColumnIndex>

Parameter Descriptions and Values (NOTE : -s IS OPTIONAL. REST MANDATORY):
-m : It specifies which measure is to be used for Decision Tree.
	 Values are { gini, information_gain }

-i : Input data file to be tested upon. File should have comma seperated values and 		 no header details.

-c : It specifies which column is the category column and needs to be targeted.
	 Example : If data has 5 columns (0,1,2,3,4) and last column is supposed to be predicted the parameter value will be 4.

[optional]

-s : It specifies the Identifier column which needs to be skipped.
	 Example : If data has first column as identifier unique for each row, It can be specified with value 0.

Sample command to execute Decision Tree with gini measure, iris dataset which has category column as 4 and no skip idenfier column:

$ python3 DecisionTree.py -m gini -i iris.txt -c 4

Same command for breast cancer dataset will be:

$ python3 DecisionTree.py -m gini -i breast_cancer.txt -c 1 -s 0
