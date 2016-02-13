__author__ = 'Girish'
import os
import sys
from copy import deepcopy
import math
import json



global metadata
'''
Design of MetaData File:

1. Whether each attribute is discrete or continuous (to decide branching)
2. Statistic of each attribute domain (if required)


'''

class node:
    def __init__(self, attr, split_point, children=list()):
        self.children = children;
        self.criteria = {"attr": attr, "split_point":split_point}
        self.class_distr = None
        self.class_label = None


    def set_class_label(self,l):
        self.class_label = l


def load_metadata(filename):
    global metadata
    metadata = json.loads(filename)



def create_decision_tree(dataset, labels):
     #Root Node has no split point or attribute
    attr_count = metadata['attr_count']
    attr_list = set(range(0, attr_count))
    generate_subtree(dataset, labels, attr_list )



def generate_subtree(dataset, labels, partition, attr_list, split_pt=None, subpart=None):
    #Stop building the subtree of there are no attributes left or if all the members are in the same class
    if len(set([labels[instance] for instance in partition]))==1: #There is only class of examples left
        root =  node(None, None, partition);
        root.set_class_label(labels[partition[0]])

    elif len(attr_list)==0:
        maj_label = get_class_majority(dataset, labels, partition)
        root = node(None, None, partition, None);
        root.set_class_label(maj_label)

    else:
        best_attr, split_pt, new_parititons = get_splitting_criteria(partition, labels, attr_list)
        #Here we distinguish between discrete and continuous
        root = node(best_attr, split_pt, subpart);

        if(split_pt==None): #A discrete attribute has been chosen to split!
            attr_domain = set([dataset[instance][best_attr] for instance in partition])
            attr_list.remove(best_attr)
            for x in attr_domain: #Create the new children by partitioning this attribute
                subpart = [instance for instance in partition if dataset[instance][best_attr]==x]
                root.children.append(generate_subtree(dataset, labels, subpart,attr_list, x, attr_list))

        else: #Continuos attribute, so binary branching
            l,r = [], []
            attr_list.remove(best_attr);
            for instance in partition:
                l.append(instance) if dataset[instance][best_attr]<split_pt else r.append(instance)
            root.children.append(generate_subtree(dataset, labels, l,attr_list, split_pt, attr_list))
            root.children.append(generate_subtree(dataset, labels, r,attr_list, split_pt, attr_list))

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

        if metadata['attributes'][attribute] == 'd':
            info, split_pt = find_entropy_discrete(dataset, labels, partition, attribute)

        else:
            info, split_pt = find_entropy_continuous(dataset, labels, partition, attribute)

        if (S - info) > best_gain:
            best_attr = attribute
            best_gain = (S - info)
            best_split_pt = split_pt

    return best_attr, best_split_pt

def find_entropy_continuous(dataset, labels, partition, attribute):
    E = 0
    attr_domain =  set([dataset[instance][attribute] for instance in partition])
    split_pt = None
    min_E =  sys.maxint
    sorted_domain =  sorted(attr_domain)

    for x in range(0, len(sorted_domain)-1):
        mid = (sorted_domain[x] + sorted_domain[x+1])/2
        l,r = [], []
        for instance in partition:
            l.append(instance) if dataset[instance][attribute]<mid else r.append(instance)
        E = compute_entropy(dataset, labels, l) + compute_entropy(dataset, labels, r)
        if(E<min_E):
            min_E = E
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
    for l in subpart.keys():
        pi = count[l]/len(subpart)
        e = e - (pi * math.log(pi, 2))
    return e




def prune_tree:
    #Fill in this code later, simply because error measurement isn't clear!


def classify(root, tuple):
