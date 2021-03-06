import ast
from evaluate import static_evaluate, UnknownValue
from type_objects import NoneType, Maybe
from context import Symbol


class Visitor(ast.NodeVisitor):
    def __init__(self):
        ast.NodeVisitor.__init__(self)
        self.names = []

    def visit_Name(self, node):
        self.names.append(node.id)


def get_names(node):
    visitor = Visitor()
    visitor.visit(node)
    return visitor.names


def maybe_inferences(test, context):
    types = {name: context.get_type(name) for name in get_names(test)}
    maybes = {k: v for k, v in types.items() if isinstance(v, Maybe)}

    if_inferences = {}
    else_inferences = {}
    for name, maybe_type in maybes.items():
        context.begin_scope()
        context.add(Symbol(name, NoneType(), None))
        none_value = static_evaluate(test, context)
        context.end_scope()
        if none_value is False:
            if_inferences[name] = maybe_type.subtype
        if none_value is True:
            else_inferences[name] = maybe_type.subtype
        context.begin_scope()
        context.add(Symbol(name, maybe_type.subtype, UnknownValue()))
        non_none_value = static_evaluate(test, context)
        context.end_scope()
        if non_none_value is False:
            if_inferences[name] = NoneType()
        if non_none_value is True:
            else_inferences[name] = NoneType()
    return if_inferences, else_inferences

