############################################################
# This class writes VM commands into a file.
# It encapsulates the VM command syntax.
############################################################

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

# SEGMENTS
CONSTANT = "constant"

# ERRORS MSGs
POP_TO_CONST_MSG = "Pop to constant segment is forbidden"

# MORE
SPACE = " "


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

    def __init__(self, output_file_name):
        """
        Create a new VMWriter object, creates a new output file and prepares it
        for writing
        """
        self.__output = open(output_file_name, 'w')

    ##################
    # PUBLIC METHODS #
    ##################

    def writePush(self, segment, index):
        """
        Writes a VM push command.
        :param segment: CONST, ARG, LOCAL, STATIC, THIS, THAT, POINTER, TEMP.
        :param index: The index of a register in the segment.
        """
        self.__output.write(PUSH + SPACE + segment + SPACE + str(index))

    def writePop(self, segment, index):
        """
        Writes a VM pop command.
        :param segment: CONST, ARG, LOCAL, STATIC, THIS, THAT, POINTER, TEMP.
        :param index: The index of a register in the segment.
        """

        # The constant segment is virtual - It doesn't exists.
        if segment == CONSTANT:
            raise ValueError(POP_TO_CONST_MSG)

        self.__output.write(POP + SPACE + segment + SPACE + str(index))

    def writeArithmetic(self, command):
        """
        Writes a VM arithmetic command.
        :param command: ADD, SUB, NEG, EQ, GT, LT, AND, OR, NOT
        """
        self.__output.write(command)

    def writeLabel(self, label):
        """
        Writes a VM label command.
        :param label: Label's name.
        """
        self.__output.write(LABEL + SPACE + label)

    def writeGoto(self, label):
        """
        Writes a VM label command.
        :param label: Label's name.
        """
        self.__output.write(GOTO + SPACE + label)

    def writeIf(self, label):
        """
        Writes a VM If-goto command.
        :param label: The name of the label into which the instruction pointer
        will jump to if the condition is fulfilled.
        """
        self.__output.write(IF_GOTO + SPACE + label)

    def writeCall(self, name, n_args):
        """
        Writes a VM call command.
        :param name: The name of the called function.
        :param n_args: The number of arguments of the called function.
        """
        self.__output.write(CALL + SPACE + name + SPACE + str(n_args))

    def writeFunction(self, name, n_locals):
        """
        Writes a VM function command.
        :param name: The name of the declared function.
        :param n_locals: The number of local variables it has.
        """
        self.__output.write(
            FUNCTION_DEC + SPACE + name + SPACE + str(n_locals))

    def writeReturn(self):
        """
        Writes a VM return command.
        """
        self.__output.write(RETURN)

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
