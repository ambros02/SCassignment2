<h1>LGL_Interpreter Documentation</h1>

<p>The following documentation concerns the implementation of an LGL_interpreter which allows to interpret a Little German Language into python code.<p>


<h3>Usage</h3>

<p>>>>python lgl_interpreter.py file.gsc   | executes the gsc file where file has to be in the same directory as lgl_interpreter.py<br>
<br>
options:<p>
        <ul>
            <li>--trace file.log    | writes logging information to file.log</li>
        </ul>

<h3>General implementation info</h3>

<p>The LGL interpreter was designed as a class for two main reasons. First classes allow inheritance, which increases the scalability possibilities. With a child class the functions of the general LGL language can be extended with more or adapted functionalities. Second classes allow many design patterns, such as decorators or introspection.<br>
The program starts in the main function where the validity of the command is evaluated. If the trace option is specified the main function will try to write to the file specified, if it suceeds it will configure the basic logging to this file. This allows to write to the file from within the class without passing the filename.<br>
The class is used by instantiating an object with a list of executions and an optional logging argument to enable logging. The object can then use run to start interpreting the code line by line with the interpret method.<br>
The interpret method allows int,float,str,bool and Nonetype as terminal values. Otherwhise it will get the name of the instruction and then call the method for it by using introspection on the methods it has. Naming is used to mark methods which calculate an instruction, they all start with interpret_. Also it only evaluates nested expressions for the first element of the instruction to know which method to call. This implies that all methods have to implement the evaluation of nested expressions. This was decided, since different expressions have different evaluation needs e.g. an expression to instantiate a function does not want the instructions to be evaluated before storing it.<br>
The class keeps track of variables by adding them to a list of dicitonaries which represent local environments with the first entry being the global scope. To ensure the integrity of the data in the environment 4 functions are defined to interract with the environment. We can set, get, inspect and delete variables from the environments</p>

<h3>Capabilities</h3>

<p>The LGL allows to set and get variables with a string as the name (note names starting with class_ are reserved for classes to avoid name conflicts).<br>
It further allows for the definition and calling of functions with parameters. If a function with more than one expression in the body is to be specified the seq expression has to be used. The seq expressions iterates through a list of expressions breaking and returning if it sees a retournieren statement. Functions append a new environment where all local variables will be stored. After the execution the local environment is removed.</p>


<h1>1 More Capabilites</h1>



<h3>1.1 Implementation</h3>

<h5>1.5 Dicitonaries</h5>
<p>Dictionaries are implemented with python dictionaries. The dictionaries need to be stored in a variable or they can not be accessed anymore. Also the LGL only allows strings as dictionaries names. For now keys are limited to strings and integers, however if tuples get introduced they can be added aswell. Setting a dictionary value will overwrite existing values without asking. If a dicitonary or a key is not found an error is thrown. Using the dictionary verbinden will result in a new dictionary which is a copy of the second dictionary and then adding all items from  the first dictionary overwriting the second dictionary if there are key conflicts (equal to all items from first with only items from second where the key is not in the first).</p>

<h3>1.2 Use</h3>

<p>The file example_operations.gsc showcases the usage of the implementations requested.<br>
Firstly a variable cond is set to 0 and a list ist initialized with size 3. After that the basic operations multiplication, division and power are used to populate the first to third elements of the list. The list is then printed by a while loop with the condition cond is not equal to 3. The body of the loop prints the list element at index=cond and then increments cond by 1, resulting in the whole list being printed.<br>
Further two dictionaries are initialized: first_dict with elements 1:1,2:2,3:3 and second_dict which has elements 1:2,4:first_dict[2] which will result in 1:2,4:2<br>
The dictionaries are merged into a new dictionary called fused dict, note  that the call was called with first_dict as its first element and therefore it will subscript the keys of second_dict -> resulting in {1:1,2:2,3:3,4:2} which is printed to the console</p>

<h1>2 An Object System</h1>

<h3>2.1 Implementation</h3>

