from enum import Enum

class House(Enum):
    BROBNAR = "Brobnar"
    DIS = "Dis"
    LOGOS = "Logos"
    MARS = "Mars"
    SANCTUM = "Sanctum"
    SHADOWS = "Shadows"
    UNTAMED = "Untamed"

class Card():
    def __init__(self, house, amberBonus = 0):
        self.house = house
        self.amberBonus = amberBonus
        self.playAbility = lambda x: None

class Action(Card):
    pass

class Artifact(Card):
    pass

class Creature(Card):
    def __init__(self, house, amberBonus = 0, power = 1, armour = 0):
        super().__init__(house, amberBonus)
        self.damage = 0
        self.power = power
        self.max_armour = armour
        self.cur_armour = armour

    @property
    def armour(self):
        #TODO should this return max or current?
        return self.max_armour

    @armour.setter
    def armour(self, value):
        self.max_armour = value
        self.cur_armour = value

    def take_damage(self, amount):
        self.damage += max(amount - self.cur_armour, 0)
        self.cur_armour = max(self.cur_armour - amount, 0)

class Upgrade(Card):
    pass

class Battleline():
    def __init__(self, creatures=None):
        if creatures is None:
            self.line = []
        else:
            self.line = creatures

    def __eq__(self,other):
        if isinstance(other, type(self)):
            return self.line == other.line
        #TODO do I want to make battlelines equal to arrays that match line?
        return false

    def __iter__(self):
        return iter(self.line)

    def __len__(self):
        return len(self.line)

    def get_all(self):
        return self.line

    def get_flanks(self):
        if len(self.line) == 0:
            return []

        elif len(self.line) == 1:
            return self.line

        return [self.line[0],self.line[-1]]

    def add(self, creature, leftFlank):
        if not type(creature) is Creature:
            raise ValueError("Only creatures may be added to the battleline.")

        self.line.insert(0 if leftFlank else -1, creature)

    def remove(self, creature):
        self.line.remove(creature)
