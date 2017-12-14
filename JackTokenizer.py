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
TOKEN_TYPE_KEYWORD = "keyword"
TOKEN_TYPE_SYMBOL = "symbol"
TOKEN_TYPE_INTEGER = "integerConstant"
TOKEN_TYPE_STRING = "stringConstant"
TOKEN_TYPE_IDENTIFIER = "identifier"
TOKEN_TYPE_NONE = "TOKEN_TYPE_NONE"
TOKEN_NONE = "TOKEN_NONE"
TOKEN_ROOT = "tokens"

class JackTokenizer:
    def __init__(self, in_file):
        """
     Reads the (already open) input file/stream and gets ready to tokenize it.
     :param in_file: The input jack file descriptor.
     """
        self.__in_file = in_file
        self.__code = EMPTY_STRING  # Default value
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
        for line in self.__in_file:
            self.__code += line
        # Shtik for compensating the fact we don't handle the last token
        # in the file when iterating while hasMoreTokens().
        # Purposely planting a garbage last token which will not be read:
        #self.__code += TOKEN_NONE

    ##################
    # PUBLIC METHODS #
    ##################

    def hasMoreTokens(self):
        """
        Do we have more tokens in the input?
        :return: True if there are more tokens.
        """
        return self.__code != EMPTY_STRING

    def __tokenize_match(self, match):
        """
        Set the given match as the current token and strip it off from the
        jack code.
        :param match: result of re.match() on some lexical element
        """
        # Extract matched token
        self.__current_token = self.__code[:match.end()]
        # Strip it from the file
        self.__code = self.__code[match.end():]

    def advance(self):
        """
        Gets the next token from the input and makes it the current token.
        This method should only be called if hasMoreTokens() is true.
        Initially there is no current token.
        """

        # Remove Comments and Spaces
        whitespace_or_comment = RE_WHITESPACE_AND_COMMENTS_COMPILED.match(
            self.__code)
        if whitespace_or_comment:
            self.__code = self.__code[whitespace_or_comment.endpos:]

        if not self.hasMoreTokens():
            # RazK: TODO: This is going to be a bug, handle what happens if
            # the last part of the code is a comment.
            return

        # Match current token
        keyword = RE_KEYWORDS_COMPILED.match(self.__code)
        if keyword:
            self.__current_token_type = TOKEN_TYPE_KEYWORD
            self.__tokenize_match(keyword)
            return

        symbol = RE_SYMBOLS_COMPILED.match(self.__code)
        if symbol:
            self.__current_token_type = TOKEN_TYPE_SYMBOL
            self.__tokenize_match(symbol)
            return

        integer = RE_INTEGER_COMPILED.match(self.__code)
        if integer:
            self.__current_token_type = TOKEN_TYPE_INTEGER
            self.__tokenize_match(integer)
            return

        string = RE_STRING_COMPILED.match(self.__code)
        if string:
            self.__current_token_type = TOKEN_TYPE_STRING
            self.__tokenize_match(string)
            return

        identifier = RE_IDENTIDIER_COMPILED.match(self.__code)
        if identifier:
            self.__current_token_type = TOKEN_TYPE_IDENTIFIER
            self.__tokenize_match(identifier)
            return

        # No match?

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
        if self.__current_token not in KEYWORDS:
            raise ValueError("Current token {} is not a keyword".format(
                self.__current_token))
        return self.__current_token

    def symbol(self):
        """
        Returns the character which is the current token. Should be called only
        when tokenType() is SYMBOL.
        """
        if self.__current_token not in SYMBOLS:
            raise ValueError("Current token {} is not a symbol".format(
                self.__current_token))
        if self.__current_token in RE_SYMBOLS_SPECIAL_TRANSLATE:
            return RE_SYMBOLS_SPECIAL_TRANSLATE[self.__current_token]
        return self.__current_token

    def identifier(self):
        """
        Returns the identifier which is the current token. Should be called
        only when tokenType() is IDENTIFIER.
        """
        if not RE_IDENTIDIER_COMPILED.match(self.__current_token):
            raise ValueError("Current token {} is not an identifier".format(
                self.__current_token))
        return self.__current_token

    def intVal(self):
        """
        Returns the integer value of the current token. Should be called only
        when tokenType() is INT_CONST.
        """
        if not RE_INTEGER_COMPILED.match(self.__current_token):
            raise ValueError("Current token {} is not an integer".format(
                self.__current_token))
        return self.__current_token

    def stringVal(self):
        """
        Returns the string value of the current token, without the double
        quotes. Should be called only when tokenType() is STRING_CONST.
        """
        if not RE_STRING_COMPILED.match(self.__current_token):
            raise ValueError("Current token {} is not a string".format(
                self.__current_token))
        # Replace special characters
        string = self.__current_token
        for special in RE_SYMBOLS_SPECIAL_TRANSLATE:
            string = string.replace(special, RE_SYMBOLS_SPECIAL_TRANSLATE[
                special])
        # Remove the opening and closing " characters.
        return string[1:-1]

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
