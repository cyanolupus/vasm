from sys import argv, stderr
from parser import Parser

def main():
    with open(argv[1], "r") as f:
        code = f.read()

    try:
        instructions = Parser().parse(code)
    except Exception as e:
        print(e, file=stderr)
        exit(1)

    for instruction in instructions:
        print(instruction)

if __name__ == "__main__":
    main()
        