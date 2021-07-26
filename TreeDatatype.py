#Node in python
#https://stackoverflow.com/questions/2358045/how-can-i-implement-a-Node-in-python
#https://www.tutorialspoint.com/python_data_structure/python_binary_Node.htm 

#https://medium.com/swlh/making-data-trees-in-python-3a3ceb050cfd 

import keyword  #used to test for keywords in __repr__ func of Node class
import copy     #used to deepcopy instances

class Node(object):
    "Generic Tree Node class. No infinite lists of children are allowed"
    def __init__(self, name='root', children=[], data=None): #CHILDREN MUST BE LIST (or iterable) 
        self.name = name
        self.data = data
        self.children = [] #different from children

        self.delete = False #used for moving nodes in Tree
        
        for child in children:
            self.add_child(child)

                
    def __str__(self):
        #dict: only give the key, not value
        if type(self.name) == type(dict()):
            try:
                return ' '.join(self.name)
            except TypeError:
                d = [str(i) for i in list(self.name.keys())]
                return ' '.join(d)
        else:
            return self.name

    def __repr__(self):
##        try:
##            #iskeyword_ = keyword.iskeyword(self.data)
##        except TypeError:
##            iskeyword_ = False
        
        #convert all that is str into str format
        reprd = {'name':self.name, 'children':self.children, 'data':self.data}
        for key, attr in reprd.copy().items():
            if isinstance(attr, str):
                reprd[key] = f"'{attr}'"

        #convert dict into usable list
        listdict = [tup for tup in zip(reprd.keys(), reprd.values())]
        #print(f'listdict: {listdict}')
        goodlist = [f"{tup[0]}={tup[1]}" for tup in listdict]
        partstr  = ', '.join(goodlist)

        #convert list into return string
        reprstr  = f"Node(" + partstr + ")"
        return reprstr

        
    
    def __eq__(self, other): #compare instances of this class to "other"
        try:
            return (self.__dict__ == other.__dict__) and (self.__class__ == other.__class__)
        except AttributeError: #no Attributes --> definitely not equal
            return False
    
    def add_child(self, node):
        if isinstance(node, Node):
            node = node
        else:
            node = Node(name=str(node))
        if id(node) == id(self):
            raise TypeError(f"{id(node) = } is the same as {id(self) = }")
        else:
            self.children.append(node)
        return node

        

    def returnCompletename(self):
        " good for looking at names that are dictionaries "
        " However, dictionaries should not be used, key -> self.name; value --> self.data "
        return self.name

    def copy(self):
        import copy
        #deepcopy can usually take care of copying class instances,
        #but since self.children has classes itself, it is very complex,
        #deepcopy breaks down
        #correction using recursion:
        
        if not self.children: #children list is empty
            #l = [i for i in self.__dict__.values() if i != str(i)]
            #print(f'self: {self}, dict:{self.__dict__}, not str list: {l}')
            return copy.deepcopy(self)
                
                

    #children list has nodes
        childrenlist = self.children.copy() #copy of list

            #prepare return deepcopy instance. children must be [] to avoid the problem
        self.children = []  
        returnobj = copy.deepcopy(self)

            #copied, revert children
        self.children = childrenlist.copy() #copy of list
        
        for child in childrenlist:
            returnobj.add_child(child.copy())

        return returnobj 
        
        
        
        
#complex functions: -------------------------------------------------------------------------------------------

#Manipulate Tree with list ------------------------------------------------------------
    def indextree(self, list_, node = None):
        """
        Return a node at the Tree List Value. Zero indexing
        Each value of the list corresponds with the child number
        """
        #eg: [1,2] would give child #2 of child #1 of a node
        if node == None:
            node = self

        try:
            for n in list_:
                node = node.children[n]
        except IndexError:
            nodechildren = [str(node) for node in node.children]
            raise IndexError(f"node.children list: {nodechildren} does not have index {n}. Node that is being searched for index: '{node}'\nOriginal list: {list_}")

        return node

    def insertnode(self, list_, node, startingnode = None):
        "Insert a node at the end point of a list"
        if startingnode == None:
            startingnode = self

        try:
            startnode = startingnode
            for n in list_[:-1]:
                startnode = startnode.children[n]            
        except IndexError:
            print('Original Node of Error:')
            startnode.Render()
            raise IndexError(f"node.children list: {[str(i) for i in startnode.children]} does not have index {str(n)}. ")

        try: 
            startnode.children.insert(list_[-1], node)
        except IndexError:
            print('Original Node of Error:')
            startnode.Render()
            raise IndexError(f"Node does not have proper indexing {list_[-1]}. \
                                Node children: {[str(i) for i in startnode.children]}")
            
        return node

    def deletenode(self, list_, startingnode = None):
        "Delete a node at the end point of a list"
        if startingnode == None:
            startingnode = self

        try:
            node = startingnode
            for n in list_[:-1]:
                node = node.children[n]            
        except IndexError:
            node.Render()
            raise IndexError(f"node.children list: {node.children} does not have index {n}. Original Node: {node}, render above")

        try: 
            del node.children[list_[-1]]
        except IndexError:
            node.Render()
            raise IndexError(f"Node {node} does not have proper indexing {list_[-1]}. Node children: {node.children}, render above")
        except TypeError:
            raise TypeError(f"{list_[-1] = }; {list_ = } \
                            list indices must be integers or slices, not list")
        return None


    
