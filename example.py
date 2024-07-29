import matplotlib.pyplot as plt
import numpy as np
from core import InputVariable, Rule, FuzzySystem
from membership_functions import TriangularMembershipFunction

def test(system: FuzzySystem):
    test_values = [
        (10, 10),
        (4, 4),
        (0, 0),
        (10, 0),
        (0, 10),
        (2, 6),
        (6, 2),
    ]

    # PRINT TIP VALUES
    for test_value in test_values:
        tip = system.compute(food=test_value[0], service=test_value[1])
        print(f'Food: {test_value[0]}/10\t Service: {test_value[1]}/10\t Tip: {tip:.1f}%')


def draw_tip_value_plot(system):
    resolution = 30
    food_values = np.linspace(0, 10, resolution)
    service_values = np.linspace(0, 10, resolution)

    # GRID
    food_grid, service_grid = np.meshgrid(food_values, service_values)
    tip_grid = np.zeros_like(food_grid)

    for food_index in range(resolution):
        for service_index in range(resolution):
            food_value = food_values[food_index]
            service_value = service_values[service_index]
            tip_grid[food_index, service_index] = system.compute(food=food_value, service=service_value)

    fig, ax = plt.subplots()
    cp = ax.contourf(service_grid, food_grid, tip_grid, 200)

    ax.set_xlabel('Service quality')
    ax.set_ylabel('Food qualiy')
    ax.set_title('Tip values')
    ax.grid()
    fig.colorbar(cp, label='Tip ( % )')
    fig.show()


if __name__ == '__main__':
    service = InputVariable('service', input_range=[0, 10])
    food = InputVariable('food', input_range=[0, 10])

    service['bad'] = TriangularMembershipFunction(0, 0, 5)
    service['medium'] = TriangularMembershipFunction(0, 5, 10)
    service['good'] = TriangularMembershipFunction(5, 10, 10)

    food['bad'] = TriangularMembershipFunction(0, 0, 5)
    food['medium'] = TriangularMembershipFunction(0, 5, 10)
    food['good'] = TriangularMembershipFunction(5, 10, 10)

    tip_rules = [
        Rule(food['good'] & service['good'], 15),
        Rule(food['medium'], 10),
        Rule(food['good'] & service['bad'], 5),
        Rule(food['bad'] & service['good'], 10),
        Rule(food['bad'] & service['bad'], 0),
    ]

    fuzzy_system = FuzzySystem(tip_rules)
    draw_tip_value_plot(fuzzy_system)

    test(fuzzy_system)
