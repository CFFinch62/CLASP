# Logo Programming Tutorial

*A beginner's guide to Logo as a serious programming language*

---

Logo is far more than "that turtle graphics language." Developed at MIT in 1967 by Seymour Papert, Wally Feurzeig, and others, Logo is a full-featured language with powerful list processing, recursion, and functional programming capabilities. It was designed to teach computational thinking—and it excels at serious work.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Variables and Data](#variables-and-data)
3. [Procedures](#procedures)
4. [Lists: Logo's Secret Weapon](#lists-logos-secret-weapon)
5. [Recursion](#recursion)
6. [Word Processing](#word-processing)
7. [Higher-Order Functions](#higher-order-functions)
8. [Data Structures](#data-structures)
9. [Algorithms](#algorithms)
10. [Turtle Graphics (Bonus)](#turtle-graphics-bonus)

---

## Getting Started

**Example file:** `01_hello_world.logo`

The simplest Logo command is `print`:

```logo
print "Hello
print [Hello, World!]
```

- Words are prefixed with `"` (a quote mark)
- Phrases/lists are enclosed in `[brackets]`

**Try it:** Open `01_hello_world.logo` in CLASP and press **F5** to run.

---

## Variables and Data

**Example file:** `02_variables.logo`

Create variables with `make`:

```logo
make "name "Alice
make "age 25
make "colors [red green blue]
```

Access values with `:` prefix:

```logo
print :name        ; Alice
print :age         ; 25
print first :colors ; red
```

**Key insight:** Variables can hold words, numbers, or lists—Logo treats them uniformly.

---

## Procedures

**Example file:** `03_procedures.logo`

Define reusable procedures with `to` and `end`:

```logo
to square :n
  output :n * :n
end

print square 5    ; 25
```

- **Inputs** are declared after the procedure name with `:`
- Use `output` to return a value
- Use `stop` to exit without returning

**Multi-input procedures:**

```logo
to rectangle.area :width :height
  output :width * :height
end
```

---

## Lists: Logo's Secret Weapon

**Example file:** `04_lists.logo`

Lists are Logo's primary data structure and its most powerful feature:

```logo
make "data [10 20 30 40 50]
```

**Essential list operations:**

| Command | Result | Description |
|---------|--------|-------------|
| `first :data` | 10 | First element |
| `last :data` | 50 | Last element |
| `butfirst :data` | [20 30 40 50] | All but first |
| `butlast :data` | [10 20 30 40] | All but last |
| `count :data` | 5 | Length |
| `item 3 :data` | 30 | Element at position |
| `fput 5 :data` | [5 10 20 30 40 50] | Add to front |
| `lput 60 :data` | [10 20 30 40 50 60] | Add to end |

**Building lists:**

```logo
sentence [a b] [c d]   ; [a b c d] - flat combination
list [a b] [c d]       ; [[a b] [c d]] - nested
```

---

## Recursion

**Example file:** `05_recursion.logo`

Recursion is natural in Logo. Many problems become elegant one-liners:

```logo
to factorial :n
  if :n = 0 [output 1]
  output :n * factorial :n - 1
end
```

**Recursive list processing:**

```logo
to sum.list :lst
  if emptyp :lst [output 0]
  output (first :lst) + sum.list butfirst :lst
end

print sum.list [1 2 3 4 5]  ; 15
```

**Pattern:** Most recursive list functions follow this template:
1. Base case: empty list returns identity value
2. Recursive case: process first element, recurse on rest

---

## Word Processing

**Example file:** `06_word_processing.logo`

Words (strings) work like lists of characters:

```logo
make "word "programming
print first :word       ; p
print butfirst :word    ; rogramming
print count :word       ; 11
```

**Build words with `word`:**

```logo
print word "hello "world   ; helloworld
```

**Example: Reverse a word**

```logo
to reverse.word :w
  if emptyp :w [output "]
  output word reverse.word butfirst :w first :w
end

print reverse.word "hello  ; olleh
```

---

## Higher-Order Functions

**Example file:** `07_higher_order.logo`

Logo supports functions as first-class values:

**Map - transform each element:**

```logo
to double :n
  output :n * 2
end

print map "double [1 2 3 4 5]  ; [2 4 6 8 10]
```

**Filter - keep matching elements:**

```logo
to even? :n
  output (remainder :n 2) = 0
end

print filter "even? [1 2 3 4 5 6]  ; [2 4 6]
```

**Foreach - iterate:**

```logo
foreach [apple banana cherry] [
  print sentence [I like] ?
]
```

---

## Data Structures

**Example file:** `08_data_structures.logo`

Build any data structure from lists:

**Association list (dictionary):**

```logo
make "person [[name Alice] [age 30] [city Boston]]

to assoc :key :alist
  if emptyp :alist [output []]
  if (first first :alist) = :key [output last first :alist]
  output assoc :key butfirst :alist
end

print assoc "name :person   ; Alice
```

**Stack:**

```logo
make "stack []
to push :item
  make "stack fput :item :stack
end
to pop
  make "top first :stack
  make "stack butfirst :stack
  output :top
end
```

---

## Algorithms

**Example file:** `09_algorithms.logo`

Implement classic algorithms elegantly:

**Quicksort:**

```logo
to quicksort :lst
  if count :lst < 2 [output :lst]
  local "pivot
  make "pivot first :lst
  output (sentence
    quicksort filter [? < :pivot] butfirst :lst
    :pivot
    quicksort filter [? >= :pivot] butfirst :lst
  )
end
```

**GCD (Euclid's algorithm):**

```logo
to gcd :a :b
  if :b = 0 [output :a]
  output gcd :b remainder :a :b
end
```

**Prime check:**

```logo
to prime? :n
  if :n < 2 [output "false]
  output prime.helper :n 2
end

to prime.helper :n :divisor
  if :divisor * :divisor > :n [output "true]
  if (remainder :n :divisor) = 0 [output "false]
  output prime.helper :n :divisor + 1
end
```

---

## Turtle Graphics (Bonus)

**Example file:** `10_turtle_basics.logo`

Yes, Logo has turtle graphics—and they're wonderful for visualizing algorithms:

```logo
; Draw a square
repeat 4 [forward 100 right 90]

; Any regular polygon
to polygon :sides :size
  repeat :sides [fd :size rt 360 / :sides]
end

polygon 6 50  ; hexagon
```

Enable graphics in CLASP via **View → Graphics Window** (Ctrl+G).

---

## Learning More

Logo has a rich history and deep ideas. Recommended reading:

- **Computer Science Logo Style** by Brian Harvey (free online)
- **Mindstorms** by Seymour Papert
- **Turtle Geometry** by Abelson and diSessa

---

*CLASP - Coding in Logo to Attack Serious Problems*
