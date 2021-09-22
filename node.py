class Node:
    def __init__(self, condition, conclusion, parent=None, except_child=None, else_child=None, corner_stone_cases=[], depth=0):
        self.condition = condition
        self.conclusion = conclusion
        self.parent = parent
        self.except_child = except_child
        self.else_child = else_child
        self.corner_stone_cases = corner_stone_cases
        self.depth = depth

    def satisfied(self, object):
        return eval(self.condition)

    def execute_conclusion(self, object):
        return eval(self.conclusion)

    def append_corner_stone_case(self, case):
        self.corner_stone_cases.append(case)

    def check(self, object):
        if self.satisfied(object):
            self.execute_conclusion(object)
            if self.except_child:
                self.except_child.check(object)
        else:
            if self.else_child:
                self.else_child.check(object)

    def check_depth(self, object, length):
        if self.depth <= length:
            if self.satisfied(object):
                self.execute_conclusion(object)
                if self.except_child:
                    self.except_child.check_depth(object, length)
            else:
                if self.else_child:
                    self.else_child.check_depth(object, length)

    def find_parent(self):
        node = self
        parent_node = node.parent
        while parent_node:
            if parent_node.except_child == node:
                break
            node = parent_node
            parent_node = node.parent
        return parent_node

    def add_else_child(self, node):
        parent_node = self.find_parent()
        for object in parent_node.corner_stone_cases:
            if node.satisfied(object):
                print("The new rule fires the cornerstone cases of its father node!!!")
                self.find_parent().corner_stone_cases.remove(object)
        self.else_child = node
        return True

    def add_except_child(self, node):
        for object in self.corner_stone_cases:
            if node.satisfied(object):
                print("The new rule fires the cornerstone cases of its father node!!!")
                self.corner_stone_cases.remove(object)
        self.except_child = node
        return True

    def write_to_file_with_seen_cases(self, fout, depth):
        space = '\t' * depth
        fout.write(space + self.condition + ' : ' + self.conclusion + '\n')
        for case in self.corner_stone_cases:
            fout.write(' ' + space + 'cc: ' + str(case) + '\n')
        if self.except_child:
            self.except_child.write_to_file(fout, depth + 1)
        if self.else_child:
            self.else_child.write_to_file(fout, depth)

    def write_to_file(self, fout, depth):
        space = '\t' * depth
        fout.write(space + self.condition + ' : ' + self.conclusion + '\n')
        if self.except_child:
            self.except_child.write_to_file(fout, depth + 1)
        if self.else_child:
            self.else_child.write_to_file(fout, depth)