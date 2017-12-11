# The analyzer program operates on a given source, where source is either a
# file name of the form Xxx.jack or a directory name containing one or more
# such files. For each source Xxx.jack file, the analyzer goes through the
# following logic:
#   1.  Create a JackTokenizer from the Xxx.jack input file;
#   2.  Create an output file called Xxx.xml and prepare it for writing;
#   3.  Use the CompilationEngine to compile the input JackTokenizer into the
#       output file.

import os
import sys
from JackTokenizer import JackTokenizer

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
        with open(sourcename, 'r') as source, open (outname, 'w') as output:
            # Create a JackTokenizer from the Xxx.jack input file
            tokenizer = JackTokenizer(source)

            # Parse each command line in the source and translate
            while (tokenizer.hasMoreCommands()):
                # Use the CompilationEngine to compile the input
                # JackTokenizer into the output file
                pass # TODO
                tokenizer.advance()

        # Flush output to file
        output.flush()

if (__name__ == "__main__"):
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main(DEFAULT_SOURCE_FILE)