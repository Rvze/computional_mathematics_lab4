from colorama import Fore, Style

FILE_INPUT = "/Users/nurgunmakarov/PycharmProjects/Lab4/iomanager/file_input.txt"
FILE_OUTPUT = "file_output.txt"


def input_from_file():
    data = {"dots": []}
    with open(FILE_INPUT, "rt", encoding="UTF-8") as f:
        try:
            for line in f:
                dot = tuple(map(float, line.strip().split()))
                if len(dot) != 2:
                    raise ValueError
                data["dots"].append(dot)
            if len(data["dots"]) < 2:
                raise AttributeError
        except AttributeError:
            return "FF"
        except ValueError:
            return "AA"
    return data


def input_from_keyboard():
    data = {"dots": []}
    print("Введите координаты")
    while True:
        try:
            dot = input(Fore.BLUE + "   >>  " + Style.RESET_ALL).strip()
            if dot == "stop":
                if len(data["dots"]) < 2:
                    raise AttributeError
                break
            dot_val = tuple(map(float, dot.split()))
            if len(dot_val) != 2:
                raise ValueError
            data["dots"].append(dot_val)
        except AttributeError:
            return None
        except ValueError:
            return "FF"
    print(data)
    return data