#Iterations over all children levels of node------------------------------------
    def generate_allchildren(self, node = None, recursionli = None):
        "Generate all children levels of Node"
        #recursive generator function: https://realpython.com/introduction-to-python-generators/

        if node == None:
            node = self

        if recursionli == None: #used to create position list of node
            recursionli = [0]

        for child in node.children:
            yield child, recursionli.copy() #no .copy for recursionli makes list comprehension on this func not work 
            #print(recursionli)
            if child.children:
                
                recursionli.append(0)
                yield from child.generate_allchildren(recursionli = recursionli.copy())

                recursionli = recursionli[:-1]

            recursionli[-1]+=1

        
    def findnode_bynode(self,node):
        returnnodeli = []
        for n, path in self.generate_allchildren():
            if n == node:
                returnnodeli.append([n, path])

        return returnnodeli
    
#todo: change these functions so that they use the generator function? Simpler to read
#find value (name or data, dictated by "find") in all tree of node, :
    def findnode_byvalue(self, value, find='name', node = None, indexval_li = []):
        "Find a value in ALL nodes of node Tree\nReturn {node name: [Node obj, Relativepath_list]"
        #recursive
        
        if node == None:
            node = self


        def ismatch(node, value, find = find):
            nodeval = exec(f"node.{find}")
            if str(node.name) == str(value):
                return True
            else:
                return False



        return_dict = {}

        #make sure indexval_li makes sense
        if node.children == []:
            return
        
        tempn = -1
        for child in node.children:
            tempn+=1
            indexval_li.append(tempn)
##            print(f'''    Bool: {ismatch(child, value)}, child: {child}, return_dict = {return_dict}
##data_: {child.data}
##value: {value}
##N: {tempn}; indexval: {indexval_li}
##
##''')            
            if child.children: #children list (of child) is not empty
                
                #check if node (has children) itself is a match
                if ismatch(child, value):
                    return_dict = {**return_dict, str(child):[child, indexval_li.copy()]}
                    #print(f'ismatch: d: {return_dict}, child: {child}, value: {value}')

                #recursively look for values in children
                foundval = child.findnode_byvalue(value = value, find = find, indexval_li = indexval_li)
                if foundval: #not None
                    return_dict = {**return_dict, **foundval}
                
            else:
                if ismatch(child, value):
                    return_dict = {**return_dict, str(child):[child, indexval_li.copy()]}

            del indexval_li[-1]


            
        if return_dict: #return_dict not empty
            return return_dict
        else:
            return
        

    def movenode(self, orignodepos, newnodepos):
        """Move a node from one position to another. "=

        Not limited to the same leaf levels
        Don't have to worry about insertion issues;
           Insertion will push nodes forwards

        process: (move original node (keep id); copying)
        1) find node at orignodepos (not needed, see step 5)
        2) create copy
            3) set copy: self.delete = True
            4) delete original node
            5) insert copy node into original node pos (to push everything back into regular position)
            #these indented processes are required to keep id the same for moved node
        6) Insert original node to new node pos
        7) Delete all that have self.delete = True
        
        """
        #move node:
            #note: Do account for moving nodes:
                #case 1: Newnodepos is not moved
                #case 2: Newnodepos loc is moved back because old node deletion was before on the node list ([1,2,3] --> [1,3]), 3 moved up
            #this is all avoided via self.delete
                #checks
        
        if not isinstance(orignodepos, list):
            s = f"orignodepos: {orignodepos} is not a list. It is a {type(orignodepos)}"
            raise TypeError(s)
        if not isinstance(newnodepos, list):
            s = f"newnodepos: {newnodepos} is not a list. It is a {type(newnodepos)}"
            raise TypeError(s)


    #find node
        moveNode = self.indextree(orignodepos)

    #create copy of node
        copyNode = moveNode.copy() #method defined above
    #set copy delete val
        copyNode.delete = True
        

    #delete original node
        self.deletenode(orignodepos)

    #insert copy node
        self.insertnode(list_ = orignodepos, node = copyNode)

    #insert original node to new node pos
        self.insertnode(list_ = newnodepos, node = moveNode)


    #delete all nodes with "self.delete = True"
        self.node_deleteTrue()
        
    def node_deleteTrue(self):
        "recursively delete all Child Nodes with self.delete = True"

        indexnum = 0
        childlist = self.children.copy() #must have a copy to not change the iterating list: https://stackoverflow.com/questions/6260089/strange-result-when-removing-item-from-a-list-while-iterating-over-it
        
        for child in self.children: #if self.children = [], then this is skipped (no worries)
            #print(f'child: {child}, del val: {child.delete}')
            if child.delete == True: #check child.delete
                del childlist[indexnum]
            indexnum+=1
            
            if child.children: #recursion if children list is not empty
                child.node_deleteTrue()

        self.children = childlist
                
            
        
            

        
