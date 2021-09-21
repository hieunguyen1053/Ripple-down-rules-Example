class Car:
    def __init__(self, buying=None, maint=None, doors=None, persons=None, lug_boot=None, safety=None, label=None):
        self.buying = buying
        self.maint = maint
        self.doors = doors
        self.persons = persons
        self.lug_boot = lug_boot
        self.safety = safety
        self.label = label

    def __str__(self):
        return 'Car[' + ','.join([str(att) for att in self.__dict__.values()][:-1]) + ']'

    def reason(self):
        return ' and '.join(['{}=={}'.format(att, value) for att, value in self.__dict__.items() if value is not None])