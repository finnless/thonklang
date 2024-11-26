# esolang ![](https://github.com/finnless/esolang/workflows/tests/badge.svg)

A simple esolang for experimenting with different syntax and semantics of programming languages.



## Example Test Cases

### If Statements

- `🤔` is the `if` keyword
- `😅` is the `else` keyword
- `0` is the condition that evaluates to `True`
- Any other condition evaluates to `False`


```
> interpreter.visit(parser.parse("🤔 0 1 😅 2"))
1
> interpreter.visit(parser.parse("🤔 1 1 😅 2"))
2
> interpreter.visit(parser.parse("a = 0; 🤔 a 5 😅 10"))
5
> interpreter.visit(parser.parse("🤔 1 + 1 3 😅 4"))
4
```


### For Loops

For loops accept arbitrary expressions inside of range() or a fixed constant.

```
> interpreter.visit(parser.parse("a=10; for i in range(a) { a = a - 1 }"))
0
```

### While Loops

- `while` is the keyword for the while loop
- The condition is evaluated before each iteration of the loop
- If the condition evaluates to `0`, the loop continues
- If the condition evaluates to any other value, the loop terminates

```
> interpreter.visit(parser.parse("a=0; while a { a = 1 }"))
1
> interpreter.visit(parser.parse("a=1; while a { a = 0 }"))
> interpreter.visit(parser.parse("a=0; b=0; while a { b = b + 1; 🤔 b - 3 a = 1 😅 a = 0; }; b"))
3
```