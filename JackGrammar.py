###############################################################################
# Contains regular expressions and other utilities related to the grammar of
# the Jack Programming Language.
###############################################################################
import re

############################
# WHITESPACES AND COMMENTS #
############################
RE_WHITESPACES = r'\s'  # https://regex101.com/r/evyXL2/1
RE_COMMENT_END_OF_LINE = r'//.*[\r\n]+'  # https://regex101.com/r/PbLBSc/1
RE_COMMENT_INLINE = r'/\*[\s\S]*?\*/'  # https://regex101.com/r/PbLBSc/3
RE_COMMENT_END_OF_LINE_COMPILED = re.compile(RE_COMMENT_END_OF_LINE)
RE_COMMENT_INLINE_COMPILED = re.compile(RE_COMMENT_INLINE)
RE_WHITESPACE_COMPILED = re.compile(RE_WHITESPACES)

############
# KEYWORDS #
############
"""
'class ' | 'constructor ' | 'function ' | 'method ' | 'field ' | 'static ' |
'var ' | 'int ' | 'char ' | 'boolean ' | 'void ' | 'true ' | 'false ' |
'null ' | 'this ' | 'let ' | 'do ' | 'if ' | 'else ' | 'while ' | 'return '
"""
RE_CLASS = r'class '
RE_CONSTRUCTOR = r'constructor '
RE_FUNCTION = r'function '
RE_METHOD = r'method '
RE_FIELD = r'field '
RE_STATIC = r'static '
RE_VAR = r'var '
RE_INT = r'int '
RE_CHAR = r'char '
RE_BOOLEAN = r'boolean '
RE_VOID = r'void '
RE_TRUE = r'true '
RE_FALSE = r'false '
RE_NULL = r'null '
RE_THIS = r'this '
RE_LET = r'let '
RE_DO = r'do '
RE_IF = r'if '
RE_ELSE = r'else '
RE_WHILE = r'while '
RE_RETURN_NOTHING = r'return;'
RE_RETURN_SOMETHING = r'return '

KEYWORDS = [RE_CLASS, RE_CONSTRUCTOR, RE_FUNCTION, RE_METHOD, RE_FIELD,
            RE_STATIC, RE_VAR, RE_INT, RE_CHAR, RE_BOOLEAN, RE_VOID,
            RE_TRUE, RE_FALSE, RE_NULL, RE_THIS, RE_LET, RE_DO, RE_IF,
            RE_ELSE, RE_WHILE, RE_RETURN_NOTHING, RE_RETURN_SOMETHING]
RE_KEYWORDS = r'|'.join(KEYWORDS)  # https://regex101.com/r/eVCEmK/2
RE_KEYWORDS_COMPILED = re.compile(RE_KEYWORDS)

###########
# SYMBOLS #
###########
'''
'{' | '}' | '(' | ')' | '[' | ']' | '. ' | ', ' | '; ' | '+' | '-' | '*' | '/' 
| '&' | '|' | '<' | '>' | '=' | '~' 
'''
RE_BRACKETS_CURLY_LEFT      = r'{'
RE_BRACKETS_CURLY_RIGHT     = r'}'
RE_BRACKETS_LEFT            = r'('
RE_BRACKETS_RIGHT           = r')'
RE_BRACKETS_SQUARE_LEFT     = r'['
RE_BRACKETS_SQUARE_RIGHT    = r']'
RE_DOT                      = r'.'
RE_COMMA                    = r','
RE_SEMICOLON                = r';'
RE_PLUS                     = r'+'
RE_BAR                      = r'-'
RE_ASTERISK                 = r'*'
RE_SLASH                    = r'/'
RE_AMPERSAND                = r'&'
RE_VBAR                     = r'|'
RE_LT                       = r'<'
RE_GT                       = r'>'
RE_EQ                       = r'='
RE_TILDA                    = r'~'
SYMBOLS = [RE_BRACKETS_CURLY_LEFT, RE_BRACKETS_CURLY_RIGHT,
           RE_BRACKETS_LEFT, RE_BRACKETS_RIGHT, RE_BRACKETS_SQUARE_LEFT,
           RE_BRACKETS_SQUARE_RIGHT, RE_DOT, RE_COMMA, RE_SEMICOLON,
           RE_PLUS, RE_BAR, RE_ASTERISK, RE_SLASH, RE_AMPERSAND, RE_VBAR,
           RE_LT, RE_GT, RE_EQ, RE_TILDA]
RE_SYMBOLS = "\\" + '|\\'.join(SYMBOLS)  # https://regex101.com/r/eVCEmK/4
RE_SYMBOLS_COMPILED = re.compile(RE_SYMBOLS)
XML_AMPERSAND = "&amp;"
XML_LT = "&lt;"
XML_GT = "&gt;"
RE_SYMBOLS_SPECIAL_TRANSLATE = {
    RE_AMPERSAND: XML_AMPERSAND,
    RE_LT: XML_LT,
    RE_GT: XML_GT}
#####################
# INTEGER CONSTANTS #
#####################
'''
A decimal number in the range 0 .. 32767. 
'''
RE_INTEGER = r'\d+'  # https://regex101.com/r/8eIoqD/1
RE_INTEGER_COMPILED = re.compile(RE_INTEGER)

###################
# STRING CONSTANT #
###################
'''
'"' A sequence of Unicode characters not including double quote or newline '"' 
'''
RE_STRING = r'\".*\"'  # https://regex101.com/r/rcXjLE/1
RE_STRING_COMPILED = re.compile(RE_STRING)

###############
# IDENTIFIERS #
###############
'''
A sequence of letters, digits, and underscore ( '_' ) not starting with a  
digit. 
'''
RE_IDENTIDIER = r'[a-zA-Z_$][a-zA-Z_$0-9]*'  # https://regex101.com/r/ZGwjj3/1
RE_IDENTIDIER_COMPILED = re.compile(RE_IDENTIDIER)


def main():
    """
    Tests for JackGrammar module.
    """
   # print(RE_WHITESPACE_AND_COMMENTS)
    print(RE_KEYWORDS)
    print(RE_SYMBOLS)
    print(RE_INTEGER)
    print(RE_STRING)
    print(RE_IDENTIDIER)
    TEST_STRING = 'if (x < 153) {let city = "Paris";}'
    # m = RE_KEYWORDS_COMPILED.match(TEST_STRING)
    # print(m)


if __name__ == '__main__':
    main()
