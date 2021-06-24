#Node in python
#https://stackoverflow.com/questions/2358045/how-can-i-implement-a-Node-in-python
#https://www.tutorialspoint.com/python_data_structure/python_binary_Node.htm 

#https://medium.com/swlh/making-data-trees-in-python-3a3ceb050cfd 

class Node(object):
    "Generic Tree Node class. "
    def __init__(self, name='root', children=None): #CHILDREN MUST BE LIST (or iterable) 
        self.name = name
        self.children = [] #different from children
        
        if children is not None:
            for child in children:
                self.add_child(child)
                
    def __repr__(self):
        return self.name
    
    def add_child(self, node):
        if isinstance(node, Node):
            self.children.append(node)
        else:
            self.children.append(Node(name=str(node)))






#render functions
#todo:
#fancy: Add line to connect branches, even if there is(are) child node(s)
    def Render(self, lastleaflist = None): #printChildNodes
        "recursive, each loop checks if parent is last node in branch and prints the leaf"

        if lastleaflist is None:
            lastleaflist = [None]
            print(self.name)
            
        #print(f'start: {lastleaflist}')
        #connectors
        none_str = '    '
        
        con_none = '│   '
        
        con_more = '├── '
        
        con_one  = '└── '
        
        indentval = 3

        try:
            lastval = self.children[-1]
        except IndexError: #self.children is empty
            print(f'IndexError, self.children is empty')
            print(self.name)
            return 
            

        #Make connecter branches via list

        def formatstr(enterval):
            #get "tails" of list / specific leaf
            retl = []
            for b in lastleaflist[:-1]: retl.append(none_str) if b else retl.append(con_none)

            #"head" of list / specific leaf
            retl.append(con_one) if lastleaflist[-1] else retl.append(con_more)

            #print(''.join(retl))
            return ''.join(retl) + child.name

        for child in self.children:

            #gets the list
            #print(f'bool make: c: {child}, last: {lastval}, {child == lastval}')
            if child == lastval:
                lastleaflist[-1] = True
            else:
                lastleaflist[-1] = False

            #print(f"child: {child}; lastleaflist: {lastleaflist}")
            if child.children: #not empty
                print(formatstr(child))

                if str(self.name) == str(lastval): #is the parent the last one?
                    lastleaflist.append(False)
                else:
                    lastleaflist.append(True)
                lastleaflist = child.Render(lastleaflist = lastleaflist) #passes mutable parameter on, recursive part
                
            else:
                #print(f"leaf: {child}, oldtreedict: {Tree_dict}")
                print(formatstr(child))

        lastleaflist = lastleaflist[:-1]
        return lastleaflist #return list so it is given from Child to Parent (recursions)  





        
    def TreeintoDict(self,Tree_dict = None): #None to avoid annoying mutable value rememberance from last run
        " recursive func to get dict of child nodes "
        if Tree_dict == None:
            Tree_dict = {}
        
        for child in self.children:
            if child.children: #not empty
                #print(f"parent node: {child}")
                Tree_dict[child] = child.TreeintoDict(Tree_dict = {}) #argument is mutable, must re input
            else:
                Tree_dict[child] = {}
                #print(f"leaf: {child}, oldtreedict: {Tree_dict}")

        #print(f'return Tree dict: {Tree_dict}')
        return Tree_dict

    def dictintoTree(self, dict_ = None, node = None):
        " recursive func to turn dict into tree-struct"
        if dict_ == None:
            dict_ = {}
        if node == None:
            node = Node(name='root')
            
        #print(con_more, con_one, indentval, iternum)
        for key, value in dict_.items():
            key = str(key)
            #print(f'Key: {key}; Value: {value}')
            if value: #not empty
                #rstr += ' '*(indentval*iternum) + con_more+key.name + '\n'
                parent_node = Node(key) #must create a node because function is method of class
                                          #also use for parent of 
                parent_node.dictintoTree(dict_=value, node = parent_node) 
                #print(f'children_nodes: {parent_node}, {parent_node.children}')
                node.add_child(parent_node) #Node(name=key, children = children_nodes))
                
            else:
                #print(f'add child: {key}')
                node.add_child(Node(name=key))
    
        return node
                

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
    t = Node('*', [Node('1'),
                   Node('2'),
                   Node('+', [Node('3'),
                              Node('4', [Node('4a'), Node('4b')])]
                        ),
                   Node('4'),
                   Node('5')]
             )



    simplet = Node('a', [Node('1'),
                   Node('2'),
                   Node('b', [Node('last')])
                         ]
             )
    print('simple t: ')
    simplet.Render()

    print('complex t: ')
    t.Render()



