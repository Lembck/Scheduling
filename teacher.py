from constants import *

class Teacher:
    def __init__(self, name):
        self.name = name
        self.availability = [True, True, True, True, True, True, True, True]
        self.placements = [None, None, None, None, None, None, None, None]

    def hasAvailability(self):
        return any(self.availability)

    def whenAvailable(self):
        return [i for i in range(TIME_PERIODS) if self.availability[i]]

    def whenBreakable(self):
        return [i for i in range(2, TIME_PERIODS-2)]

    def setBreak(self, time):
        self.assignClassroom("Break", time)

    def getClassroom(self, time):
        return self.placements[time]

    def assignClassroom(self, classroom, time):
        self.availability[time] = False
        self.placements[time] = classroom

    def __str__(self):
        return self.name + "'s schedule: " + ", ".join([str(p) for p in self.placements])

    def isLead(self):
        return False

    def isFloat(self):
        return False

class LeadTeacher(Teacher):
    def __init__(self, name, classroom):
        Teacher.__init__(self, name)
        self.classroom = classroom

    def isLead(self):
        return True

class AssitantTeacher(Teacher):
    pass

class Float(Teacher):
    def isFloat(self):
        return True
