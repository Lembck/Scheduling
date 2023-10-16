from constants import *

class Classroom:
    def __init__(self, name):
        self.name = name
        self.fullyStaffed = [False] * TIME_PERIODS
        self.placements = [(None,)] * TIME_PERIODS

    #Returns True if class is fully staffed throughout the day
    def isStaffed(self):
        return all(self.fullyStaffed)

    #Returns a list of times the classroom is not fully staffed
    def whenUnstaffed(self):
        return [time for time, staffed in enumerate(self.fullyStaffed) if not staffed]

    #Assigns a teacher to classroom at given time (limit of 2)
    def assignTeacher(self, teacher, time):
        if self.fullyStaffed[time]:
            print("Classroom already full at this time")
            return
        if self.placements[time] == (None,):
            self.placements[time] = (teacher,)
        else:
            self.placements[time] = self.placements[time] + (teacher,)
            self.fullyStaffed[time] = True

    #Replaces oldTeacher with newTeacher at given time
    def swapTeachers(self, newTeacher, oldTeacher, time):
        self.placements[time] = tuple(teacher for teacher in self.placements[time] if teacher != oldTeacher) + (newTeacher,)

    #Creates a string of the classroom object to print
    def __str__(self):
        return self.name + "'s schedule: " + ", ".join([str(placement) for placement in self.placements])
