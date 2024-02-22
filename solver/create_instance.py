import sys
import pandas
import math

def arguments_are_ok(argv):
    if (len(argv) < 5):
        text = "Formato de entrada:"
        text += "\n\n"
        text += "python create_instance.py <previsao>.csv <dados-produtos>.csv "
        text += "<initial-date> <num-semanas> <path-to-save>.txt <semana-init>"
        text += "\n\n"
        text += "Obrigatórios: <previsao> <dados-produtos> <initial-date> <num-semanas> <path-to-save>"
        text += "\n"
        text += "Opcional: <semana-init> (= 0)"
        print(text)
        return False
    return True


def create_demands_matrix(csv_data, number_of_weeks, initial_week_index):
    products_ids = sorted(csv_data["Item"].unique().tolist())
    number_of_products = len(products_ids)

    products_mapping = {
        products_ids[j] : j
        for j in range(number_of_products)
    }
    
    demands_matrix = []
    for j in range(number_of_products):
        demands_matrix.append([])
        for t in range(number_of_weeks):
            demands_matrix[j].append(0)
    
    csv_sorted = csv_data.sort_values(by="semana")
    products_column = csv_sorted["Item"].tolist()
    weeks_column = [k-1 for k in csv_sorted["semana"].tolist()]
    demands_column = csv_sorted["Transactio_Quantity"].tolist()

    for i in range(len(products_column)):
        j = products_mapping[products_column[i]]
        demands_matrix[j][weeks_column[i]] = demands_column[i]

    demands_matrix = [demands_matrix[j][initial_week_index:] for j in range(len(demands_matrix))]

    # text = "Demanda"
    # for row in demands_matrix:
    #     text += "\n"
    #     for item in row:
    #         text += str(item) + " "
    # print(text)

    return demands_matrix


def read_csv_file(file_name):
    daily_df_predicted = pandas.read_csv(file_name)
    return daily_df_predicted


def filter_products(demands_data, products_data):
    prod_with_data = products_data["Item"].to_numpy().tolist()
    return demands_data[demands_data["Item"].isin(prod_with_data)]

def get_num_products(products_data):
    return len(products_data["Item"].unique().tolist())



def create_instance(argv):
    demands_data = read_csv_file(argv[1])
    products_data = read_csv_file(argv[2])
    initial_date = argv[3]
    last_week_index = int(argv[4])
    out_path = argv[5]
    if (len(argv) == 7):
        initial_week_index = int(argv[6])
    else:
        initial_week_index = 0
    
    products_data = products_data.sort_values(by="Item")

    num_prods = get_num_products(products_data)
    text = ""
    text += "Numero_Produtos " + str(num_prods)
    text += "\n"

    text += "Código Descrição"
    text += "\n"
    codes = products_data["Item"].to_numpy().tolist()
    descriptions = products_data["Descricao"].to_numpy().tolist()
    for i in range(num_prods):
        text += codes[i] + " " + descriptions[i]
        text += "\n"
    
    periods = last_week_index - initial_week_index
    text += "Numero_Períodos " + str(periods)
    text += "\n"

    text += "Data_Inicial " + initial_date
    text += "\n"

    purchase_costs = products_data["Custos_Compra"].to_numpy().tolist()
    text += "Custos_Compra"
    text += "\n"
    for cost in purchase_costs:
        for t in range(periods):
            text += str(round(cost, 2)) + " "
        text += "\n"

    fixed_costs = products_data["Custo_Fixo"].to_numpy().tolist()
    text += "Custos_Fixos"
    text += "\n"
    for cost in fixed_costs:
        for t in range(periods):
            text += str(round(cost, 2)) + " "
        text += "\n"
    
    lead_times = products_data["Lead_Times"].to_numpy().tolist()
    text += "Lead_Times"
    text += "\n"
    for lead_time in lead_times:
        text += str(math.ceil(lead_time))
        text += "\n"
    
    inventory_costs = products_data["Custos_Estoque"].to_numpy().tolist()
    text += "Custos_Estoque"
    text += "\n"
    for cost in inventory_costs:
        for t in range(periods):
            text += str(round(cost, 2)) + " "
        text += "\n"
    
    old_inventory = products_data["Estoque_Inicial"].to_numpy().tolist()
    text += "Estoque_Inicial"
    text += "\n"
    for value in old_inventory:
        text += str(value)
        text += "\n"

    min_lots = products_data["Lote_Minimo"].to_numpy().tolist()
    text += "Lote_Mínimo"
    text += "\n"
    for value in min_lots:
        if (value == 0):
            value = 1
        text += str(value)
        text += "\n"

    lot_sizes = products_data["Tamanho_Lote"].to_numpy().tolist()
    text += "Tamanho_Lote"
    text += "\n"
    for value in lot_sizes:
        if (value == 0):
            value = 1
        text += str(value)
        text += "\n"

    demands_data = filter_products(demands_data, products_data)
    demands_matrix = create_demands_matrix(demands_data, last_week_index, initial_week_index)
    text += "Demanda"
    text += "\n"
    for i in range(len(demands_matrix)):
        line = demands_matrix[i]
        for demand in line:
            text += str(demand) + " "
        if (i != len(demands_matrix)-1):
            text += "\n"

    with open(out_path, "w") as out_file:
        out_file.write(text)
    
if __name__=="__main__":
    argv = sys.argv
    if (arguments_are_ok(argv)):
        create_instance(argv)

