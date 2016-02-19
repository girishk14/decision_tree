#This module contains routines for pruning the decision tree

import sys
import os
import math
import decision_tree
import classification

def collect_nodes(root, nodestack, leafstack):
	
	if root.isLeaf == True:
		leafstack.append(root)
	else:
		nodestack.append(root)
		for child in root.children:
			collect_nodes(child, nodestack, leafstack)





def reduced_error_pruning(d_tree, dataset, labels,  X_valid, Y_valid): 


	#This module implements reduced error pruning and returns a tree with some of the subtree replaces by a majoirity classifer
#Here, dataset and labels are the training set that this tree was trained on

	
	while True:
		print("Pruning Iteration")
		pre_error = 1 -  classification.get_classification_error(d_tree, dataset, labels, X_valid, Y_valid)
		nodestack = [] 
		leafstack = []
		collect_nodes(d_tree, nodestack, leafstack)

		
		prune_me = None
		max_error_red = 0
		
		for node in nodestack:
			node.leafify(dataset, labels)
			post_error = 1- classification.get_classification_error(d_tree, dataset, labels, X_valid, Y_valid)			
			error_reduction = pre_error - post_error
			print("Pre-Error :", pre_error, "Post-Error", post_error,"Error Reduction", error_reduction)			
			if error_reduction > max_error_red:	
				max_error_red = error_reduction
				prune_me = node
			node.unleafify()

		
		for leaf in leafstack:
			if len(leaf.children) > 0:
				node.unleafify()
				post_error = 1- classification.get_classification_error(d_tree, dataset, labels, X_valid, Y_valid)			
				error_reduction = pre_error - post_error
				print("Pre-Error :", pre_error, "Post-Error", post_error,"Error Reduction", error_reduction)			
				if error_reduction > max_error_red:	
					max_error_red = error_reduction
					prune_me = node
				node.leafify()

				
				


		if max_error_red <= 0:
			return d_tree				
			
		print("Error Reduction : ", max_error_
		if prune_me.isLeaf:
			prune_me.unleafify()
		else:
			prune_me.leafify(dataset, labels)

			
						
						

