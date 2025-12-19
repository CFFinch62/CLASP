# PyLogo Language Reference

This document details the primitives, special forms, and features of the PyLogo dialect implemented in CLASP. It follows the UCBLogo standard where possible but includes specific Python-based extensions and Object-Oriented features.

## Data Types
- **Word**: Strings or numbers.
- **List**: Ordered collection of data `[a b c]`.
- **Array**: (Limited support)
- **True/False**: Boolean values.

## Special Forms
Special forms are core language constructs that determine evaluation order or scope.

- **`MAKE "var value` / `MAKE :var value`**: Assigns `value` to variable `var`.
- **`LOCAL "var`**: Declares `var` as local to the current procedure.
- **`LOCALMAKE "var value`**: Helper for `LOCAL "var` then `MAKE "var value`.
- **`TO procname :input1 :input2 ...`**: Defines a new procedure.
- **`FOR "var [start stop] [instructionlist]`**: Loop `var` from start to stop.
- **`TELL object`**: Sets context to `object` (OO feature).
- **`ASK object [instructionlist]`**: Runs instructions in context of `object`.
- **`MAKEATTR object "attr value`**: Sets an attribute on an object.

## Control Structures
- **`RUN [instructionlist]`**: Runs the instructions.
- **`REPEAT num [instructionlist]`**: Runs list `num` times.
- **`FOREVER [instructionlist]`**: Runs list indefinitely (use `STOP` or `BYE` to exit).
- **`IF condition [if-true-list]`**: Runs list if condition is TRUE.
- **`IFELSE condition [true-list] [false-list]`**: Runs true-list or false-list.
- **`TEST condition`**: Sets a hidden "test" flag.
- **`IFTRUE [list]` / `IFT [list]`**: Runs if last `TEST` was TRUE.
- **`IFFALSE [list]` / `IFF [list]`**: Runs if last `TEST` was FALSE.
- **`STOP`**: Exits the current procedure.
- **`OUTPUT value` / `OP value`**: Exits and returns `value`.
- **`BYE`**: Exits CLASP.
- **`IGNORE value`**: Discards a value (useful for side-effect-only calls).

## Data Structure Primitives

### Constructors
- **`WORD word1 word2`**: Concatenates words.
- **`LIST thing1 thing2`**: Creates a list.
- **`SENTENCE thing1 thing2` / `SE`**: Flattens lists and combines elements.
- **`FPUT thing list`**: Puts thing at front of list.
- **`LPUT thing list`**: Puts thing at end of list.
- **`COMBINE thing1 thing2`**: generic combiner.
- **`REVERSE list`**: Reverses list.
- **`GENSYM`**: Generates a unique symbol/word (e.g., `G1`).

### Selectors
- **`FIRST thing`**: First char or element.
- **`LAST thing`**: Last char or element.
- **`BUTFIRST thing` / `BF`**: All but first.
- **`BUTLAST thing` / `BL`**: All but last.
- **`ITEM index thing`**: Gets item at index (1-based).
- **`PICK list`**: Random element from list.
- **`REMOVE thing list`**: Removes all occurrences of thing.
- **`REMDUP list`**: Removes duplicates.

### Predicates (return TRUE/FALSE)
- **`WORD? thing` / `WORDP`**
- **`LIST? thing` / `LISTP`**
- **`EMPTY? thing` / `EMPTYP`**
- **`EQUAL? thing1 thing2` / `EQUALP`**
- **`BEFORE? word1 word2` / `BEFOREP`**
- **`MEMBER? thing list` / `MEMBERP`**
- **`SUBSTRING? thing1 thing2` / `SUBSTRINGP`**
- **`NUMBER? thing` / `NUMBERP`**

### Queries
- **`COUNT thing`**: Length of word or list.
- **`ASCII char`**: ASCII code.
- **`CHAR int`**: Char from ASCII code.
- **`MEMBER thing list`**: Returns sublist starting at thing.
- **`LOWERCASE word`**
- **`UPPERCASE word`**

## Arithmetic
- **`SUM a b` / `+`**
- **`DIFFERENCE a b` / `-`**
- **`PRODUCT a b` / `*`**
- **`QUOTIENT a b` / `/`**
- **`REMAINDER a b`** (Same sign as dividend)
- **`MODULO a b`** (Same sign as divisor)
- **`INT num`**: Truncate to integer.
- **`ROUND num`**: Round to nearest integer.
- **`ABS num`**
- **`SQRT num`**
- **`POWER base exp`**
- **`EXP num`** (e^num)
- **`LOG10 num`**
- **`LN num`**
- **`SIN deg` / `COS deg` / `ARCTAN num`**
- **`RADSIN rad` / `RADCOS rad` / `RADARCTAN num`**
- **`ISEQ from to`**: List of integers.
- **`RSEQ from to count`**: List of rationals.
- **`RANDOM num`**: Random integer 0..num-1.
- **`RERANDOM seed`**: Reseed RNG.

## Bitwise
- **`BITAND a b`**
- **`BITOR a b`**
- **`BITXOR a b`**
- **`BITNOT a`**
- **`ASHIFT num bits`** (Arithmetic shift)
- **`LSHIFT num bits`** (Logical shift)

## Logic
- **`AND tf1 tf2 ...`**
- **`OR tf1 tf2 ...`**
- **`NOT tf`**

## Turtle Graphics
(Aliases in parentheses)

- **`FORWARD dist` / `FD`**
- **`BACKWARD dist` / `BK` / `BACK`**
- **`LEFT deg` / `LT`**
- **`RIGHT deg` / `RT`**
- **`PENUP` / `PU`**
- **`PENDOWN` / `PD`**
- **`PENWIDTH width`**
- **`PENCOLOR color` / `PC`**
- **`HIDETURTLE` / `HT`**
- **`SHOWTURTLE` / `ST`**
- **`TURTLEWRITE text`**
- **`STARTFILL` / `ENDFILL`**
- **`SETXY x y`**
- **`SETX x` / `SETY y`**
- **`POSX` / `POSY`**
- **`HEADING` / `SETHEADING deg`**
- **`HOME`**
- **`CLEAR` / `CS` / `CLEARSCREEN`**
- **`DISTANCE turtle`**
- **`CREATETURTLE`**: Adds a new turtle actor.
- **`ALLTURTLES`**: format list of all turtles.
- **`CLONE`**: Clones current turtle.

## Workspace Management
- **`DEFINE procname [[inputs] [line1] [line2]...]`**
- **`TEXT procname`**: Get procedure source.
- **`THING "var` / `:var`**: Get variable value.
- **`PROCEDURE? name` / `PRIMITIVE?` / `DEFINED?` / `NAME?`**
- **`PROCEDURES`**: List user procedures.
- **`NAMES`**: List user variables.
- **`ERASE list` / `ER`**: Delete proc/var.
- **`ERALL`**: Erase everything.
- **`LOAD "filename`**: Load `.logo` or `.py` file.
- **`HELP "name`**: Print docstring of primitive.

## File I/O & OOP
- **`PRINT thing` / `PR`**
- **`TYPE thing`**
- **`SHOW thing`**
- **`READLIST` / `RL`**: Read line as list.
- **`READRAWLINE`**: Read line as word.
- **`OPENREAD "file`**: Returns Reader object.
- **`OPENWRITE "file`**: Returns Writer object.
- **`OPENAPPEND "file`**
- **`CLOSE fileobj`**
- **`CLOSEALL`**
- **`ERASEFILE "file` / `ERF`**
- **`FILE? "file`**: Exists?
- **`ACTOR object`**: Push object to actor stack.
- **`REMOVEACTOR object`**: Pop object.
