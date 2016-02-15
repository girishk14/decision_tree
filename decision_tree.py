__author__ = 'Girish'
import os
import sys
from copy import deepcopy
import math
import json
import random
import preprocess


global metadata
'''
Design of MetaData File:

1. Whether each attribute is discrete or continuous (to decide branching)
2. Statistic of each attribute domain (if required)


'''

class node:
    def __init__(self, attr, split_point, partition):
        self.children = []
        self.criteria = {"attr": attr, "split_point":split_point}
        self.partition = partition
        self.class_distr = None
        self.class_label = None


    def set_class_label(self,l):
        self.class_label = l

    def print_node(self):
        print(self.criteria)
        print(self.children)
        print(self.partition)
        print(self.class_label)
	print("\n")
def load_metadata(meta):
    global metadata
    metadata = meta



def create_decision_tree(dataset, labels):
     #Root Node has no split point or attribute
    global metadata 
    attr_count = len(metadata['attr_types'])
    attr_list = set(range(0, attr_count))
    #print(attr_list)
    return generate_subtree(dataset, labels, range(0, len(dataset)),  attr_list )
    
	


def generate_subtree(dataset, labels, partition, attr_list, parent_split_pt=None,depth = 0):
    #Stop building the subtree of there are no attributes left or if all the members are in the same class
    if len(set([labels[instance] for instance in partition]))==1: #There is only class of examples left
        root =  node(None, parent_split_pt, partition)
	#print(attr_list)
#	print(labels[partition[0]], "is the only class left")
        root.set_class_label(labels[partition[0]])

    elif len(attr_list)==0:
        maj_label = get_class_majority(dataset, labels, partition)
        root = node(None, parent_split_pt, partition)
  #     print(attr_list)
#	print("No attributes left, hence assigning majority class", maj_label)
        root.set_class_label(maj_label)
 
    else: 
        best_attr, split_pt = get_splitting_criteria(dataset,  labels, partition, attr_list)
        #Here we distinguish between discrete and continuous
#	print(attr_list)
 #       print(best_attr, split_pt, parent_split_pt) 
	root = node(best_attr, parent_split_pt, partition);
        if(split_pt==None): #A discrete attribute has been chosen to split!
            attr_domain = set([dataset[instance][best_attr] for instance in partition])
            attr_list.remove(best_attr)		
            for x in attr_domain: #Create the new children by partitioning this attribute
                subpart = [instance for instance in partition if dataset[instance][best_attr]==x]
                root.children.append(generate_subtree(dataset, labels, subpart,attr_list, x))

        else: #Continuos attribute, so binary branching
            l,r = [], []
            attr_list.remove(best_attr);
            for instance in partition:
                l.append(instance) if dataset[instance][best_attr]<split_pt else r.append(instance)

	   # print([dataset[x][best_attr] for x in range(0, len(dataset))if x in l])
            #print("\n")
	    #print([dataset[x][best_attr] for x in range(0, len(dataset)) if x in d_treplit_
            root.children.append(generate_subtree(dataset, labels, l,deepcopy(attr_list), split_pt,'l'))
            root.children.append(generate_subtree(dataset, labels, r,deepcopy(attr_list), split_pt, 'r'))
    #print(depth)
    #print(attr_list)
    #root.print_node() 

   
  
    return root


def get_class_majority(dataset, labels, partition):
    lst  = [labels[instance] for instance in partition]
    return max(set(lst), key=lst.count)

def get_splitting_criteria(dataset, labels, partition, attr_list):
    S = compute_entropy(dataset, labels, partition);
    best_attr = -1
    best_gain = -1
    best_split_pt = None
    for attribute in attr_list:
        info = 0;
        split_pt = None

        if metadata['attr_types'][attribute] == 'd':
            info, split_pt = find_entropy_discrete(dataset, labels, partition, attribute)

        else:
            info, split_pt = find_entropy_continuous(dataset, labels, partition, attribute)

        if (S - info) > best_gain:
            best_attr = attribute
            best_gain = (S - info)
            best_split_pt = split_pt

    return best_attr, best_split_pt

def find_entropy_continuous(dataset, labels, partition, attribute):
    #print("Find entropy")
    E = 0
    attr_domain =  set([dataset[instance][attribute] for instance in partition])
    split_pt = None
    min_E =  sys.maxint
    sorted_domain =  sorted(attr_domain)
 #   print(sorted_domain)
    for x in range(0, len(sorted_domain)-1):
        mid = (sorted_domain[x] + sorted_domain[x+1])/2
        l,r = [], []
        for instance in partition:
            l.append(instance) if dataset[instance][attribute]<mid else r.append(instance)
        lweight  = float(len(l))/float(len(partition))
        rweight = float(len(r))/float(len(partition))
	#print(lweight, rweight)
        E = lweight  * compute_entropy(dataset, labels, l) + rweight*compute_entropy(dataset, labels, r)
        if(E<min_E):
            min_E = E
#	    print("min_E changign to ", E)
            split_pt = mid

    return min_E, split_pt





def find_entropy_discrete(dataset, labels, partition, attribute):
    E = 0
    attr_domain =  set([dataset[instance][attribute] for instance in partition])
    for x in attr_domain: #For each possible attribute value
        subpart = [instance for instance in partition if dataset[instance][attribute]==x]
        #Add the weighted entropy of every subpartiton
        E  = E +  (len(instance)/len(partition)) * compute_entropy(dataset, labels, subpart)

    return E, None


def compute_entropy(dataset, labels, subpart):
    count = {}
         
  
    for i in subpart:
        if labels[i] not in count.keys():
            count[labels[i]] = 1
        else:
            count[labels[i]]+=1

    e = 0	
  
    for l in count.keys():
        pi = count[l]/float(len(subpart))
	#print(pi)
        e = e - (pi * math.log(pi, 2))
    return e




def prune_tree():
	pass#Fill in this code later, simply because error measurement isn't clear!


def classify_tuple(root, test_tuple): #Given the root of a decsion tree, and a new tuple, return its class
    #print(tuple)
    #print(root)
    trav = root
    while(len(trav.children)>0):
		curr_attr = trav.criteria['attr'] 
                if metadata['attr_types'][curr_attr] == 'c':
		    if test_tuple[curr_attr] < trav.children[0].criteria['split_point']:
			trav = trav.children[0]
		    else:
		        trav = trav.children[1]


    return trav.class_label


def shuffle_order(a, b):	
	c = list(zip(a, b))
	random.shuffle(c)
	a, b = zip(*c)
	return a,b



def classic_hold_out(dataset, labels):
    no_train = int(0.7 * len(dataset))
    training_X =  dataset[0:no_train]
    training_Y = labels[0:no_train]
	
    test_X = dataset[no_train:]
    test_Y = labels[no_train:]

    d_tree  = create_decision_tree(training_X, training_Y)
    
    count = 0
    for i in range(0, len(test_X)):
	if classify_tuple(d_tree, test_X[i]) == test_Y[i]:
		count+=1
    
    print("Accuracy  on test set = ",  count/float(len(test_X)))
    
def main():
    preprocess.make_control_files()
    ctrl_file = sys.argv[1] 
    dataset, labels, meta = preprocess.pre_process(ctrl_file);
    load_metadata(meta)  #Sets the global metadata information
    dataset, labels = shuffle_order(dataset, labels)
    classic_hold_out(dataset, labels)

	


if __name__ == "__main__":
	main()
