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
the function body is executed. After that, the result of the execution is returned</p>
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