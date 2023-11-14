import logging
import os
import sys
import json
import math
from copy import deepcopy
from datetime import datetime
from time import time



class LGL_Interpreter:

    """This class provides an interpreter for the little german language.
        It features basic operations, while loops and sequences with return statements
        aswell as functions and classes with single inheritance.
        The interpreter also provides a logging functionality to log all functions called in the gsc file"""

    def __init__(self, source_code: list, logging:bool=False) -> None:
        """Initialize a new LGL_Interpreter with a gsc file contents. Set up a global environment to keep track of global variables
        setting self.logging to True will result in logging information to the specified file"""
        self._code = source_code
        self._environment = [{}]
        self.logging = logging

    def run(self) -> None:
        """Run the programm. This will start the execution of the gsc code by taking the contents of the gsc file and then give it to the
        interpret method line by line"""

        assert len(self._code) > 0, "there is no code to read"
        #case only one operation is in the file
        if not isinstance(self._code[0],list):
            self._code = [self._code]

        for instruction in self._code:
            self.interpret(instruction)


    def _decorator(func_call):
        """this decorator allows logging for the interpret_funktion_aufrufen method to log information about the functions executed
        in the gsc file"""
        def logger(self,instructions):
            """log functions called with id, name, even and time"""
            if self.logging:
                function_name = self.interpret(instructions[1])
                func_id = str(id(self.environment_get(function_name)))

                logging.info(",".join([func_id,function_name,"start",str(datetime.fromtimestamp(time()))]))
                a = func_call(self,[instructions[0]] + [function_name] + [instructions[2]]) #call with calculated to avoid nesting twice
                logging.info(",".join([func_id,function_name,"end",str(datetime.fromtimestamp(time()))]))
                return a
            else:
                return func_call(self,instructions)
                
        return logger



    """[environment methods]  to interract with the environment"""

    def environment_set(self, name:str, value) -> None:
        """set variable in the current environment"""
        assert isinstance(name,str), "name of variable needs to be a string"
        self._environment[-1][name] = value
        return None

    def environment_get(self, name:str):
        """get the instance in the top most environment (top stack of function calls)"""
        assert isinstance(name,str), "name of variable needs to be a string"
        for env in reversed(self._environment):
            if name in env.keys():
                return env[name]
        raise LookupError ("the variable specified is non-existent")
    
    def environment_inspect(self, name:str) -> bool:
        """use to check for existence True if it exists False otherwise"""
        assert isinstance(name,str), "name of variable needs to be a string"
        for env in reversed(self._environment):
            if name in env.keys():
                return True
        return False
        
    
    def environment_delete(self, name:str) -> None:
        """delete the first instance from the top most environment"""
        assert isinstance(name,str), "name of variable needs to be a string"

        for env in reversed(self._environment):
            if name in env.keys():
                del env[name]
                return None
        raise LookupError ("the specified variable was not found")

    """[/environment methods]"""



    def interpret(self, instruction:list) -> None:
        """Tnterpret the functions"""    

        #terminal conditions  
        if isinstance(instruction,(int,str,bool,type(None))):
            return instruction
        
        if isinstance(instruction[0],list): 
            instruction[0] = self.interpret(instruction[0])
        assert "interpret_" + str(instruction[0]) in dir(self.__class__), f"Unknown operation: {instruction[0]}"
        #get the name of the method to execute then get the actual method and execute
        method_name = [method for method in dir(self.__class__) if method.replace("interpret_","") == instruction[0]][0]
        method_body = getattr(self, method_name)
        return method_body(instruction)



    """[math methods] useful arithmetic functions"""

    def interpret_hoch(self, line: list):
        """this method is for calculating powers"""
        assert len(line) == 3, "bad usage of hoch try: ['hoch',<base>,<power>]"

        base = self.interpret(line[1])
        power = self.interpret(line[2])

        assert isinstance(base,(int,float)), "the base needs to be an int"
        assert isinstance(power,(int,float)), "the power needs to be an int"

        return base ** power


    def interpret_pi(self, line: list) -> float:
        assert len(line) == 1, "bad usage of pi: try ['pi']"
        return math.pi

    def interpret_addieren(self, line: list):
        """add an arbitrary amount of numbers together"""
        assert len(line) >= 3, "bad usage of addieren, need at least 2 arguments"

        result = 0
        for expression in line[1:]:
            number = self.interpret(expression)
            assert isinstance(number,(int,float)), "addieren needs arguments to be int or float"
            result += number

        return result


    def interpret_multiplizieren(self, line:list):
        """multiplay an arbitrary amount of numbers"""
        assert len(line) >= 3, "bad usage of multiplizieren, need at least 2 arguments"

        result = 1
        for expression in line[1:]:
            number = self.interpret(expression)
            assert isinstance(number,(int,float)), "addieren needs arguments to be int or float"
            result *= number

        return result


    def interpret_dividieren(self, line: list):
        """divide 2 numbers"""
        assert len(line) == 3, "bad usage of dividieren try: ['dividieren',<value1>,<value2>]"

        dividend = self.interpret(line[1])
        divisor = self.interpret(line[2])

        assert isinstance(dividend,(int,float)), "bad usage of dividieren: dividend must be int or float"
        assert isinstance(divisor,(int,float)), "bad usage of dividieren: divisor must be int or float"
        assert divisor != 0, "bad usage of dividieren: divisor can't be 0"

        return dividend/divisor


    """[/math methods]"""

    def interpret_print(self, line: list):
        """This method allows to use the print statement given in the gsc file"""
        assert len(line) > 0, "bad usage of print try: ['print', <value>]"
        value = self.interpret(line[1])
        print(value)

    def interpret_while(self, line: list):
        """Implement while loops in LGL with a bool condition and an operation
        after each iteration the condition gets evaluated again"""

        assert len(line) == 3, "Bad usage of 'while'. Try: ['while', <condition>, <operation>]"

        condition = self.interpret(line[1])
        assert isinstance(condition,bool), "Bad usage of while, condition must be a bool"
        operation = line[2]

        while condition:
            self.interpret(operation)
            condition = self.interpret(line[1])
            assert isinstance(condition,bool), "Bad usage of while, condition must be a bool"


    """[list methods] manipulate fixed sized arrays"""
    

    def interpret_liste_erstellen(self, line: list) -> None:
        """This method creates lists for the lgl and returns them"""
        assert len(line) == 2, "bad usage of liste ersellen: Try ['liste_erstellen', '<size>']"
        size = self.interpret(line[1])
        assert isinstance(size, int), "the size of the list needs to be a int"
        new_list = []
        for x in range(size):
            new_list.append(None)
        return new_list

    def interpret_liste_setzen(self, line: list) -> None:
        """This method sets a value to an index in a list. If the list does not exist an error is thrown."""
        assert len(line) == 4, "bad usage of liste setzen: Try ['liste_setzen', '<name>', '<idx:int>', '<value>']"
        name = self.interpret(line[1])
        assert isinstance(name,str), "bad usage of liste_setzen: the name of the list needs to be a string"
        index = self.interpret(line[2])
        assert isinstance(index,int), "bad usage of liste_setzen: index must be an int"
        value = self.interpret(line[3])
        try:
            new_list = self.environment_get(name)
        except Exception:
            raise Exception(f"the list {name} does not exist")
        assert index < len(new_list), "bad usage of liste_setzen: the index is out of range"
        new_list[index] = value 
        return None

    def interpret_liste_finden(self, line: list) -> None:
        """This method allows the user to find values in the list by index. If the name or index does not exist an error is thrown, otherwise the value is returned"""
        assert len(line) == 3, "bad usage of liste finden: Try ['liste_finden', '<name>', '<idx:int>']"
        name = self.interpret(line[1])
        assert isinstance(name,str), "bad usage of liste finden: name needs to be a string"
        index = self.interpret(line[2])
        assert isinstance(index, int), "bad usage of liste finden: the index of the list needs to be an integer"
        try:
            new_list = self.environment_get(name)
        except Exception:
            raise Exception(f"the list {name} does not exist")
        assert index < len(new_list), "bad usage of liste finden: the index is out of range"
        return new_list[index]

    """[/list methods]"""


    """[condition methods]"""

    def interpret_gleich(self,line:list) -> bool:
        """this method allows to compare two expressions for equality of the value"""
        assert len(line) == 3, "bad usage of gleich try: ['gleich',<value>,<value>]"

        left = self.interpret(line[1])
        right = self.interpret(line[2])

        return left == right

    def interpret_ungleich(self,line:list) -> bool:
        """this method allows to compare two expressions for inequality of the value"""
        assert len(line) == 3, "bad usage of gleich try: ['gleich',<value>,<value>]"

        left = self.interpret(line[1])
        right = self.interpret(line[2])

        return left != right


    """[/condition methods]"""


    def interpret_retournieren(self, line:list):
        """use this method to return in functions"""
        assert len(line) == 2, "bad usage of retournieren try: ['retournieren',<value>]"
        value = self.interpret(line[1])
        return value
    
    def interpret_seq(self, instructions:list) -> None:
        """This method allows for the lgl to use seq to specify a sequence of instructions that breaks when a retournieren statement is used"""
        assert len(instructions) > 1, "The sequence has nothing inside it"

        for instr in instructions[1:]:
            #special case where first part of expression is an expression
            instr_name = self.interpret(instr[0])

            if "interpret_" + instr_name == "interpret_retournieren":
                return self.interpret(instr)
            self.interpret(instr)
            
        return None
    

    """[dictionary methods]"""

    def interpret_dictionary_erstellen(self, line:list) -> dict:

        assert len(line) == 1, "bad usage of dictionary erstellen: Try ['dictionary_erstellen']"
        return {}
    

    def interpret_dictionary_setzen(self, line:list) -> None:
        """This method sets a value to a key in a dictionary. If the dictionary does not exist an error is thrown.
        If the key already exists the value is overwriten"""

        assert len(line) == 4, "bad usage of dictionary setzen: Try ['dictionary_setzen','<name>','<key:str/int>','<value>']"

        name = self.interpret(line[1])
        key = self.interpret(line[2])
        value = self.interpret(line[3])

        assert isinstance(key,(int,str)), "bad usage of dictionary setzen: the key of the dictionary needs to be a string or an int"
        try:
            name_dict = self.environment_get(name)
        except Exception:
            raise Exception (f'bad usage of dictionary setzen: the dictionary {name} does not exist')
        name_dict[key] = value
        
        return None

    def interpret_dictionary_finden(self, line:list):
        """This method allows the user to find values in the dictionary by a specified key.
        If the name or key does not exist an error is thrown, otherwhise the value is returned"""

        assert len(line) == 3, "bad usage of dictionary finden: Try ['dictionary_finden','<name>','<key:str/int>']"

        name = self.interpret(line[1])
        key = self.interpret(line[2])

        try:
            value = self.environment_get(name)
            assert isinstance(value,dict), f"bad usage of dictionary finden: the variable {name} is not a dictionary"
            return value[line[2]]
        except LookupError:
            raise Exception (f'bad usage of dictionary finden: the dictionary {name} or the key {key} does not exist')
        #return value


    def interpret_dictionary_verbinden(self, line:list) -> dict:
        """This method allows to merge two dictionaries. The method will return a dictionary which has all items of the first
        dictionary and all items from the second which have no key already in the first dictionary"""

        assert len(line) == 3, "bad usage of dictionary verbinden: Try ['dictionary_verbinden','<name>','<name>']"

        name_first = self.interpret(line[1])
        name_second = self.interpret(line[2])
        
        assert(isinstance(name_first,str)), "bad usage of dictionary verbinden: names of dictionaries must be strings"
        assert(isinstance(name_second,str)), "bad usage of dictionary verbinden: names of dictionaries must be strings"

        dictionaries = []
        try:
            dictionaries.append(self.environment_get(name_first))
            dictionaries.append(self.environment_get(name_second))
        except LookupError:
            raise Exception (f'bad usage of dictionary verbinden: the dictionary you specified does not exist')

        return dictionaries[1] | dictionaries[0]
    
    """[/dictionary methods]"""    
 

    """[variable methods]"""

    def interpret_variable_setzen(self, line:list) -> None:
        """this method allows to store variables into the self.variables dictionary"""

        assert len(line) == 3, "bad usage of variable setzen try: ['variable_setzen','<name:str>',<value>]"
        assert isinstance(line[1],str), "bad usage of variable setzen: variable name needs to be a string"
        
        name = self.interpret(line[1])
        value = self.interpret(line[2])

        #assert not isinstance(line[2],(list,dict)), "to store lists and dictionaries use dictionary/liste_erstellen"
        #self.environment[-1][line[1]] = line[2]
        self.environment_set(name,value)

        return None


    def interpret_variable_holen(self, line:list):
        """this method allows to access stored variables"""

        assert len(line) == 2, "bad usage of variable_holen try: ['variable_holen','<name:str>']"
        name = self.interpret(line[1])
        assert isinstance(name,str), "bad usage of variable_holen: variable name needs to be a string"
        try:
            return self.environment_get(name)
        except Exception as e:
            raise Exception (f'bad usage of variable_holen: the variable {name} does not exist')
    
    """[/variable methods]"""


    """[function methods]"""

    def interpret_funktion_erstellen(self, line:list) -> list:
        """this method allows to create functions with parameters and some code to exectue"""

        assert len(line) == 3, "bad usage of funktion_erstellen try: ['funktion_erstellen',[<para1>,<para2>],[<code>]]"
        assert isinstance(line[1],list), "bad usage of funktion_erstellen parameter names for a function must be given in a list"

        for para in line[1]:
            assert isinstance(para,str), "bad usage of funktion_erstellen name of parameters must be strings"
        assert isinstance(line[2],list) and line[2] != [], "bad usage of funktion_erstellen function body instruction is not valid if you want multiple lines of code try ['seq',[<instruction1>],....]"

        return ["funktion",line[1],line[2]]
    
    @_decorator 
    def interpret_funktion_aufrufen(self, line:list):
        """this method allows to call functions by their name"""

        assert len(line) == 3, "bad usage of funktion_aufrufen try: ['funktion_aufrufen',<name:str>,[<arguments>]]"
        assert isinstance(line[2],list), "bad usage of funktion_aufrufen: the arguments for funktion aufrufen where not passed in a list"

        name = self.interpret(line[1])
        assert isinstance(name,str), "bad usage of funktion_aufrufen: the name of the function must be a string"

        arguments = []
        for arg in line[2]:
            arguments.append(self.interpret(arg))
        
        try:
            func = deepcopy(self.environment_get(name))
            assert func[0] == "funktion"
        except LookupError:
            raise NotImplementedError (f'bad usage of funktion_aufrufen: the function {name} does not exist')
        except Exception:
            raise TypeError(f'bad usage of funktion_aufrufen: the function specified: {name} is not a function')
        
        assert len(arguments) == len(func[1]), f"the function: {name} must be called with {len(func[1])} arguments but you specified {len(arguments)}"
        #assert len(line[2]) == len(self.environment[line[1]][1]), f"you tried to call the function {line[1]} with a wrong amount of parameters"

        #create a local environment, variable_set will store variables in there now until the function ends
        local_env = dict(zip(func[1],arguments))
        self._environment.append(local_env)
        result = self.interpret(func[2])
        self._environment.pop(-1)
        return result
    
    """[/function methods]"""

    
    """[class/object methods]"""
    
    def interpret_klasse_erstellen(self, line:list) -> None:
        """method to create a new class"""

        assert len(line) in (3,4), "bad usage of klasse_erstellen try: ['klasse_erstellen',<name:str>,[[<name>,<funktion:name>],[<name>,<funktion>]],'<parent>=None']"

        name = self.interpret(line[1])
        assert isinstance(name,str), "bad usage of klasse_erstellen: the name of a class must be a string"
        assert not self.environment_inspect("class_"+name), f'bad usage of klasse_erstellen: the class {name} does already exist'

        assemble = {"name":name}

        assert isinstance(line[2],list) and line[2] != [], f"bad usage of klasse_erstellen: please define proper methods for class {name}"
        for method in line[2]:
            assert len(method) == 2, f"bad usage of klasse_erstellen: define methods for class {name} properly try: [[<name>,<funktion:name>],[<name>,<funktion>]]"
            method_name = self.interpret(method[0])
            func_name = self.interpret(method[1])
            assert self.environment_inspect(func_name), f"bad usage of klasse_erstellen: the function {func_name} is not implemented"
            assemble[method_name] = func_name

        if len(line) == 3:
            parent = None
        else:
            parent = self.interpret(line[3])
            assert isinstance(parent,(str,type(None))), f"the parent name has to be a string or None"
            assert self.environment_inspect("class_" + parent), f"the parent {parent} does not exist"

        assemble["parent"] = parent      
        self.environment_set("class_" + name, assemble)

        return None

    def interpret_objekt_instanzieren(self,line:list) -> dict:
        """instantiate objects of a class by using the standard neu->dict method"""
        assert len(line) == 3, "bad usage of objekt_instanzieren try: ['objekt_instanzieren',<class>,[<arg>,<arg>]]"
        
        class_name = self.interpret(line[1])
        assert isinstance(class_name,str), "objekt instanzieren: the name of a class must be a string"
        assert self.environment_inspect("class_" + class_name), f"bad usage of objekt_instanzieren: the class {class_name} does not exist"

        assert isinstance(line[2],list), f"bad usage of objekt_instanzieren: the argumentss for an object instantiation must be given in a list"
        arguments = []
        for arg in line[2]:
            arguments.append(self.interpret(arg))

        assemble = {"class":"class_" + class_name}

        try:
            function_name = self.find_method(assemble["class"],"neu")
            object_variables = self.interpret(["funktion_aufrufen",function_name,arguments])
            assert isinstance(object_variables,dict), f"bad usage of objekt_instanzieren: the class {class_name} did not implement neu to return a dictionary"
            assemble |= object_variables
        except Exception:
            pass
        
        return assemble

    def interpret_objekt_methode(self, line:list):
        """lets objects use their methods"""
        assert len(line) == 4, "bad usage ob objekt_methode try: ['objekt_methode',<name(object)>,<name(method)>,[<arg>,<arg>]]"

        object_name = self.interpret(line[1])
        assert isinstance(object_name,str), "bad usage of objekt_methode: the name of an object must be a string"
        assert self.environment_inspect(object_name), f"bad usage ob objekt_methode: the object {object_name} does not exist"

        method_name = self.interpret(line[2])
        assert isinstance(method_name,str), "bad usage of objekt_methode: the name of a method must be a string"

        arguments = []
        assert isinstance(line[3],list), "bad usage of objekt_methode: the arguments for a method must be given in a list"
        for arg in line[3]:
            arguments.append(self.interpret(arg))

        func_name = self.find_method(self.environment_get(object_name)["class"],method_name)
        return self.interpret(["funktion_aufrufen",func_name,arguments])
    
    def interpret_klasse_methode(self, line:list):
        """lets classes use their methods"""
        return None
    
    """[/class/objects methods]"""    


    def find_method(self,class_name:str,method_name:str) -> bool:
        """finds if a method is implemented for a class respectively in its parentclass and returns the functionname"""
        cla = self.environment_get(class_name)
        while True:
            if method_name in cla:
                return cla[method_name]
            elif cla["parent"] == None:
                raise NotImplementedError (f'the method {method_name} is not implemented for the class {class_name}')
            else:
                cla = self.environment_get("class_"+cla["parent"])


    



def main() -> None:
    """get the user input gsc file create a LGL_Interpreter object and start to run the code"""

    assert len(sys.argv) in (2,4), "bad usage: python lgl_language.py <filename>.gsc"

    parent_path = os.path.dirname(__file__)
    
    #gsc files are located in the same directory as this file
    with open(os.path.join(parent_path,sys.argv[1]),'r') as file:
        source_lines = json.load(file)
    assert isinstance(source_lines, list), "badly formatted code"

    if len(sys.argv) == 4:
        assert sys.argv[2] == "--trace", f"option {sys.argv[2]} is not implemented"
        assert isinstance(sys.argv[3],str), "option --trace needs a filename"
        #clean file and check if it works
        try:
            with open(sys.argv[3],"w"):
                pass
        except Exception:
            raise Exception ('the filename you specified is not valid')
        logging.basicConfig(filename='trace_file.log', level=logging.INFO, format='%(message)s')
        german_interpreter = LGL_Interpreter(source_lines,True)
        german_interpreter.run()
    else:
        german_interpreter = LGL_Interpreter(source_lines)
        german_interpreter.run()

if __name__ == "__main__":
    main()