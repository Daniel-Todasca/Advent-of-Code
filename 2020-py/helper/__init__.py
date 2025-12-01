class IO:
    b_cleared_output = False

    @staticmethod
    def read_all_from(path):
        file = open(path, "r")
        input_data = [line for line in file]
        file.close()
        return input_data

    @staticmethod
    def read_all():
        return IO.read_all_from("input.txt")

    @staticmethod
    def write(*args, **kwargs):
        open_mode = "w"
        if IO.b_cleared_output:
            open_mode = "a"
        IO.b_cleared_output = True

        sep = " "
        fin = "\n"

        for key, value in kwargs.items():
            if key == "sep":
                sep = value
            elif key == "fin":
                fin = value

        file = open("output.txt", open_mode)
        for arg in args:
            file.write(str(arg))
            file.write(str(sep))
        file.write(str(fin))
        file.close()
