import os
from mip import *

class SchedulingModel():

    def __init__(self, constants_data):
        self.num_products = constants_data["num_products"]
        self.periods = constants_data["periods"]
        self.purchase_costs = constants_data["purchase_costs"]
        self.fixed_costs = constants_data["fixed_costs"]
        self.holding_costs  = constants_data["holding_costs"]
        self.lead_times  = constants_data["lead_times"]
        self.demands = constants_data["demands"]

        self.initialize_model()

    def initialize_model(self):
        self.model = Model(sense=MINIMIZE, solver_name="GRB")
        self.create_vars()
        return

    def define_object_function(self):
        return

    def create_vars(self):
        self.production = [
            [
                self.model.add_var("x_"+str(j)+","+str(t), var_type=CONTINUOUS, lb=0)
                for t in range(self.periods)
            ]
            for j in range(self.num_products)
        ] # X_jt
        setup = [] # Y_jt
        inventory = [] # I_jt



        return

    def create_constraints(self):
        return

    def solve_problem(self):
        data = {}
        return data

    def print_model(self):
        self.model.write("temp.lp")
        with open("temp.lp", "r") as f_model:
            text = f_model.read()
            print(text)
            os.remove("temp.lp")
        
        return

