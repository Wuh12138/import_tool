class Matcher:
    def __init__(self):
        self.matcher_list = list()

    @staticmethod
    def is_greater(a, b):
        if a > b:
            return True
        else:
            return False

    @staticmethod
    def is_greater_equal(a, b):
        if a >= b:
            return True
        else:
            return False

    @staticmethod
    def is_smaller(a, b):
        if a < b:
            return True
        else:
            return False

    @staticmethod
    def is_smaller_equal(a, b):
        if a <= b:
            return True
        else:
            return False

    @staticmethod
    def is_content(a: str, b: str):
        if b in a:
            return True
        else:
            return False

    def generate_match_list(self, requirements: str):
        pass

    def add_to_list(self, symbol:str):
        match symbol:
            case ">":
                self.matcher_list.append(self.is_greater)
            case ">=":
                self.matcher_list.append(self.is_greater_equal)
            case "<":
                self.matcher_list.append(self.is_smaller)
            case "<=":
                self.matcher_list.append(self.is_smaller_equal)
            case "(":
                self.matcher_list.append(self.is_content)

if __name__ == "__main__":
    m = Matcher()
    m.add_to_list(">")
    for i in m.matcher_list:
        print(i(1, 2))
