import py
from rpython.rlib.parsing.ebnfparse import parse_ebnf, make_parse_function
from AST import *

grammar = py.path.local('./').join('grammar.txt').read("rt")
regexs, rules, ToAST = parse_ebnf(grammar)
_parse = make_parse_function(regexs, rules, eof=True)

class Transformer(object):
    """ Transforms AST from the obscure format given to us by the ennfparser
    to something easier to work with
    """
    def _grab_stmts(self, star, context):
        stmts = []
        while star:
            stmt = self.visit_stmt(star.children[0], context)
            if isinstance(stmt, Function):
                context[stmt.name] = stmt
            # elif isinstance(stmt, ApplyFunc):
            #     for i in range(stmt.loop):
            #         stmts.append(stmt)
            else:
                stmts.append(stmt)

            if len(star.children) == 2:
                star = star.children[1]
            else:
                break
        return stmts
    
    def visit_program(self, node):

        if len(node.children) == 2:
            context = {}
            stmts = self._grab_stmts(node.children[0], context)
            # for name in context:
            #     context[name]._print()
            return Function('main', stmts)
        else:
            return Function('main', [])

    def visit_stmt(self, node, context):
        stmt_type = node.children[0].symbol
        # print('stmt type:' , stmt_type)
        if stmt_type == 'def':
            return self.visit_def(node.children[0], context)
        if stmt_type == 'await':
            return self.visit_await(node.children[0], context)
        if stmt_type == 'apply':
            return self.visit_apply(node.children[0], context)
        if stmt_type == 'print':
            return self.visit_print(node.children[0], context)
        if stmt_type == 'compute':
            return self.visit_compute(node.children[0], context)
        raise NotImplementedError

    def visit_def(self, node, context):
        name, _, star, _ = node.children
        return Function(name.additional_info, self._grab_stmts(star, context))
    def visit_await(self, node, context):
        _, target = node.children
        if target.symbol == 'apply':
            return AwaitAnother(self.visit_apply(target, context))
        if target.symbol == 'INTEGER':
            return AwaitSleep(int(target.additional_info))
    def visit_apply(self, node, context):
        name, _, loop = node.children
        return ApplyFunc(context[name.additional_info], int(loop.additional_info))
    def visit_print(self, node, context):
        _, target = node.children
        return Print(target.additional_info.strip('\"'))
    def visit_compute(self, node, context):
        _, target = node.children
        return Compute(int(target.additional_info))

transformer = Transformer()
def parse(source):
    """ Parse the source code and produce an AST
    """
    x = transformer.visit_program(_parse(source))
    # x._print()
    return x
    # return _parse(source)


