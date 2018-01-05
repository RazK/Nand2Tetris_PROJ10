############################################################################
# Effects the actual compilation output. Gets its input from a JackTokenizer
# and emits its parsed structure into an output file/stream. The output is
# generated by a series of compilexxx()routines, one for every syntactic
# element xxx of the Jack grammar. The contract between these routines is that
# each compilexxx() routine should read the syntactic construct xxx from the
# input, advance() the tokenizer exactly beyond xxx, and output the parsing of
# xxx. Thus, compilexxx()may only be called if indeed xxx is the next syntactic
# element of the input. In the first version of the compiler, described in
# Chapter 10, this module emits a structured printout of the code, wrapped in
# XML tags. In the final version of the compiler, described in Chapter 11,
# this module generates executable VM code. In both cases, the parsing logic
# and module API are exactly the same
##############################################################################
from JackTokenizer import *
from SymbolTable import *
from VMWriter import *

XML_DELIM_TERMINAL = " "
XML_INDENT_CHAR = "  "
TOKEN_TYPE_CLASS_NAME = TOKEN_TYPE_IDENTIFIER
TOKEN_TYPE_SUBROUTINE_NAME = TOKEN_TYPE_IDENTIFIER
TOKEN_TYPE_VAR_NAME = TOKEN_TYPE_IDENTIFIER
UNIQUE_DELIMITER = ""
WHILE_EXP = "WHILE_EXP"
WHILE_END = "WHILE_END"
IF_TRUE = "IF_TRUE"
IF_FALSE = "IF_FALSE"
IF_END = "IF_END"

# Identifiers
STATUS_DEFINE = "definition"
STATUS_USE = "usage"
CATEGORY_VAR = KIND_VAR
CATEGORY_ARG = KIND_ARG
CATEGORY_STATIC = KIND_STATIC
CATEGORY_FIELD = KIND_FIELD
CATEGORY_CLASS = RE_CLASS
CATEGORY_SUBROUTINE = "subroutine"
INDEX_NONE = -1

