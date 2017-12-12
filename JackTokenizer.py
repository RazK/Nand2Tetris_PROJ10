##############################################################################
# This is the Jack Tokenizer, it removes all comments and white space from the
#  input stream and breaks it into Jacklanguage tokens,
# as specified by the Jack grammar.
##############################################################################

#############
# CONSTANTS #
#############
EMPTY_STRING = ""
NO_MORE_TOKENS_ERROR_MSG = "There are no more tokens."

###########
# IMPORTS #
###########
from JackGrammar import *
import re


class JackTokenizer:
    def __init__(self, in_file):
        """
     Opens the input file/stream and gets ready to tokenize it.
     :param in_file: The input jack file.
     """
        self.__in_file_name = in_file
        self.__in_file_line = EMPTY_STRING  # Default value
        self.__current_token = EMPTY_STRING  # Default value

        self.__readFileToLine()
        self.__removeSpacesAndComments()

    ###################
    # PRIVATE METHODS #
    ###################

    def __readFileToLine(self):
        """
        Reads the source file text into one line.
        """
        with open(self.__in_file_name) as file:
            for line in file:
                line = re.sub(RE_END_OF_LINE_COMMENT, EMPTY_STRING, line)
                self.__in_file_line += line

    def __removeSpacesAndComments(self):
        """
        Removes spaces and comments from source file.
        """
        self.__in_file_line = re.sub(RE_WHITESPACES, EMPTY_STRING,
                                     self.__in_file_line)
        self.__in_file_line = re.sub(RE_IN_LINE_COMMENTS, EMPTY_STRING,
                                     self.__in_file_line)

    ##################
    # PUBLIC METHODS #
    ##################

    def hasMoreTokens(self):
        """
        Do we have more tokens in the input?
        :return: True if there are more tokens.
        """
        return not self.__in_file_line == EMPTY_STRING

    def advance(self):
        """
        Gets the next token from the input and makes it the current token.
        This method should only be called if hasMoreTokens() is true.
        Initially there is no current token.
        """
        if self.hasMoreTokens():
            pass
        else:
            raise ValueError(NO_MORE_TOKENS_ERROR_MSG)

    def tokenType(self):
        """
        Returns the type of the current token.
        :return: KEYWORD, SYMBOL, IDENTIFIER, INT_CONST, STRING_CONST
        """

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
