# owscript
Python-like scripting language which transpiles into Overwatch Workshop script rulesets.

## Usage
*See example code in `Tests/`.*

#### Comments
Comments are written as text followed by a colon before any rule. They can
be used for type hints once autocompletion is done for text editors.
```
Event
    Event_Type: Ongoing - Event Player
    other_comment_tag: All
```

#### Variables
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

#### Vectors
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