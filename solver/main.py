import sys
from read_file import read_file
from scheduling_model import SchedulingModel


if __name__=="__main__":
    args = sys.argv[1:]

    if (len(args) < 1):
        print("Input não foi passado")
        exit(0)

    file_name = args[0]

    constants, mapping_names = read_file(args[0])

    print(constants)

    scheduling = SchedulingModel(constants_data=constants)
    scheduling.print_model()
    scheduling.solve_problem()

    for name, value in scheduling.solution_data.items():
        print(name, value)
    
