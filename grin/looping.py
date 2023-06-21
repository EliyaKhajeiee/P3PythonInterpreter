import grin


# noinspection PyTypeChecker
class Loop_de_loop:
    """Class to take all my things"""
    def __init__(self):
        self.tokens = []
        self.print_values_list = []
        self.new_tokens = []
        self.line_count = 0
        self.i_and_line_count = {}
        self.result_dict = {}
        self.chunk_checker = {}
        self.return_line = 0

    def is_float(self,val): #checls to see if it is a float
        """Function to check if a number is a float"""
        try:
            float(val)
            return True
        except ValueError:
            return False

    def while_loop(self):
        """Start of my code to grab all the inputs"""
        self.line_count = 1
        i=0
        while True:
            inp = input()
            inplist = [inp]
            token_list = (grin.parse(inplist))
            for token in token_list: #give us everything in terms of tokens, i starts at 0
                for token_app in token:
                    self.tokens.append({
                        "kind": token_app.kind(),
                        "text": token_app.text(),
                        "location": token_app.location(),
                        "value": token_app.value(),
                        "line": self.line_count,
                        "i" : int(i)
                    })
                    i+=1
                self.i_and_line_count.setdefault(self.line_count, []).append(int(i))
                self.result_dict = {key: len(value) for key, value in self.i_and_line_count.items()} #{1:3, 2:5} ETC
            self.line_count += 1
            if inp.replace(" ","") == ".":
                break
        self.print_values()
        self.the_end()

    def print_values(self): #will print all the values where it is, need to fix for when a b
        """My long function to parse through everything and add it to a function that prints whenever needed"""
        variables = {}
        var_changes = {}
        label_dict = {}
        i = 0
        return_list = []

        for index, each_one in enumerate(self.tokens):  # This will give me label_dict being {1: "LINE1"}
            if each_one['kind'] == grin.GrinTokenKind.COLON:
                if index + 1 < len(self.tokens):
                    label_dict[each_one['line']] = self.tokens[index - 1]['value']
                    self.chunk_checker[self.tokens[index - 1]['value']] = False  # SETS WHATEVER VALUE OF CHUNK TO FALSE

        while i < len(self.tokens): #i starts at 0,
            if self.tokens[i]['kind'] == grin.GrinTokenKind.GOTO or self.tokens[i]['kind'] == grin.GrinTokenKind.GOSUB: #GOTO "CZZ"
                if len(self.tokens) == 2 and self.tokens[i+1]['value'] != 1:
                    print("You can't jump to something that doesn't exist silly")
                    quit()
                if len(self.tokens) == 2 and self.tokens[i+1]['value'] == 1:
                    quit()
                try:
                    if self.tokens[i+2]['kind'] == grin.GrinTokenKind.IF:
                        comparator = self.tokens[i+4]['text']
                        val_if_1 = 0
                        val_if_2 = 0
                        if self.tokens[i+5]['kind'] == grin.GrinTokenKind.LITERAL_INTEGER or self.tokens[i+5]['kind'] == grin.GrinTokenKind.LITERAL_FLOAT:
                            val_if_1 = self.tokens[i+3]['value']
                        if self.tokens[i+3]['kind'] == grin.GrinTokenKind.IDENTIFIER:
                            lookup_var = self.tokens[i + 3]['value']
                            if lookup_var in variables:
                                val_if_1 = variables[lookup_var]
                        if self.tokens[i+3]['kind'] == grin.GrinTokenKind.LITERAL_STRING:
                            val_if_1 = self.tokens[i + 3]['value']

                        if self.tokens[i+5]['kind'] == grin.GrinTokenKind.LITERAL_INTEGER or self.tokens[i+5]['kind'] == grin.GrinTokenKind.LITERAL_FLOAT:
                            val_if_2 = self.tokens[i + 5]['value']
                        if self.tokens[i+5]['kind'] == grin.GrinTokenKind.IDENTIFIER:
                            lookup_var = self.tokens[i + 5]['value']
                            if lookup_var in variables:
                                val_if_2 = variables[lookup_var]
                        if self.tokens[i+5]['kind'] == grin.GrinTokenKind.LITERAL_STRING:
                            val_if_2 = self.tokens[i + 5]['value']
                        boo = grin.Math_Operations(val_if_1,val_if_2)
                        if_checker = boo.evaluate_comparison(comparator)
                        if if_checker:
                            pass
                        else:
                            i+= 5
                except IndexError:
                    pass
                if self.tokens[i]['kind'] == grin.GrinTokenKind.GOSUB:
                    cl = self.tokens[i]['line']
                    return_list.append(cl+1)

                identifier_token = self.tokens[i+1]
                if identifier_token['kind'] == grin.GrinTokenKind.LITERAL_INTEGER: #WHEN IT IS AN INT
                    lines_to_skip = identifier_token['value']
                    if lines_to_skip == 0:
                        print("You can't GOTO 0")
                        quit()
                    current_line = self.tokens[i]['line']
                    total_lines_forward = (lines_to_skip + current_line)
                    if abs(total_lines_forward) >= self.line_count:
                        print("You can't jump that far")
                        quit()
                    for each_one_check in self.tokens:
                        if each_one_check['line'] == total_lines_forward:
                            i = each_one_check['i']
                            break

                if identifier_token['kind'] == grin.GrinTokenKind.LITERAL_STRING or identifier_token['kind'] == grin.GrinTokenKind.IDENTIFIER: #WHEN IT IS A STRING OR LITERAL
                    id_checker = None
                    if identifier_token['kind'] == grin.GrinTokenKind.IDENTIFIER:
                        for var_name, var_value in variables.items():
                            if var_name == identifier_token['value']:
                                id_checker = var_value  # GIVES US THE ID,VALUE, for num is a number
                    if type(id_checker) == int: #WHEN LITERAL IS A INT
                        lines_to_skip = int(id_checker)
                        if lines_to_skip == 0:
                            print("You can't GOTO 0")
                            quit()
                        current_line = self.tokens[i]['line']
                        total_lines_forward = (lines_to_skip + current_line)
                        if abs(total_lines_forward) >= self.line_count:
                            print("You can't jump that far")
                            quit()
                        for each_one_check in self.tokens:
                            if each_one_check['line'] == total_lines_forward:
                                i = each_one_check['i']
                                break

                    elif type(id_checker) == str or identifier_token['kind'] == grin.GrinTokenKind.LITERAL_STRING:
                        if len(label_dict) == 0: #IF THERE ARE NO VZ: ETC
                            i+=2
                            print("You can't go to a label that doesnt exist")
                            quit()
                        else:
                            for line_num,checker in label_dict.items(): #WHERE THE CZ IS {2: "CZ"}
                                if str(checker) == str(self.tokens[i+1]['value']) or checker == id_checker: #WORKS TO HERE, NEED TO INITIALIZE THE LINES, CZZ == CZZ
                                    for each_check in self.tokens:
                                        if int(each_check['line']) == line_num: #gives the start i of the NEXT LINE AFTER THE
                                            i = each_check['i'] #Correct, i starts at 0 remember
                                            self.chunk_checker[checker] = True #{CZ: TRUE
                                            break
                                    break
                            else: #IF NOTHING IS FOUND BY THE GOTO #
                                i += 2
                                print("You can't goto something that doesn't exist")
                                quit()


            elif self.tokens[i]['kind'] == grin.GrinTokenKind.LET:
                identifier_token = self.tokens[i + 1]
                literal_token = self.tokens[i + 2]
                if literal_token['kind'] == grin.GrinTokenKind.IDENTIFIER:
                    found_match = False
                    for var_name, var_value in variables.items():
                        if var_name == literal_token['value']:
                            var_changes[identifier_token['text']] = var_value
                            found_match = True
                            break
                    if not found_match:
                        var_changes[identifier_token['text']] = 0
                else:
                    variables[identifier_token['text']] = literal_token['value']
                i += 3
                variables.update(var_changes)

            elif self.tokens[i]['kind'] == grin.GrinTokenKind.END:
                i += 1
                break

            elif self.tokens[i]['kind'] == grin.GrinTokenKind.RETURN:
                try:
                    gosub_found = False
                    for token in self.tokens:
                        if token['kind'] == grin.GrinTokenKind.GOSUB:
                            gosub_found = True
                            break
                    if not gosub_found:
                        print("There are no GoSub statements, can't use return")
                        quit()
                except:
                    pass
                for tok in self.tokens:
                    try:
                        if return_list[-1] == tok['line']:
                            i = tok['i']
                            return_list.pop(-1)
                            break
                    except IndexError:
                        quit()#QUIT

            elif self.tokens[i]['kind'] == grin.GrinTokenKind.ADD: #WORKS
                identifier_token = self.tokens[i + 1]
                literal_token = self.tokens[i + 2]
                val1 = 0
                val2 = 0
                if not variables:
                    if identifier_token['kind'] == grin.GrinTokenKind.IDENTIFIER:
                        val1 = 0
                    if literal_token['kind'] == grin.GrinTokenKind.IDENTIFIER:
                        val2 = 0
                    if literal_token['kind'] == grin.GrinTokenKind.LITERAL_FLOAT or literal_token[
                        'kind'] == grin.GrinTokenKind.LITERAL_INTEGER:
                        val2 = literal_token['value']
                    if literal_token['kind'] == grin.GrinTokenKind.LITERAL_STRING:
                        val2 = literal_token['value']

                else:
                    for var in variables: #first one has to be a var
                        if identifier_token['text'] == var and identifier_token['kind'] == grin.GrinTokenKind.IDENTIFIER: #first one identifyer
                            val1 = variables[var]
                        if literal_token['text'] == var and literal_token['kind'] == grin.GrinTokenKind.IDENTIFIER: #second one identiyer
                            val2 = variables[var]
                        if literal_token['kind'] == grin.GrinTokenKind.LITERAL_FLOAT or \
                                literal_token['kind'] == grin.GrinTokenKind.LITERAL_INTEGER:
                            val2 = literal_token['value']
                        if literal_token['kind'] == grin.GrinTokenKind.LITERAL_STRING:
                            val2 = literal_token['value']

                if type(val1) == str and type(val2) == str:
                    boo = grin.Math_Operations(str(val1), str(val2))
                    newval_add = boo.add_string()
                else:
                    boo = grin.Math_Operations(val1, val2)
                    newval_add = boo.add()
                variables[identifier_token['text']] = newval_add
                i += 3

            elif self.tokens[i]['kind'] == grin.GrinTokenKind.SUB:
                identifier_token = self.tokens[i + 1]
                literal_token = self.tokens[i + 2]
                val1 = 0
                val2 = 0
                if not variables:
                    if identifier_token['kind'] == grin.GrinTokenKind.IDENTIFIER:
                        val1 = 0
                    if literal_token['kind'] == grin.GrinTokenKind.IDENTIFIER:
                        val2 = 0
                    if literal_token['kind'] == grin.GrinTokenKind.LITERAL_FLOAT or literal_token[
                        'kind'] == grin.GrinTokenKind.LITERAL_INTEGER:
                        val2 = literal_token['value']
                else:
                    for var in variables: #first one has to be a var
                        if identifier_token['text'] == var and identifier_token['kind'] == grin.GrinTokenKind.IDENTIFIER: #first one identifyer
                            val1 = variables[var]
                        if literal_token['text'] == var and literal_token['kind'] == grin.GrinTokenKind.IDENTIFIER: #second one identiyer
                            val2 = variables[var]
                        if literal_token['kind'] == grin.GrinTokenKind.LITERAL_FLOAT or \
                                literal_token['kind'] == grin.GrinTokenKind.LITERAL_INTEGER:
                            val2 = literal_token['value']

                boo = grin.Math_Operations(val1, val2)
                newval_sub = boo.subtract()
                variables[identifier_token['text']] = newval_sub
                i += 3

            elif self.tokens[i]['kind'] == grin.GrinTokenKind.MULT:
                identifier_token = self.tokens[i + 1]
                literal_token = self.tokens[i + 2]
                val1 = 0
                val2 = 0
                if not variables:
                    if identifier_token['kind'] == grin.GrinTokenKind.IDENTIFIER:
                        val1 = 0
                    if literal_token['kind'] == grin.GrinTokenKind.IDENTIFIER:
                        val2 = 0
                    if literal_token['kind'] == grin.GrinTokenKind.LITERAL_FLOAT or literal_token[
                        'kind'] == grin.GrinTokenKind.LITERAL_INTEGER:
                        val2 = literal_token['value']
                    if literal_token['kind'] == grin.GrinTokenKind.LITERAL_STRING:
                        val2 = literal_token['value']
                else:
                    for var in variables:
                        if identifier_token['text'] == var and identifier_token['kind'] == grin.GrinTokenKind.IDENTIFIER: #first one identifier
                            val1 = variables[var]
                        if literal_token['text'] == var and literal_token['kind'] == grin.GrinTokenKind.IDENTIFIER: #second one identifier
                            val2 = variables[var]
                        if literal_token['kind'] == grin.GrinTokenKind.LITERAL_FLOAT or \
                                literal_token['kind'] == grin.GrinTokenKind.LITERAL_INTEGER:
                            val2 = literal_token['value']
                        if literal_token['kind'] == grin.GrinTokenKind.LITERAL_STRING:
                            val2 = literal_token['value']

                if type(val1) == str or type(val2) == str:
                    boo = grin.Math_Operations(val1, val2)
                    newval_mult = boo.multiply_string()
                else:
                    boo = grin.Math_Operations(val1, val2)
                    newval_mult  = boo.multiply()
                variables[identifier_token['text']] = newval_mult
                i += 3

            elif self.tokens[i]['kind'] == grin.GrinTokenKind.DIV:
                identifier_token = self.tokens[i + 1]
                literal_token = self.tokens[i + 2]
                val1 = 0
                val2 = 0
                if not variables:
                    if identifier_token['kind'] == grin.GrinTokenKind.IDENTIFIER:
                        val1 = 0
                    if literal_token['kind'] == grin.GrinTokenKind.IDENTIFIER:
                        val2 = 0
                    if literal_token['kind'] == grin.GrinTokenKind.LITERAL_FLOAT or literal_token[
                        'kind'] == grin.GrinTokenKind.LITERAL_INTEGER:
                        val2 = literal_token['value']
                else:
                    for var in variables: #first one has to be a var
                        if identifier_token['text'] == var and identifier_token['kind'] == grin.GrinTokenKind.IDENTIFIER: #first one identifyer
                            val1 = variables[var]
                        if literal_token['text'] == var and literal_token['kind'] == grin.GrinTokenKind.IDENTIFIER: #second one identiyer
                            val2 = variables[var]
                        if literal_token['kind'] == grin.GrinTokenKind.LITERAL_FLOAT or \
                                literal_token['kind'] == grin.GrinTokenKind.LITERAL_INTEGER:
                            val2 = literal_token['value']

                boo = grin.Math_Operations(val1, val2)
                if type(val1) == int and type(val2) == int:
                    newval_div = boo.divide_ints()
                else:
                    newval_div = boo.divide()

                variables[identifier_token['text']] = newval_div
                i += 3

            elif self.tokens[i]['kind'] == grin.GrinTokenKind.INNUM: #KIND IS INNUM (INNUM X LITERAL)
                var = self.tokens[i + 1]['value']
                identifier_token = self.tokens[i+1]
                user_inp = input()
                user_inp = user_inp.replace(" ","")
                if user_inp.startswith('-') and user_inp[1:].isdigit():
                    var_changes[var] = -int(user_inp[1:])  # Negative integer input
                elif user_inp.startswith('-') and self.is_float(user_inp[1:]):
                    var_changes[var] = -float(user_inp[1:])  # Negative float input
                elif user_inp.isdigit():
                    var_changes[var] = int(user_inp)  # Positive integer input
                elif self.is_float(user_inp):
                    var_changes[var] = float(user_inp)
                else:
                    print("Invalid input. Expected a number.")
                    quit()
                if identifier_token['kind'] == grin.GrinTokenKind.LITERAL_STRING:
                    print("This is not a valid input for INNUM") #SOMEHOW HIT IF STATEMENT
                    quit()
                variables.update(var_changes)
                i += 2


            elif self.tokens[i]['kind'] == grin.GrinTokenKind.INSTR:
                var = self.tokens[i + 1]['value']
                user_inp = input()
                if isinstance(user_inp,str):
                    var_changes[var] = str(user_inp)
                variables.update(var_changes)
                i += 2

            elif self.tokens[i]['kind'] == grin.GrinTokenKind.PRINT:
                var = self.tokens[i + 1]['value']
                identifier_token = self.tokens[i+1]
                if var in variables and identifier_token['kind'] == grin.GrinTokenKind.IDENTIFIER:
                    print(variables[var])
                else:
                    if identifier_token['kind'] == grin.GrinTokenKind.LITERAL_STRING:
                        print(identifier_token['value'])
                    if identifier_token['kind'] == grin.GrinTokenKind.IDENTIFIER:
                        print(0)
                if type(var) == int or type(var) == float:
                    print(var)
                i += 2

            elif self.tokens[i]['kind'] == grin.GrinTokenKind.IDENTIFIER:#INSTANCES WHERE IT IS A CHUNK TO START, WITH GOTO OR GOSUB
                if self.tokens[i+1]['kind'] == grin.GrinTokenKind.COLON:
                    if self.chunk_checker[self.tokens[i]['value']]:
                        i+=2
                    else: #instances where the value is not equal to anything, but it is a colon
                        line_number = (self.tokens[i]['line'])
                        for line_num, i_val in self.result_dict.items():
                            if line_number == line_num:
                                i += i_val
                                break
            else:
                i += 1

    def the_end(self):
        """Function for printing the end values whenever needed"""
        for x in self.print_values_list:
            print(x)
__all__ = [
    Loop_de_loop.__name__,]
