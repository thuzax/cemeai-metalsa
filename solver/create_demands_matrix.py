import sys
import pandas


def create_intance(argv):
    if (len(argv) < 3):
        print("Arquivo de entrada e numero de semanas são necessários.")
        return

    csv_data = read_csv_file(argv[1])
    number_of_weeks = int(argv[2])

    if (len(argv) >= 4):
        initial_week_index = int(argv[3])
    else:
        initial_week_index = 0



    # 0 -> 29
    # 1 -> 30

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
    weeks_column = csv_sorted["semana"].tolist()
    demands_column = csv_sorted["Transactio_Quantity"].tolist()

    for i in range(len(products_column)):
        j = products_mapping[products_column[i]]
        demands_matrix[j][weeks_column[i]] = demands_column[i]

    demands_matrix = [demands_matrix[j][initial_week_index:] for j in range(len(demands_matrix))]

    text = "Demanda"
    for row in demands_matrix:
        text += "\n"
        for item in row:
            text += str(item) + " "
    print(text)
    


def read_csv_file(file_name):
    daily_df_predicted = pandas.read_csv(file_name)
    return daily_df_predicted

if __name__=="__main__":
    create_intance(sys.argv)

