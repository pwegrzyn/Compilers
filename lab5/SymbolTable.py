# Patryk Wegrzyn
# Kompilatory - laboratorium - poniedziałek 11:15

class Symbol(object):
    pass


class VariableSymbol(Symbol):

    def __init__(self, name, type):
        self.name = name
        self.type = type

    def __str__(self):
        return str(self.type)


class MatrixType(object):

    def __init__(self, dim_1, dim_2, content_type):
        self.dim_1 = dim_1
        self.dim_2 = dim_2
        self.content_type = content_type

    def __str__(self):
        return 'matrix'


class VectorType(object):

    def __init__(self, dim, content_type):
        self.dim = dim
        self.content_type = content_type

    def __str__(self):
        return 'vector'


class ErrorType(object):

    def __str__(self):
        return 'error type'


class SymbolTable(object):
    
    def __init__(self, parent, name): # parent scope and symbol table name
        self.parent = parent
        self.name = name
        self.symbols = dict()

    def put(self, name, symbol): # put variable symbol or fundef under <name> entry
        self.symbols[name] = symbol

    def get(self, name): # get variable symbol or fundef from <name> entry
        try:
            symbol = self.symbols[name]
            return symbol
        except:
            if not self.parent is None:
                return self.getParentScope().get(name)
            return None

    def getParentScope(self):
        return self.parent

    def pushScope(self, name):
        new_scope = SymbolTable(self, name)
        return new_scope

    def popScope(self):
        return self.parent

