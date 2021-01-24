#!/usr/bin/python3
# Extension: arbitrary number of arguments supported by using list to store
#   function arguments and using get_next_arg() method to append arbitrary
#   number of next arguments into list           


import sys


class ParsingError(Exception):
    pass


class Expression:
    def __init__(self, raw_text):
        self.raw_text = raw_text
        self.split_text = raw_text.split(" ")
        self.type = self.get_type()

        self.args = []

        if self.type != "int":
            self.get_args()

    # get_type(self) determines whether the Expression is INTEGER, ADD,
    #   or MULTIPLY
    def get_type(self):
        if self.raw_text[0] != "(":
            return "int"
        elif self.split_text[0][1:] == "add":
            return "add"
        elif self.split_text[0][1:] == "multiply":
            return "multiply"
        else:
            raise ParsingError("Error: Expression type not supported")

    # get_args(self) finds all the arguments in a function Expresion
    def get_args(self):
        if len(self.split_text) > 1:
            self.args.append(self.get_next_arg())
            self.get_args()

    # is_function(self, raw_text) determines whether raw text is a
    #   function call
    def is_function(self, raw_text):
        return raw_text[0] == "("

    # get_next_arg(self) finds the next argument in a function Expression
    def get_next_arg(self):
        if self.type == "int":
            raise ParsingError("Error: can't get first arg of int")
        elif not self.is_function(self.split_text[1]):
            return self.get_next_int()
        else:
            return Expression(self.get_nested_exp())

    # get_next_int(self) finds the next integer argument in a function
    #   Expression
    def get_next_int(self):
        last_arg = self.split_text[1][-1] == ")"

        if last_arg:
            new_exp = Expression(self.split_text[1][:-1])
            self.split_text[0] = self.split_text[0] + ")"
        else:
            new_exp = Expression(self.split_text[1])

        del self.split_text[1]
        self.raw_text = " ".join(self.split_text)

        return new_exp

    # get_nested_exp(self) finds the nested expression and removes it from the
    #   raw_text and split_text fields
    def get_nested_exp(self):
        rest_split_text = self.split_text[1:]
        joined_text = " ".join(rest_split_text)
        joined_text = joined_text[1:]
        open_brackets = 0

        for i in range(len(joined_text)):
            current_char = joined_text[i]

            if current_char == "(":
                open_brackets += 1
            elif current_char == ")":
                if open_brackets == 0:
                    self.raw_text = self.split_text[0] + joined_text[i+1:]
                    self.split_text = self.raw_text.split(" ")
                    return "(" + joined_text[:i+1]
                else:
                    open_brackets -= 1

    # get_value(self) evaluates the Expression
    def get_value(self):
        if self.type == "int":
            return int(self.raw_text)
        elif self.type == "add":
            return_sum = 0

            for i in self.args:
                return_sum += i.get_value()

            return return_sum
        elif self.type == "multiply":
            return_product = 1

            for i in self.args:
                return_product *= i.get_value()

            return return_product
        else:
           raise ParsingError("Error: invalid Expression type")


def main(args):
    exp1 = Expression(args[0])
    print(exp1.get_value())


if __name__ == "__main__":
    main(sys.argv[1:])