#render function --------------------------------------------------------------------------------------------------------
    def Render(self, displayval = 'name', lastleaflist = None): #printChildNodes
        """
recursive, each loop checks if parent is last node in branch and prints the leaf"
        lastleaflist and Returned Value are not useful,
        they are used to exchange information
        (lists that tell if previous nodes were last) between recursions.
        
        displayval will display node.{displayval} in tree
        """

            #is children list bad; Recursive function only applies when child Nodes have their own children,
            #this is only for the root Node
                #(note: use value of index instead of Node because there can be identical nodes
        lastindex = len(self.children) -1
        if lastindex <= -1: #self.children is empty
            print(f"{self.name}'s children is empty, index of last value: {lastindex}")
            print(self.name)
            return None

        if lastleaflist is None: #loop one
            lastleaflist = [None]
            print(self.name)


            
        #print(f'start: {lastleaflist}')
        #connectors
        none_str = '    '
        con_none = '│   '
        con_more = '├── '
        con_one  = '└── '
        
        indentval = 3

        #Make connecter branches via list

        def formatstr(child):
            #print(lastleaflist)
                    #lastleaflist:
                #not last values:
            #True = Connector
            #False = No connector
                #last value in list:
            #True = Is last value
            #False = Not last value
            
                #get "tails" of list / specific leaf
            retl = []
            for b in lastleaflist[:-1]: retl.append(none_str) if b else retl.append(con_none)

                #"head" of list / specific leaf
            retl.append(con_one) if lastleaflist[-1] else retl.append(con_more)

            #print(''.join(retl))
            try:
                disval = str(eval(f"child.{displayval}"))
            except NameError:
                #raise NameError(f"child.{displayval} does not exist. ")
                disval = f'Attribute does not exist: {displayval}'
            except KeyError:
                disval = f'Dict Key does not exist: {displayval}'

            returnval = ''.join(retl) + disval


            if len(returnval) >= 100: #obnoxiously long, display will be bad
                returnval = returnval[:90] + ' ...'
            return returnval


        curr_indexval = -1
        
        for child in self.children:

            #gets the list
            #print(f'bool make: c: {child}, last: {lastval}, {child == lastval}')
            #print(type(child), id(child), type(lastval), id(lastval))
            #print(lastleaflist)
            curr_indexval+=1
            if curr_indexval == lastindex:
                lastleaflist[-1] = True
            else:
                lastleaflist[-1] = False

            #print(f"child: {child}; lastleaflist: {lastleaflist}")
            if child.children: #Node's child's childrenlist is not empty
                #print(f'{child} has children {child.children}')
                print(formatstr(child))

##                if str(self.name) == str(lastval): #is the parent the last one?
##                    lastleaflist.append(False)
##                else:
##                    lastleaflist.append(True)
                lastleaflist.append(lastleaflist[-1])
                lastleaflist = child.Render(lastleaflist = lastleaflist, displayval=displayval) #passes mutable parameter on, recursive part
                
            else:
                #print(f"leaf: {child}, oldtreedict: {Tree_dict}")
                print(formatstr(child))

        lastleaflist = lastleaflist[:-1]
        return lastleaflist #return list so it is given from Child to Parent (recursions)  





