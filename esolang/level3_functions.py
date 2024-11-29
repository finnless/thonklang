import lark
import pprint
import esolang.level2_loops
import re


grammar = esolang.level2_loops.grammar + r"""
    %extend start: function_call
        | function_def

    function_def: "lambda" NAME ("," NAME)* ":" start

    ?args_list: start ("," start)*

    function_call: NAME "(" args_list ")"
        | NAME "(" ")"
"""
parser = lark.Lark(grammar)


class Interpreter(esolang.level2_loops.Interpreter):
    '''
    >>> interpreter = Interpreter()
    >>> interpreter.visit(parser.parse("a=3; print(a)"))
    3
    >>> interpreter.visit(parser.parse("a=4; b=5; stack()"))
    [{'a': 4, 'b': 5}]
    >>> interpreter.visit(parser.parse("a=4; b=5; {c=6}; stack()"))
    [{'a': 4, 'b': 5}]
    >>> interpreter.visit(parser.parse("print(10)"))
    10
    >>> interpreter.visit(parser.parse("for i in range(10) {print(i)}"))
    0
    1
    2
    3
    4
    5
    6
    7
    8
    9
    >>> interpreter.visit(parser.parse(r"f = lambda x : x; f(5)"))
    5
    >>> interpreter.visit(parser.parse(r"f = lambda x,y : x+y; f(5, 6)"))
    11
    >>> interpreter.visit(parser.parse(r"f = lambda x,y,z : x+y-z; f(5, 6, 7)"))
    4
    >>> interpreter.visit(parser.parse(r"f = lambda x,y,z : {print(x); print(y); print(z); {z = 10; print(z);}; print(z);}; f(5, 6, 7)"))
    5
    6
    7
    10
    10
    >>> clean_code = lambda text: re.sub(r'\s+|\\n', ' ', re.sub(r'#.*$', '', text, flags=re.MULTILINE)).strip()
    >>> interpreter.visit(parser.parse("is_divisible = lambda n,d: 🤔 n - ((n/d) * d) + 1 1 😅 0;"))
    >>> interpreter.visit(parser.parse("is_divisible(10, 2)"))
    1
    >>> interpreter.visit(parser.parse("is_divisible(10, 3)"))
    0
    >>> interpreter.visit(parser.parse("is_divisible(9, 3)"))
    1
    >>> interpreter.visit(parser.parse("is_divisible(8, 2)"))
    1
    >>> interpreter.visit(parser.parse("is_divisible(7, 2)"))
    0
    >>> interpreter.visit(parser.parse("is_divisible(7, 3)"))
    0
    >>> interpreter.visit(parser.parse("is_divisible(7, 4)"))
    0
    # is_prime = lambda n: { result = 1; for i in range(n-2) { d = i + 2; 🤔 is_divisible(n,d) { result = 0; } 😅 { result = result; }; }; result };

    >>> is_prime_func_str = clean_code("""
    ... is_prime = lambda n: {
    ...     result = 1;  # Assume prime until proven otherwise
    ...     for i in range(n-2) {
    ...         d = i + 2;  # Makes d go from 2 to n-1
    ...         🤔 is_divisible(n,d) {
    ...             result = 0;  # Found a divisor, not prime
    ...         } 😅 {
    ...             result = result;  # No divisor found yet
    ...         };
    ...     };
    ...     result
    ... };
    ... """)
    >>> interpreter.visit(parser.parse(is_prime_func_str))
    >>> interpreter.visit(parser.parse("is_prime(3)"))
    1
    >>> interpreter.visit(parser.parse("is_prime(7)"))
    1
    >>> interpreter.visit(parser.parse("is_prime(8)"))
    0
    >>> interpreter.visit(parser.parse("is_prime(9)"))
    0
    >>> interpreter.visit(parser.parse("is_prime(10)"))
    0
    >>> interpreter.visit(parser.parse("is_prime(11)"))
    1
    >>> interpreter.visit(parser.parse("is_prime(15)"))
    0
    '''
    # TODO is_prime(2) and 1 is broken
    # >>> interpreter.visit(parser.parse("is_prime(2)"))
    # 1
    def __init__(self):
        super().__init__()

        # we add a new level to the stack
        # the top-most level will be for "built-in" functions
        # all lower levels will be for user-defined functions/variables
        # the stack() function will only print the user defined functions
        self.stack.append({})
        self.stack[0]['print'] = print
        self.stack[0]['stack'] = lambda: pprint.pprint(self.stack[1:])

    def function_def(self, tree):
        names = [token.value for token in tree.children[:-1]]
        body = tree.children[-1]
        def foo(*args):
            self.stack.append({})
            for name, arg in zip(names, args):
                self._assign_to_stack(name, arg)
            ret = self.visit(body)
            self.stack.pop()
            return ret
        return foo

    def function_call(self, tree):
        name = tree.children[0]

        # the tree can be structured in different ways depending on the number of arguments;
        # the following lines convert the params list into a single flat list
        params = [self.visit(child) for child in tree.children[1:]]
        params = [param for param in params if param is not None]
        if len(params) > 0 and isinstance(params[-1], list):
            params = params[0]

        return self._get_from_stack(name)(*params)
