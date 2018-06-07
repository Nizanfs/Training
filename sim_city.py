class City:

    def __init__(self):
        self.neighborhoods = {}
        self.base_city_tax = 1000

    def how_much_money(self):
        neighborhoods_tax = sum([self.__calculate_neighborhood_tax(neighborhood) for neighborhood in self.neighborhoods])
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

    @staticmethod
    def __calculate_house_tax(house):
        return house.size * house.family_members

    @staticmethod
    def __calculate_neighborhood_committee_tax(neighborhood):
        return (neighborhood.parks * 5) + (len(neighborhood.houses) * 3)

    def __calculate_neighborhood_tax(self, neighborhood):
        committee_tax = self.__calculate_neighborhood_committee_tax(neighborhood)
        families_tax = sum([self.__calculate_house_tax(house) for house in neighborhood.houses])
        return committee_tax + families_tax


class House:
    def __init__(self, size, family_members):
        self.size = size
        self.family_members = family_members


class Neighborhood:
    def __init__(self, name):
        self.name = name
        self.houses = []
        self.parks = 0


def calculate_house_tax(house_size, family_members):
    return house_size * family_members


def build_city():
    pass


if __name__ == '__main__':
    build_city()
