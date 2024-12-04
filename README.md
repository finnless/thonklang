# Thonklang ![](https://github.com/finnless/thonklang/workflows/tests/badge.svg)

Thonklang is a simple esolang for experimenting with different syntax and semantics of programming languages. It directly references the main control flow operator (🤔).

More information is availible on the [Thonklang entry of the esolangs wiki](https://esolangs.org/wiki/Thonklang).

## Installation

To install Thonklang, follow these steps:

1. Clone the repository:
    ```
    $ git clone https://github.com/finnless/thonklang.git
    $ cd thonklang
    ```

2. Install the requirements:
    ```
    $ pip install -r requirements.txt
    ```

3. Set the `PYTHONPATH` and run the esolang:
    ```
    $ export PYTHONPATH=.
    $ python -m esolang
    ```

## Examples


### Truth Machine
```
truth = lambda n: {
    🤔 n {
        # If input is 1, enter infinite loop
        while 1 {
            print(1);
        };
    } 😅 {
        # If input is 0, print once and terminate
        print(0);
    };
};
```


### If Statements

- `🤔` is the `if` keyword
- `😅` is the `else` keyword
- `1` is the condition that evaluates to `True`
- Any other condition evaluates to `False`


```
>>> interpreter.visit(parser.parse("🤔 1 1 😅 2"))
1
>>> interpreter.visit(parser.parse("🤔 0 1 😅 2"))
2
>>> interpreter.visit(parser.parse("a = 1; 🤔 a 5 😅 10"))
5
>>> interpreter.visit(parser.parse("🤔 1 - 1 3 😅 4"))
4
```


### For Loops

For loops accept arbitrary expressions inside of range() or a fixed constant.

```
>>> interpreter.visit(parser.parse("a=10; for i in range(a) { a = a - 1 }"))
0
```

### While Loops

- `while` is the keyword for the while loop
- The condition is evaluated before each iteration of the loop
- If the condition evaluates to `1`, the loop continues
- If the condition evaluates to any other value, the loop terminates

```
>>> interpreter.visit(parser.parse("a=1; while a { a = 0 }"))
0
>>> interpreter.visit(parser.parse("a=0; while a { a = 1 }"))
0
>>> interpreter.visit(parser.parse("a=1; b=0; while a { b = b + 1; 🤔 b - 2 a = 0 😅 a = 1; }; b"))
3
```


### Functions: Prime Numbers Demo

The following code is a demo of how to use functions to find prime numbers.

```
>>> interpreter.visit(parser.parse("is_divisible = lambda n,d: 🤔 n - ((n/d) * d) + 1 1 😅 0;"))
>>> interpreter.visit(parser.parse("is_divisible(10, 2)"))
1
>>> interpreter.visit(parser.parse("is_divisible(10, 3)"))
0
>>> interpreter.visit(parser.parse("is_divisible(9, 3)"))
1
>>> interpreter.visit(parser.parse("is_prime = lambda n: { result = 1; 🤔 n 0 😅 { for i in range(n-2) { d = i + 2; 🤔 is_divisible(n,d) { result = 0;  } 😅 { result = result; }; }; }; result };"))
>>> interpreter.visit(parser.parse("is_prime(1)"))
0
>>> interpreter.visit(parser.parse("is_prime(2)"))
1
>>> interpreter.visit(parser.parse("is_prime(3)"))
1
>>> interpreter.visit(parser.parse("is_prime(7)"))
1
>>> interpreter.visit(parser.parse("is_prime(8)"))
0
>>> interpreter.visit(parser.parse("find_primes = lambda n: { for i in range(n-1) { num = i + 2; 🤔 is_prime(num) { print(num); } 😅 0; }; };"))
>>> interpreter.visit(parser.parse("find_primes(50)"))
2
3
5
7
11
13
17
19
23
29
31
37
41
43
47
```