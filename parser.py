from token import TokenType
from errors import LoxError, ParseError

class Binary:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def evaluate(self):
        def isEqual(a, right):
            if a is None and b is Null:
                return True
            if a is None:
                return False
            return a == b

        left = self.left.evaluate()
        right = self.right.evaluate()

        match self.operator.type:
            case TokenType.MINUS:
                return float(self.left) - float(self.right)
            case TokenType.SLASH:
                return float(self.left) / float(self.right)
            case TokenType.STAR:
                return float(self.left) * float(self.right)
            case TokenType.PLUS:
                if type(left) is float and type(right) is float:
                    return float(left) + float(right)
                
                if type(left) is str and type(right) is str:
                    return f"{str(left)}{str(right)}"
            case TokenType.LESS:
                return float(left) < float(right)
            case TokenType.LESS_EQUAL:
                return float(left) <= float(right)
            case TokenType.GREATER:
                return float(left) > float(right)
            case TokenType.GREATER_EQUAL:
                return float(left) >= float(right)
            case TokenType.BANG_EQUAL:
                return not self.isEqual(left, right)
            case TokenType.EQUAL_EQUAL:
                return self.isEqual(left, right)


        # Unreachable
        return None


class Grouping:
    def __init__(self, expression):
        self.expression = expression

    def evaluate(self):
        return self.expression.evaluate()


class Literal:
    def __init__(self, value):
        self.value = value

    def evaluate(self):
        return self.value


class Unary:
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

    def evaluate(self):
        def isTruthy(ob):
            if ob is True or ob is False:
                return ob
            raise ParseError("Can only use ! on boolean values")

        match self.operator.type:
            case TokenType.MINUS:
                return -1 * float(self.right)
            case TokenType.BANG:
                return not(isTruthy(self.right))

        # Unreachable 
        return None


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    # Helper methods
    def advance(self):
        if not self.isAtEnd():
            self.current += 1
        
        return self.previous()

    def match(self, *types):
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False

    def check(self, type):
        if self.isAtEnd():
            return False
        return self.peek().type == type

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]

    def isAtEnd(self):
        return self.peek().type == TokenType.EOF

    def consume(self, type, message):
        if self.check(type):
            return self.advance()

        raise ParseError(message)

    def parse(self):
        try:
            return self.expression()
        except ParseError as error:
            print(error)
            return None

    def expression(self):
        return self.equality()
    
    def equality(self):
        expr = self.comparison()

        while self.match(TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)

        return expr

    def comparison(self):
        expr = self.term()

        while self.match(
            TokenType.LESS, 
            TokenType.LESS_EQUAL,
            TokenType.GREATER,
            TokenType.GREATER_EQUAL
        ):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)

        return expr

    def term(self):
        expr = self.factor()

        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)

        return expr

    def factor(self):
        expr = self.unary()

        while self.match(TokenType.STAR, TokenType.SLASH):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)

        return expr

    def unary(self):
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return self.Unary(operator, right)

        return self.primary()

    def primary(self):
        if self.match(TokenType.FALSE):
            return Literal(False)
        if self.match(TokenType.TRUE):
            return Literal(True)
        if self.match(TokenType.NIL):
            return Literal(None)

        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().literal)

        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)
 