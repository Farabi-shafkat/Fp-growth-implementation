#Md Shafkat Rahman Farabi
#160041002 
#task 3


import numpy as np
import os
import argparse as arg
import time

class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None
        self.parent = parentNode    
        self.children = {} 
  
    def inc(self, numOccur):
        self.count += numOccur
       
    def disp(self, ind=1):
        print ('  '*ind, self.name, ' ', self.count)
        for child in self.children.values():
            child.disp(ind+1)
     
    
    
def update_header_table(node,table):
    cur = table[node.name][1]
 
    if cur==node:
        return 
    while cur.nodeLink!=None:
        if cur.nodeLink==node:
            return 
       
        cur=cur.nodeLink
    cur.nodeLink = node
    return 
    
def fp_tree(data,min_sup):
    freq={}
    for row in data:
        for item in row:
            if item in freq:
                freq[item]+=1
            else:
                freq[item]=0
    freq=list(freq.items())
    freq= sorted(freq, key=lambda x: (-1*x[1],x[0]))
    freq={x[0]:x[1] for x in freq}
  
    def comp(itm):
        return freq[itm]
    for row in data:
        row=[x  for x in row if freq[x]>=min_sup]

    header_table=freq

    
    for k in header_table:
        header_table[k]=[header_table[k],None]
 
    count=0
    rootNode=treeNode("root",1,None)
    for row in data:

        count+=1
        #if count % 100 ==0:
         #   print('-',end =" ")
        curNode=rootNode
      
        for item in row:
            if item in (curNode.children.keys()):
                curNode=curNode.children[item]
            else: 
                curNode.children[item]=treeNode(item,0,curNode)
                curNode=curNode.children[item]
            curNode.inc(1) 
      
            if header_table[curNode.name][1] is None:
                header_table[curNode.name][1]=curNode
            else :
                update_header_table(curNode,header_table)
                   

    return rootNode,header_table
                
                
                
                

def ascendTree(treeNode,path):
    path.append(treeNode.name)
    ret=0
    if treeNode.parent.name!='root':
        ascendTree(treeNode.parent,path)
    return 



def find_prefix_path(treeNode):
    condPat={}
    name=treeNode.name

    while treeNode!=None:
       
        path=[]
        ascendTree(treeNode,path)
  
        if len(path) > 1 :
            condPat[tuple(path[1:])]=treeNode.count
        treeNode=treeNode.nodeLink
    return condPat
    
    

def main(input_name,min_sup,output_name):
    print("Taking input from ",input_name)
    data_lst = np.loadtxt(fname=input_name,usecols=0,delimiter='\n',dtype='str')
    data = []
    for string in data_lst:
        dt = string.split()
        dt = [int(x) for x in dt]
     
        data.append(dt)
    print("Creating FP-Tree, this might take a while.......")
    rootNode,header_table=fp_tree(data,min_sup)
    print('\n')
    print("fp tree generated")
    print('creating frequent pattern base.........')
  
    frqPatBase={}
    for item in header_table.keys():
        
        condPatBase=find_prefix_path(header_table[item][1])
 
        data= []
        for pat in condPatBase.keys():
            pat_list=list(pat)
            for i in range(condPatBase[pat]):

                data.append(pat_list)
    
        frqPatBase[item]=[]

        condRootNode,condHeader_table=fp_tree(data,min_sup)
        for condItem in condHeader_table.keys():
            if condHeader_table[condItem][0]<min_sup:
                continue
            condCondPatBase=find_prefix_path(condHeader_table[condItem][1])
            for x in condCondPatBase.keys():
                frqPat=[item,condItem]

                for y in list(x):
                    frqPat.append(y)
                frqPat=(frqPat,condCondPatBase[x])
        
            if frqPat[1]>=min_sup:
                frqPatBase[item].append(frqPat)
    print('Frequent Patter Base Generated')
    return frqPatBase

        

if __name__=='__main__':
    start_time = time.time()
    parser = arg.ArgumentParser()
    parser.add_argument("input",help='input file name',type=str)
    parser.add_argument("min_sup",help='minimum support count',type=int)
    parser.add_argument("output",help='output file name',type=str)
   
    args=parser.parse_args()
    input_file=args.input
    output_file=args.output
    min_sup=args.min_sup

    print('minimum support count set to ',min_sup)
    frqPatBase=main(input_file,min_sup,output_file)
    print('saving frequent itemsets in ',output_file)
    output_name=output_file
    f = open(output_name, "w")
    frqPatBaseList=frqPatBase.values()
    out=' '
    number= 0
    for pat in frqPatBase.values():
    
        if len(pat)==0:
            continue
        pat=pat[0]
        for el in pat[0]:

            out = out+str(el)+' '
  
        out= out+' ('+str(pat[1])+') \n'
        number+=1
    f.write(out)
    f.close()
    print("DONE!!!!!!!!!!!!!")
    print("number of frequent itemset: ",number)
    tm =(time.time() - start_time)
    print("Execution Time:--- %s minutes %s seconds ---" %((tm//60),(tm%60)))