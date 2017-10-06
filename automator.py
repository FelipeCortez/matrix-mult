import matplotlib.pyplot as plt
import numpy as np
import subprocess

plt.style.use("ggplot")

filenamePrefix = "matrizes/"
filenameSuffix = ".txt"

#sizes = [2 ** x for x in range(2, 12)][:-2]
sizes = [512]

repeats = 20

times_sequential = {}
times_concurrent = {}

def run_program(name, args):
    args = " ".join(args)
    command = "".join(["./", name, " ", args])
    result_str = subprocess.check_output(command, shell=True)
    # Output é bytestring e ultimo caractere é um newline
    result_str = result_str[:-1].decode("utf-8")
    # Remove os dois últimos caracteres (unidade) e converte pra inteiro
    return float(result_str[:-2])

for i in range(repeats):
    for s in sizes:
        result_sequential = run_program("multimat_sequencial", [str(s)])
        result_threaded_2 = run_program("multimat_concorrente", [str(s), '2'])
        result_threaded_3 = run_program("multimat_concorrente", [str(s), '3'])
        result_threaded_4 = run_program("multimat_concorrente", [str(s), '4'])

        k = "t" + str(s)
        if k not in times_sequential:
            times_sequential[k] = {"mat_size": str(s) + "x" + str(s), "times": []}
        if k not in times_concurrent:
            times_concurrent[k] = {"mat_size": str(s) + "x" + str(s), "times": []}
        times_sequential[k]["times"].append(result_sequential)
        times_concurrent[k]["times"].append(result_threaded_4)
        print(k)
    print("---")

for s in sizes:
    k = "t" + str(s)
    print(k)
    print("Média: ", np.mean(times_sequential[k]["times"]))
    print("Desvio:", np.std(times_concurrent[k]["times"]))

#boxplot_labels = ["512 (seq)", "512 (4 threads)"]
#plt.figure()
#plt.boxplot([times_sequential["t512"]["times"],
#            times_concurrent["t512"]["times"]],
#            positions = [1, 2],
#            widths = 0.6,
#            labels=boxplot_labels)
#plt.show()
