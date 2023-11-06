import sys
import json


def do_abfolge(env, args):
    assert len(args) > 0
    for operation in args:
        result = do(env, operation)
    return result


# Multiplizieren
def do_multiplizieren(env, args):
    assert len(args) == 2
    left = do(env, args[0])
    right = do(env, args[1])
    return left * right


# Dividieren
def do_dividieren(env, args):
    assert len(args) == 2
    left = do(env, args[0])
    right = do(env, args[1])
    return left / right


# Potenzieren
def do_potenzieren(env, args):
    assert len(args) == 2
    left = do(env, args[0])
    right = do(env, args[1])
    return left ** right


# Print
def do_print(env, args):
    assert len(args) > 0
    print(args)


# While
def do_while(env, args):
    assert len(args) == 2
    cond = args[0]
    operation = args[1]
    if isinstance(cond, bool):
        while cond:
            exec(operation)
    elif isinstance(cond, int):
        count = 0
        while count < cond:
            exec(operation)
            count += 1


OPERATIONS = {
    func_name.replace("do_", ""): func_body
    for (func_name, func_body) in globals().items()
    if func_name.startswith("do_")
}


def do(env, expr):
    if isinstance(expr, int):
        return expr

    assert isinstance(expr, list)
    assert expr[0] in OPERATIONS, f"Unknown operation {expr[0]}"
    func = OPERATIONS[expr[0]]
    return func(env, expr[1:])


def main():
    assert len(sys.argv) == 2, "Usage: lgl_interpreter.py filename.gsc"
    with open(sys.argv[1], "r") as source_file:
        program = json.load(source_file)
    assert isinstance(program, list)
    env = {}
    result = do(env, program)
    print(f"=> {result}")


if __name__ == "__main__":
    main()
