class Stdin(object):

    def read_value(self):
        value = int(input("Enter a value (0-999)"))
        return value


class Stdout(object):

    def write(self, value):
        print(value)
