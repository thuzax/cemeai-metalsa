
def read_file(file_name):
    purchase_costs = [] # p_jt
    fixed_costs = [] # s_jt
    holding_costs = [] # h_jt
    lead_times = [] # l_j
    demands = [] # d_jt

    with open(file_name, 'r') as f:
        number_of_products = int(f.readline().split()[1])
        periods = int(f.readline().split()[1])	
		
        purchase_costs = [0 for j in range(number_of_products)]
        f.readline()
        for j in range(number_of_products):
            purchase_costs[j] = int(f.readline())

        fixed_costs = [0 for j in range(number_of_products)]
        f.readline()
        for j in range(number_of_products):
            fixed_costs[j] = int(f.readline())

        lead_times = [0 for j in range(number_of_products)]
        f.readline()
        for j in range(number_of_products):
            lead_times[j] = int(f.readline())

        holding_costs = [0 for j in range(number_of_products)]
        f.readline()
        for j in range(number_of_products):
            holding_costs[j] = int(f.readline())

        demands = [[0 for t in range(periods)] for j in range(number_of_products)]
        f.readline()
        for j in range(number_of_products):
            e = f.readline().split()
            for t in range(periods):
                demands[j][t] = int(e[t])
    

    max_lead_time = max(lead_times)

    for j in range(number_of_products):
        for t in range(max_lead_time):
            demands[j].insert(0, 0)

    periods += max_lead_time
    
    constants = {
        "num_products": number_of_products,
        "periods": periods,
        "purchase_costs": tuple(purchase_costs), 
        "fixed_costs": tuple(fixed_costs),
        "holding_costs": tuple(holding_costs),
        "lead_times": tuple(lead_times),
        "demands": tuple(demands)
    }

    return (constants)