import random
import math

BASE_CITY_INITIAL_TAX = 1000


class City:

    def __init__(self):
        self.neighborhoods = []
        self.base_city_tax = BASE_CITY_INITIAL_TAX

    def how_much_money(self):
        neighborhoods_tax = sum([neighborhood.calculate_tax() for neighborhood in self.neighborhoods])
        return self.base_city_tax + neighborhoods_tax

    def build_a_neighborhood(self, neighborhood_name):
        print(f'Neighborhood \'{neighborhood_name}\' built')
        new_neighborhood = Neighborhood(neighborhood_name)
        self.neighborhoods.append(new_neighborhood)
        self.base_city_tax += (self.base_city_tax * 0.1)
        return 0

    def build_a_house(self, neighborhood_name, family_members, size):
        print(f'House built in \'{neighborhood_name}\' with {family_members} family members and of size {size}')
        new_house = House(size, family_members)
        neighborhood = self.__find_neighborhood(neighborhood_name)
        neighborhood.houses.append(new_house)
        return 0

    def ruin_a_neighborhood(self, neighborhood_name):
        print(f'Neighborhood \'{neighborhood_name}\' ruined')
        neighborhood = self.__find_neighborhood(neighborhood_name)
        self.neighborhoods.remove(neighborhood)
        self.base_city_tax += (self.base_city_tax * 0.05)

    def build_a_park(self, neighborhood_name):
        print(f'Park built in \'{neighborhood_name}\'')
        neighborhood = self.__find_neighborhood(neighborhood_name)
        neighborhood.parks += 1

    def __find_neighborhood(self, neighborhood_name):
        return [n for n in self.neighborhoods if n.name == neighborhood_name][0]


class House:
    def __init__(self, size, family_members):
        self.size = size
        self.family_members = family_members

    def calculate_tax(self):
        return self.size * self.family_members


class Neighborhood:
    def __init__(self, name):
        self.name = name
        self.houses = []
        self.parks = 0

    def __calculate_committee_tax(self):
        return (self.parks * 5) + (len(self.houses) * 3)

    def calculate_tax(self):
        committee_tax = self.__calculate_committee_tax()
        families_tax = sum([house.calculate_tax() for house in self.houses])
        return committee_tax + families_tax


def build_city():
    synville = City()
    synville.build_a_neighborhood(f'Neighborhood dummy1')
    synville.build_a_neighborhood(f'Neighborhood dummy2')
    tax = synville.how_much_money();
    for index in range(60):
        action = random.randint(1, 4)

        if action == 1:
            synville.build_a_neighborhood(f'Neighborhood {index}')

        elif action == 2:
            neighborhood = random.choice(synville.neighborhoods)
            synville.build_a_park(neighborhood.name)

        elif action == 3:
            neighborhood = random.choice(synville.neighborhoods)
            synville.build_a_house(neighborhood.name, random.randint(1,5), random.randint(40, 120))

        elif action == 4:
            if len(synville.neighborhoods) > 1:
                neighborhood = random.choice(synville.neighborhoods)
                synville.ruin_a_neighborhood(neighborhood.name)
            else:
                print('Skipped ruining, not enough neighborhoods')

        new_tax = synville.how_much_money()
        trend = 'DECREASED' if tax > new_tax else 'INCREASED'
        tax_diff = math.fabs(new_tax - tax)
        print(f'tax {trend} by {tax_diff}. Current: {new_tax}')
        tax = new_tax

    print(synville.how_much_money())


if __name__ == '__main__':
    build_city()
