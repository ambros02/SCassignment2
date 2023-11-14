

<h1>LGL_Interpreter Documentation</h1>

<p>The following documentation concerns the implementation of an LGL_interpreter which allows to interpret a Little German Language into python code.<p>


<h3>Usage</h3>

<p>python lgl_interpreter.py file.gsc   | executes the gsc file where file has to be in the same directory as lgl_interpreter.py<br>
options:
    <ul>
        <li>--trace file.log    | writes logging information to file.log</li>
    </ul>
<p>

<h3>General implementation info</h3>

<p>The LGL interpreter was designed as a class for two main reasons. First classes allow inheritance, which increases the scalability possibilities. With a child class the functions of the general LGL language can be extended with more or adapted functionalities. Second classes allow many design patterns, such as decorators or introspection.<br>
The program starts in the main function where the validity of the command is evaluated. If the trace option is specified the main function will try to write to the file, if it suceeds it will configure the basic logging to this file. This allows to write to the file from within the class without passing the filename.<br>
The class is used by instantiating an object with a list of executions and an alternativ logging argument to enable logging. The object can then use run to start interpreting the code line by line with the interpret method.<br>
The interpret method allows int,float,str,bool and Nonetype as terminal values. Otherwhise it will get the name of the instruction and then call the method for it. It only evaluates nested expressions for the first element of the instruction to know which method to call. This implies that all methods have to implement the evaluation of nested expressions. This was decided, since different expressions have different evaluation needs e.g. an expression to instantiate a function does not want the instructions to be evaluated before storing it.<br>
The class keeps track of variables by adding them to a list of dicitonaries which represent local environments with the first entry being the global scope. To ensure the integrity of the data in the environment 4 functions are defined to interract with the environment. We can set, get, inspect and delete variables from the environments</p>

<h3>Capabilities</h3>

<p>The LGL allows to set and get variables with a string as the name (note names starting with class_ are reserved for classes to avoid name conflicts).<br>
It further allows for the definition and calling of functions with parameters. If a function with more than one expression in the body is to be specified the seq expression has to be used. The seq expressions iterates through a list of expressions breaking and returning if it sees a retournieren statement. Functions append a new environment where all local variables will be stored. After the execution the local environment is removed.</p>


<h1>1 More Capabilites</h1>



<h3>1.1 Implementation</h3>

<h5>1.5 Dicitonaries</h5>
<p>Dictionaries are implemented with python dictionaries. The dictionaries need to be stored in a variable or they can not be accessed anymore. Also the LGL only allows strings as dictionaries names. For now keys are limited to strings and integers, however if tuples get introduced they can be added aswell. Setting a dictionary value will overwrite existing values without asking. If a dicitonary or a key is not found an error is thrown. Using the dictionary verbinden will result in a new dictionary with all the items of the first specified and all items of the second which keys are not in the first.</p>

<h3>1.2 Use</h3>

<h1>2 An Object System</h1>

<h3>2.1 Implementation</h3>

<h5>Class definition and Object instantiation</h5>
<p>Klasse_erstellen allows for definition of classes. It takes a name, a list of lists consisting of method names and functionnames and an optional parameter parent.<br>
Storing: The class is stored in the current environment using the name prefix with _class as key. In the value a dictionary is written that maps the classes method names to function names which can be exectued, aswell as the parent name. This generates more overhead than storing the functions directly, however it allows for adaption of the methods at runtime. A word of caution though, since defining functions with the same name as a method function in a local environment will adapt the behaviour of the class.<br>
Object instantiation: Objects get instantiated as a dictionary with the name of the object as the key. The value is a dictionary containing the name, the specific object variables and the classname it belongs to. Classes can specify the special method neu which will be called upon object instantiation it is expected to return a dictionary with name, value pairs which make up the instance variables.<br>
Usage of methods: Objects can use the class specified methods by using their class entry to map to the class dicitonary which has the function names stored for the method names.</p>

<h5>Single Inheritance and Polymorphism</h5>
<p>The optional parent parameter allows to specify a parent class of which all methods will be available as long as they are not supscripted in the child class. The inheritance is limited to one parent. The interpreter allows inheritance and polymorphism by taking a bottom up approach in the search of class methods. The object will first try to find the method in its own class if it can not find it it will go to the parent. Responsible for this is the find_method</p>

<h3>2.2 Use</h3>

<p>In the example_class.gsc the code does as requested in task 2. Mainly it consists of 4 parts. First are the definition of the functions which are being used as methods in the classes. This includes the constructors for shape,square and circle, which will create an object with a name and a side for a square or a radius for a circle. It also has the square and circle area which calculate the area of the object, by taking the instance as a parameter and accessing its side respectively radius. Lastly the density function return the density, by calculating the area of the instance and then use this as the divisor for a given weight.<br>
Second the classes are created, note that the Shape class has to be created first.<br>
Third is the instanciation of a circle object ci with radius 2 and a square object sq with side 3<br>
Fourth and last the sum of the densities is calculated and printed to the console.</p>

<h1>3 Tracing</h1>

<p>The lgl interpreter can be called with the optional argument --trace filename to log details about function execution.</p>

<h3>3.1 Logging</h3>

<p>Logging of the functions called in the gsc file is achieved by a decorator around the funktion_aufrufen function. This allows to get detailed information about the execution, runtime etc of functions without changing the original behaviour. This comes in handy for debugging and improving performance. It should be noted however, that the decorator function will start the call of a nested expression in the given function name parameter. Normally this would be done by the funktion aufrufen methode, however the name must be evaluated before the execution to be able to store a correct logging message. This implies, that if we have an expression that calls funktion_aufrufen in the name of the function in the funktion_aufrufen, then the evaluation of the name will trigger the next funktion aufrufen. Therefore the evaluated name has to be given to the actual funktion_aufrufen method, so it does not call the same function again, resulting in more evaluations than would normally trigger.<br>
The values are stored in the file specified in the command and take the following form: id:str,name:str,event:str,datetime:str. Where the name is simply the name of the function, while the id is the address of said function in the environment. This allows to trace different functions of the same name differently. This works since functions with the same name can be defined in multiple environments (inside another function), resulting in two functions with same name but different behaviour and id.</p>

<h3>3.2 Reporting</h3>

<h5>Functionality</h5>

<p>The reporter class allows for detailed report about logged functions. It displays information from a file produced by the logging mechanism. Displayed will be the name of the function, number of calls of said function, the total runtime of the function and the average runtime of the function. The class achieves this two main methods and a helper method.<br>
The calculate method takes the data from the file and evaluates number of calls aswell as total and average runtime. For this it uses the set_start method which keeps track of the start times of function calls. For this a stack is used where for a given function every start time is pushed onto a stack and whenever an end statement is encountered the last element of the functions stack is popped to calculate the runtime. This follows the principle that if a function calls a function the called function needs to evaluate before the caller function. The id is no longer needed for the reporting, however we need it for the stacks with the start times, since only ids are unique (unlike names).</p>

<h5>example_trace</h5>

<p>the example_trace.gsc file has been adapted to this verison of the lgl to demonstrate the usage.</p>