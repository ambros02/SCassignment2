import os
import sys
import json


class LGL_Interpreter:


    def __init__(self, source_code: list) -> None:
        self.code = source_code
        self.dictionaries= {}

    def run(self) -> None:
        assert len(self.code) > 0, "there is no code to read"
        """ if self.code[0] == "seq":
            for line in self.code[1:]:
                self.interpret(line)

        else:
            self.interpret(self.code)"""
        if not isinstance(self.code[0],list):
            self.code = [self.code]

        for instruction in self.code:
            self.interpret(instruction)

        



    def interpret(self, instruction:list) -> None:
        if isinstance(instruction,(int,str)):
            return instruction

        assert "interpret_" + instruction[0] in dir(self.__class__), f"Unknown operation: {instruction[0]}"
        method_name = [method for method in dir(self.__class__) if method.replace("interpret_","") == instruction[0]][0]
        my_method = getattr(self, method_name)
        return my_method(instruction)
        

    def interpret_dictionary_erstellen(self, line:list) -> None:
        
        if isinstance(line[1],list):
            line[1] = self.interpret(line[1])

        assert len(line) == 2, "bad usage of dictionary erstellen: Try ['dictionary_erstellen','<name>']"

        assert isinstance(line[1],str), "the dictionary name should be a string"
        self.dictionaries[line[1]] = {}
        return None
    
    def interpret_dictionary_setzen(self, line:list) -> None:
        
        assert len(line) == 4, "bad usage of dictionary setzen: Try ['dictionary_setzen','<name>','<key:str/int>','<value>']"

        for index,value in enumerate(line[1:3]):
            if isinstance(value,list):
                line[index+1] = self.interpret(line)
                

        assert line[1] in self.dictionaries.keys(), "the dictionary of which you want to set values does not exist"
        assert isinstance(line[2],(int,str)), "the key of the dictionary needs to be a string or an int"

        self.dictionaries[line[1]][line[2]] = line[3]
        return None

    def interpret_seq(self, instructions:list) -> None:
        assert len(instructions) > 1, "The sequence has nothing inside it"
        for code in instructions[1:]:
            self.interpret(code)
        return None

    def interpret_dictionary_finden(self, line:list):

        assert len(line) == 3, "bad usage of dictionary finden: Try ['dictionary_finden','<name>','<key:str/int>']"
        assert line[1] in self.dictionaries.keys(), "the dictionary of which you want to find values does not exist"
        assert line[2] in self.dictionaries[line[1]].keys(), f"the key {line[2]} does not exist in dictionary {line[1]}"

        value = self.dictionaries[line[1]][line[2]]

        return value


    def interpret_dictionary_verbinden(self,line:list) -> None:

        assert len(line) in (3,4), "bad usage of dictionary verbinden: Try ['dictionary_verbinden','<name>','<name>','<newname:optional>']"
        for name in line[1:]:
            assert(isinstance(name,str)), "names of dictionaries must be strings"
        for name in line[1:2]:
            assert name in self.dictionaries.keys(), f"the dictionary {name} does not exist"

        if len(line) == 3:
            for key,value in self.dictionaries[line[2]].items():
                if key not in self.dictionaries[line[1]].keys():
                    self.dictionaries[line[1]][key] = value
            del self.dictionaries[line[2]]
        else:
            self.dictionaries[line[3]] = self.dictionaries[line[1]].copy()
            for key,value in self.dictionaries[line[2]].items():
                if key not in self.dictionaries[line[1]].keys():
                    self.dictionaries[line[3]][key] = value
            del self.dictionaries[line[1]]
            del self.dictionaries[line[2]]
        return None



def main() -> None:

    assert len(sys.argv) == 2, "bad usage: python lgl_language.py <filename>.gsc"

    parent_path = os.path.dirname(__file__)
    
    with open(os.path.join(parent_path,sys.argv[1]),'r') as file:
        source_lines = json.load(file)
    assert isinstance(source_lines, list), "badly formatted code"
        
    german_interpreter = LGL_Interpreter(source_lines)
    german_interpreter.run()
    print(german_interpreter.dictionaries)

if __name__ == "__main__":
    main()