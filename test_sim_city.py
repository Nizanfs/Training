from sim_city import City, House, Neighborhood

BASIC_CITY_SIZE_TAX = 1308  # 1100 Base + 5 (Park) + 3 (House) + 200 (on the single house)


def build_basic_city():
    city = City()
    neighborhood_name = 'N1'
    city.build_a_neighborhood(neighborhood_name)
    city.build_a_park(neighborhood_name)
    city.build_a_house(neighborhood_name, 2, 100)
    return city


def test_basic_calculation():
    city = build_basic_city()
    assert city.how_much_money() == BASIC_CITY_SIZE_TAX
    city.ruin_a_neighborhood(city.neighborhoods[0].name)
    # 1100 Base + 5%.
    assert city.how_much_money() == 1155


def test_adding_park_calculation():
    city = build_basic_city()
    city.build_a_park(city.neighborhoods[0].name)
    assert city.how_much_money() == BASIC_CITY_SIZE_TAX + 5


def test_adding_house_calculation():
    city = build_basic_city()
    family_members = 5
    house_size = 200
    city.build_a_house(city.neighborhoods[0].name, family_members, house_size)
    # Base + new house tax + additional neighborhood tax.
    new_tax = BASIC_CITY_SIZE_TAX + (family_members * house_size) + 3
    assert city.how_much_money() == new_tax


def test_adding_new_neighborhood():
    city = build_basic_city()
    city.build_a_neighborhood('another')
    # Empty neighborhood , + (1100 City Base + 10%)
    new_tax = BASIC_CITY_SIZE_TAX + (1100 * 0.1)
    assert city.how_much_money() == new_tax


def test_basic_house_calculation():
    house = House(150, 5)
    assert house.calculate_tax() == 750


def test_basic_neighborhood_calculation():
    neighborhood = Neighborhood('some name')
    assert neighborhood.calculate_tax() == 0
    house = House(150, 5)
    neighborhood.houses.append(house)
    assert neighborhood.calculate_tax() == 753
    neighborhood.parks += 1
    assert neighborhood.calculate_tax() == 758
