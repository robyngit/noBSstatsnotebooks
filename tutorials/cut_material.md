

### Example 3

Write a function water_phase(temp) that takes input temperature temp in Celcius, uses if/else statements to find what state water is in (assume pressure is 1atm). The function returns a string, which is one of "Solid", "Liquid", "Gas".

```
def water_phase(temp):
    """
    Returns phase of water at `temp`.
    Input temp is temperature in Celcius (int or float)
    temp must be greater than -273.15.
    """
    if temp > 0 and temp < 100:
        return 'Liquid'
    elif temp <= 0:
        return 'Solid'
    elif temp >= 100:
        return 'Gas'
```


## tests to try: correct implementation of `water_phase` should return all True

print( water_phase(20.0) == "Liquid" )
print( water_phase(-20.0) == "Solid" )
print( water_phase(200.0) == "Gas" )
print( water_phase(0.0) in ["Liquid", "Solid"] )

## range tests

```
results = []
for temp in range(1, 100):
    result = (water_phase(temp) == 'Liquid')
    results.append(result)

# temp <= 0
for temp in range(-100, 1):
    result = (water_phase(temp) == 'Solid')
    results.append(result)

# temp >= 100
for temp in range(100, 5000):
    result = (water_phase(temp) == 'Gas')
    results.append(result)

print('Completed a total of', len(results), 'checks...')
all(results)  # True if all results are True
```

Completed a total of 5100 checks...






Certain functions do not return a value (we call these _procedures_) and they consist of sequences of commands we want to execute, that don't have any outputs. FunctIons can also be attached to objects, in which case they are called _methods_. We'll talk about these layer on, for now let's focus on simple math-like functions that receive some input and produce output:

TODO: mention multiple return values



Functions are all over the place:
- In high school math (the green book) we learn the basic vocabulary of $y=f(x)$ functions
  and their parameters, which allows us to describe any real world process
- In calculus we analyze functions $f(x)$ behaviour over time
  (integral of f = sum of values of $f(x)$ between x=start and x=finish;
  and derivative of f at a = the slope of the graph of f(x) when x=a)
- In linear algebra we study linear transformations, which are functions
  that satisfy $f(ax+by)=af(x)+bf(y)$, meaning a linear combination of inputs
  produces the same linear combination of outputs.
- In probability theory we use functions to describe the probability density of
  a random variables. For example $X = \mathcal{N}(\mu, \sigma^2)$ is a random variable
  whose density is described by the function p(x) = K*exp(-((x-mu)/sigma)^2/2)
  in stats we talk about functions computed from samples (estimators)
- In ML we learn about probabilistic models and use them to predict y from given input x

<!-- 
see also https://www.pythonlikeyoumeanit.com/Module2_EssentialsOfPython/Functions.html
-->




# average value of the list `scores`
avg = sum(scores) / len(scores)
avg

Instead of using the existing, convenient `sum` Python builtin function,



, listed in order from highest energy to lowest energy.


