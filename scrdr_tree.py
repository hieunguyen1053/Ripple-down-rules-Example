from car import Car
from node import Node


class SCRDRTree:
    def __init__(self, root:Node=None):
        self.root = root

    def find_depth_node(self, node, depth):
        while node.depth != depth:
            node = node.parent
        return node

    def classify(self, obj):
        self.root.check(obj)

    def write_to_file_with_seen_cases(self, file_path):
        fout = open(file_path, 'w')
        self.root.write_to_file_with_seen_cases(fout, 0)
        fout.close()

    def write_to_file(self, file_path):
        fout = open(file_path, 'w')
        self.root.write_to_file(fout, 0)
        fout.close()

    def read_from_file(self, file_path):
        self.root = Node(Car(), 'unacc', None, None, None, [], 0)
        curr_node = self.root
        curr_depth = 0

        fin = open(file_path, 'r')
        lines = fin.readlines()

        for i in range(1, len(lines)):
            line = lines[i]
            depth = 0
            for c in line:
                if c == '\t':
                    depth += 1
                else:
                    break

            line = line.strip()
            if len(line) == 0:
                continue

            temp = line.find('cc')
            if temp == 0:
                continue

            condition = get_condition(line.split(" : ", 1)[0].strip())

            conclusion = get_concrete_value(line.split(" : ", 1)[1].strip())

            node = Node(condition, conclusion, None, None, None, [], depth)

            if depth > curr_depth:
                curr_node.except_child = node
            elif depth == curr_depth:
                curr_node.else_child = node
            else:
                while curr_node.depth != depth:
                    curr_node = curr_node.parent
                curr_node.else_child = node

            node.parent = curr_node
            curr_node = node
            curr_depth = depth

    def find_fired_node(self, obj):
        curr_node = self.root
        fired_node = None

        reasons = []

        while True:
            not_none_atts = []
            for att in curr_node.condition.__dict__:
                if att == 'label':
                    continue
                if getattr(curr_node.condition, att) is not None:
                    not_none_atts.append(att)

            satisfied = True
            for att in not_none_atts:
                if getattr(curr_node.condition, att) is None:
                    continue
                if getattr(curr_node.condition, att) != getattr(obj, att):
                    satisfied = False
                    break

            if satisfied:
                fired_node = curr_node
                reasons.append(curr_node.condition.reason())
                except_child = curr_node.except_child
                if except_child is None:
                    break
                else:
                    curr_node = except_child
            else:
                else_child = curr_node.else_child
                if else_child is None:
                    break
                else:
                    curr_node = else_child
        return fired_node, reasons

def get_concrete_value(str):
    return str[str.find('"') + 1 : len(str) - 1]

def get_condition(str_condition):
    condition = Car()

    for rule in str_condition.split(" and "):
        rule = rule.strip()
        key = rule[rule.find(".") + 1 : rule.find(" ")]
        value = get_concrete_value(rule)

        if key == 'buying':
            condition.buying = value
        elif key == 'maint':
            condition.maint = value
        elif key == 'doors':
            condition.doors = value
        elif key == 'persons':
            condition.persons = value
        elif key == 'lug_boot':
            condition.lug_boot = value
        elif key == 'safety':
            condition.safety = value
        elif key == 'label':
            condition.label = value
    return condition

def get_num_rules(node: Node):
    if node is None:
        return 0
    if(node.except_child is None and node.else_child is None):
        return 1
    if(node.except_child is None and node.else_child is not None):
        return 1 + get_num_rules(node.else_child)
    if(node.except_child is not None and node.else_child is None):
        return 1 + get_num_rules(node.except_child)
    return 1 + get_num_rules(node.except_child) + get_num_rules(node.else_child)