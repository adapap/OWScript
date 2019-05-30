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
  * [Variables](#variables)
  * [Vectors](#vectors)
  * [Time](#time)
  * [Arrays](#arrays)
* [Functions](#functions)

Values / Actions
================
Values and actions are the main types that come up when working in the Workshop. In general, anything with parameters can be written in two ways (which can be interchanged) with all semicolons ignored:

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
Annotations are ways to remind yourself what the type of a variable. It is written as text followed by a colon. Comments are written as most traditional languages (`/* comment */`). Both are ignored in the code output.
```
Event
    /* Set up event attributes */
    Event_Type: Ongoing - Event Player
    Annotation_2: All
```

Assignment / Arithmetic
=======================
Assignment (regular and augmented), as well as most arithmetic operators work as they do in Python or other traditional programming languages. Operators include: `+ - * / ^ %` as well as the augmented equivalents: `+= -= *= /= ^= %=`
```
x = 1
x += 1
x *= 3
x = x ^ (x + x) % 3
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
the number of variables that can be created is the maximum length of an array.

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
Wait(1500ms)
Wait 1.5s
Wait
    0.025min
```

Arrays
======
Arrays are created, modified, and accessed as in Python notation.
*WIP - Currently, only Empty Arrays work by setting a variable equal to*`[]`

Functions
=========
Functions allow you to write a block of code once and reuse it many times (parameters are WIP). All functions must be defined before they are called, and they must be defined at the top level scope (same as where rules are defined):

**Input**
```
%event_func
    Event
        On Each Player
        All
        All
Rule "Function Demo"
    %event_func()
    Actions
        X = 1
```
**Output**
```
rule("Function Demo") {
    Event {
        Ongoing - Each Player;
        All;
        All;
    }

    Actions {
        Set Global Variable At Index(A, 0, 1);
    }
}

```