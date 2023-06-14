import sys

from scanner import Scanner
from parser import Parser
from interpreter import Interpreter

from errors import LoxError

def runFile(file):
    print(f"Running lox file: {file}")

def runConsole():
    print("Running lox console...")
    while True:
        try:
            line = input("> ")
            run(line)
        except LoxError as e:
            print(e)
        except (EOFError, KeyboardInterrupt):
            print("Closed lox console.")
            break 

def run(source):
    # First step is scanning
    # Taking a list of characters and
    # turning them into a list of tokens
    scanner = Scanner(source)
    tokens = scanner.scanTokens()

    for token in tokens:
        # Just print the tokens for now
        print(token)

    # Second step is parsing
    # Taking a list of tokens and
    # turning them into abstract syntax trees
    parser = Parser(tokens)
    expression = parser.parse()

    # The final step is simply evaluating the ASTs
    interpreter = Interpreter()
    interpreter.interpret(expression)


if __name__ == "__main__":
    # Running a console
    if len(sys.argv) == 1:
        runConsole()
    elif len(sys.argv) == 2:
        file = sys.argv[1]
        runFile(file)
    else:
        print("Usage: python lox.py [script]")