class Teacher:

    def __init__(self, name):
        self.name = name
        # slot,course ID
        self.time_slots = {}

    def __str__(self):
        return str(self.name) + " " + str(self.time_slots)
