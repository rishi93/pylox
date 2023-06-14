from token import Token, TokenType, keywords
from errors import LoxError

class Scanner:
    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0

    def isAtEnd(self):
        return self.current >= len(self.source)

    def advance(self):
        c = self.source[self.current]
        self.current += 1
        return c

    def peek(self):
        if self.isAtEnd():
            return "\0"
        return self.source[self.current]

    def peekNext(self):
        if current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]
        

    def match(self, expected):
        if self.isAtEnd():
            return False
        
        if self.source[self.current] != expected:
            return False

        # If it is the expected character, then consume it
        self.current += 1
        return True
    
    def addToken(self, type, literal=None):
        lexeme = self.source[self.start:self.current]
        self.tokens.append(Token(type, lexeme, literal))

    def string(self):
        # if the next character is not the enclosing quotes
        # And also if the next character is not the end of the file
        while self.peek() != '"' and not self.isAtEnd():
            self.advance()

        if self.isAtEnd():
            raise LoxError("Unterminated string")

        # Consume the enclosing quote
        self.advance()

        value = self.source[self.start + 1:self.current - 1]
        self.addToken(TokenType.STRING, value)

    def number(self):
        while self.isDigit(self.peek()):
            self.advance()
        
        # Look for a fractional part
        if self.peek() == "." and self.isDigit(self.peekNext()):
            # Consume the decimal point
            self.advance()
            # Consume the numbers after the decimal point
            while self.isDigit(self.peek()):
                self.advance()

        lexeme = self.source[self.start:self.current]
        value = float(lexeme)
        self.addToken(TokenType.NUMBER, float(lexeme))

    def isDigit(self, c):
        return c >= '0' and c <= '9'

    def isAlpha(self, c):
        return (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z')  or (c == '_')

    def isAlphaNumeric(self, c):
        return self.isAlpha(c) or self.isDigit(c)

    def identifier(self):
        while self.isAlphaNumeric(self.peek()):
            self.advance()

        text = self.source[self.start:self.current]
        type = keywords.get(text, None)

        if type is None:
            type = TokenType.IDENTIFIER

        self.addToken(type)

    def scanToken(self):
        c = self.advance()

        match c:
            # All single character tokens
            case "(":
                self.addToken(TokenType.LEFT_PAREN)
            case ")":
                self.addToken(TokenType.RIGHT_PAREN)
            case "{":
                self.addToken(TokenType.LEFT_BRACE)
            case "}":
                self.addToken(TokenType.RIGHT_BRACE)
            case ",":
                self.addToken(TokenType.COMMA)
            case ".":
                self.addToken(TokenType.DOT)
            case "-":
                self.addToken(TokenType.MINUS)
            case "+":
                self.addToken(TokenType.PLUS)
            case ";":
                self.addToken(TokenType.SEMICOLON)
            case "*":
                self.addToken(TokenType.STAR)
            case "/":
                self.addToken(TokenType.SLASH)

            # All two character tokens
            case "!":
                self.addToken(TokenType.BANG_EQUAL if self.match("=") else TokenType.BANG)
            case "=":
                self.addToken(TokenType.EQUAL_EQUAL if self.match("=") else TokenType.EQUAL)
            case "<":
                self.addToken(TokenType.LESS_EQUAL if self.match("=") else TokenType.LESS)
            case ">":
                self.addToken(TokenType.GREATER_EQUAL if self.match("=") else TokenType.GREATER)
            
            # Skip whitespace
            case " " | "\r" | "\t" | "\n":
                pass

            # String literals
            case '"':
                self.string()

            case _:
                if self.isDigit(c):
                    self.number()
                elif self.isAlpha(c):
                    self.identifier()
                else:
                    raise LoxError("Unexpected character")

    def scanTokens(self):
        while not self.isAtEnd():
            self.start = self.current
            self.scanToken()

        # Add a EOF token after reading the entire source code
        self.tokens.append(Token(TokenType.EOF, "", None))
        return self.tokens