<h5>Class definition and Object instantiation</h5>
<p>Klasse_erstellen allows for definition of classes. It takes a name, a list of lists consisting of method names and functionnames and an optional parameter parent.<br>
Storing: The class is stored in the current environment using the name prefixed with _class as key. In the value a dictionary is written that has 'name':name as first item and then maps the classes method names to function names which can be exectued, aswell as the parent name. This generates more overhead than storing the functions directly, however it allows for adaption of the methods at runtime. A word of caution though, since defining functions with the same name as a method function in a local environment will adapt the behaviour of the class.<br>
Object instantiation: Objects get instantiated as a dictionary with the name of the object as the key. The value is a dictionary containing the name, the specific object variables and the name of the class it belongs to. Classes can specify the special method neu which will be called upon object instantiation it is expected to return a dictionary with name, value pairs which make up the instance variables.<br>
Usage of methods: Objects can use the class specified methods by using their class entry to map to the class dicitonary which has the function names stored for the method names.</p>

<h5>Single Inheritance and Polymorphism</h5>
<p>The optional parent parameter allows to specify a parent class of which all methods will be available as long as they are not supscripted in the child class. The inheritance is limited to one parent. The interpreter allows inheritance and polymorphism by taking a bottom up approach in the search of class methods. The object will first try to find the method in its own class if it can not find it it will go to the parent. Responsible for this is the find_method</p>

<h3>2.2 Use</h3>

<p>In the example_class.gsc the code does as requested in task 2. Mainly it consists of 4 parts. First are the definition of the functions which are being used as methods in the classes. This includes the constructors for shape,square and circle, which will create an object with a name and a side for a square or a radius for a circle. It also has the square and circle area which calculate the area of the object, by taking the instance as a parameter and accessing its side respectively radius. Lastly the density function return the density, by calculating the area of the instance and then use this as the divisor for a given weight.<br>
Second the classes are created, note that the Shape class has to be created first, since the others inherit from it.<br>
Third is the instanciation of a circle object ci with radius 2 and a square object sq with side 3<br>
Fourth and last the sum of the densities is calculated and printed to the console.</p>

<h1>3 Tracing</h1>

<p>The lgl interpreter can be called with the optional argument --trace filename to log details about function execution.</p>

<h3>3.1 Logging</h3>

<p>Logging of the functions called in the gsc file is achieved by a decorator around the funktion_aufrufen function. This allows to get detailed information about the execution, runtime etc of functions without changing the original behaviour. This comes in handy for debugging and improving performance. It should be noted however, that the decorator function will start the call of a nested expression in the given function name parameter. Normally this would be done by the funktion aufrufen methode, however the name must be evaluated before the execution to be able to store a correct logging message. This implies, that if we have a nested expression that calls funktion_aufrufen in the evaluation of the name of the function in the funktion_aufrufen, then the evaluation of the name will trigger the next funktion aufrufen. Therefore the evaluated name has to be given to the call of funktion_aufrufen method, so it does not call the same function again, resulting in more evaluations than would normally trigger.<br>
The values are stored in the file specified in the command and take the following form: id:str,name:str,event:str,time:str. Where the name is simply the name of the function, while the id is the address of said function in the environment. This allows to trace different functions of the same name differently. This works since functions with the same name can be defined in multiple environments (inside another function), resulting in two functions with same name but different behaviour and id. The event is either start or end respectively and time is a timestamp in datetime format as a string.</p>

<h3>3.2 Reporting</h3>

<h5>Functionality</h5>

<p>The reporter class allows for detailed report about logged functions. It displays information from a file produced by the logging mechanism. Displayed will be the name of the function, number of calls of said function, the total runtime of the function and the average runtime of the function. The class achieves this with two main methods and a helper method.<br>
The calculate method takes the data from the file and evaluates number of calls aswell as total and average runtime and then stores the resutls in the self.results. For this it uses the set_start method which keeps track of the start times of function calls. For this a stack is used where for a given function every start time is pushed onto a stack and whenever an end statement is encountered the last element of the functions stack is popped to calculate the runtime. This follows the principle that if a function calls a function the called function needs to evaluate before the caller function. The id is no longer needed for the reporting display, however we need it for the stacks with the start times, since only ids are unique (unlike names).<br>
The present method then takes the results from the calculate method and displays them in a formatted way to the console.</p>

