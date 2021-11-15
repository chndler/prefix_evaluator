import sys
import re

class FunctionError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

class PrefixSyntax(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)


# setPosition
#   purpose:
#       Sets the value for the global current parse position to the passed
#       value
#   parameters:
#       val - value to set the current parse position to
#   retuns:
#       N/A
def setPosition(val):
    global cur_pars_pos
    cur_pars_pos = val

# prettyPrintTokens
#   purpose:
#       Prints the parsed token array in a readable format for testing
#   parameters:
#       token_array - array containing the tokens to be printed
#   retuns:
#       N/A
def prettyPrintTokens(token_array):
    if token_array != None:
        print("  ", end="")
        for token in token_array:
            print(token, end=" ")
        print()
    else:
        print("Error: token_array is empty")

# prefixReader
#   purpose:
#       Reads each text line in the input file (which was passed as a command
#       argument).  For each text line:
#           - It should print the prefix text string, preceded by "> "
#           - It  must tokenize the expression using Python's regex
#           - Reset the global current parsing pos to 0
#           - It should invoke prefixEval passing the token array.  If that
#               function returned successfully (i.e., it didn't raise an
#               exception), it should print the value returned from prefixEval.
#           - It should provide a try… except block which prints errors.  After
#               printing an error do not exit the program.
#   parameters:
#       line - text line in the input file
#   retuns:
#       N/A
def prefixReader(line):
    regObj = re.compile(r'(\w+|>|<|\(|\)|\+|\-|\*|\/)')
    print(">", line, end="")
    token_array = regObj.findall(line)
    leftparens = 0
    rightparens = 0
    try:
        for token in token_array:
            if token == '(':
                leftparens += 1
            if token == ')':
                rightparens += 1
        if (leftparens > rightparens):
            raise PrefixSyntax("Missing closing ')'")
    except (FunctionError, PrefixSyntax) as e:
        print(e.args[1])
        return

    #prettyPrintTokens(token_array)
    # resetting the global current parsing pos to 0
    setPosition(0)
    try:
        return_val = prefixEval(token_array)
        print(return_val)
    except (FunctionError, PrefixSyntax) as e:
        print(e.args[1])



# prefixEval
#   purpose:
#       passed a token array and modifies the global current parsing pos. Based
#       on the token at the current position, if if is a:
#           "(" it is evaluating a function. Should treat the next token as a
#           function name.  It now needs to evaluate the arguments for that
#           function:
#               - Assume the function has only two arguments
#               - It should invoke prefixEval to get the value of each argument
#                   (appropriately advancing the global current parsing position).
#               - It should advance the global current parsing position past its
#                   corresponding ")".
#               - It should invoke evalOperator passing the function and
#                   arguments and return that value as prefixEval's functional
#                   value.
#       Uses another function to actually apply the function to the operands.
#       Supports the following functions: +, -, *, /, >, <, and, or
#       advances the global current parsing position to the position immediately
#       after its expression
#   parameters:
#       token_array -
#   returns:
#       evaluated expression's value
def prefixEval(token_array):
    if token_array[cur_pars_pos] == '(':
        setPosition(cur_pars_pos+1)
        functionName = token_array[cur_pars_pos]
        setPosition(cur_pars_pos+1)
        try:
            argument1 = prefixEval(token_array)
        except:
            raise
        setPosition(cur_pars_pos+1)
        try:
            argument2 = prefixEval(token_array)
            if token_array[cur_pars_pos+1].isdigit():
                raise FunctionError()
        except (FunctionError, PrefixSyntax) as e:
            if type(e) == type(FunctionError()):
                raise FunctionError('Incorrect number of operands - must be 2 for \''
                                            + functionName + '\'')
            raise e
        if functionName == '/': # forces integer division
            functionName = functionName + "/"
        try:
            val = eval(str(argument1) + ' ' + functionName + ' ' + str(argument2))
        except:
            print("Trailing exception")
        return val

    if token_array[cur_pars_pos] == ')':
        if cur_pars_pos != len(token_array) - 1:
            setPosition(cur_pars_pos+1)
            val2 = prefixEval(token_array)
            return val2
        else:
            raise FunctionError()

    # at this point we're only looking for ints
    # only looking for ints past token_array[0]
    if cur_pars_pos > 0:
        isDigit = token_array[cur_pars_pos].isdigit()
        if isDigit == False:
            raise PrefixSyntax("Expected int found: '" +
                                token_array[cur_pars_pos] + "'")
        temp = int(token_array[cur_pars_pos])
        return temp

# main
#   purpose:
#       drives general functionality of program. Opens file, then
#       for each line in file performs the necessary actions
def main():
    file = open(sys.argv[1], "r")
    teams = {}
    for line in file:
        prefixReader(line)
    file.close()

# call main and execute
if __name__ == "__main__":main()
