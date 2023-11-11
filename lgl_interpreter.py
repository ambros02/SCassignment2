import os
import sys
import json
import math


class LGL_Interpreter:

    """This class provides an interpreter for the little german language.
        It features multiple basic functionalities aswell as lists and dictionaries"""

    def __init__(self, source_code: list) -> None:
        """Initialize a new LGL_Interpreter with a gsc file contents. Set up a dictionary to keep track of all dictionaries"""
        self.code = source_code
        self.environment = [{}]

    def run(self) -> None:
        """Run the programm. This will start the execution of the gsc code by taking the contents of the gsc file and then give it to the interpret method line by line"""

        assert len(self.code) > 0, "there is no code to read"
        #case only one operation is in the file
        if not isinstance(self.code[0],list):
            self.code = [self.code]

        for instruction in self.code:
            self.interpret(instruction)

    def environment_set(self, name:str, value) -> None:
        """use to set environment variables"""
        assert isinstance(name,str), "name of variable needs to be a string"
        self.environment[-1][name] = value
        return None

    def environment_get(self, name:str):
        """use to get environment variables"""
        assert isinstance(name,str), "name of variable needs to be a string"
        for env in reversed(self.environment):
            if name in env.keys():
                return env[name]
        raise LookupError ("the variable specified is non-existent")
    
    def environment_inspect(self, name:str) -> bool:
        """use to check for existence True if it exists False otherwise"""
        assert isinstance(name,str), "name of variable needs to be a string"
        for env in reversed(self.environment):
            if name in env.keys():
                return True
        return False
        
    
    def environment_delete(self, name:str) -> None:

        assert isinstance(name,str), "name of variable needs to be a string"

        for env in reversed(self.environment):
            if name in env.keys():
                del env[name]
                return None
        raise LookupError ("the specified variable was not found")

    def list_transform(self,value) -> list:

        if not isinstance(value,list):
            return [value]
        return value

    def call_clean(self,line:list,low_limit:int = 1, high_limit:int = None) -> list:
        
        if not isinstance(line,list):
            return line
        if len(line) == 0:
            return line

        if all([not isinstance(instr,list) for instr in line]):
            return self.clean([line],low_limit,high_limit)[0]

        return self.clean(line,low_limit,high_limit)

    def clean(self, line:list,low_limit:int = 1,high_limit:int = None) -> list:
        """Interpret the nested functions in the lines, define low and high limit for the range of elements which should be interpreted if possible"""
        if not isinstance(line,list):
            return line

        a = line.copy()

        for index,value in enumerate(a[low_limit:high_limit]):
            if isinstance(value,list) and value[0] in [name.replace("interpret_","") for name in dir(self.__class__) if name.startswith("interpret_")]:
                a[index+low_limit] = self.interpret(value)

        return a


    def interpret(self, instruction:list) -> None:
        """Tnterpret the functions """    
          
        if isinstance(instruction,(int,str,type(None))):
            return instruction
        
        if isinstance(instruction[0],list):
            instruction = self.call_clean(instruction,0,1)
        assert "interpret_" + str(instruction[0]) in dir(self.__class__), f"Unknown operation: {instruction[0]}"
        #get the name of the method to execute then get the actual method
        method_name = [method for method in dir(self.__class__) if method.replace("interpret_","") == instruction[0]][0]
        method_body = getattr(self, method_name)
        return method_body(instruction)
        
    def interpret_hoch(self, line:list):
        """this method is for calculating powers"""
        assert len(line) == 3, "bad usage of hoch try: ['hoch',<base>,<power>]"
        line = self.call_clean(line)
        for num in line[1:]:
            assert isinstance(num,(int,float)), "bad usage of hoch, the base and the power need to be ints or floats"
        return line[1]**line[2]

    def interpret_pi(self,line:list) -> float:
        assert len(line) == 1, "bad usage of pi: try ['pi']"
        return math.pi
    
    def interpret_addieren(self, line:list):
        assert len(line) >= 3, "bad usage of interpret addieren, need at least 2 arguments"
        line = self.call_clean(line)
        result = line[1]
        for value in line[2:]:
            result += value
        return result

    def interpret_multiplizieren(self, line:list):
        assert len(line) == 3, "bad usage of multiplizieren try: ['multiplizieren',<value1>,<value2>]"
        line = self.call_clean(line)
        for num in line[1:]:
            assert isinstance(num,(int,float)), "bad usage of multiplizieren, values need to be int or float"
        return line[1]*line[2]
    
    def interpret_dividieren(self, line:list):
        assert len(line) == 3, "bad usage of dividieren try: ['dividieren',<value1>,<value2>]"
        line = self.call_clean(line)
        for num in line[1:]:
            assert isinstance(num,(int,float)), "bad usage of division, values need to be int or float"
        assert line[2] != 0, "bad usage of division: division by 0 is not allowed"
        return line[1]/line[2]



    def interpret_dictionary_erstellen(self, line:list) -> dict:
        """This method creates a dictionary and returns it"""

        assert len(line) == 1, "bad usage of dictionary erstellen: Try ['dictionary_erstellen']"
        return {}
    

    def interpret_seq(self, instructions:list) -> None:
        """This method allows for the lgl to use seq to specify a sequence of instructions"""
        assert len(instructions) > 1, "The sequence has nothing inside it"
        for instr in instructions[1:]:
            if "interpret_" + instr[0] == "interpret_retournieren":
                return self.interpret(instr)
            self.interpret(instr)
        return None
    

    def interpret_dictionary_setzen(self, line:list) -> None:
        """This method sets a value to a key in a dictionary. If the dictionary does not exist an error is thrown. If the key already exists the value is overwriten"""

        assert len(line) == 4, "bad usage of dictionary setzen: Try ['dictionary_setzen','<name>','<key:str/int>','<value>']"
        line = self.call_clean(line)

        try:
            new_dict = self.environment_get(line[1])
        except Exception:
            raise Exception (f'the dictionary {line[1]} does not exist')
        assert isinstance(line[2],(int,str)), "the key of the dictionary needs to be a string or an int"
        new_dict[line[2]] = line[3]
        
        return None

    def interpret_dictionary_finden(self, line:list):
        """This method allows the user to find values in the dictionary by a specified key. If the name or key does not exist an error is thrown, otherwhise the value is returned"""

        assert len(line) == 3, "bad usage of dictionary finden: Try ['dictionary_finden','<name>','<key:str/int>']"
        line = self.call_clean(line)
        #assert line[1] in self.environment.keys(), "the dictionary of which you want to find values does not exist"
        #assert line[2] in self.environment[line[1]].keys(), f"the key {line[2]} does not exist in dictionary {line[1]}"

        #value = self.environment[line[1]][line[2]]

        try:
            value = self.environment_get(line[1])
            assert isinstance(value,dict), f"the variable {line[1]} is not a dictionary"
            return value[line[2]]
        except LookupError:
            raise Exception (f'the dictionary {line[1]} or the key {line[2]} does not exist')
        #return value


    def interpret_dictionary_verbinden(self, line:list) -> dict:
        """This method allows to merge two dictionaries. Either a new name is specified and both directories get merged there, or the second dictionary gets appended to the first.
        If there are key conflicts the keys of the first dictionary will be used"""

        assert len(line) == 3, "bad usage of dictionary verbinden: Try ['dictionary_verbinden','<name>','<name>']"

        line = self.call_clean(line)

        for name in line[1:]:
            assert(isinstance(name,str)), "names of dictionaries must be strings"
        #for name in line[1:2]:
        #    assert name in self.environment.keys(), f"the dictionary {name} does not exist"

        dictionaries = []
        try:
            for index in range(1,3):
                dictionaries.append(self.environment_get(line[index]))
        except LookupError:
            raise Exception (f'the dictionary {line[index]} does not exist')

        for key,value in dictionaries[1].items():
            if key not in dictionaries[0].keys():
                dictionaries[0][key] = value
        return dictionaries[0]
    
        
 

    def interpret_variable_setzen(self, line:list) -> None:
        """this method allows to store variables into the self.variables dictionary"""
        assert len(line) == 3, "bad usage of variable setzen try: ['variable_setzen','<name:str>',<value>]"
        assert isinstance(line[1],str), "variable name needs to be a string"
        line = self.call_clean(line)
        #assert not isinstance(line[2],(list,dict)), "to store lists and dictionaries use dictionary/liste_erstellen"
        #self.environment[-1][line[1]] = line[2]
        self.environment_set(line[1],line[2])

        return None


    def interpret_variable_holen(self, line:list):
        """this method allows to access stored variables"""
        assert len(line) == 2, "bad usage of variable_holen try: ['variable_holen','<name:str>']"
        line = self.call_clean(line)
        assert isinstance(line[1],str), "variable name needs to be a string"
        try:
            return self.environment_get(line[1])
        except Exception as e:
            raise Exception (f'the variable {line[1]} does not exist')

        #assert line[1] in self.environment.keys()
        #return self.environment[line[1]]
    
    def interpret_funktion_erstellen(self, line:list) -> list:
        """this method allows to create functions"""
        assert len(line) == 3, "bad usage of funktion_erstellen try: ['funktion_erstellen',[<arg1>,<arg2>],[<code>]]"
        assert isinstance(line[1],list), "parameter names for a function must be given in a list"
        for para in line[1]:
            assert isinstance(para,str), "name of parameters must be strings"
        assert isinstance(line[2],list) and line[2] != [], "function body instruction is not valid if you want multiple lines of code try ['seq',[<instruction1>],....]"

        return ["funktion",line[1],line[2]]
    

    def interpret_funktion_aufrufen(self, line:list):
        """this method allows to call functions by their name"""
        assert len(line) == 3, "bad usage of funktion_aufrufen try: ['funktion_aufrufen',<name:str>,[<arguments>]]"
        line = self.call_clean(line,1,2)
        assert isinstance(line[1],str), "the name of the function must be a string"
        #assert line[1] in self.environment.keys(), "this function does not exist"
        try:
            func = self.environment_get(line[1])
            assert func[0] == "funktion"
        except LookupError:
            raise NotImplementedError (f'the function {line[1]} does not exist')
        except Exception:
            raise TypeError(f'the function specified: {line[1]} is not a function')
        
        assert isinstance(line[2],list), "the arguments for funktion aufrufen where not passed in a list"
        line[2] = self.call_clean(line[2],0,None)
        assert len(self.list_transform(line[2])) == len(func[1]), f"the function: {line[1]} must be called with {len(func[1])} arguments but you specified {len(line[2])}"
        #assert len(line[2]) == len(self.environment[line[1]][1]), f"you tried to call the function {line[1]} with a wrong amount of parameters"

        

        local_env = dict(zip(func[1],self.list_transform(line[2])))
        self.environment.append(local_env)
        result = self.interpret(func[2])
        self.environment.pop(-1)
        return result
    
    def interpret_retournieren(self, line:list):
        """use this method to return in functions"""
        assert len(line) == 2, "bad usage of retournieren try: ['retournieren',<value>]"
        line = self.call_clean(line)
        return line[1]
    
    def interpret_klasse_erstellen(self, line:list) -> None:
        """method to create a new class"""
        assert len(line) in (3,4), "bad usage of klasse_erstellen try: ['klasse_erstellen',<name:str>,[[<name>,<funktion:name>],[<name>,<funktion>]],'<parent>=None']"
        line = self.call_clean(line,1,2)
        assert isinstance(line[1],str), "the name of a class must be a string"
        assert isinstance(line[2],list) and line[2] != [], f"please define proper methods for class {line[1]}"


        assert not self.environment_inspect("class_"+line[1]), f'the class {line[1]} does already exist'


        if len(line) == 3:
            line.append(None)
        line = self.call_clean(line,3)
        assert isinstance(line[3],(str,type(None))), f"the parent name has to be a string or None"

        if line[3] != None:
            try:
                parent = self.environment_get("class_"+line[3])
            except LookupError:
                raise Exception (f'the parent {line[3]} does not exist')

        assemble = {"name":line[1],}

        
        for method in line[2]:
                    assert len(method) == 2, f"incorrect methods specified for class {line[1]}"
                    try:
                        func = self.environment_get(method[1])
                        assemble[method[0]] = method[1]
                        pass
                    except LookupError:
                        raise NotImplementedError (f'the function {method[1]} is not implemented')
        assemble["parent"] = line[3]       

        self.environment_set("class_"+line[1], assemble)
        return None

    def interpret_objekt_instanzieren(self,line:list) -> dict:
        """instantiate objects of a class by using the standard neu->dict method"""
        assert len(line) == 3, "bad usage of objekt_instanzieren try: ['objekt_instanzieren',<class>,[<arg>,<arg>]]"
        line = self.call_clean(line,1,2)
        assert isinstance(line[1],str), "objekt instanzieren: the name of a class must be a string"
        assert self.environment_inspect("class_"+line[1]), f"the class {line[1]} does not exist"
        assert isinstance(line[2],list), f"the argumentss for an object instantiation must be given in a list"
        assemble = {"class":"class_"+line[1]}
        try:
            function_name = self.find_method(assemble["class"],"neu")
            object_variables = self.interpret_funktion_aufrufen(["funktion_aufrufen",function_name,line[2]])
            assert isinstance(object_variables,dict), f"the class {line[1]} did not implement neu to return a dictionary"
            assemble |= object_variables
        except Exception:
            pass
        """ if "neu" in self.environment_get(assemble["class"]).keys():
            object_variables = self.interpret_funktion_aufrufen(["funktion_aufrufen",self.environment_get(assemble["class"])["neu"],line[2]])
            assert isinstance(object_variables,dict), f"the class {line[1]} did not implement neu to return a dictionary"
            assemble |= object_variables """
        
        return assemble
        

    def find_method(self,class_name:str,method_name:str) -> bool:
        """finds if a method is implemented for a class"""
        cla = self.environment_get(class_name)
        while True:
            if method_name in cla:
                return cla[method_name]
            elif cla["parent"] == None:
                raise NotImplementedError (f'the method {method_name} is not implemented for the class {class_name}')
            else:
                cla = self.environment_get("class_"+cla["parent"])


    def interpret_objekt_methode(self, line:list):
        """lets objects use their methods"""
        assert len(line) == 4, "bad usage ob objekt_methode try: ['objekt_methode',<name(object)>,<name(method)>,[<arg>,<arg>]]"
        line = self.call_clean(line,1,3)
        for name in line[1:3]:
            assert isinstance(name,str), "the name of an object/method must be a string"
        assert isinstance(line[3],list), "the arguments for a method must be given in a list"
        for index,arg in enumerate(line[3]):
            line[3][index] = self.call_clean(arg)
        try:
            obj = self.environment_get(line[1])
        except Exception:
            raise Exception (f'the object {line[1]} does not exist')
        
        meth = self.find_method(obj["class"],line[2])
        return self.interpret_funktion_aufrufen(["funktion_aufrufen",meth,line[3]])
    
    def interpret_klasse_methode(self, line:list):
        """lets classes use their methods"""
        return None
        



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