SymPy: see examples of solutions to math problems expressed as sympy commands in this [paper](https://arxiv.org/pdf/2112.15594.pdf#page=11) (see [this video](https://www.youtube.com/watch?v=9JZdAq8poww?t=169) for explainer).



Example: printing a ;-separated list of integers

Let's say you want to print the list of scores with the character ; separating each value. The string method join can be used to join a list of strings, but you have a list of ints. No problem, we can use the list-comprehension syntax to convert the list of ints, to a list of strings, in no time.

```
scores = [61, 79, 98, 72]
";".join([str(score) for score in scores])
# '61;79;98;72'
```


##### Example 2: Converting float to str
```
s = str(42.5)

s
'42.5'

type(s)
str
```




from collections.abc import Iterable

isinstance(profile.keys(), Iterable)

isinstance(list(profile.keys()), Iterable)



You can use the built-in function `sorted` to sort the list:

```
sorted(scores)  # returns a new list
[61, 72, 79, 98]
```

Note using the sorted function does not change the original list:

```
scores
[98, 79, 72, 61]
```





```Python
print('\n\n\n')  # '\n' is a special character (an escape sequence) that prints a newline
                 # we'll use this kind of preint-nelines statements to logically
                 # separate the out outplut lines
```

```Python
print('not True ==', not True)
print('not False ==', not False)
print('True and True ==', True and True)
print('True and False ==', True and False)
print('True or False ==', True or False)
print('False or False ==', False or False)

not True == False
not False == True
True and True == True
True and False == False
True or False == True
False or False == False
```


```Python
True and True, True and False, False and True, False and False
(True, False, False, False)

True or True, True or False, False or True, False or False
(True, True, True, False)
```



### Additional reading material

- Review Python syntax cheatsheet [https://blog.finxter.com/wp-content/uploads/2020/07/Finxter_WorldsMostDensePythonCheatSheet.pdf](https://blog.finxter.com/wp-content/uploads/2020/07/Finxter_WorldsMostDensePythonCheatSheet.pdf)
  - add single dot next to concepts you've hear about
  - double dot next to python concepts you understand
  - triple dot next to concepts you've used in your code
- Try poking-around and explore expressions involving numbers (`int` and `float`)
  and  strings (`str`).
- Go through all quiz questions in reading material as notebooks:
  - 03-Variables: [https://introductorypython.github.io/tutorials/03-Variables.html](https://introductorypython.github.io/tutorials/03-Variables.html)
  - 04-Operarators: [https://introductorypython.github.io/tutorials/04-Operators.html](https://introductorypython.github.io/tutorials/04-Operators.html)
<!--
- 06-Data types: [https://introductorypython.github.io/tutorials/06-DataTypes.html](https://introductorypython.github.io/tutorials/06-DataTypes.html) 
  - Review Collections: Lists section. This is important because we can use lists
    to represent vectors in Python, for example the two-dimensional vector can be defined as `v = [3,2]`
  - Complete the section on for loops in 07-Loops notebook.
    The for loop is important because it allows you to do operations for each element in the list.
-->


```
scores.insert(2, 25)
scores
[61, 72, 25, 79, 98, 22]

scores.remove(25)
scores
[61, 72, 79, 98, 22]
```



Additionally, there is a conventions about values are considered "truthy" (i.e. get converted to True when converted to boolean using bool) and which expressions are falsy (i.e. get converted to False when passed through bool).

bool(0)
False

bool(1)
True

Any non-zero float is considered is truthy

bool(133.3)
True

Any non-empty string is considered truthy:

bool("something")
True

But empty string is falsy:

bool("")
False

Boolean expressions are important to understand because they are used in conditional statements.



We can obtain a similar output using the Python function globals(), which returns a dictionary of all the variables and functions in the global namespace.

## ALT. print variables names

# [key for key in globals().keys() if not key.startswith("_")]









**BONUS TOPIC**: You can explore the different methods available on any python object `int`, `float`, `str`, etc.  by starting to type the dot `.` after the name, e.g., `message.` then pressing the TAB button to get an "autocomplete" dropdown of all the methods available on the variable `message`. Most of these methods are common to all strings in Python. For example, try typing in `message.split()` and `message.upper()`.



Don't worry about the lists and dictionary examples—I know they are complicated and we haven't explained all the syntax. We'll get to that in just a little bit. First let's practice computing some Python expressions.



You can also use Python for spreadsheet-like functionality,
manipulate tabular data, compute totals, etc.

Whereas calculators allow only simple arithmetic calculations,
the Python prompt accepts entire "paragraphs" of commands allowing you to write complicated multi-step procedures.
This is what people call "coding" or "programming."

```
# int/int --> float autoconversion
print('If you divide an integrer by an integer in Python using the / operator...')
print('...you get a float number', 6/5, 'has type', type(6/5))
```

```
# Expression involving a list
scores = [61, 85, 92, 72]
average = sum(scores)/len(scores)
#        `sum` computes the sum of values in the list
#                and `len` gives you the length of the list
print("The average score is", average)
```

```
# String expression using a values from a dictionary
profile = {"first_name":"Julie", "last_name":"Tremblay", "score":98}
message2 = "Hi " + profile["first_name"]
print(message2)
```




### Useful anything-to-int conversions

# str --> int
number_as_str = '65'
print(number_as_str, 'has type', type(number_as_str))
number = int(number_as_str)
print(number, 'has type', type(number))

#  float --> int
precise_number_as_float = 3.2
print(precise_number_as_float, 'has type', type(precise_number_as_float))
rounded_number = int(precise_number_as_float)
print(rounded_number, 'has type', type(rounded_number))

#  bool --> int
true_value = True
false_value = False
print('When converted to an int, True is', int(True), 'and False is', int(False))


### Useful anything-to-float conversions

# str --> float
print(float('1.2'))  # note using decimal dot . not decimal , as in Europe
print(float('1e6'))  # one million = 1000000 = 1x10^6. The e is shorthand for x10^
print(float('4'))

# int/int --> float autoconversion
print('If you divide an integrer by an integer in Python using the / operator...')
print('...you get a float number', 6/5, 'has type', type(6/5))

print('There is also an divistion without autoconversion operator // which ...')
print('...you get an integer', 6//5, 'has type', type(6//5))



### Common anything-to-str conversions

# use the str function
str1 = str(42)
str2 = str(4.2)
str3 = str(True)
str4 = 'a string'
print('string representations', str1, str2, str3, str4)

# float -> str
import math
pi = math.pi  # constant equal to ratio of circumference to diameter of a circle
print('str(math.pi) =', str(math.pi))  # defaults to max precision

# control precision and print formatting using format. For more info, see
# https://python-reference.readthedocs.io/en/latest/docs/functions/format.html
print('pi to two decimals', '{:.2f}'.format(pi))
print('pi to seven decimals', '{:.7f}'.format(pi))




### Common anything-to-boolean conversions

Up until now we were in the land of math and text manipulation of numbers, which all make sense intuitively. 

Next we'll talk about the boolean values of Python expressions. This will feel a little weird at first since we're forcing some arbitray Python object (could be a number, a string, a list, a dictionary, etc) and asking the questions is the value `True` or `False` ?

There is a specific convention about which values are considered "truthy" (i.e. get converted to `True` when converted to boolean using `bool`) and which expressions are falsy (i.e. get converted to `False` when passed through `bool`). 

I know this seems like boring details, but please read the next example carefully because "truthyness" and "falsyness" will play a big role in coding: every time you use an if or elif statement in Python, we are implicitly calling `bool` on an expression so it's a good idea to get to know what `bool` does to different types of variables.


# int --> bool
print('Any non-zero integer is considered as True')
print(bool(1), bool(-2), bool(10000))
print('Zero is False')
print(bool(0), bool(-0), bool(int('0')))

print('\n')

# float --> bool
print('Any non-zero float is considered as True')
print(bool(1.0), bool(-2.0), bool(10000.0))
print('Zero is False')
print(bool(0.0), bool(-0.0), bool(float('0.0')))


# str --> bool
print('Any non-empty string is considered True')
print(bool('as'), bool(''))

print('\n')

# list --> bool
print('Any non-empty list is considered True')
print(bool([1]), bool([1,2]), bool(range(0,10000)))
print('Empty list is considered False')
print(bool([]), bool(list()), bool(list('[]')))

print('\n')

# dict --> bool
print('Any non-empty dict is considered True')
print(bool({1:11}), bool({1:11,-2:22}))
print('Empty dict is considered False')
print(bool({}), bool(dict()))








### Bonus topics
  - Command line basics: similar to how in computing user interfaces click (or  double click) means "run <program>", a command line interface allows us to run programs by simply typing out their name, as in    program    and pressing. Enter. This is where the notion of "calling a program/function" comes from, you   just write it's name in a command line prompt and this is equivalent to "calling it" (making it run, just click clicking on it)
  - Command line scripts: run any python code on command line using  python
  myscript.py (or if configured as an executable script, simply ./myscript.py)
  - Documentation: READMEs, __doc__ strings, and other technical altruism basics
  - Debugging (intro to JupyterLab debugger)
  - Code Testing (e.g. test_fun: a function that checks that `fun` returns the expected outputs on some set of inputs)
  - Algorithms: different approaches for solving computational problem

  

This notebook contains some exercises to get you familiar with basic Python programming notions.




There are multiple data types in Python 
Similar to the notion of number sets in math $\mathbb{Z}$, $\mathbb{R}$ etc., computers variables also come in different types



Just enough to be dangerous with numbers and for loops.
Nothing fancy. We'll be mostly using Python as a basic calculator for math expressions,


and "boring" calculations that require repeating the same action many times (for loops).

So if you know how to use a calculator, then you know how to use Python too.


If you remember some basic math concepts like variables, expressions, and functions,
then you already know most of all there is to know!



We can access individual values within the series using the square brackets, and zero-based indexing. Recall this is the same syntax that we use to access elements in a Python list.
>>> s[0]

If you want just the values, get `.values` first, then slice

    >>> s.values[0:3]
    array([3, 5, 7])

or slice then get the values

    >>> s[0:3].values
    array([3, 5, 7])