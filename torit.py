class School:
    def __init__(self, teachers=[], classrooms=[]):
        self.teachers = teachers
        self.classrooms = classrooms

    def hasInvalidSchedule(self):
        alwaysStaffed = all([classroom.is_staffed() for classroom in self.classrooms])
        singleStaffed = self.isSingleStaffed()
        return not (alwaysStaffed and singleStaffed)

    def isSingleStaffed(self):
        allPlacements = [classroom.placements for classroom in self.classrooms]
        hourlyPlacements = [list(x) for x in zip(*allPlacements)]
        def noOneDoubleBooked(hourOfPlacements):
            seen = set()
            nonNonePlacements = [x for x in sum(hourOfPlacements, ()) if x is not None]
            return not any(person in seen or seen.add(person) for person in nonNonePlacements)
        return all([noOneDoubleBooked(hour) for hour in hourlyPlacements])

    
    def teachersHaveNoAvailability(self):
        return not any([teacher.has_availability for teacher in self.teachers])

    def assignTeacherToClassroom(self, teacher, classroom, times):
        for time in times:
            teacher.assign_classroom(classroom.name, time)
            classroom.assign_teacher(teacher.name, time)

    def leadTeachersByClass(self, classroom):
        return [teacher for teacher in self.teachers if teacher.isLead()]

    def noSolutionPossible(self):
        print("No Solution Possible")
        print(self)

    def complete(self):
        print("Solution Found")
        print(self)

    def __str__(self):
        return "\n".join([teacher.__str__() for teacher in self.teachers]) + "\n" + "-" * 30 + "\n" + "\n".join([classroom.__str__() for classroom in self.classrooms])

class Teacher:
    def __init__(self, name):
        self.name = name
        self.availability = [True, True, True, True, True, True, True, True]
        self.placements = [None, None, None, None, None, None, None, None]

    def has_availability(self):
        return any(self.availability)

    def when_available(self):
        return [i for i in range(len(self.availability)) if self.availability[i]]

    def assign_classroom(self, classroom, time):
        self.availability[time] = False
        self.placements[time] = classroom

    def __str__(self):
        return self.name + "'s schedule: " + ", ".join([str(p) for p in self.placements])

    def isLead(self):
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
    pass

class Classroom:
    def __init__(self, name):
        self.name = name
        self.fully_staffed = [False, False, False, False, False, False, False, False]
        self.placements = [tuple([None]) for i in range(8)]

    def is_staffed(self):
        return all(self.fully_staffed)

    def when_unstaffed(self):
        return [i for i in range(len(self.fully_staffed)) if not self.fully_staffed[i]]

    def assign_teacher(self, teacher, time):
        if self.placements[time] == tuple([None]):
            self.placements[time] = tuple([teacher])
        else:
            self.placements[time] = self.placements[time] + tuple([teacher])
            self.fully_staffed[time] = True

    def __str__(self):
        return self.name + "'s schedule: " + ", ".join([str(p) for p in self.placements])

def setup():
    leadTeacherNames = ["Abby", "Beatrice", "Charlotte", "Danielle"]
    leadTeacherClassrooms = ["Infants", "Toddlers", "Toddlers", "Toddlers"]
    leadTeacherInfo = zip(leadTeacherNames, leadTeacherClassrooms)
    teachers = [LeadTeacher(name, classroom) for name, classroom in leadTeacherInfo]

    floatNames = ["Emilia", "Francisca"]    
    teachers.extend([Float(name) for name in floatNames])

    classroom_names = ["Infants", "Toddlers"]
    classrooms = [Classroom(name) for name in classroom_names]

    return School(teachers, classrooms)


def main():
    torit = setup()
    while torit.hasInvalidSchedule():
        if torit.teachersHaveNoAvailability():
            torit.noSolutionPossible()
            break
        for classroom in torit.classrooms:
            if classroom.is_staffed():
                continue
            
            times_unstaffed = classroom.when_unstaffed()
            for teacher in torit.leadTeachersByClass(classroom):
                if not teacher.has_availability():
                    continue
                
                times_available = teacher.when_available()
                times_aligned = set(times_unstaffed).intersection(set(times_available))
                torit.assignTeacherToClassroom(teacher, classroom, times_aligned)

                if not torit.hasInvalidSchedule():
                    return torit

                if classroom.is_staffed():
                    break
                

torit = main()
torit.complete()
