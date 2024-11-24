# esolang ![](https://github.com/finnless/esolang/workflows/tests/badge.svg)

A simple esolang for experimenting with different syntax and semantics of programming languages.



## Example Test Cases

### If Statements

Explination:
- `🤔` is the `if` keyword
- `😅` is the `else` keyword
- `0` is the condition that evaluates to `True`
- Any other condition evaluates to `False`

Examples:

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