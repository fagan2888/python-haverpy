def simpleparser(expression):
# To use the operatorPrecedence helper:
#   1.  Define the "atom" operand term of the grammar.
#       For this simple grammar, the smallest operand is either
#       and integer or a variable.  This will be the first argument
#       to the operatorPrecedence method.
#   2.  Define a list of tuples for each level of operator
#       precendence.  Each tuple is of the form
#       (opExpr, numTerms, rightLeftAssoc, parseAction), where
#       - opExpr is the pyparsing expression for the operator;
#          may also be a string, which will be converted to a Literal
#       - numTerms is the number of terms for this operator (must
#          be 1 or 2)
#       - rightLeftAssoc is the indicator whether the operator is
#          right or left associative, using the pyparsing-defined
#          constants opAssoc.RIGHT and opAssoc.LEFT.
#       - parseAction is the parse action to be associated with 
#          expressions matching this operator expression (the
#          parse action tuple member may be omitted)
#   3.  Call operatorPrecedence passing the operand expression and
#       the operator precedence list, and save the returned value
#       as the generated pyparsing expression.  You can then use
#       this expression to parse input strings, or incorporate it
#       into a larger, more complex grammar.
#
# Copyright 2006, by Paul McGuire
# Updated 2019, Santiago Sordo-Palacios
# http://www.ccp4.ac.uk/dist/checkout/pyparsing-2.0.1/examples/simpleArith.py  

    integer = Word(nums).setParseAction(lambda t:int(t[0]))
    variable = Word(alphanums)
    operand = integer | variable

    signop = oneOf('+ -')
    multop = oneOf('* /')
    plusop = oneOf('+ -')

    expr = operatorPrecedence( operand,
    [("!", 1, opAssoc.LEFT),
     ("^", 2, opAssoc.RIGHT),
     (signop, 1, opAssoc.RIGHT),
     (multop, 2, opAssoc.LEFT),
     (plusop, 2, opAssoc.LEFT),]
    )

    parsed = expr.parseString(expression)
    return(parsed)
