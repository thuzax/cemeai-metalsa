import os
import math
from mip import *

class SchedulingModel():

    def __init__(self, constants_data):
        self.num_products = constants_data["num_products"]
        self.periods = constants_data["periods"]
        self.purchase_costs = constants_data["purchase_costs"]
        self.fixed_costs = constants_data["fixed_costs"]
        self.holding_costs  = constants_data["holding_costs"]
        self.lead_times  = constants_data["lead_times"]
        self.init_inventory = constants_data["init_inventory"]
        self.min_lot_sizes = constants_data["min_lot_sizes"]
        self.lot_sizes = constants_data["lot_sizes"]
        self.demands = constants_data["demands"]

        self.initialize_model()

    def initialize_model(self):
        self.model = Model(sense=MINIMIZE, solver_name="GRB")
        self.create_vars()
        self.define_object_function()
        self.create_constraints()
        return

    def define_object_function(self):
        self.model.objective = sum([
            sum([
                self.purchase_costs[j][t]*self.products[j][t] + 
                self.holding_costs[j][t]*self.inventory[j][t] + 
                self.fixed_costs[j][t]*self.setup[j][t]
            
                for t in range(self.periods)
            ])
            for j in range(self.num_products)
        ])


    def create_vars(self):
        # X_jt
        self.products = [
            [
                self.model.add_var("X_"+str(j)+","+str(t), var_type=INTEGER, lb=0)
                for t in range(self.periods)
            ]
            for j in range(self.num_products)
        ]

        # Y_jt
        self.setup = [
            [
                self.model.add_var("Y_"+str(j)+","+str(t), var_type=BINARY, lb=0)
                for t in range(self.periods)
            ]
            for j in range(self.num_products)
        ]
         
        # I_jt
        self.inventory = [
            [
                self.model.add_var("I_"+str(j)+","+str(t), var_type=CONTINUOUS, lb=0)
                for t in range(self.periods)
            ]
            for j in range(self.num_products)
        ]

        return

    def create_constraints(self):
        # I_j,(t-1) + X_j,(t-lt_j)*lotSize_j = I_j,t + D_j,t para todo j e para todo t
        ## periodo inicial nao tem I_j,(t-1)
        ## t - lt_j < 0
        ## estoque inicial adiciona no t == maxlt - 1

        max_lead_time = max(self.lead_times)

        self.flow_constraints = []
        for j in range(self.num_products):
            for t in range(self.periods):
                left_side = 0
                if (t > 0):
                    left_side += self.inventory[j][t-1]
                if t-self.lead_times[j] >= 0:
                    left_side += self.products[j][t-self.lead_times[j]] * self.lot_sizes[j]
                if (t == max_lead_time):
                    left_side += self.init_inventory[j]
                flow_constraint = self.model.add_constr(
                    left_side == self.inventory[j][t] + self.demands[j][t],
                    name='flow_'+str(j)+","+str(t)
                )
                self.flow_constraints.append(flow_constraint)

        # X_jt <= Y_jt * bigM/lotSize_j
        self.setup_constraint = [
            [
                self.model.add_constr(
                    self.products[j][t] 
                        <= 
                    self.setup[j][t] * 
                    math.ceil(sum([
                        self.demands[j][k] for k in range(t, self.periods)
                        ])
                        /
                        self.lot_sizes[j]
                    ),
                    name="setup_"+str(j)+","+str(t)
                )    
                for j in range(self.num_products)
            ]
            for t in range(self.periods)
        ]

        #  X_jt <= Y_jt * ceil(lotSize_j/lotSizeMin_j)
        self.lot_min_constraint = [
            [
                self.model.add_constr(
                    self.products[j][t] 
                        >= 
                    self.setup[j][t] * 
                    math.ceil(self.lot_sizes[j]/self.min_lot_sizes[j]),
                    name="lotMin_"+str(j)+","+str(t)
                )    
                for j in range(self.num_products)
            ]
            for t in range(self.periods)
        ]


    def solve_problem(self):
        status = self.model.optimize(max_seconds=300)
        if (status == OptimizationStatus.INFEASIBLE):
            print("Solução não encontrada!")
            exit(1)
        elif (status == OptimizationStatus.FEASIBLE):
            print("Solução não ótima encontrada")
        elif (status == OptimizationStatus.OPTIMAL):
            print("Solução ótima encontrada")

        self.solution_data = {}
        for var in self.model.vars:
            self.solution_data[var.name] = var.x

    def print_model(self):
        self.model.write("temp.lp")
        with open("temp.lp", "r") as f_model:
            text = f_model.read()
            print(text)
            os.remove("temp.lp")
        
        return