#convert to Dictionary and Back --------------------------------------------------------------------------------
    def TreetoDict(self,Tree_dict = None): #None to avoid annoying mutable value rememberance from last run
        " recursive func to get dict of child nodes "
        if Tree_dict == None:
            Tree_dict = {}
        
        for child in self.children:
            if child.children: #not empty
                #print(f"grand: {self}, parent node: {child}, childlist: {child.children}")
                Tree_dict[str(child)] = child.TreetoDict(Tree_dict = {}) #argument is mutable, must re input
            else:
                Tree_dict[str(child)] = {}
                #print(f"leaf: {child}, oldtreedict: {Tree_dict}")

        #print(f'return Tree dict: {Tree_dict}')
        return Tree_dict

    def DicttoTree(self, dict_ = None, node = None):
        " recursive func to turn dict into tree-struct"
        if dict_ == None:
            dict_ = {}
        if node == None:
            node = Node(name='root')
            
        #print(con_more, con_one, indentval, iternum)
        for key, value in dict_.items():
            key = str(key)
            #print(f'Key: {key}; Value: {value}')
            if value or type(value) != type(dict()): #not empty or not dict
                #rstr += ' '*(indentval*iternum) + con_more+key.name + '\n'
                parent_node = Node(key) #must create a node because function is method of class
                                          #also use for parent of 
                parent_node.DicttoTree(dict_=value, node = parent_node) 
                #print(f'children_nodes: {parent_node}, {parent_node.children}')
                node.add_child(parent_node) #Node(name=key, children = children_nodes))
                
            else:
                #print(f'add child: {key}')
                node.add_child(Node(name=key))
    
        return node

#actual way to save nodes:
    def saveNode(self, saveloc):
        "save the Tree via Pickle at save location (path"
        import pickle

        with open(saveloc, "wb" ) as f: #with takes care of opening / closing
            pickle.dump(self, f)

        return

    def retrieveNode(self, saveloc):
        "Retrive saved Tree via Pickle at save location (path)"
        import pickle

        try:
            with open(saveloc, "rb" ) as f: #with takes care of opening / closing
                returnself = pickle.load(f)
        except FileNotFoundError:
            with open(saveloc, "wb") as f:
                pickle.dump(Node(), f)
                return Node()
        return returnself

#    *
#   /|\
#  1 2 +
#     / \
#    3   4
##
##├-- 1
##├-- 2
##├-- +
##    ├-- 3
##    └── 4
##        ├-- 4a
##        └── 4b
##├-- 4
##└── 5

if __name__ == "__main__":
    
    t1 = Node('a', [Node('1'),
                    Node('b'),
                    Node('2')
                         ]
             )
    
    t2 = Node('*', [Node('1'),
                   Node('2'),
                   Node('+', [Node('3'),
                              Node('4')]
                        ),
                   Node('4'),
                   Node('5')]
             )
    
    t3 = Node(name='*', children=[Node(name='1', children=[], data='data1'),
                                Node(name='2', children=[], data='data2'),
                                Node(name='+', children=[Node(name='4a', children=[], data='data4a1'),
                                                         Node(name='3', children=[], data='data3.1'),
                                                         Node(name='4', children=[Node(name='4a', children=[], data=None),
                                                                                  Node(name='4b', children=[], data=None)],
                                                              data=None)], data=None),
                                Node(name='4', children=[], data=None),
                                Node(name='5', children=[], data=None)],
            data=None)


    t4 = Node(name='*',
                    children=[Node(name='1', children=[], data='data1'),
                              Node(name='2', children=[], data='data2'),
                              Node(name='+', children=[Node(name='4a', children=[], data='data4a1'),
                                                       Node(name='3', children=[], data='data3.1'),
                                                       Node(name='4', children=[Node(name='4a', children=[], data=None),
                                                                                Node(name='4b', children=[], data=None)],
                                                            data=None)], data=None),
                              Node(name='4', children=[Node(name='4- 1 child',
                                                            children=[Node(name='4child, child', children=[], data=None)],
                                                            data=None)], data=None), Node(name='5', children=[], data=None),
                              Node(name='+', children=[Node(name='4a', children=[], data='data4a1'),
                                                       Node(name='3', children=[], data='data3.1'),
                                                       Node(name='4', children=[Node(name='4a', children=[], data=None),
                                                                                Node(name='4b', children=[], data=None)],
                                                            data=None)],
                                   data=None)],
                    data=None)
    
##    print('one layer tree: ')
##    t1.Render()
##
##    print('two layer tree:')
##    t2.Render()
##    
##    print('three layer tree: ')
##    t3.Render()
##
    print('most complex tree: ')
    t4.Render()

    m = t1.generate_allchildren()

    



