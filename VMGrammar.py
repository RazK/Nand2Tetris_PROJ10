from JackGrammar import *

VM_ADD = "add"
VM_SUB = "sub"
VM_NEG = "neg"
VM_EQ = "eq"
VM_GT = "gt"
VM_LT = "lt"
VM_AND = "and"
VM_OR = "or"
VM_NOT = "not"
VM_MULT = "call Math.multiply 2"
VM_DIV = "call Math.divide 2"
JACK_2_VM_ARITHMETIC_BINARY = {
    RE_PLUS         : VM_ADD,
    RE_BAR          : VM_SUB,
    RE_EQ           : VM_EQ,
    RE_GT           : VM_GT,
    XML_GT          : VM_GT,
    RE_LT           : VM_LT,
    XML_LT          : VM_LT,
    RE_AMPERSAND    : VM_AND,
    XML_AMPERSAND   : VM_AND,
    RE_VBAR         : VM_OR,
    RE_ASTERISK     : VM_MULT,
    RE_SLASH        : VM_DIV
}
JACK_2_VM_ARITHMETIC_UNARY = {
    RE_BAR  : VM_NEG,
    RE_TILDA: VM_NOT
}

JACK_BRACKET_SQUARE_CLOSE = ']'

VM_SEGMENT_ARGUMENT = "argument"
VM_SEGMENT_VAR = "local"
VM_SEGMENT_STATIC = "static"
VM_SEGMENT_FIELD = "this"
VM_SEGMENT_CONSTANT = "constant"
VM_SEGMENT_TEMP = "temp"
VM_SEGMENT_POINTER = "pointer"
VM_SEGMENT_THAT = "that"

OS_STRING_NEW = "String.new" # Takes 1 argument
OS_STRING_APPEND_CHAR = "String.appendChar" # Takes 2 arguments
OS_MEMORY_ALLOC = "Memory.alloc" # Takes 1 argument

VM_SELF = VM_SEGMENT_FIELD # this