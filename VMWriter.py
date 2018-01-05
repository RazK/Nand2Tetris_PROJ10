############################################################
# This class writes VM commands into a file.
# It encapsulates the VM command syntax.
############################################################
import VMGrammar as vg
from JackGrammar import *

##########################
# CONSTANTS - VM GRAMMAR #
##########################

# COMMANDS:
RETURN = "return"
PUSH = "push"
POP = "pop"
LABEL = "label"
GOTO = "goto"
IF_GOTO = "if-goto"
CALL = "call"
FUNCTION_DEC = "function"

# CONSTANT VM COMMANDS
POP_RETURN = "pop temp 0"
PUSH_VOID = "push constant 0"

# ERRORS MSGs
POP_TO_CONST_MSG = "Pop to constant segment is forbidden"

# FUNCTIONS
FUNC_NAME_DELIMITER = '.'

# MORE
SPACE = " "
NEWLINE = "\n"


#############
# VM WRITER #
#############

class VMWriter:
    """
    Writes VM commands into the output file.
    """

    ################
    # CONSTRUCTORS #
    ################

    def __init__(self, in_filename, output_file):
        """
        Create a new VMWriter object, creates a new output file and prepares it
        for writing
        """
        self.__in_filename = in_filename
        self.__output = output_file

    ##################
    # PUBLIC METHODS #
    ##################

    def writePush(self, segment, index):
        """
        Writes a VM push command.
        :param segment: CONST, ARG, LOCAL, STATIC, THIS, THAT, POINTER, TEMP.
        :param index: The index of a register in the segment.
        """
        self.__output.write(
            PUSH + SPACE + segment + SPACE + str(index) + NEWLINE)

    def writePop(self, segment, index):
        """
        Writes a VM pop command.
        :param segment: CONST, ARG, LOCAL, STATIC, THIS, THAT, POINTER, TEMP.
        :param index: The index of a register in the segment.
        """

        # The constant segment is virtual - It doesn't exists.
        if segment == vg.VM_SEGMENT_CONSTANT:
            raise ValueError(POP_TO_CONST_MSG)

        self.__output.write(POP + SPACE + segment + SPACE + str(index) +
                            NEWLINE)

    def writeArithmetic(self, command, isBinary=True):
        """
        Writes a VM arithmetic command.
        :param command: ADD, SUB, NEG, EQ, GT, LT, AND, OR, NOT
        """
        translate = vg.JACK_2_VM_ARITHMETIC_UNARY
        if isBinary:
            translate = vg.JACK_2_VM_ARITHMETIC_BINARY
        vm_command = translate[command]
        self.__output.write(vm_command + NEWLINE)

    def writeLabel(self, label):
        """
        Writes a VM label command.
        :param label: Label's name.
        """
        self.__output.write(LABEL + SPACE + label + NEWLINE)

    def writeGoto(self, label):
        """
        Writes a VM label command.
        :param label: Label's name.
        """
        self.__output.write(GOTO + SPACE + label + NEWLINE)

    def writeIf(self, label):
        """
        Writes a VM If-goto command.
        :param label: The name of the label into which the instruction pointer
        will jump to if the condition is fulfilled.
        """
        self.__output.write(IF_GOTO + SPACE + label + NEWLINE)

    def writeCall(self, name, n_args):
        """
        Writes a VM call command.
        :param name: The name of the called function.
        :param n_args: The number of arguments of the called function.
        """
        #funcname = self.__funcname(name)
        self.__output.write(
            CALL + SPACE + name + SPACE + str(n_args) + NEWLINE)

    def writeFunction(self, name, n_locals):
        """
        Writes a VM function command.
        :param name: The name of the declared function.
        :param n_locals: The number of local variables it has.
        """
        #funcname = self.__funcname(name)
        self.__output.write(
            FUNCTION_DEC + SPACE + name + SPACE + str(n_locals) + NEWLINE)

    def writeReturn(self, isVoid=False):
        """
        Writes a VM return command.
        """
        # Void functions forced to push 0 before returning
        # (Non-void already pushed return value before reaching here)
        if (isVoid):
            self.__output.write(PUSH_VOID + NEWLINE)
        # Write 'return' statement
        self.__output.write(RETURN + NEWLINE)

    def writeSymbol(self, symbol):
        """
        Writes the VM command matching the given symbol
        :param symbol: a Jack symbol
        """
        if symbol in vg.JACK_2_VM_ARITHMETIC_BINARY:
           self.writeArithmetic(symbol, True)
        elif symbol in vg.RE_BRACKETS_SQUARE_RIGHT:  # x[1] --> ]=add
           self.writeArithmetic(vg.RE_PLUS, True)

    def close(self):
        """
        Closes the output file.
        """
        self.__output.close()

########################
# TESTS - REMOVE LATER #
########################

def main():
    """
    Tests for this class.
    """
    VMW = VMWriter("potato")
    VMW.writePush("potato", 2)


if __name__ == '__main__':
    main()
