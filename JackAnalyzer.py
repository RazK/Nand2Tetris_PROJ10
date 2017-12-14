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
from JackTokenizer import *
import xml.etree.cElementTree as ET

SOURCE_EXTENSION = ".jack"
OUTPUT_EXTENSION = ".xml"
DEFAULT_SOURCE_FILE = "..\\Square.jack"

def main(path):
    """
    Translate the .jack source file (or files) in the given path into a token
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

def addToken(parent, token, token_type):
    ET.SubElement(parent, token_type).text = " {} ".format(token)

def analyze(sources):
    """
    For each source Xxx.jack file, the analyzer goes through the
    following logic:
    1.  Create a JackTokenizer from the Xxx.jack input file;
    2.  Create an output file called Xxx.xml and prepare it for writing;
    3.  Use the CompilationEngine to compile the input JackTokenizer into the
        output file.
    :param sources: list of names of sources to compile.
    """

    # Parse each source and translate to it the output
    for sourcename in sources:
        base = os.path.splitext(sourcename)[0]
        outname = base + OUTPUT_EXTENSION

        # Open source for analyzing, output file for writing
        with open(sourcename, 'r') as source:
            # Create a JackTokenizer from the Xxx.jack input file
            tokenizer = JackTokenizer(source)
            root = ET.Element(TOKEN_ROOT)

            # Parse each command line in the source and translate
            while (tokenizer.hasMoreTokens()):
                # Use the CompilationEngine to compile the input
                # JackTokenizer into the output file
                tokenizer.advance()
                token_type = tokenizer.tokenType()
                if token_type == TOKEN_TYPE_KEYWORD:
                    keyword = tokenizer.keyWord()
                    addToken(root, keyword, TOKEN_TYPE_KEYWORD)
                elif token_type == TOKEN_TYPE_SYMBOL:
                    symbol = tokenizer.symbol()
                    addToken(root, symbol, TOKEN_TYPE_SYMBOL)
                elif token_type == TOKEN_TYPE_INTEGER:
                    integer = tokenizer.intVal()
                    addToken(root, integer, TOKEN_TYPE_INTEGER)
                elif token_type == TOKEN_TYPE_STRING:
                    string = tokenizer.stringVal()
                    addToken(root, string, TOKEN_TYPE_STRING)
                elif token_type == TOKEN_TYPE_IDENTIFIER:
                    identifier = tokenizer.identifier()
                    addToken(root, identifier, TOKEN_TYPE_IDENTIFIER)

        # Write XML to file
        tree = ET.ElementTree(root)
        tree.write(outname)

if (__name__ == "__main__"):
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main(DEFAULT_SOURCE_FILE)