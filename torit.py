class School:
    def __init__(self, teachers=[], classrooms=[]):
        self.teachers = teachers
        self.classrooms = classrooms
        self.reasonsInvalid = []

    def hasValidSchedule(self):
        def allTeachersInOnePlaceAtOnce():
            allPlacements = [classroom.placements for classroom in self.classrooms]
            hourlyPlacements = [list(x) for x in zip(*allPlacements)]
            def noOneDoubleBooked(hourOfPlacements):
                seen = set()
                nonNonePlacements = [x for x in sum(hourOfPlacements, ()) if x is not None]
                return not any(person in seen or seen.add(person) for person in nonNonePlacements)
            return all([noOneDoubleBooked(hour) for hour in hourlyPlacements])

        def allTeachersHaveBreaks():
            return all(["Break" in teacher.placements for teacher in self.teachers])
            
        def allClassroomsAlwaysStaffed():
            return all([classroom.isStaffed() for classroom in self.classrooms])

        requirements = [allClassroomsAlwaysStaffed(), allTeachersInOnePlaceAtOnce(), allTeachersHaveBreaks()]
        
        if not all(requirements):
            self.reasonsInvalid = [i for i, x in enumerate(requirements) if not x]
            
        return all(requirements)
    
    def teachersHaveNoAvailability(self):
        return not any([teacher.hasAvailability for teacher in self.teachers])

    def staffClassrooms(self):
        for classroom in self.classrooms:
            if classroom.isStaffed():
                continue
            
            timesUnstaffed = classroom.whenUnstaffed()
            for teacher in self.leadTeachersByClass(classroom):
                if not teacher.hasAvailability():
                    continue
                
                timesAvailable = teacher.whenAvailable()
                timesAligned = set(timesUnstaffed).intersection(set(timesAvailable))
                self.assignTeacherToClassroom(teacher, classroom, timesAligned)

                if self.hasValidSchedule():
                    return True

                if classroom.isStaffed():
                    break

    def leadTeachersByClass(self, classroom):
        return [teacher for teacher in self.teachers if teacher.isLead()]

    def assignTeacherToClassroom(self, teacher, classroom, times):
        for time in times:
            teacher.assignClassroom(classroom.name, time)
            classroom.assignTeacher(teacher.name, time)

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

    def hasAvailability(self):
        return any(self.availability)

    def whenAvailable(self):
        return [i for i in range(len(self.availability)) if self.availability[i]]

    def assignClassroom(self, classroom, time):
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
        self.fullyStaffed = [False, False, False, False, False, False, False, False]
        self.placements = [tuple([None]) for i in range(8)]

    def isStaffed(self):
        return all(self.fullyStaffed)

    def whenUnstaffed(self):
        return [i for i in range(len(self.fullyStaffed)) if not self.fullyStaffed[i]]

    def assignTeacher(self, teacher, time):
        if self.placements[time] == tuple([None]):
            self.placements[time] = tuple([teacher])
        else:
            self.placements[time] = self.placements[time] + tuple([teacher])
            self.fullyStaffed[time] = True

    def __str__(self):
        return self.name + "'s schedule: " + ", ".join([str(p) for p in self.placements])

def setup():
    leadTeacherNames = ["Abby", "Beatrice", "Charlotte", "Danielle"]
    leadTeacherClassrooms = ["Infants", "Toddlers", "Toddlers", "Toddlers"]
    leadTeacherInfo = zip(leadTeacherNames, leadTeacherClassrooms)
    teachers = [LeadTeacher(name, classroom) for name, classroom in leadTeacherInfo]

    floatNames = ["Emilia", "Francisca"]    
    teachers.extend([Float(name) for name in floatNames])

    classroomNames = ["Infants", "Toddlers"]
    classrooms = [Classroom(name) for name in classroomNames]

    return School(teachers, classrooms)


def main():
    torit = setup()
    while not torit.hasValidSchedule():
        if torit.teachersHaveNoAvailability():
            torit.noSolutionPossible()
            break

        if 0 in torit.reasonsInvalid:
            if torit.staffClassrooms():
                return torit

        if 2 in torit.reasonsInvalid:
            print("yea")
            return torit
        
                

torit = main()
torit.complete()
