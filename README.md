<h1>1 More Capabilites</h1>
<h3>1.1 Implementation</h3>
<h5>1.1.1 Multiplication, Division, and Power operations</h5>
<p>To use the multiplication function we have defined an "interpret_multiplizieren" function. The function only accepts a list, but the list must have at least 3 elements, the first one must be "multiplizieren" so that the lgl and gsc file have the same language. Next, you must have at least 2 either intergers or floats in the list and the function gives us the multiplication of these intergers or floats.<br>
The division function works in a similar way. The difference is that it list must have 3 elements. The first element "dividieren" and either interger or floats as dividend and divisor. We also make sure that we the divisor is not equal 0.<br>
The power function is called "hoch" like in the german language. The list also must have 3 elements, the first "hoch" and then again interger or floats as base and power.<br>
We use self.interpret() in every function here so that we can also work with nested functions.
</p>
<h5>1.1.2 Print statements</h5>
<p>The print function takes a list, which must not be empty. We return the value which we want to print. We also use self.interpret() here so that we can print the result of a function and not the function itself.
</p>
<h5>1.1.3 While loops</h5>
<p>The while loop only takes a bool as a condition. The condition gets evaluated by using self.interpret(). After that, while the condition is true we evaluate the operation with self.interpret(). The condition gets evaluated again after each iteration to reduce the risk of an infinite loop. We also have two condition methods called "interpret_gleich" and "interpret_ungleich". They compare if one value in the list is equal to the other value or not. It helps us with the condition of the while loop.
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
