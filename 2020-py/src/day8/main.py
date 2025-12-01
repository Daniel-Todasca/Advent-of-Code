from src.helper import IO


def run_instructions(instr):
    accumulator = 0
    pointer = 0
    execution_set = set()
    b_finished = True

    while pointer < len(instr):
        if pointer in execution_set:
            b_finished = False
            break
        execution_set.add(pointer)

        keyword, args = instr[pointer].split()
        if keyword == "nop":
            pointer += 1
        elif keyword == "jmp":
            pointer += int(args)
        elif keyword == "acc":
            accumulator += int(args)
            pointer += 1

    return accumulator, b_finished


# IO.write(run_instructions(IO.read_all()))
orig_instr = IO.read_all()
for index in range(len(orig_instr)):
    instr_type = orig_instr[index].split()[0]
    saved_line = orig_instr[index]
    
    if instr_type == "nop":
        orig_instr[index] = orig_instr[index].replace("nop", "jmp")
    if instr_type == "jmp":
        orig_instr[index] = orig_instr[index].replace("jmp", "nop")

    acc, flag = run_instructions(orig_instr)
    if flag is True:
        IO.write(acc)
        break

    orig_instr[index] = saved_line
