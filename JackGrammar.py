###############################################################################
# Contains regular expressions and other utilities related to the grammar of
# the Jack Programming Language.
###############################################################################

#######################
# REGULAR EXPRESSIONS #
#######################
import re

RE_WHITESPACES = r'\s' # https://regex101.com/r/evyXL2/1

############
# KEYWORDS #
############
"""
'class' | 'constructor' | 'function' | 'method' | 'field' | 'static' |
'var' | 'int' | 'char' | 'boolean' | 'void' | 'true' | 'false' | 'null' | 'this' |
'let' | 'do' | 'if' | 'else' | 'while' | 'return'
"""
RE_CLASS        = r'class'
RE_CONSTRUCTOR  = r'constructor'
RE_FUNCTION     = r'function'
RE_METHOD       = r'method'
RE_FIELD        = r'field'
RE_STATIC       = r'static'
RE_VAR          = r'var'
RE_INT          = r'int'
RE_CHAR         = r'char'
RE_BOOLEAN      = r'boolean'
RE_VOID         = r'void'
RE_TRUE         = r'true'
RE_FALSE        = r'false'
RE_NULL         = r'null'
RE_THIS         = r'this'
RE_LET          = r'let'
RE_DO           = r'do'
RE_IF           = r'if'
RE_ELSE         = r'else'
RE_WHILE        = r'while'
RE_RETURN       = r'return'
KEYWORDS = [RE_CLASS, RE_CONSTRUCTOR, RE_FUNCTION, RE_METHOD, RE_FIELD,
             RE_STATIC, RE_VAR, RE_INT, RE_CHAR, RE_BOOLEAN, RE_VOID,
            RE_TRUE, RE_FALSE, RE_NULL, RE_THIS, RE_LET, RE_DO, RE_IF,
            RE_ELSE, RE_WHILE, RE_RETURN]
RE_KEYWORDS = r'|'.join(KEYWORDS) # https://regex101.com/r/eVCEmK/2
RE_KEYWORDS_COMPILED = re.compile(RE_KEYWORDS)


def main():
    TEST_STRING = 'if (x < 153) {let city = ”Paris”;}'
    m = RE_KEYWORDS_COMPILED.match(TEST_STRING)
    print(m)

if __name__ == '__main__':
    main()