import os
import pandas
import numpy
import datetime
from scheduling_model import SchedulingModel

def write_file(file_path_str, data):
    # Input data
    ## Aux inputs
    mapping_names = data[0]
    initial_date_str = data[1]
    ## Problem inputs
    num_products = data[2]["num_products"]
    periods = data[2]["periods"]
    purchase_costs = data[2]["purchase_costs"]
    fixed_costs = data[2]["fixed_costs"]
    holding_costs  = data[2]["holding_costs"]
    lead_times  = data[2]["lead_times"]
    init_inventory = data[2]["init_inventory"]
    min_lot_sizes = data[2]["min_lot_sizes"]
    lot_sizes = data[2]["lot_sizes"]
    demands = data[2]["demands"]
    
    solution_variables_values = data[3]


    max_lead_time = max(lead_times)

    initial_date = datetime.datetime.strptime(initial_date_str, "%d/%m/%Y")
    dates = [initial_date + datetime.timedelta(7 * i) for i in range(periods-max_lead_time)]

    products_id = []
    products_name = []
    for key, data in mapping_names.items():
        products_id.append(data[0])
        products_name.append(data[1])

    # Dados dependentes da solução
    products_lots = []
    total_products = []
    total_inventory = []
    for j in range(num_products):
        products_lots.append([])
        total_products.append([])
        total_inventory.append([])
        for t in range(max_lead_time, periods):
            var_name_product = SchedulingModel.get_var_name("X", j, t)
            value_product = solution_variables_values[var_name_product]
            products_lots[j].append(value_product)
            total_products[j].append(value_product * lot_sizes[j])
            
            var_name_inventory = SchedulingModel.get_var_name("I", j, t)
            value_inventory = solution_variables_values[var_name_inventory]
            total_inventory[j].append(value_inventory)
        
        # var_name_inventory = SchedulingModel.get_var_name("I", j, max_lead_time-1)
        # value_inventory = solution_variables_values[var_name_inventory]
        # total_inventory[j].insert(0, value_inventory)

    produtcs_arrived = []

    for j in range(num_products):
        produtcs_arrived.append([])
        for t in range(max_lead_time-lead_times[j], periods):
            var_name_product = SchedulingModel.get_var_name("X", j, t)
            value_product = solution_variables_values[var_name_product]
            produtcs_arrived[j].append(value_product * lot_sizes[j])


    # Data|Peça ID|Descrição|   Número de   |Tamanho| Estoque|    Total de   | Previsão |  Estoque   |  Custo  |
    #                       |Lotes a Comprar|do Lote|Anterior|Peças a Comprar|de Demanda|após Atender|de Compra| 


    dataframe_matrix = []
    for t in range(periods-max_lead_time):
        for j in range(num_products):
            line = []
            line.append(datetime.datetime.strftime(dates[t], "%d/%m/%Y"))
            line.append(products_id[j])
            line.append(products_name[j])
            line.append(products_lots[j][t])
            line.append(lot_sizes[j])
            line.append(total_products[j][t])
            if (t == 0):
                line.append(init_inventory[j])
            else:
                line.append(total_inventory[j][t-1])
            line.append(produtcs_arrived[j][t])
            line.append(demands[j][t+max_lead_time])
            line.append(total_inventory[j][t])
            cost_setup = 0
            if (total_products[j][t] != 0):
                cost_setup = fixed_costs[j][t]
            line.append(total_products[j][t]*purchase_costs[j][t+max_lead_time]+cost_setup)
            dataframe_matrix.append(line)

    dataframe_output = pandas.DataFrame(
        dataframe_matrix,
        columns=[
            "Data",
            "ID Produto",
            "Descrição",
            "Número de Lotes a Comprar",
            "Tamanho do Lote",
            "Total de Produtos a Comprar",
            "Estoque Anterior",
            "Produtos que Chegaram",
            "Previsão de Demanda",
            "Estoque após Atender",
            "Custo de Compra"
        ]
    )    

    # print(dataframe_output)

    file_path = os.path.join("", file_path_str)
    dataframe_output.to_csv(str(file_path), index=False)