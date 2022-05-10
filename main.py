import numpy as np
from colorama import Fore, Style

import solver
from iomanager import iomanager as io
import graphic


def pirson_parse(r):
    print("\nКоэффициент Пирсона:")
    print(temporary_ans[0]['pirson'].real)
    if r < 0.3:
        print(Fore.RED + "Связь слабая" + Style.RESET_ALL)
    elif 0.3 <= r < 0.5:
        print(Fore.YELLOW + "Связь умеренная" + Style.RESET_ALL)
    elif 0.5 <= r < 0.7:
        print(Fore.BLUE + "Связь заметная" + Style.RESET_ALL)
    elif 0.7 <= r < 0.9:
        print(Fore.GREEN + "Связь высокая" + Style.RESET_ALL)
    elif 0.9 <= r < 0.99:
        print(Fore.GREEN + "Связь весьма высокая" + Style.RESET_ALL)
    elif r >= 0.99:
        print(Fore.GREEN + "Связь очень высокая" + Style.RESET_ALL)


if __name__ == '__main__':
    data = {"dots": []}
    print("Лабораторная работа №4")
    print("Аппроксимация функции")
    print("\nОсуществить ввод с файла(f), с консоли(c)")
    choise = None
    while (choise != "f") and (choise != "c"):
        choise = input(Fore.MAGENTA + ">>  " + Style.RESET_ALL)

    if choise == "f" or choise == "F":
        data = io.input_from_file()
        print(data)
    else:
        data = io.input_from_keyboard()
    answer = []
    temporary_ans = [solver.lin_appr(data["dots"]),
                     solver.sqrt_appr(data["dots"]),
                     solver.pol_3_appr(data["dots"]),
                     solver.exp_appr(data["dots"]),
                     solver.log_appr(data["dots"]),
                     solver.pow_appr(data["dots"])]
    if temporary_ans[4] is None:
        print(Fore.RED + "Подлогарифмическое выражение должно быть больше нуля!" + Style.RESET_ALL)

    if temporary_ans[5] is None:
        print(Fore.RED + "Значения степенной функции должны быть больше нуля!" + Style.RESET_ALL)
    if temporary_ans[3] is None:
        print(Fore.RED + "Эксп. функция не меньше нуля!" + Style.RESET_ALL)

    for i in temporary_ans:
        if i is not None:
            answer.append(i)

    print("%20s %35s" % (Fore.GREEN + "Вид функции", "Среднеквадратичное отклонение" + Style.RESET_ALL))
    print(Fore.BLUE + "_" * 200 + Style.RESET_ALL)
    for i in answer:
        print('%30s %20s %1s %15s %20s %1s %10s %20s %1s %10s %20s %1s %10s %20s' % (
            i['str_func'], i['stdev'].real, Fore.YELLOW + "|" + Style.RESET_ALL, Fore.CYAN + "a = " + Style.RESET_ALL,
            i["a"].real,
            Fore.MAGENTA + "|" + Style.RESET_ALL,
            Fore.CYAN + "b = " + Style.RESET_ALL,
            i["b"].real, Fore.MAGENTA + "|" + Style.RESET_ALL, Fore.CYAN + "c = " + Style.RESET_ALL,
            i["c"].real if "c" in i else Fore.RED + "   None             " + Style.RESET_ALL,
            Fore.MAGENTA + "|" + Style.RESET_ALL,
            Fore.CYAN + "d = " + Style.RESET_ALL,
            i["d"].real if "d" in i else Fore.RED + "   None             " + Style.RESET_ALL,
        ))
    print(Fore.BLUE + "_" * 200 + Style.RESET_ALL)

    x = np.array([dot[0] for dot in data['dots']])
    y = np.array([dot[1] for dot in data['dots']])
    plot_x = np.linspace(np.min(x), np.max(x), 100)
    plot_y = []
    labels = []
    for i in answer:
        plot_y.append([i['func'](x) for x in plot_x])
        labels.append(i['str_func'])
    graphic.plot(x, y, plot_x, plot_y, labels)

    best_answer = min(answer, key=lambda z: z['stdev'].real)
    print("\nНаилучшая аппроксимирующая функция это:")
    print(f" {best_answer['str_func']}, где")
    print(f"  a = {best_answer['a'].real}")
    print(f"  b = {best_answer['b'].real}")
    print(f"  c = {best_answer['c'].real if 'c' in best_answer else 'None'}")
    print(f"  d = {best_answer['d'].real if 'd' in best_answer else 'None'}")
    pirson_parse(temporary_ans[0]["pirson"].real)
