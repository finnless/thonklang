import lark
import esolang.level1_statements


grammar = esolang.level1_statements.grammar + r"""
    %extend start: forloop
        | whileloop

    forloop: "for" NAME "in" range block

    whileloop: "while" condition block

    range: "range" "(" start ")"
"""
parser = lark.Lark(grammar)


class Interpreter(esolang.level1_statements.Interpreter):
    '''
    >>> interpreter = Interpreter()
    >>> interpreter.visit(parser.parse("for i in range(10) {i}"))
    9
    >>> interpreter.visit(parser.parse("a=0; for i in range(10) {a = a + i}"))
    45
    >>> interpreter.visit(parser.parse("a=0; for i in range(10) {a = a + i}; a"))
    45
    >>> interpreter.visit(parser.parse("a=0; for i in range(10) {a = a + i}; i")) # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    ValueError: Variable i undefined
    >>> interpreter.visit(parser.parse("a=10; for i in range(a) { a = a - 1 }"))
    0
    >>> interpreter.visit(parser.parse("a=1; while a { a = 0 }"))
    0
    >>> interpreter.visit(parser.parse("a=0; while a { a = 1 }"))
    0
    >>> interpreter.visit(parser.parse("a=1; b=0; while a { b = b + 1; 🤔 b - 2 a = 0 😅 a = 1; }; b"))
    3
    '''
    def range(self, tree):
        return range(self.visit(tree.children[0]))

    def forloop(self, tree):
        varname = tree.children[0].value
        xs = self.visit(tree.children[1])
        self.stack.append({})
        for x in xs:
            self.stack[-1][varname] = x
            result = self.visit(tree.children[2])
        self.stack.pop()
        return result

    def whileloop(self, tree):
        self.stack.append({})
        result = 0
        condition = self.visit(tree.children[0])
        while condition == 1:
            result = self.visit(tree.children[1])
            condition = self.visit(tree.children[0])
        self.stack.pop()
        return result
