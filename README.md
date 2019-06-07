# OWScript
Python-like scripting language which transpiles into Overwatch Workshop script rulesets.

## Setup
Installation
====================
1. Install Python with `pip` if you have not done so already.
2. Install the requirements using `pip install -r requirements.txt` on your machine.
~3. Run the command `python owscript.py <filename>` to convert a file into workshop rules.~ 

## Documentation
*See example code in the `Examples/` folder. `.ows` files are input, `.ow` files are output.*
* [Values / Actions](#values--actions)
* [Annotations / Comments](#annotations--comments)
* [Assignment / Arithmetic](#assignment--arithmetic)
* [Logic](#logic)
* Data Types & Structures
  * [Variables](#variables)
  * [Strings](#strings)
  * [Vectors](#vectors)
  * [Time](#time)
  * [Arrays](#arrays)
* [Functions](#functions)
* [Loops](#loops)

## Notes
- Be sure not to conflict variable/function names with built-in functions such as `Add`, `Wait`, or `Damage`.

Values / Actions
================
Values and actions are the main types that come up when working in the Workshop. In general, anything with parameters can be written in two ways (which can be interchanged):

**Indented Blocks**
```
Round
    Count Of
        All Players
            Team 2
    Up
```
** Parenthesized **
```
Round(Count Of(All Players(Team 2)), Up) /* Same as output */
```

Annotations / Comments
======================
Annotations are ways to remind yourself what the type of a variable. It is written as text followed by a colon. Comments are written as most traditional languages (`// line comment`, `/* multiline comment */`). Both are ignored in the code output.
```
Event
    /* Set up event attributes */
    Event_Type: Ongoing - Event Player // Event_Type is an annotation (cannot have spaces!)
    Annotation_2: All
```

Assignment / Arithmetic
=======================
Assignment (regular and augmented), as well as most arithmetic operators work as they do in Python or other traditional programming languages. Operators include: `+ - * / ^ %` as well as the augmented equivalents: `+= -= *= /= ^= %=`
```
x = 1
x += -1
x *= 3
x = x ^ (x + x) % 3
```

Logic
=====
Boolean logic is implemented exactly as in Python. The operators `and`, `or`, and `not` function as C-style `&&`, `||`, and `!`. Comparison operators include the traditional `<`, `>`, `<=`, `>=`, `!=`, `==` as well as containment operators `in` and `not in`.
```
x = True and not True
Count Of
    Everyone
== 12 // The reason why == 12 is here is to distinguish between the constant "Everyone" and the value "Count Of".
// You can choose to write this expression inline for less ambiguity:
Count Of(Everyone) == 12
y = Event Player in Players In Radius(<1, 2, 3>, 15)
```

Variables
=========
There are 3 ways to manipulate variables:

**Explicit Global Assignment**
```
gVar globalvarname = 1
```
**Explicit Player Assignment**
```
pVar playervarname = 2
```
**Implicit Global Assignment**
```
varname = 3
```

Using the technique from [@ItsDeltin](https://github.com/ItsDeltin), the limit to
the number of variables that can be created is the maximum length of an array (\~1000 variables).

Strings
=======
There are two types of strings in the workshop: string literals and "formatted" strings, which take children as parameters to display. To write a string literal, simply enclose it in `"quotes"`, which can be used for rulenames. Formatted strings are enclosed with backticks (\`) and have the children nested the same way as a value.
```
Rule "String Demo"
    Event
        On Each Player
        All
        All
    Actions
        Msg(Event Player, "Hello") // Alias for Small Message
        Big Msg(Event Player, `{0}: {1}`
            "Money"
            pvar money
        )
        Small Msg(Event Player, `{0}!`("Victory"))
```

Vectors
=======
Vectors can be created in 3 ways as well:

**Function**
```
Vector(1, 2, 3)
```
**Constructor**
```
Vector
    1
    2
    3
```

**Idiomatic**
```
<1, 2, 3>
```

Time
====
Time can be represented in *ms*, *s*, or *min*.
```
Wait(1s + 500ms)
Wait
    0.025min
```

Arrays
======
Arrays are created, modified, and accessed as in Python notation. Arrays can be nested inside the global/player variables, which allows for more complex operations on arrays. (No slice support yet)

**Creation**
```
empty = []
costs = [5, 15, 30]
```
**Modification**
```
costs[1] = 20
total = costs[0] + costs[1] + costs[2]
```

Functions
=========
Functions allow you to write a block of code once and reuse it many times. They can be used to generate HUDs like a macro or used as a rule factory. All functions must be defined before they are called, and they must be defined at the top level scope (same as where rules are defined):

**Input**
```
%event_func
    Event
        On Each Player
        All
        All
%add_rule(a, b, name_)
    Rule name_
        event_func()
        x = a + b
Rule "Function Demo"
    event_func()
add_rule(1, 5, "Add Two")
```
**Output**
```
rule("Function Demo") {
   Event {
      Ongoing - Each Player;
      All;
      All;
   }
}

rule("Add Two") {
   Event {
      Ongoing - Each Player;
      All;
      All;
   }

   Actions {
      Set Global Variable At Index(A, 0, Add(1, 5));
   }
}
```

Loops
=====
The while loop is syntactic sugar for using the `Loop` action in the Workshop. At the moment, only use while loops if the purpose of the rule is solely to repeat code until a condition is met.
```
while pvar life > 10:
    Damage(Event Player, Null, 10)
```