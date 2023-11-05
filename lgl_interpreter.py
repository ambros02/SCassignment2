import os
import sys
import json


class LGL_Interpreter:


    def __init__(self, source_code: list) -> None:
        self.code = source_code


    def interpret() -> None:
        pass


    def interpret_dictionary() -> None:
        pass




def main() -> None:

    assert len(sys.argv) == 2, "bad usage: python lgl_language.py <filename>.gsc"

    parent_path = os.path.dirname(__file__)
    
    with open(os.path.join(parent_path,sys.argv[1]),'r') as file:
        source_lines = json.load(file)
        
    german_interpreter = LGL_Interpreter(source_lines)
    german_interpreter.interpret()

if __name__ == "__main__":
    main()