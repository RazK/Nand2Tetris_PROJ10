##############################################################################
# This is the Jack Tokenizer, it removes all comments and white space from the
#  input stream and breaks it into Jacklanguage tokens,
# as specified by the Jack grammar.
##############################################################################

############
# CONSTANTS
############
DEFAULT_IN_FILE_LINE = ""

##########
# IMPORTS
##########
from JackGrammar import *

class JackTokenizer:
    def __init__(self, in_file):
        """
     Opens the input file/stream and gets ready to tokenize it.
     :param in_file: The input jack file.
     """
        self.__in_file_name = in_file
        self.__in_file_line = DEFAULT_IN_FILE_LINE
        self.__readFileToLine()

    ##################
    # PRIVATE METHODS
    ##################

    def __readFileToLine(self):
        """
        Reads the source file text into one line.
        :return:
        """
        with open(self.__in_file_name) as file:
            for line in file:
                test = "noy babe12"
                new = test.replace(RE_WHITESPACES, "")
                print(new)
                self.__in_file_line += line

    def __removeSpacesAndComments(self):
        """
        Removes spaces and comments from source file.
        :return:
        """
        pass

    #################
    # PUBLIC METHODS
    #################

    def hasMoreTokens(self):
        """
        Do we have more tokens in the input?
        :return: True if tere are more tokens.
        """
        pass

    def advance(self):
        """
        Gets the next token from the input and makes it the current token.
        This method should only be called if hasMoreTokens() is true.
        Initially there is no current token.
        :return: KEYWORD, SYMBOL, IDENTIFIER, INT_CONST, STRING_CONST
        """
        pass

    def keyWord(self):
        """
        Returns the keyword which is the current token. Should be called only
        when tokenType() is KEYWORD.
        :return: CLASS, METHOD, FUNCTION, CONSTRUCTOR, INT, BOOLEAN, CHAR,
        VOID, VAR, STATIC, FIELD, LET, DO, IF, ELSE, WHILE, RETURN, TRUE,
        FALSE, NULL, THIS.
        """
        pass

    def symbol(self):
        """
        Returns the character which is the current token. Should be called only
        when tokenType() is SYMBOL.
        """
        pass

    def identifier(self):
        """
        Returns the identifier which is the current token. Should be called
        only when tokenType() is IDENTIFIER.
        """
        pass

    def intVal(self):
        """
        Returns the integer value of the current token. Should be called only
        when tokenType() is INT_CONST.
        """
        pass

    def stringVal(self):
        """
        Returns the string value of the current token, without the double
        quotes. Should be called only when tokenType() is STRING_CONST.
        """
        pass


#################
# TESTS and shit
#################

def main():
    """
    Tests for the Tokenizer module
    """

    tok = JackTokenizer("file.jack")


if __name__ == "__main__":
    main()
