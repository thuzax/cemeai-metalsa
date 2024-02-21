
def read_file(file_name):

    with open(file_name, 'r') as input_file:

        # Número de produtos
        number_of_products = int(input_file.readline().split()[1])
        
        # Pula linha de título
        input_file.readline()

        # Mapeia nome e código do produto com índice da linha

        mapping_products_name = {}
        for j in range(number_of_products):
            code_and_name = input_file.readline().split()
            product_code = code_and_name[0]
            product_name = " ".join(code_and_name[1:])
            mapping_products_name[j] = (product_code, product_name)
        
        # Número de períodos
        periods = int(input_file.readline().split()[1])	
        
        # Data Inicial
        initial_date = input_file.readline().split()[1]

        # Pula linha de título
        input_file.readline()

        # Custos de compra
        purchase_costs = []
        for j in range(number_of_products):
            line = input_file.readline().split()

            purchase_costs.append([])
            for t in range(periods):
                purchase_costs[j].append(float(line[t]))
    
        # Pula linha de título
        input_file.readline()
        
        # Custo de setup
        fixed_costs = []
        for j in range(number_of_products):
            line = input_file.readline().split()
            
            fixed_costs.append([])
            for t in range(periods):
                fixed_costs[j].append(float(line[t]))

        # Pula linha de título
        input_file.readline()

        # Lead times
        lead_times = []
        for j in range(number_of_products):
            lead_times.append(int(input_file.readline()))

        # Pula linha de título
        input_file.readline()

        # Custo de estoque
        holding_costs = []
        for j in range(number_of_products):
            line = input_file.readline().split()
            holding_costs.append([])
            for t in range(periods):
                holding_costs[j].append(float(line[t]))

        # Pula linha de título
        input_file.readline()

        # Estoque inicial
        initial_inventory = []
        for j in range(number_of_products):
            initial_inventory.append(int(input_file.readline()))

        # Pula linha de título
        input_file.readline()

        min_lot_sizes = []
        for j in range(number_of_products):
            min_lot_sizes.append(int(input_file.readline()))

        # Pula linha de título
        input_file.readline()

        lot_sizes = []
        for j in range(number_of_products):
            lot_sizes.append(int(input_file.readline()))

        # Pula linha de título
        input_file.readline()

        # Previsão de demandas
        demands = []
        for j in range(number_of_products):
            line = input_file.readline().split()

            demands.append([])
            for t in range(periods):
                demands[j].append(int(line[t]))
    

    # Adiciona períodos de acordo com o máximo de demandas
    max_lead_time = max(lead_times)
    for j in range(number_of_products):
        for t in range(max_lead_time):
            demands[j].insert(0, 0)
            purchase_costs[j].insert(0, purchase_costs[j][0])
            fixed_costs[j].insert(0, fixed_costs[j][0])
            holding_costs[j].insert(0, holding_costs[j][0])


    periods += max_lead_time

    constants = {
        "num_products": number_of_products,
        "periods": periods,
        "purchase_costs": tuple(tuple(k) for k in purchase_costs), 
        "fixed_costs": tuple(tuple(k) for k in fixed_costs),
        "lead_times": tuple(lead_times),
        "holding_costs": tuple(tuple(k) for k in holding_costs),
        "init_inventory": tuple(initial_inventory),
        "min_lot_sizes": tuple(min_lot_sizes),
        "lot_sizes": tuple(lot_sizes),
        "demands": tuple(demands)
    }

    return (constants, mapping_products_name, initial_date)