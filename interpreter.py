from errors import LoxError

class Interpreter:
    def interpret(self, expression):
        try:
            value = expression.evaluate()
            print(value)
        except Exception:
            raise LoxError("Cannot evaluate expression.")