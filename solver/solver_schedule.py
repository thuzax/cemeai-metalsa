import sys
import copy
from read_input import read_file
from write_output import write_file
from scheduling_model import SchedulingModel



def solve_shopping_scheduling(argv):

    if (len(argv) < 3):
        msg = "É necessário passar por parâmetro os caminhos "
        msg += "para os arquivos de entrada e saída, respectivamente."
        print(msg)
        return 0

    input_file_name = argv[1]
    output_file_name = argv[2]
    solver_name = "CBC"
    if (len(argv) >= 4):
        solver_name = argv[3]

    constants, mapping_names, initial_date = read_file(input_file_name)

    # print(constants)

    scheduling = SchedulingModel(constants_data=constants, solver_name=solver_name)
    # scheduling.print_model()
    scheduling.solve_problem()

    # for name, value in scheduling.solution_data.items():
    #     print(name, value)
    
    # print(mapping_names)
    # print(initial_date)

    data_to_write = (
        mapping_names,
        initial_date,
        constants,
        copy.deepcopy(scheduling.solution_data)
    )

    write_file(output_file_name, data_to_write)
    


    return 0

if __name__=="__main__":
    solve_shopping_scheduling(sys.argv)
