# OWScript
Python-like scripting language which transpiles into Overwatch Workshop script rulesets.
## Installation / Usage
1. Install Python with `pip` if you have not done so already.
2. Install the requirements using `pip install -r requirements.txt` on your machine.
~3. Run the command `python owscript.py <filename>` to convert a file into workshop rules.~ 

## Documentation
*See example code in the `Tests/` folder. `.ows` files are input, `.ow` files are output.*

### Annotations / Comments
Annotations are ways to remind yourself what the type of a variable. It is written as text followed by a colon. Comments are written as most traditional languages (`/* comment */`)
```
Event
    /* Set up event attributes */
    Event_Type: Ongoing - Event Player
    Annotation_2: All
```

### Assignment / Arithmetic
Assignment (regular and augmented), as well as most arithmetic operators work as they do in Python or other traditional programming languages.
```
x = 1
x += 1
x *= 3
x = x ^ (x + x) % 3
```

### Variables
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

### Vectors
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

### Arrays
Arrays are created, modified, and accessed as in Python notation.
*WIP - Currently, only Empty Arrays work by setting a variable equal to `[]`*