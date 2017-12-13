##############################################################################
# This is the Jack Tokenizer, it removes all comments and white space from the
#  input stream and breaks it into Jacklanguage tokens,
# as specified by the Jack grammar.
##############################################################################
from JackGrammar import *
import re

#############
# CONSTANTS #
#############
EMPTY_STRING = ""
NO_MORE_TOKENS_ERROR_MSG = "There are no more tokens."
TOKEN_TYPE_NONE = "none"
TOKEN_TYPE_KEYWORD = "TOKEN_KEYWORD"
TOKEN_TYPE_SYMBOL = "TOKEN_SYMBOL"
TOKEN_TYPE_INTEGER = "TOKEN_INTEGER"
TOKEN_TYPE_STRING = "TOKEN_STRING"
TOKEN_TYPE_IDENTIFIER = "TOKEN_IDENTIFIER"
TOKEN_NONE = "TOKEN_NONE"


class JackTokenizer:
    def __init__(self, in_file):
        """
     Opens the input file/stream and gets ready to tokenize it.
     :param in_file: The input jack file.
     """
        self.__in_file_name = in_file
        self.__jack = EMPTY_STRING  # Default value
        self.__current_token_type = TOKEN_TYPE_NONE  # Default value
        self.__current_token = TOKEN_NONE
        self.__readFileToString()

    ###################
    # PRIVATE METHODS #
    ###################

    def __readFileToString(self):
        """
        Reads the source file text into a string.
        """
        with open(self.__in_file_name) as file:
            for line in file:
                self.__jack += line

    ##################
    # PUBLIC METHODS #
    ##################

    def hasMoreTokens(self):
        """
        Do we have more tokens in the input?
        :return: True if there are more tokens.
        """
        return self.__jack != EMPTY_STRING

    def __tokenize_match(self, match):
        """
        Set the given match as the current token and strip it off from the
        jack code.
        :param match: result of re.match() on some lexical element
        """
        # Extract matched token
        self.__current_token = self.__jack[:match.end()]
        # Strip it from the file
        self.__jack = self.__jack[match.end():]

    def advance(self):
        """
        Gets the next token from the input and makes it the current token.
        This method should only be called if hasMoreTokens() is true.
        Initially there is no current token.
        """

        # Remove Comments and Spaces
        whitespace_or_comment = RE_WHITESPACE_AND_COMMENTS_COMPILED.match(
            self.__jack)
        if whitespace_or_comment:
            self.__jack = self.__jack[whitespace_or_comment.endpos:]

        if not self.hasMoreTokens():
            # RazK: TODO: This is going to be a bug, handle what happens if
            # the last part of the code is a comment.
            return

        # Match current token
        keyword = RE_KEYWORDS_COMPILED.match(self.__jack)
        if keyword:
            self.__current_token_type = TOKEN_TYPE_KEYWORD
            self.__tokenize_match(keyword)
            return

        symbol = RE_SYMBOLS_COMPILED.match(self.__jack)
        if symbol:
            self.__current_token_type = TOKEN_TYPE_SYMBOL
            self.__tokenize_match(symbol)
            return

        integer = RE_INTEGER_COMPILED.match(self.__jack)
        if integer:
            self.__current_token_type = TOKEN_TYPE_INTEGER
            self.__tokenize_match(integer)
            return

        string = RE_STRING_COMPILED.match(self.__jack)
        if string:
            self.__current_token_type = TOKEN_TYPE_STRING
            self.__tokenize_match(string)
            return

        identifier = RE_IDENTIDIER_COMPILED.match(self.__jack)
        if identifier:
            self.__current_token_type = TOKEN_TYPE_IDENTIFIER
            self.__tokenize_match(identifier)
            return

    def tokenType(self):
        """
        Returns the type of the current token.
        :return: KEYWORD, SYMBOL, IDENTIFIER, INT_CONST, STRING_CONST
        """
        return self.__current_token_type

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

    def debugPring(self):
        print("{} : {}".format(self.__current_token_type,
                               self.__current_token))


#################
# TESTS and shit
#################

def main():
    """
    Tests for the Tokenizer module
    """
    tok = JackTokenizer("testing/advance.jack")
    while tok.hasMoreTokens():
        tok.debugPring()
        tok.advance()


if __name__ == "__main__":
    main()
