#This module contains routines for pruning the decision tree

import sys
import os
import math


def get_classificaton_error(tree,  seen_dataset, seen_labels, unseen_labels)
	count = 0
	for i in range(0, len(unseen_dataset)):
        	if classify_tuple(d_tree, seen_dataset, seen_labels, unseen_dataset[i]) == Y_test[i]:
	        count+=1


return (count/float(len(unseen_dataset)))





def classify_tuple(root, dataset, labels, test_tuple): #Given the root of a decsion tree, and a new tuple, return its class
    #print(tuple)
    #print(root)
    trav = root
    while(trav.isLeaf is not True):
		curr_attr = trav.criteria['next_split_attr'] 
                if metadata['attr_types'][curr_attr] == 'c':
		    if test_tuple[curr_attr] < trav.children[0].criteria['parent_split_point']:
			trav = trav.children[0]
		    else:
		        trav = trav.children[1]

		
		else:
 		    flag = 0
		    for child in trav.children:
			if child.criteria['parent_split_point'] == test_tuple[curr_attr]:
			    trav = child
                            flag = 1

                    if flag==0: #If there is no way to classify this tuple in the tree;wq
			print("No confidence to classify this")
	                guess =  get_class_majority(dataset, labels, trav.partition)
			return guess
    return trav.class_label