<h5>example_trace</h5>

<p>the example_trace.gsc file has been adapted to this verison of the lgl to demonstrate the usage.</p>

<h1>1. More Capabilities</h1>

<h3>1.1 Implementation</h3>

<b>1.1.4 Arrays</b>
<p>Arrays are implemented with python lists. To create an array, the name of the list has first to be stored in a 
variable, and then the size of the array has to be passed. To set or get values from the array, the name, index and for 
the set function the value has to be passed. The name needs to be a string and the index is restricted to integers.</p>

<b>1.1.6 Other Functionalities</b>
<p>Additionally, more functions are implemented to enhance our LGL Interpreter. Get and set functions for variables
allow to store and access variables from the interpreter`s environment. Next the environment functions handle the 
interpreter`s environment. The set and get functions set and get the variables from the current environment. The inspect
functions checks if a variable exists in the environment. Booleans are returned if the variable is found or not. The
delete function deletes a variable from the environment, if it exists.</p>
<p>Besides that, there are also the functions to create and execute functions in the LGL. Funktion_erstellen defines the 
structure of a function and needs parameters and the code to be executed. The parameters must be given in a list and the
last instruction passed to funktion_erstellen represents the body of a function. At the end a list representing the 
created function is returned. The funktion_aufrufen calls and executes the function. It has to check if the function
given is really a function and if the correct number of arguments are passed. Then a local environment is created where
the function body is executed. After that, the result of the execution is returned.</p>
<p>The seq function handles sequences of
instructions. It iterates over the instructions, interpreting each one, and breaks if there is a retournieren statement. 
The retournieren function returns the value passed from a function.</p>

<h3>1.2 Use</h3>

<h1>2. An Object System</h1>

<h3>2.1 Implementation</h3>

<h3>2.2 Use</h3>

<h1>3. Tracing</h1>

<h3>3.1 Logging</h3>

<h3>3.2 Reporting</h3>

<h1>1 More Capabilites</h1>
<h3>1.1 Implementation</h3>
<h5>1.1.1 Multiplication, Division, and Power operations</h5>
<p>To use the multiplication function we have defined an "interpret_multiplizieren" method. The method only accepts a list, but the list must have at least 3 elements, the first one must be "multiplizieren" so that the lgl and gsc file have the same language. Next, you must have at least 2 either intergers or floats in the list and the function returns the multiplication of these intergers or floats for us.<br>
The division function works in a similar way. The difference is that it list must have 3 elements. The first element "dividieren" and either interger or floats as dividend and divisor. We also make sure that we the divisor is not equal 0.<br>
The power function is called "hoch" like in the german language. The list also must have 3 elements, the first "hoch" and then again interger or floats as base and power.<br>
We use self.interpret() in every method here so that we can also work with nested functions.
</p>
<h5>1.1.2 Print statements</h5>
<p>The print function takes a list, which must not be empty. We print the value of the list. We also use self.interpret() here so that we can print the result of the value and not the function itself.
</p>
<h5>1.1.3 While loops</h5>
<p>The while loop only takes a bool as a condition. The condition gets evaluated by using self.interpret(). After that, while the condition is true we evaluate the operation with self.interpret(). The condition gets evaluated again after each iteration to reduce the risk of an infinite loop. We also have two condition methods called "interpret_gleich" and "interpret_ungleich". They compare if one value in the list is equal to the other value or not. It gives us a few more options how we can use the while loop.
</p>
<h3>1.2 Use</h3>
<p>
</p>
<h1>2 An Object System</h1>
<p>
</p>
<h3>2.1 Implementation</h3>
<p>
</p>
<h3>2.2 Use</h3>
<p>
</p>
<h1>3 Tracing</h1>
<p>
</p>
<h3>3.1 Logging</h3>
<p>
</p>
<h3>3.2 Reporting</h3>
<p>
</p>
