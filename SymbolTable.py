class SymbolTable:
    def __init__(self):
        """
        Creates a new empty symbol table
        """
        pass

    def startSubroutine(self):
        """
        Starts a new subroutine scope (i.e. erases all names in the previous
        subroutine’s scope.)
        """
        pass

    def define(self, name, type, kind):
        """
        Defines a new identifier of a given name, type, and kind and assigns it
        a running index. STATIC and FIELD identifiers have a class scope,
        while ARG and VAR identifiers have a subroutine scope.
        :param name: (string)
        :param type: (string)
        :param kind: (STATIC, FIELD, ARG or VAR)
        """
        pass

    def varCount(self, kind):
        """
        Returns the number of variables of the given kind already defined in
        the current scope.
        :param kind: (STATIC, FIELD, ARG, or VAR)
        :return: (int) number of variables of the given kind already defined in
        the current scope.
        """
        pass

    def kindOf(self, name, ):
        """
        Returns the kind of the named identifier in the current scope.
        Returns NONE if the identifier is unknown in the current scope.
        :param name: (String)
        :return: (STATIC, FIELD, ARG, VAR, NONE)
        """
        pass

    def typeOf(self, name):
        """
        Returns the type of the named identifier in the current scope.
        :param name: (String)
        :return: (String) type of the named identifier in the current scope.
        """
        pass

    def indexOf(self, name):
        """
        Returns the index assigned to named identifier.
        :param name: (String)
        :return: (int) index assigned to named identifier.
        """
        pass