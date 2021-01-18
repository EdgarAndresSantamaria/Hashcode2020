# This is a sample Python script.
# data structure convenions ...
from collections import defaultdict
from collections import Counter
# multiprocess
from multiprocessing import Pool
# logging
import time

class pizza_hut:

    '''
    Initializer object pizza hut
    '''
    def __init__(self, in_path, out_path):
        self.in_path = in_path  #input path
        self.out_path = out_path  # output path
        self.delivered = []  # the list of already took pizzas
        self.D = 0  # number of deliveries
        self.result = []  # list containing the output deliveries to write

        self.load()  # loading the initial data
        self.sorted_amounts = sorted(list(self.Amounts_2_ids.keys()), reverse=True)  #sorted amount list descending order
        # data information display
        print(" number of pizzas: {} \n number of 2 people teams {} \n number of 3 people teams {} \n number of 4 people teams {} \n\n ".format(
                self.M, self.T2, self.T3, self.T4))
        self.manage_deliveries()  #manage the deliveries launch
        self.write_out()  #generate the submission file

    '''
    Method that aims to fill the required output format
    '''
    def write_out(self):
        with open(self.out_path, "w") as f:
            f.write(str(self.D) + " \n")
            for line in self.result:f.write(line)

    '''
    Method that manages the control logic for each deliveries group
    '''
    def manage_deliveries(self):
        # control logic for deliveries
        # todo: here we must alleviate the effect of many teams (scalability phase)
        # must apply concurrency technologies to afford many teams efficiently
        acc = 0
        '''
        develop this idea somewhere....
        
        n_threats = 32   
         with Pool(n_threats) as p: # n_threats processes
                 p.map(self.deliver, [2])
        '''
        for loop in range(int(self.T2)): #deliver (number of 2 people teams: T2) pizza pairs
            start = time.time()
            self.deliver(2)
            end = time.time()
            acc += (end - start)

        for loop in range(int(self.T3)):  # deliver (number of 3 people teams: T3) pizza pairs
            start = time.time()
            self.deliver(3)
            end = time.time()
            acc += (end - start)
        for loop in range(int(self.T4)):  # deliver (number of 4 people teams: T4) pizza pairs
            start = time.time()
            self.deliver(4)
            end = time.time()
            acc += (end - start)
        print("time for delivery {}".format(acc))

    '''
    Method that delivers a pizza composition for a group
    - takes into account the ingredients already selected to maximize the distinct
    '''
    def deliver(self, team_number):
        #distributed deliveries
        base_id, amount_id = self.find_best_pizza()
        if base_id == -1:return
        amount_lst = [amount_id]
        # locally management of locks
        deliver_lst = [base_id]
        while len(deliver_lst) < team_number :
            best_pizza, best_amount_id = self.find_best_pizza(mode = "pair", pizza_lst=deliver_lst)  #get the best match for current ingredents
            if best_pizza == -1:return
            deliver_lst.append(best_pizza) #append the best pizza we found
            amount_lst.append(best_amount_id)

        # todo: quality controls (must ensure the formats and control errors in selection)
        for i, amount in enumerate(amount_lst):  #update available pizzas
            # this method alleviates the computattion with many pizzas
            amount_ids = self.Amounts_2_ids.pop(amount)
            amount_ids.remove(deliver_lst[i])
            self.Amounts_2_ids[amount] = amount_ids
        deliver_lst = [str(i) for i in deliver_lst]  #format output as string
        self.result.append("{} {} \n".format(team_number, " ".join(deliver_lst)))  #create submission line
        self.D += 1  #count new delivery

    '''
    In this method we aim to count the intersected items in the given lists
    - the method achieves linear computational cost O(n + m)
    '''
    def count_intersections(self, lst1, lst2):
        # this method alleviates the computation with many ingredients
        c1 = Counter(lst1)
        c2 = Counter(lst2)
        return {k: min(c1[k], c2[k]) for k in c1.keys() & c2.keys()}

    '''
    In this method we aim to find the pizza with: (base mode)
    - maximum possible amount of ingredients from available pizzas
    In this method we aim to find the pizza with: (pair mode)
    - less overlapped ingredients with the given ingredient list
    - maximum possible amount of ingredients from available pizzas
    '''
    def find_best_pizza(self, mode = "base", pizza_lst = []):
        pizza_id = -1
        amount_id = -1
        if mode == "pair":
            ingredient_lst = []
            non_overlap_amount = 0
            for pizza in pizza_lst: ingredient_lst += self.ids_2_ingredents[pizza]  # we create the current ingredents list
            ingredient_lst = list(set(ingredient_lst))  # get current unique ingredents
            max_overlapped = len(ingredient_lst)
        # programm the logic
        for amount in self.sorted_amounts:  # search every amount in descending order
            pizza_ids = self.Amounts_2_ids[amount]  # retrieve the current amount pizza list
            # heuristic prunning the non-probable best pizzas alleviates many pizzas problem
            if (mode == "pair"):
                if (amount < non_overlap_amount) or (amount == non_overlap_amount):
                    break #prune those non-probable amounts

            for pizza in pizza_ids:  # search every pizza in current amount
                if (mode == "pair") and (pizza not in pizza_lst):
                    current_ingredients = self.ids_2_ingredents[pizza]
                    overlap = sum(self.count_intersections(ingredient_lst, current_ingredients).values())
                    if overlap < max_overlapped:
                        pizza_id = pizza  # return the pizza with maximum ingredents
                        amount_id = amount
                        # apply heuristic to avoid keep searching until best pair is reached
                        # if the non - overlapped amount is bigger than amount we can discard
                        non_overlap_amount = amount - overlap

                elif (mode == "base"):
                    pizza_id = pizza  # return the pizza with maximum ingredients
                    amount_id = amount
                    break  # break search once encountered

            if pizza_id != -1 and (mode == "base"): break  # break search once encountered
        return pizza_id, amount_id

    def load(self):
        with open(self.in_path) as f:
            self.M, self.T2, self.T3, self.T4 = f.readline().split()  #headers loading
            self.Amounts_2_ids = defaultdict(list)  #we map the number of ingredents into pizza id's
            self.ids_2_ingredents = {}  # we map pizza id's with ingredents
            id = 0  #pizza identifier counter
            for pizza in f.readlines():  #loading pizza information
                self.Amounts_2_ids[int(pizza.split()[0])] += [id]
                self.ids_2_ingredents[id] = pizza.split()[1:]
                id+=1

