##############################################################################
# This is the Symbol Table, it associates names with information needed for
# Jack compilation: type, kind, and running index.
# The symbol table has 2 nested scopes (class/subroutine).
##############################################################################
from JackGrammar import *
from VMGrammar import *
KIND_STATIC = RE_STATIC
KIND_FIELD = RE_FIELD
KIND_VAR = RE_VAR
KIND_ARG = "ARG"
KIND_NONE = "NONE"
IDENTIFIERS_CLASS = {KIND_STATIC, KIND_FIELD}
IDENTIFIERS_SUBROUTINE = {KIND_ARG, KIND_VAR}

ERROR_UNKNOWN_IDENTIFIER_KIND = "Unknown identifier kind {}"
ERROR_INVALID_SCOPE = "Invalid scope for identifier kind {}"
ERROR_IDENTIFIER_NOT_IN_SCOPE = "Identifer {} is not int the current scope"

KIND_2_SEGMENT = {KIND_ARG      : VM_SEGMENT_ARGUMENT,
                  KIND_VAR      : VM_SEGMENT_VAR,
                  KIND_FIELD    : VM_SEGMENT_FIELD,
                  KIND_STATIC   : VM_SEGMENT_STATIC}

class SymbolTable:
    class __NamedIdentifier:
        """
        Helper class for the named identifier data type
        """
        def __init__(self, name, type, kind, index):
            self.name = name
            self.type = type
            self.kind = kind
            self.index = index

    def __init__(self):
        """
        Creates a new empty symbol table
        """
        self.__subroutine_scope = dict()
        self.__class_scope = dict()
        self.__current_scope = self.__class_scope
        self.__initIndexes()

    def startSubroutine(self):
        """
        Starts a new subroutine scope (i.e. erases all names in the previous
        subroutine’s scope.)
        """
        self.__subroutine_scope = dict()
        self.__current_scope = self.__subroutine_scope
        self.__initIndexes()

    def __initIndexes(self):
        self.__running_indexes  = { KIND_FIELD  : 0,
                                    KIND_VAR    : 0,
                                    KIND_ARG    : 0,
                                    KIND_STATIC : 0}


    def define(self, name, type, kind):
        """
        Defines a new identifier of a given name, type, and kind and assigns it
        a running index. STATIC and FIELD identifiers have a class scope,
        while ARG and VAR identifiers have a subroutine scope.
        :param name: (string)
        :param type: (string)
        :param kind: (STATIC, FIELD, ARG or VAR)
        """
        # RazK TODO: Figure out when to use which scope:
        # Should we validate scope here, or rather actually determine it here?

        # Generate named identifier from parameters
        var = self.__NamedIdentifier(name, type, kind, self.__giveIndex(kind))

        # Handle class identifier
        if kind in IDENTIFIERS_CLASS:
            if self.__current_scope != self.__class_scope:
                raise EnvironmentError(ERROR_INVALID_SCOPE.format(kind))
            self.__class_scope[name] = var

        # Handle subroutine identifier
        elif kind in IDENTIFIERS_SUBROUTINE:
            if self.__current_scope != self.__subroutine_scope:
                raise EnvironmentError(ERROR_INVALID_SCOPE.format(kind))
            self.__subroutine_scope[name] = var

        # Handle errors
        else:
            raise NameError(ERROR_UNKNOWN_IDENTIFIER_KIND.format(kind))

    def varCount(self, kind):
        """
        Returns the number of variables of the given kind already defined in
        the current scope.
        :param kind: (STATIC, FIELD, ARG, or VAR)
        :return: (int) number of variables of the given kind already defined in
        the current scope.
        """
        if kind in {KIND_FIELD, KIND_STATIC}:
            scope = self.__class_scope
        else:
            scope = self.__current_scope
        return len([var for var in scope.values()
                    if var.kind == kind])

    def segmentOf(self, name):
        """
        returns the VM segment of the variable with the given name
        :param name: (String)
        :return: VM segment of the given variable
        """
        return KIND_2_SEGMENT[self.kindOf(name)]

    def kindOf(self, name):
        """
        Returns the kind of the named identifier in the current scope.
        Returns NONE if the identifier is unknown in the current scope.
        :param name: (String)
        :return: (STATIC, FIELD, ARG, VAR, NONE)
        """
        if name not in self.__current_scope:
            if name not in self.__class_scope:
                return KIND_NONE
            return self.__class_scope[name].kind
        return self.__current_scope[name].kind

    def typeOf(self, name):
        """
        Returns the type of the named identifier in the current scope.
        :param name: (String)
        :return: (String) type of the named identifier in the current scope.
        """
        if name not in self.__current_scope:
            if name not in self.__class_scope:
                raise EnvironmentError(ERROR_IDENTIFIER_NOT_IN_SCOPE.format(name))
            return self.__class_scope[name].type
        return self.__current_scope[name].type

    def indexOf(self, name):
        """
        Returns the index assigned to named identifier.
        :param name: (String)
        :return: (int) index assigned to named identifier.
        """
        if name not in self.__current_scope:
            if name not in self.__class_scope:
                raise EnvironmentError(
                    ERROR_IDENTIFIER_NOT_IN_SCOPE.format(name))
            return self.__class_scope[name].index
        return self.__current_scope[name].index

    def __giveIndex(self, kind):
        """
        Returns the next available running index and increments the running
        index.
        :return: (int) next available running index.
        """
        index = self.__running_indexes[kind]
        self.__running_indexes[kind] += 1
        return index
