




<h1>1 More Capabilites</h1>



<h3>1.1 Implementation</h3>

<h5>1.5 Dicitonaries</h5>
<p>Dictionaries are implemented with python dictionaries. The dictionaries need to be stored in a variable or they can not be accessed anymore. Also the LGL only allows strings as dictionaries names. For now keys are limited to strings and integers, however if tuples get introduced they can be added aswell.</p>

<h3>1.2 Use</h3>

<h1>2 An Object System</h1>

<h3>2.1 Implementation</h3>

<h5>Class definition and Object instantiation</h5>
<p>Klasse_erstellen allows for definition of classes. It takes a name, a list of lists consisting of method names and functionnames and an optional parameter parent.<br>
Storing: The class is stored in the current environment using the name prefix with _class as key. In the value a dictionary is written that maps the classes method names to function names which can be exectued, aswell as the parent name.<br>
Object instantiation: Objects get instantiated as a dictionary with the name of the object as the key. The value is a dictionary containing the name, the specific object variables and the classname it belongs to. Classes can specify the special method neu which will be called upon object instantiation it is expected to return a dictionary with name, value pairs which make up the instance variables.<br>
Usage of methods: Objects can use the class specified methods by using their class entry to map to the class dicitonary which has the function names stored for the method names.</p>

<h5>Single Inheritance and Polymorphism</h5>
<p>The optional parent parameter allows to specify a parent class of which all methods will be available as long as they are not supscripted in the child class. The inheritance is limited to one parent. The interpreter allows inheritance and polymorphism by taking a bottom up approach in the search of class methods. The object will first try to find the method in its own class if it can not find it it will go to the parent.</p>

<h3>2.2 Use</h3>

<h1>3 Tracing</h1>

<h3>3.1 Logging</h3>

<h3>3.2 Reporting</h3>