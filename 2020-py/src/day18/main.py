from src.helper import IO


def end_of_expression(partial_expression):
    cnt_parenthesis = 0
    for idx, ch in enumerate(partial_expression):
        if ch == '(':
            cnt_parenthesis += 1
        elif ch == ')':
            if cnt_parenthesis == 0:
                return idx
            cnt_parenthesis -= 1
        elif ch not in "0123456789" and cnt_parenthesis == 0:
            return idx
    return len(partial_expression)


def eval_expression(expression):
    expression = [ch for ch in expression]
    stack = [0]
    idx = 0
    while idx < len(expression):
        ch = expression[idx]
        if ch == '(':
            stack.append(idx+1)
        elif ch == ')':
            stack.pop(-1)
        # elif ch in "+*":
        elif ch == "*":
            stack[-1] = idx+2
        elif ch == "+":
            expression.insert(stack[-1], '[')
            expression.insert(idx+3 + end_of_expression(expression[(idx+3):]), ']')
            idx += 1
        idx += 1
    expression = ''.join(expression).replace('[', '(').replace(']', ')')

    exec_local = {}
    exec("result = {}".format(expression), globals(), exec_local)
    return exec_local['result']


IO.write(sum([eval_expression(line) for line in IO.read_all()]))
