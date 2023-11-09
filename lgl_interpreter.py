import os
import sys
import json


class LGL_Interpreter:

    """This class provides an interpreter for the little german language.
        It features multiple basic functionalities aswell as lists and dictionaries"""

    def __init__(self, source_code: list) -> None:
        """Initialize a new LGL_Interpreter with a gsc file contents. Set up a dictionary to keep track of all dictionaries"""
        self.code = source_code
        self.dictionaries = {}
        self.variables = {}

    def run(self) -> None:
        """Run the programm. This will start the execution of the gsc code by taking the contents of the gsc file and then give it to the interpret method"""

        assert len(self.code) > 0, "there is no code to read"
        #case only one operation is in the file
        if not isinstance(self.code[0],list):
            self.code = [self.code]

        for instruction in self.code:
            self.interpret(instruction)

        

    def clean(self, line:list,low_limit:int = 0,high_limit:int = None) -> list:
        """Interpret the nested functions in the lines, define low and high limit for the range of elements which should be interpreted if possible"""

        for index,value in enumerate(line[low_limit:high_limit]):
            if isinstance(value,list):
                line[index+low_limit] = self.interpret(value)
        return line


    def interpret(self, instruction:list) -> None:
        """Tnterpret the functions """    
          
        if isinstance(instruction,(int,str)):
            return instruction
        
        elif isinstance(instruction[0],list):
            instruction[0] = self.interpret(instruction[0])

        assert "interpret_" + str(instruction[0]) in dir(self.__class__), f"Unknown operation: {instruction[0]}"
        #get the name of the method to execute then get the actual method
        method_name = [method for method in dir(self.__class__) if method.replace("interpret_","") == instruction[0]][0]
        method_body = getattr(self, method_name)
        return method_body(instruction)
        

    def interpret_dictionary_erstellen(self, line:list) -> None:
        """This method creates dictionaries for the lgl and stores them in the self.dictionaries variable of the object"""

        assert len(line) == 2, "bad usage of dictionary erstellen: Try ['dictionary_erstellen','<name>']"
        line = self.clean(line)
        assert isinstance(line[1],str), "the dictionary name should be a string"
        self.dictionaries[line[1]] = {}
        return None
    
    def interpret_dictionary_setzen(self, line:list) -> None:
        """This method sets a value to a key in a dictionary. If the dictionary does not exist an error is thrown. If the key already exists the value is overwriten"""

        assert len(line) == 4, "bad usage of dictionary setzen: Try ['dictionary_setzen','<name>','<key:str/int>','<value>']"
        line = self.clean(line,high_limit=3)

        assert line[1] in self.dictionaries.keys(), "the dictionary of which you want to set values does not exist"
        assert isinstance(line[2],(int,str)), "the key of the dictionary needs to be a string or an int"

        self.dictionaries[line[1]][line[2]] = line[3]
        return None

    def interpret_seq(self, instructions:list) -> None:
        """This method allows for the lgl to use seq to specify a sequence of instructions following"""

        assert len(instructions) > 1, "The sequence has nothing inside it"
        for code in instructions[1:]:
            self.interpret(code)
        return None

    def interpret_dictionary_finden(self, line:list):
        """This method allows the user to find values in the dictionary by a specified key. If the name or key does not exist an error is thrown, otherwhise the value is returned"""

        assert len(line) == 3, "bad usage of dictionary finden: Try ['dictionary_finden','<name>','<key:str/int>']"
        line = self.clean(line)
        assert line[1] in self.dictionaries.keys(), "the dictionary of which you want to find values does not exist"
        assert line[2] in self.dictionaries[line[1]].keys(), f"the key {line[2]} does not exist in dictionary {line[1]}"

        value = self.dictionaries[line[1]][line[2]]

        return value


    def interpret_dictionary_verbinden(self,line:list) -> None:
        """This method allows to merge two dictionaries. Either a new name is specified and both directories get merged there, or the second dictionary gets appended to the first.
        If there are key conflicts the keys of the first dictionary will be used"""

        assert len(line) in (3,4), "bad usage of dictionary verbinden: Try ['dictionary_verbinden','<name>','<name>','<newname:optional>']"

        line = self.clean(line)

        for name in line[1:]:
            assert(isinstance(name,str)), "names of dictionaries must be strings"
        for name in line[1:2]:
            assert name in self.dictionaries.keys(), f"the dictionary {name} does not exist"

        #case where second dictionary gets merged into first
        if len(line) == 3:
            for key,value in self.dictionaries[line[2]].items():
                if key not in self.dictionaries[line[1]].keys():
                    self.dictionaries[line[1]][key] = value
            del self.dictionaries[line[2]]
        #case where both dictionary go into a new one
        else:
            self.dictionaries[line[3]] = self.dictionaries[line[1]].copy()
            for key,value in self.dictionaries[line[2]].items():
                if key not in self.dictionaries[line[1]].keys():
                    self.dictionaries[line[3]][key] = value
            del self.dictionaries[line[1]]
            del self.dictionaries[line[2]]
        return None


    def interpret_variable_setzen(self,line:list) -> None:
        """this method allows to store variables into the self.variables dictionary"""
        assert len(line) == 3, "bad usage of variable setzen try: ['variable_setzen','<name:str>',<value>]"
        line = self.clean(line)
        assert isinstance(line[1],str), "variable name needs to be a string"
        assert not isinstance(line[2],(list,dict)), "list and dictionaries should not be stored in a variable but in a dictionary or list"
        self.variables[line[1]] = line[2]

        return None


    def interpret_variable_holen(self,line:list):
        """this method allows to access stored variables"""
        assert len(line) == 2, "bad usage of variable_holen try: ['variable_holen','<name:str>']"
        line = self.clean(line)
        assert isinstance(line[1],str), "varaible name needs to be a string"
        assert line[1] in self.variables.keys()

        return self.variables[line[1]]

def main() -> None:
    """get the user input gsc file create a LGL_Interpreter object and start to run the code"""

    assert len(sys.argv) == 2, "bad usage: python lgl_language.py <filename>.gsc"

    parent_path = os.path.dirname(__file__)
    
    #gsc files are located in the same directory as this file
    with open(os.path.join(parent_path,sys.argv[1]),'r') as file:
        source_lines = json.load(file)
    assert isinstance(source_lines, list), "badly formatted code"
        
    german_interpreter = LGL_Interpreter(source_lines)
    german_interpreter.run()

if __name__ == "__main__":
    main()