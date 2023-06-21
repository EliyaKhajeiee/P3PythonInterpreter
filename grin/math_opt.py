import grin

class Math_Operations:
    def __init__(self, value1, value2):
        self.value1 = value1
        self.value2 = value2

    def add(self):
        """Function for adding two values numbers"""
        try:
            return self.value1 + self.value2
        except TypeError as e:
            print("You can't do this operation on these values")
            quit()

    def add_string(self):
        """Function to add two strings together"""
        return str(self.value1) + str(self.value2)

    def subtract(self):
        """Function to subtract two values"""
        try:
            return self.value1 - self.value2
        except TypeError as e:
            print("You can't do this operation on these values")
            quit()

    def multiply(self):
        """Function to multiply two numbers"""
        return self.value1 * self.value2

    def multiply_string(self):
        """Function to multiply two strings"""
        if isinstance(self.value2, str):
            return self.value1 * str(self.value2)
        else:
            if isinstance(self.value1,str):
                return str(self.value1) * self.value2

    def divide(self):
        """Function to divide two values"""
        try:
            if self.value2 != 0:
                return self.value1 / self.value2
            else:
                raise ValueError("Division by zero is not allowed")
        except TypeError as e:
            print("You can't do this operation on these values")
            quit()

    def divide_ints(self):
        """Function to divide two ints"""
        try:
            if self.value2 != 0:
                return self.value1 // self.value2
            else:
                raise ValueError("Division by zero is not allowed")
        except TypeError as e:
            print("You can't do this operation on these values")
            quit()

    def evaluate_comparison(self, operator):
        """Function to check the evalation of the operator and give back true or false"""
        if operator == "<=":
            try:
                return self.value1 <= self.value2
            except TypeError as e:
                print("You can't do this operation on these values")
                quit()
        elif operator == "<":
            try:
                return self.value1 < self.value2
            except TypeError as e:
                print("You can't do this operation on these values")
                quit()
        elif operator == "=":
            try:
                return self.value1 == self.value2
            except TypeError as e:
                print("You can't do this operation on these values")
                quit()
        elif operator == ">":
            try:
                return self.value1 > self.value2
            except TypeError as e:
                print("You can't do this operation on these values")
                quit()
        elif operator == ">=":
            try:
                return self.value1 >= self.value2
            except TypeError as e:
                print("You can't do this operation on these values")
                quit()
        elif operator == "<>":
            try:
                return self.value1 != self.value2
            except TypeError as e:
                print("You can't do this operation on these values")
                quit()
        else:
            raise ValueError("Invalid operator")



__all__ = ["Math_Operations"]






