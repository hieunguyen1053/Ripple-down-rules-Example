from car import Car
from scrdr_tree import SCRDRTree, get_num_rules

rdr_tree = SCRDRTree()
rdr_tree.read_from_file('car.rules')


with open('data/car.data') as f:
    count = 0
    total = 0
    for line in f:
        total += 1
        line = line.strip().split(',')
        car = Car(*line[:-1])
        node, reason = rdr_tree.find_fired_node(car)
        print('Car:', car, car.label, reason)
        if node.conclusion != line[-1]:
            count += 1
            print('Wrong conclusion:', node.conclusion, 'Expected:', line[-1])

    print('Total wrong:', count, 'Total:', total, (total-count)/total)

print(get_num_rules(rdr_tree.root))
