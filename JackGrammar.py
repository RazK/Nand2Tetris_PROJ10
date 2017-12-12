###############################################################################
# Contains regular expressions and other utilities related to the grammar of
# the Jack Programming Language.
###############################################################################

#######################
# REGULAR EXPRESSIONS #
#######################

# COMMENTS AND WHITE SPACES:
RE_WHITESPACES = r'\s'  # https://regex101.com/r/evyXL2/1
RE_END_OF_LINE_COMMENT = "//.*"  # https://regex101.com/r/PbLBSc/1
RE_IN_LINE_COMMENTS = "/\*.*?\*/"  #https://regex101.com/r/PbLBSc/2

