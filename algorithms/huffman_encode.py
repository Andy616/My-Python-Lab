class _Node():
    
    def __init__(self, Lchild, Rchild):
        self.Lchild = Lchild
        self.Rchild = Rchild
        self.weight = Lchild.weight + Rchild.weight    
        self.code = ''
        

class _Leaf():
    
    def __init__(self, data, weight):
        self.weight = weight
        self.data = data
        self.code = None

        
class encode():
    '''Encode the input string to binary data.
    Usage:
        Encode:
        >>> huff = encode(String)
        >>> encoded_string = huff.encoded_text
        >>> decode_key = huff.decode_key
        Decode:
        >>> decode(decode_key, encoded_string)
        '''
    def __init__(self, text):
        self.__leaf = []
        self.__node = []
        self.__word_count(text)
        self.__init_leaf()
        self.__grow()        
        self.__encode(text)
    
    def __word_count(self, text):        
        word_count_dict = dict()
        for i in text:
            if i in word_count_dict:
                word_count_dict[i] += 1
            else:
                word_count_dict[i] = 1                
        self.word_frequency =  sorted(list((word_count_dict.items())), key=lambda x: x[1])
                    
    def __init_leaf(self):
        for i in self.word_frequency:
            leaf = _Leaf(i[0], i[1])
            self.__leaf.append(leaf)
            
    def __grow(self):
        if len(self.__leaf) == 1:
            self.__root = self.__leaf[0]
            self.__root.code = ''
        else:
            while len(self.__leaf) > 0 or len(self.__node) != 1:            
                if self.__node != []:
                    child1 = self.__leaf.pop(0) if len(self.__node) == 1 else self.__node.pop(0)
                    child2 = self.__node.pop(0) if len(self.__leaf) == 0 or self.__node[0].weight <= self.__leaf[0].weight else self.__leaf.pop(0)                
                    node = _Node(child1, child2) if child1.weight <= child2.weight else _Node(child2, child1)                    
                else:                
                    node = _Node(self.__leaf.pop(0), self.__leaf.pop(0)) 
                self.__node.append(node)
            self.__root = self.__node[0]
    
    def __encode(self, text):
        encode_key = {}
        self.encoded_text = ''
        def generate_key(node):
            if type(node) != _Leaf:        
                node.Lchild.code = node.code+'0'
                generate_key(node.Lchild)
                node.Rchild.code = node.code+'1'
                generate_key(node.Rchild)
            else:
                encode_key[node.data] = node.code
        
        generate_key(self.__root)
        self.decode_key = dict(zip(encode_key.values(), encode_key.keys()))
        for i in text:
                self.encoded_text += encode_key[i]


def decode(decode_key, encoded_text):
    '''Decode with decode_key, encoded_text from Class encode()'''
    text = ''
    code = ''
    encoded_text = encoded_text
    for i in encoded_text:
        code += i
        if code in decode_key:
            text += decode_key[code]
            code = ''
    return text