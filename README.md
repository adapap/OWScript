# owscript
Python-like scripting language which transpiles into Overwatch Workshop script rulesets.

## Usage
*See example code in `Tests/`.*

#### Comments
`comment_tag: All Players`
Comments are written as text followed by a colon before any rule. They can
be used for type hints once autocompletion is done for text editors.

#### Variables
There are 3 ways to manipulate variables:
`gVar globalvarname = 1` assigns a global variable to a value
`pVar playervarname = 2` assigns a player variable to a value
`varname = 3` defaults to a global variable

Using the technique from [@ItsDeltin](https://github.com/ItsDeltin), the limit to
the number of variables that can be created is the maximum length of an array.

#### Vectors
Vectors can be created in 3 ways as well:
**Function**
`Vector(1, 2, 3)`

**Constructor**
```Vector
    1
    2
    3
```

**Idiomatic**
`<1, 2, 3>`