if __name__ == '__main__':

    # Testing results for teams of 2, 3 and 4
    # a_example ( 0.0 secs )
    # b_little_bit_of_everything (0.20 secs )
    # c_many_ingredients (152.76883554458618 secs == 3 min)
    # d_many_pizzas ( 389.627845764160156 secs == 6 min )
    # e_many_teams ( 1683.0759224891663 sec == 28 min )

    # finalize development for team 2 data, then scale the algorithm (seems good performance )
    # todo: get better performance for e_many_teams
    pizza_hut0 = pizza_hut('C:\\Users\\BM007\\PycharmProjects\\Hashcode\\data\\a_example.in',
                          'C:\\Users\\BM007\\PycharmProjects\\Hashcode\\out\\a_example.out')

    pizza_hut1 = pizza_hut('C:\\Users\\BM007\\PycharmProjects\\Hashcode\\data\\b_little_bit_of_everything.in',
                           'C:\\Users\\BM007\\PycharmProjects\\Hashcode\\out\\b_little_bit_of_everything.out')

    pizza_hut2 = pizza_hut('C:\\Users\\BM007\\PycharmProjects\\Hashcode\\data\\c_many_ingredients.in',
                          'C:\\Users\\BM007\\PycharmProjects\\Hashcode\\out\\c_many_ingredients.out')

    pizza_hut3 = pizza_hut('C:\\Users\\BM007\\PycharmProjects\\Hashcode\\data\\d_many_pizzas.in',
                          'C:\\Users\\BM007\\PycharmProjects\\Hashcode\\out\\d_many_pizzas.out')

    pizza_hut4 = pizza_hut('C:\\Users\\BM007\\PycharmProjects\\Hashcode\\data\\e_many_teams.in',
                           'C:\\Users\\BM007\\PycharmProjects\\Hashcode\\out\\e_many_teams.out')