class CompilationEngine:
    ###############
    # CONSTRUCTOR #
    ###############

    def __init__(self, in_filename, in_file, out_xml, out_vm):
        """
        Creates a new compilation engine with the given input and output.
        The next routine called must be compileClass().
        :param in_file: Open source Jack file.
        :param out_xml: Open XML file.
        :param out_vm: Open VM file.
        """
        self.__in_filename = in_filename
        self.__in_file, self.__out_xml = in_file, out_xml
        self.__tokenizer = JackTokenizer(in_file)
        self.__symbolTable = SymbolTable()
        self.__vmWriter = VMWriter(in_filename, out_vm)
        self.__stack = list()
        self.__tokenizer.advance()
        self.__resetUniqueLabels()

    ###################
    # PRIVATE METHODS #
    ###################

    def __resetUniqueLabels(self):
        self.__unique_id_if = 0
        self.__unique_id_while = 0

    def __uniqueWhileLabels(self):
        """
        Return (IF_TRUE, IF_FALSE, IF_END) labels carrying a unique id to
        prevent collisions with other labels carrying the same name.
        Example:
            while_exp, while_end = __uniqueWhileLabels()
            -->
            while_exp = "WHILE_EXP123"
            while_end = "WHILE_END123"
        """
        unique_labels = []
        for label in [WHILE_EXP, WHILE_END]:
            unique_labels.append("{}{}{}".format(label,
                                                 UNIQUE_DELIMITER,
                                                 self.__unique_id_while))
        self.__unique_id_while += 1
        return unique_labels

    def __uniqueIfLabels(self):
        """
        Return (IF_TRUE, IF_FALSE, IF_END) labels carrying a unique id to
        prevent collisions with other labels carrying the same name.
        Example:
            if_true, if_false, if_end = __uniqueIfLabels()
            -->
            if_true = "IF_TRUE123"
            if_false = "IF_FALSE123"
            if_end = "IF_END123"
        """
        unique_labels = []
        for label in [IF_TRUE, IF_FALSE, IF_END]:
            unique_labels.append("{}{}{}".format(label,
                                                 UNIQUE_DELIMITER,
                                                 self.__unique_id_if))
        self.__unique_id_if += 1
        return unique_labels

    def __writeToken(self, token, token_type):
        """
        Writes the given token as an xml tag to the output.
        :param token:
        :param token_type:
        :return:
        """
        tag = self.__getIndentedTag("<{0}>{1}{2}{1}</{0}>\n"
                                    .format(token_type,
                                            XML_DELIM_TERMINAL,
                                            token))
        self.__out_xml.write(tag)


    def __writeTokenAndAdvance(self, token, token_type):
        """
        Writes the given token as an xml tag to the output and extracts the
        next token from the code.
        :param token: token tag value
        :param token_type: token tag type
        """
        # Build XML tag
        self.__writeToken(token, token_type)
        self.__tokenizer.advance()

    def __getIndentedTag(self, tag):
        """
        Return the given tag with trailing tabs according to current
        indentation level.
        :param tag: tag to indent
        :return: tag indented with trailing tabs.
        """
        return XML_INDENT_CHAR * len(self.__stack) + tag

    def __openTag(self, tagName):
        """
        Open an XML tag with the given name.
        All following tags will be written as inner tags until __closeTag()
        is called.
        :param tagName: name of the tag to open
        """
        tag = self.__getIndentedTag("<{}>\n".format(tagName))
        self.__out_xml.write(tag)
        self.__stack.append(tagName)

    def __closeTag(self):
        """
        Close the current open XML tag.
        All following tags will be written as outer tags in the previous
        indentation level.
        """
        tagName = self.__stack.pop()
        tag = self.__getIndentedTag("</{}>\n".format(tagName))
        self.__out_xml.write(tag)

    def __compileKeyWord(self):
        """
        Compile a keyword token
        """
        keyword = self.__tokenizer.keyWord()
        self.__writeTokenAndAdvance(keyword, TOKEN_TYPE_KEYWORD)
        return keyword

    def __compileSymbol(self):
        """
        Compile a symbol token
        """
        symbol = self.__tokenizer.symbol()
        self.__writeTokenAndAdvance(symbol, TOKEN_TYPE_SYMBOL)
        return symbol

    def __compileIdentifier(self, category, status, kind=KIND_NONE,
                            index=INDEX_NONE):
        """
        Compile an identifier token
        """

        info = "{} {}".format(category, status)
        if kind != KIND_NONE:
            info += " " + KIND_2_SEGMENT[kind]
        if index != INDEX_NONE:
            info += " " + str(index)
        info = "[{}] ".format(info)
        identifier = self.__tokenizer.identifier()
        self.__writeTokenAndAdvance(info + identifier, TOKEN_TYPE_IDENTIFIER)
        return identifier

    def __compileIntVal(self):
        """
        Compile an intVal token
        """
        intval = self.__tokenizer.intVal()
        self.__writeTokenAndAdvance(intval, TOKEN_TYPE_INTEGER)
        self.__vmWriter.writePush(VM_SEGMENT_CONSTANT, intval)
        return intval

    def __compileStringVal(self):
        """
        Compile a stringVal token
        """
        string = self.__tokenizer.stringVal()
        self.__writeTokenAndAdvance(string, TOKEN_TYPE_STRING)

        corrected = self.__correctString(string)
        self.__vmWriter.writePush(VM_SEGMENT_CONSTANT, len(corrected))
        self.__vmWriter.writeCall(OS_STRING_NEW, 1)
        for char in corrected:
            self.__vmWriter.writePush(VM_SEGMENT_CONSTANT, ord(char))
            self.__vmWriter.writeCall(OS_STRING_APPEND_CHAR, 2)

    def __compileClassName(self, status):
        """
        Compiles a variable name.
        """
        return self.__compileIdentifier(CATEGORY_CLASS, status)

    def __compileSubroutineName(self, status):
        """
        Compiles a variable name.
        """
        return self.__compileIdentifier(CATEGORY_SUBROUTINE, status)

    def __compileSubroutineCall(self):
        """
        Compiles a subroutine call.
        Syntax:
        ( className | varName) '.' subroutineName '(' expressionList ')' |
        subroutineName '(' expressionList ')'
        """
        # Compile XML
        callName = ""
        exp_count = 0
        if self.__tokenizer.lookahead() == RE_DOT:      # className | varName
            # extract var\class name
            callName = self.__tokenizer.peek()
            # className or varName?
            kind = self.__symbolTable.kindOf(callName)
            if (kind != KIND_NONE):                     # varName
                # Use class name instead of object name
                varName = callName
                callName = self.__symbolTable.typeOf(callName)
                # Push variable (this) and call class method
                index = self.__symbolTable.indexOf(varName)
                segment = self.__symbolTable.segmentOf(varName)
                self.__vmWriter.writePush(segment, index)
                # Include self as argument 0
                exp_count += 1
                self.__compileIdentifier(kind, STATUS_USE, kind, index)
            else:                                       # className
                self.__compileIdentifier(CATEGORY_CLASS, STATUS_USE)

            callName += self.__compileSymbol()          # '.'
        else:                                           # subroutineName
            # Subroutine -> className.Subroutine
            self.__vmWriter.writePush(VM_SEGMENT_POINTER, 0)
            callName += self.__className + FUNC_NAME_DELIMITER
            exp_count += 1

        callName += self.__compileSubroutineName(STATUS_USE)
        self.__compileSymbol()                          # '('
        exp_count += self.CompileExpressionList()       # expressionList
        self.__compileSymbol()                          # ')'

        # Compile VM
        self.__vmWriter.writeCall(callName, exp_count)

    def __compileVarName(self, status):
        """
        Compiles a variable name.
        """
        name = self.__tokenizer.peek()
        index = INDEX_NONE
        if status != STATUS_DEFINE:
            index = self.__symbolTable.indexOf(name)
        varName = self.__compileIdentifier(CATEGORY_VAR, status, KIND_VAR,
                                           index)
        return varName

    def __compileType(self):
        """
        Compiles a type.
        Syntax:
        'int' | 'char' | 'boolean' | className
        """
        # 'int' | 'char' | 'boolean'
        if self.__tokenizer.peek() in {RE_INT, RE_CHAR, RE_BOOLEAN}:
            type = self.__compileKeyWord()
        # className
        else:
            type = self.__compileClassName(STATUS_USE)
        return type

    def __compileSubroutineBody(self, funcType, name):
        """
        Compiles a subroutine body.
        Syntax:
        '{' varDec* statements '}'
        """
        self.__openTag('subroutineBody')    # <subroutineBody>
        self.__compileSymbol()              #   '{'
        # varDec*
        while self.__tokenizer.peek() == RE_VAR:
            self.compileVarDec()            #   varDec*
        vars = self.__symbolTable.varCount(KIND_VAR)
        self.__vmWriter.writeFunction(name, vars)
        if funcType == RE_METHOD:
            # Hold self at pointer
            self.__vmWriter.writePush(VM_SEGMENT_ARGUMENT, 0)
            self.__vmWriter.writePop(VM_SEGMENT_POINTER, 0)
        if funcType == RE_CONSTRUCTOR:
            # Allocate memory for all fields
            fields = self.__symbolTable.varCount(KIND_FIELD)
            self.__vmWriter.writePush(VM_SEGMENT_CONSTANT, fields)
            self.__vmWriter.writeCall(OS_MEMORY_ALLOC, 1)
            # Hold allocated memory at pointer
            self.__vmWriter.writePop(VM_SEGMENT_POINTER, 0)
        self.compileStatements()            #   statements
        self.__compileSymbol()              #   '}'
        self.__closeTag()                   # </subroutineBody>
        return vars

    ##################
    # PUBLIC METHODS #
    ##################

    def compileClass(self):
        """
        Compiles a complete class.
        Syntax:
        'class' className '{' classVarDec* subroutineDec* '}'
        """
        self.__openTag('class')                 # <class>
        self.__compileKeyWord()                 #   'class'
        className = self.__compileClassName(    #   className
            STATUS_DEFINE)
        self.__className = className
        self.__compileSymbol()                  #   '{'

                                                # classVarDec*
        while self.__tokenizer.peek() in {RE_STATIC, RE_FIELD}:
            self.CompileClassVarDec()

                                                # subroutineDec*
        while self.__tokenizer.peek() in {RE_CONSTRUCTOR, RE_FUNCTION,
                                          RE_METHOD}:
            self.CompileSubroutine()

        self.__compileSymbol()                  #   '}'
        self.__closeTag()                       # </class>

    def CompileClassVarDec(self):
        """
        Compiles a static declaration or a field declaration.
        Syntax:
        ('static' | 'field') type varName (',' varName)* ';'
        """
        self.__openTag('classVarDec')       # <classVarDec>
        kind = self.__compileKeyWord()      #   ('static' | 'field')
        type = self.__compileType()         #   type
        moreVars = True
        while moreVars:                     #   (',' varName)*
            name = self.__compileVarName(   #   varName
                STATUS_DEFINE)
            self.__symbolTable.define(name, type, kind)
            if self.__tokenizer.peek() != RE_COMMA:
                moreVars = False
            else:
                self.__compileSymbol()      #   ','

        self.__compileSymbol()              #   ';'
        self.__closeTag()                   # </classVarDec>

    def CompileSubroutine(self):
        """
        Compiles a complete method, function, or constructor.
        Syntax:
        ('constructor' | 'function' | 'method') ('void' | type)
        subroutineName '(' parameterList ')' subroutineBody
        """
        # Start subroutine in symbol table
        self.__resetUniqueLabels()
        self.__symbolTable.startSubroutine()

        # Compile XML
        self.__openTag('subroutineDec')         # <subroutineDec>
        funcType = self.__compileKeyWord()      #   ('constructor' |
                                                #   'function' | 'method')
        if funcType in {RE_METHOD}:
            # +1 var count for this method (+1 for self)
            self.__symbolTable.define(VM_SELF, self.__className, KIND_ARG)
        if self.__tokenizer.peek() == RE_VOID:
            type = self.__compileKeyWord()      #   'void'
        else:
            type = self.__compileType()         #   type
        subName = self.__compileSubroutineName( #   soubroutineName
            STATUS_DEFINE)
        name = self.__className + FUNC_NAME_DELIMITER + subName
        self.__compileSymbol()                  #   '('
        self.compileParameterList()             #   parameterList
        self.__compileSymbol()                  #   ')'
        self.__compileSubroutineBody(funcType,
                                     name)      #   subroutineBody
        self.__closeTag()                       # </subroutineDec>

    def compileParameterList(self):
        """
        Compiles a (possibly empty) parameter list, not including the
        enclosing "()".
        Syntax:
        ( (type varName) (',' type varName)*)?
        """
        parameters = 0                          # no parameters?
        self.__openTag('parameterList')         # <parameterList>
        if self.__tokenizer.peek() != RE_BRACKETS_RIGHT:
            moreVars = True
            while moreVars:
                parameters += 1                 # yes parameters!
                type = self.__compileType()     #   type
                name = self.__compileVarName(   #   varName
                    STATUS_DEFINE)
                self.__symbolTable.define(name, type, KIND_ARG)
                if self.__tokenizer.peek() == RE_COMMA:
                    self.__compileSymbol()      # ','
                else:
                    moreVars = False
        self.__closeTag()                       # </parametersList>
        return parameters

    def compileVarDec(self):
        """
        Compiles a var declaration.
        Syntax:
        'var' type varName (',' varName)* ';'
        """
        self.__openTag('varDec')            # <varDec>
        moreVars = True
        self.__compileKeyWord()             #   'var'
        type = self.__compileType()         #   type
        while moreVars:
            name = self.__tokenizer.peek()  #   varName
            self.__symbolTable.define(name, type, KIND_VAR)
            self.__compileVarName(STATUS_DEFINE)
            if self.__tokenizer.peek() == RE_COMMA:
                self.__compileSymbol()      #   ','
            else:
                moreVars = False
        self.__compileSymbol()              #   ';'
        self.__closeTag()                   # </varDec>

    def compileStatements(self):
        """
        Compiles a sequence of statements, not including the enclosing "{}".
        Syntax:
        statement*
        where statement is in:
        letStatement | ifStatement | whileStatement | doStatement | returnStatement
        """
        self.__openTag('statements')    # <statements>
        statement = self.__tokenizer.peek()
        while statement in {RE_LET, RE_IF, RE_WHILE, RE_DO, RE_RETURN_NOTHING,
                            RE_RETURN_SOMETHING}:
            if statement == RE_LET:
                self.compileLet()
            elif statement == RE_IF:
                self.compileIf()
            elif statement == RE_WHILE:
                self.compileWhile()
            elif statement == RE_DO:
                self.compileDo()
            elif statement == RE_RETURN_NOTHING:
                self.compileReturnNothing()
            elif statement == RE_RETURN_SOMETHING:
                self.compileReturnSomething()
            statement = self.__tokenizer.peek()
        self.__closeTag()               # </statements>

    def compileDo(self):
        """
        Compiles a do statement.
        Syntax:
        'do' subroutineCall ';'
        """
        self.__openTag('doStatement')   # <doStatement>
        self.__compileKeyWord()         #   'do'
        self.__compileSubroutineCall()  #   subroutineCall
        self.__vmWriter.writePop(VM_SEGMENT_TEMP, 0)
        self.__compileSymbol()          #   ';'
        self.__closeTag()               # </doStatement>

    def compileLet(self):
        """
        Compiles a let statement.
        Syntax:
        'let' varName ('[' expression ']')? '=' expression ';'
        """
        isArray = False
        self.__openTag('letStatement')      # <letStatement>
        self.__compileKeyWord()             #   'let'
        varName = self.__tokenizer.peek()
        index = self.__symbolTable.indexOf(varName)
        segment = self.__symbolTable.segmentOf(varName)
        self.__compileVarName(STATUS_USE)   #   varName
        if self.__tokenizer.peek() == RE_BRACKETS_SQUARE_LEFT:
            isArray = True
            self.__compileSymbol()          #   '['
            self.CompileExpression()        # expression
            self.__compileSymbol()          #   ']'
            # Add the offset to the variable address
            self.__vmWriter.writePush(segment, index)
            self.__vmWriter.writeArithmetic(RE_PLUS, True)
            # Address of array element is at stack top
        self.__compileSymbol()              #   '='
        self.CompileExpression()            # expression
        self.__compileSymbol()              #   ';'
        self.__closeTag()                   # </letStatement>

        if isArray:
            # Pop rh-expression to temp
            self.__vmWriter.writePop(VM_SEGMENT_TEMP, 0)
            # Get address of array element
            self.__vmWriter.writePop(VM_SEGMENT_POINTER, 1)
            # Push rh-expression to stack
            self.__vmWriter.writePush(VM_SEGMENT_TEMP, 0)
            # Pop rh-expression to address of element
            self.__vmWriter.writePop(VM_SEGMENT_THAT, 0)
        else:
        # Compile only if the varName was defined
        # (unlike class name of subroutine name)
        # if segment != KIND_NONE:  # varName was defined
            index = self.__symbolTable.indexOf(varName)
            self.__vmWriter.writePop(segment, index)


    def compileWhile(self):
        """
        Compiles a while statement.
        Syntax:
        'while' '(' expression ')' '{' statements '}'
        """
        LABEL_EXP, LABEL_END = self.__uniqueWhileLabels()

        self.__openTag('whileStatement')        # <whileStatement>
        self.__compileKeyWord()                 #   'while'
        self.__compileSymbol()                  #   '('
        self.__vmWriter.writeLabel(             # label WHILE_EXP
            LABEL_EXP)
        self.CompileExpression()                #   expression
        # Negate the expression
        # (jump out of while if *NOT* expression)
        self.__vmWriter.writeArithmetic(RE_TILDA, False)
        self.__compileSymbol()                  #   ')'
        self.__vmWriter.writeIf(LABEL_END)      # if-goto WHILE_END
        self.__compileSymbol()                  #   '{'
        self.compileStatements()                #   statements
        self.__compileSymbol()                  #   '}'
        self.__vmWriter.writeGoto(LABEL_EXP)    # goto WHILE_EXP
        self.__vmWriter.writeLabel(LABEL_END)   # lable WHILE_END
        self.__closeTag()                       # </whileStatement>

    def compileReturnNothing(self):
        """
        Compiles a 'return;' statement.
        Syntax:
        'return;'
        """
        # Compile XML
        self.__openTag('returnStatement')       # <returnStatement>
        self.__writeToken('return',             #   'return'
                          TOKEN_TYPE_KEYWORD)
        self.__writeTokenAndAdvance(';',        #   ';'
                                    TOKEN_TYPE_SYMBOL)
        self.__vmWriter.writeReturn(True)
        self.__closeTag()                       # </returnStatement>

    def compileReturnSomething(self):
        """
        Compiles a return statement.
        Syntax:
        'return' expression? ';'
        """
        # Compile XML
        self.__openTag('returnStatement')       # <returnStatement>
        self.__writeTokenAndAdvance('return',   #   'return'
                                    TOKEN_TYPE_KEYWORD)
        self.CompileExpression()                #   expression
        self.__compileSymbol()                  #   ';'
        self.__vmWriter.writeReturn()
        self.__closeTag()                       # </returnStatement>

    def compileIf(self):
        """
        Compiles an if statement, possibly with a trailing else clause.
        Syntax:
        'if' '(' expression ')' '{' statements '}' ( 'else' '{' statements
        '}' )?
        """
        LABEL_TRUE, LABEL_FALSE, LABEL_END = self.__uniqueIfLabels()

        self.__openTag('ifStatement')           # <ifStatement>
        self.__compileKeyWord()                 #   'if'
        self.__compileSymbol()                  #   '('
                                                # VM Code for computing ~(cond)
        self.CompileExpression()                #   expression
        self.__compileSymbol()                  #   ')'
        self.__vmWriter.writeIf(LABEL_TRUE)     # if-goto LABEL_TRUE
        self.__vmWriter.writeGoto(LABEL_FALSE)  # goto LABEL_FALSE
        self.__vmWriter.writeLabel(LABEL_TRUE)  # label LABEL_TRUE
        self.__compileSymbol()                  #   '{'
                                                # VM Code for executing TRUE
        self.compileStatements()                #   statements
        self.__compileSymbol()                  #   '}'
        if self.__tokenizer.peek() == RE_ELSE:  #
            self.__vmWriter.writeGoto(LABEL_END)# goto LABEL_END
            self.__vmWriter.writeLabel(         # label LABEL_FALSE
                LABEL_FALSE)
            self.__compileKeyWord()             #   'else'
            self.__compileSymbol()              #   '{'
                                                # VM Code for executing ELSE
            self.compileStatements()            #   statements
            self.__compileSymbol()              #   '}'
            self.__vmWriter.writeLabel(         # label END
                LABEL_END)
        else:
            self.__vmWriter.writeLabel(         # label FALSE
                LABEL_FALSE)
        self.__closeTag()                       # </ifStatement>


    def CompileExpression(self):
        """
        Compiles an expression.
        Syntax:
        term (op term)*
        """
        self.__openTag('expression')        # <expression>
        self.CompileTerm()                  # term
        while self.__tokenizer.peek() in {RE_PLUS, RE_BAR, RE_ASTERISK,
                                          RE_SLASH, RE_AMPERSAND, RE_VBAR,
                                          RE_LT, RE_GT, RE_EQ}:
            symbol = self.__compileSymbol() # op
            self.CompileTerm()              # term
            self.__vmWriter.writeSymbol(symbol)
        self.__closeTag()                   # </expression>

    def __correctString(self, string):
        """
        Convert escape characters in a string to valid chars
        :param string: string to correct
        :return: corrected strings with escaped characters corrected
        """
        correct = string.replace('\t', '\\t')
        correct = correct.replace('\n', '\\n')
        correct = correct.replace('\r', '\\r')
        return correct

    def CompileTerm(self):
        """
        Compiles a term.
        This routine is faced with a slight difficulty when trying to decide
        between some of the alternative parsing rules.
        Specifically, if the current token is an identifier, the routine
        must distinguish between a variable, an array entry, and a subroutine
        call. A single look-ahead token, which may be one
        of "[", "(", or "." suffices to distinguish between the three
        possibilities. Any other token is not part of this term and should
        not be advanced over.
        Syntax:
        integerConstant | stringConstant | keywordConstant | varName |
        varName '[' expression ']' | subroutineCall | '(' expression ')' |
        unaryOp term
        """
        self.__openTag('term')                      # <term>
        lookahead = self.__tokenizer.lookahead()
        if self.__tokenizer.peek() == RE_BRACKETS_LEFT:
            self.__compileSymbol()                  #   '('
            self.CompileExpression()                #   expression
            self.__compileSymbol()                  #   ')'
        elif self.__tokenizer.peek() in {RE_TILDA, RE_BAR}:
            symbol = self.__compileSymbol()         #   unaryOp
            self.CompileTerm()                      #   term
            self.__vmWriter.writeArithmetic(symbol, False)
        elif lookahead == RE_BRACKETS_SQUARE_LEFT:
            varName = self.__tokenizer.peek()
            self.__compileVarName(STATUS_USE)       #   varName
            self.__compileSymbol()                  #   '['
            self.CompileExpression()                #   expression
            self.__compileSymbol()                  #   ']'
            # Compile array indexing
            kind = self.__symbolTable.kindOf(varName)
            index = self.__symbolTable.indexOf(varName)
            segment = KIND_2_SEGMENT[kind]
            self.__vmWriter.writePush(segment, index)
            self.__vmWriter.writeArithmetic(RE_PLUS, True)
            self.__vmWriter.writePop(VM_SEGMENT_POINTER, 1)
            self.__vmWriter.writePush(VM_SEGMENT_THAT, 0)
        elif lookahead in {RE_BRACKETS_LEFT, RE_DOT}:
            self.__compileSubroutineCall()          #   subroutineCall |
            # (varName | className) '.' subroutineCall
        else:
            if self.__tokenizer.tokenType() == TOKEN_TYPE_INTEGER:
                self.__compileIntVal()              #   integerConstant
            elif self.__tokenizer.tokenType() == TOKEN_TYPE_STRING:
                self.__compileStringVal()           #   stringConstant
            elif self.__tokenizer.tokenType() == TOKEN_TYPE_KEYWORD:
                # true | false | null | this
                # true | false | null - pushed to stack as constants
                keyword = self.__tokenizer.peek()
                if keyword in {RE_FALSE, RE_NULL, RE_TRUE, RE_FALSE}:
                    self.__vmWriter.writePush(VM_SEGMENT_CONSTANT, 0)
                    if keyword == RE_TRUE:
                        self.__vmWriter.writeArithmetic(RE_TILDA, False)
                # this - pushes pointer
                elif keyword == RE_THIS:
                    self.__vmWriter.writePush(VM_SEGMENT_POINTER, 0)
                self.__compileKeyWord()             #   keywordConstant
            elif self.__tokenizer.tokenType() == TOKEN_TYPE_IDENTIFIER:
                name = self.__tokenizer.peek()
                kind = self.__symbolTable.kindOf(name)
                index = self.__symbolTable.indexOf(name)
                segment = self.__symbolTable.segmentOf(name)
                self.__compileIdentifier(kind, STATUS_USE, kind, index)
                self.__vmWriter.writePush(segment, index)
        self.__closeTag()                           # </term>

    def CompileExpressionList(self):
        """
        Compiles a (possibly empty) comma-separated list of expressions.
        Syntax:
        (expression (',' expression)* )?
        """
        exp_count = 0
        self.__openTag('expressionList')            # <expressionList>
        if self.__tokenizer.peek() != RE_BRACKETS_RIGHT:
            self.CompileExpression()
            exp_count += 1                          #   expression
            while self.__tokenizer.peek() == RE_COMMA:
                self.__compileSymbol()              #   ','
                self.CompileExpression()
                exp_count += 1
        self.__closeTag()                           # </expressionList>
        return exp_count

def main():
    with open("testing\Square\SquareGame.jack", 'r') as infile, \
            open("testing\Square\SquareGame.test.xml", 'w') as \
                    outfile:
        cybermaster = CompilationEngine(infile, outxml, outvm)
        cybermaster.compileClass()


if __name__ == '__main__':
    main()
