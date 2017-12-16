###############################################################################
# The analyzer program operates on a given source, where source is either a
# file name of the form Xxx.jack or a directory name containing one or more
# such files. For each source Xxx.jack file, the analyzer goes through the
# following logic:
#   1.  Create a JackTokenizer from the Xxx.jack input file;
#   2.  Create an output file called Xxx.xml and prepare it for writing;
#   3.  Use the CompilationEngine to compile the input JackTokenizer into the
#       output file.
###############################################################################
import os
import sys
from CompilationEngine import *
from JackTokenizer import *

SOURCE_EXTENSION = ".jack"
OUTPUT_EXTENSION = ".xml"
DEFAULT_SOURCE_FILE = "..\\Square.jack"

XML_DELIM_TERMINAL = " "
XML_DELIM_NON_TERMINAL = "\n"
TOKEN_ROOT_START = "<tokens>\n"
TOKEN_ROOT_END = "</tokens>\n"


def main(path):
    """
    Translates the .jack source file (or files) in the given path into a
    .xml output file.
    """

    # Collect all sources files to tokenize
    sources = None

    # Path is a single source file?
    if os.path.isfile(path):
        if not path.endswith(SOURCE_EXTENSION):
            raise FileNotFoundError("Invalid extension '{}' for source file "
                                    "(expected '{}')"
                                    .format(path, SOURCE_EXTENSION))
        sources = [path]

    # Path is a directory with source files?
    elif os.path.isdir(path):
        sources = [os.path.join(path, f) for f in os.listdir(path) if
                   f.endswith(SOURCE_EXTENSION)]

    if sources == None:
        raise FileNotFoundError("No {} files found to translate!"
                                .format(SOURCE_EXTENSION))

    # Assemble all files
    analyze(sources)


def analyze(sources):
    """
    For each source Xxx.jack file, the analyzer goes through the
    following logic:
    1.  Creates an output file called Xxx.xml and prepare it for writing;
    2.  Use the CompilationEngine to compile the input JackTokenizer into the
        output file.
    :param sources: list of names of sources to compile.
    """

    # Parse each source and translates to it the output:
    for sourcename in sources:
        base = os.path.splitext(sourcename)[0]
        outname = base + OUTPUT_EXTENSION

        # Open source for analyzing, output file for writing
        with open(sourcename, 'r') as source, open(outname, 'w') as output:
            # Create a CompilationEngine from the Xxx.jack input file
            engine = CompilationEngine(source, output)
            engine.compileClass()


if (__name__ == "__main__"):
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main(DEFAULT_SOURCE_FILE)




        ############
        # OLD CODE #
        ############

        # def addToken(outfile, token, token_type, isTerminal=True):
        #     delimiter = XML_DELIM_TERMINAL if isTerminal else XML_DELIM_NON_TERMINAL
        #     tag = "<{0}>{1}{2}{1}</{0}>\n".format(token_type, delimiter, token)
        #     outfile.write(tag)
        #
        # def analyze(sources):
        #     """
        #     For each source Xxx.jack file, the analyzer goes through the
        #     following logic:
        #     1.  Create a JackTokenizer from the Xxx.jack input file;
        #     2.  Create an output file called Xxx.xml and prepare it for writing;
        #     3.  Use the CompilationEngine to compile the input JackTokenizer into the
        #         output file.
        #     :param sources: list of names of sources to compile.
        #     """
        #
        #     Parse each source and translate to it the output
        # for sourcename in sources:
        #     base = os.path.splitext(sourcename)[0]
        #     outname = base + OUTPUT_EXTENSION
        #
        #     Open source for analyzing, output file for writing
        # with open(sourcename, 'r') as source, open(outname, 'w') as output:
        #     Create a JackTokenizer from the Xxx.jack input file
        # tokenizer = JackTokenizer(source)
        # output.write(TOKEN_ROOT_START)
        #
        # Parse each command line in the source and translate
        # while (tokenizer.hasMoreTokens()):
        #     Use the CompilationEngine to compile the input
        #     JackTokenizer into the output file
        # tokenizer.advance()
        # token_type = tokenizer.tokenType()
        # if token_type == TOKEN_TYPE_KEYWORD:
        #     keyword = tokenizer.keyWord()
        #     addToken(output, keyword, TOKEN_TYPE_KEYWORD)
        # elif token_type == TOKEN_TYPE_SYMBOL:
        #     symbol = tokenizer.symbol()
        #     addToken(output, symbol, TOKEN_TYPE_SYMBOL)
        # elif token_type == TOKEN_TYPE_INTEGER:
        #     integer = tokenizer.intVal()
        #     addToken(output, integer, TOKEN_TYPE_INTEGER)
        # elif token_type == TOKEN_TYPE_STRING:
        #     string = tokenizer.stringVal()
        #     addToken(output, string, TOKEN_TYPE_STRING)
        # elif token_type == TOKEN_TYPE_IDENTIFIER:
        #     identifier = tokenizer.identifier()
        #     addToken(output, identifier, TOKEN_TYPE_IDENTIFIER)
        # output.write(TOKEN_ROOT_END)
