




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