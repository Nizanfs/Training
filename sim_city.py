BASE_CITY_INITIAL_TAX = 1000


class City:

    def __init__(self):
        self.neighborhoods = {}
        self.base_city_tax = BASE_CITY_INITIAL_TAX

    def how_much_money(self):
        neighborhoods_tax = sum([neighborhood.calculate_tax() for neighborhood in self.neighborhoods])
        return self.base_city_tax + neighborhoods_tax

    def build_a_neighborhood(self, neighborhood_name):
        new_neighborhood = Neighborhood(neighborhood_name)
        self.neighborhoods[neighborhood_name] = new_neighborhood
        self.base_city_tax += (self.base_city_tax * 0.1)
        return 0

    def build_a_house(self, neighborhood_name, family_members, size):
        new_house = House(size, family_members)
        neighborhood = self.neighborhoods[neighborhood_name]
        neighborhood.houses.append(new_house)
        return 0

    def ruin_a_neighborhood(self, neighborhood_name):
        del self.neighborhoods[neighborhood_name]
        self.base_city_tax += (self.base_city_tax * 0.05)

    def build_a_park(self, neighborhood_name):
        neighborhood = self.neighborhoods[neighborhood_name]
        neighborhood.parks += 1


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


def calculate_house_tax(house_size, family_members):
    return house_size * family_members


def build_city():
    pass


if __name__ == '__main__':
    build_city()
