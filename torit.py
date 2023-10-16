from classroom import *
from teacher import *

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

    def staffClassrooms(self, lastRequirement = False):
        def assignTeacherToClassroom(teacher, classroom, times):
            for time in times:
                teacher.assignClassroom(classroom.name, time)
                classroom.assignTeacher(teacher.name, time)
                
        for classroom in self.classrooms:
            if classroom.isStaffed():
                continue
            
            timesUnstaffed = set(classroom.whenUnstaffed())
            for teacher in self.leadTeachersByClass(classroom):
                if not teacher.hasAvailability():
                    continue
                
                timesAvailable = set(teacher.whenAvailable())
                timesAligned = timesUnstaffed.intersection(timesAvailable)
                assignTeacherToClassroom(teacher, classroom, timesAligned)

                if lastRequirement and self.hasValidSchedule():
                    return True

                if classroom.isStaffed():
                    break

    def giveBreaks(self, lastRequirement = False):
        def idealBreakTime(possibleBreakTimes):
            return sorted(possibleBreakTimes, key = lambda time: abs((TIME_PERIODS-1)/2-time)).pop(0)
        
        for teacher in self.teachers:
            if "Break" in teacher.placements:
                continue

            #First try to find availability in their own schedule
            timesCouldHaveBreak = set(teacher.whenBreakable())
            timesAvailable = set(teacher.whenAvailable())
            timesAligned = timesCouldHaveBreak.intersection(timesAvailable)
            if timesAligned:
                teacher.setBreak(idealBreakTime(timesAligned))

            if "Break" in teacher.placements:
                continue  

            if teacher.isLead():
                sameClassroom = [classroom for classroom in self.classrooms if classroom.name == teacher.classroom][0]
                #print(sameClassroom)
                for otherTeacherName in sum(sameClassroom.placements, ()):
                    otherTeacher = [teacher for teacher in self.teachers if teacher.name == otherTeacherName][0]
                    if otherTeacher is None or not otherTeacher.hasAvailability() or teacher == otherTeacher:
                        continue
                    timesOtherTeacherAvailable = set(otherTeacher.whenAvailable())
                    timesBothAreAligned = timesCouldHaveBreak.intersection(timesOtherTeacherAvailable)
                    if timesBothAreAligned:
                        breakTime = idealBreakTime(timesBothAreAligned)
                        otherTeacher.assignClassroom(teacher.getClassroom(breakTime), breakTime)
                        #print("Taking ", teacher.name, " out of ", teacher.getClassroom(breakTime), " at ", breakTime, " so ", otherTeacher, " can cover their break")
                        teacher.setBreak(breakTime)
                        if lastRequirement and self.hasValidSchedule():
                            return True
                        break
            if "Break" in teacher.placements:
                continue      
            
            for otherTeacher in self.floatsByAvailability():
                if not otherTeacher.hasAvailability() or teacher == otherTeacher:
                    continue
                timesOtherTeacherAvailable = set(otherTeacher.whenAvailable())
                timesBothAreAligned = timesCouldHaveBreak.intersection(timesOtherTeacherAvailable)
                if timesBothAreAligned:
                    breakTime = idealBreakTime(timesBothAreAligned)
                    className = teacher.getClassroom(breakTime)
                    otherTeacher.assignClassroom(className, breakTime)
                    #print("Taking ", teacher.name, " out of ", teacher.getClassroom(breakTime), " at ", breakTime, " so ", otherTeacher, " can cover their break")
                    teacher.setBreak(breakTime)
                    classroom = [classroom for classroom in self.classrooms if classroom.name == className][0]
                    classroom.swapTeachers(otherTeacher.name, teacher.name, breakTime)
                    if lastRequirement and self.hasValidSchedule():
                        return True
                    break
                

    def leadTeachersByClass(self, classroom):
        return [teacher for teacher in self.teachers if teacher.isLead()]

    def floatsByAvailability(self): #can place floats who are already in that classroom first
        return sorted([teacher for teacher in self.teachers if teacher.isFloat()], key=lambda teacher: sum(teacher.availability), reverse=True)

    def noSolutionPossible(self):
        print("No Solution Possible")
        print(self)

    def complete(self):
        print("Solution Found")
        print(self)

    def __str__(self):
        return "=" * 60 + "\n" + "\n".join([teacher.__str__() for teacher in self.teachers]) + "\n" + "-" * 30 + "\n" + "\n".join([classroom.__str__() for classroom in self.classrooms]) + "\n" + "=" * 60


def setup():
    leadTeacherNames = ["Abby", "Beatrice", "Charlotte", "Danielle", "Emilia", "Francisca"]
    leadTeacherClassrooms = ["Infants", "Infants", "Toddlers", "Toddlers", "Pre-Primary", "Pre-Primary"]
    leadTeacherInfo = zip(leadTeacherNames, leadTeacherClassrooms)
    teachers = [LeadTeacher(name, classroom) for name, classroom in leadTeacherInfo]

    floatNames = ["Gregorica", "Hallie"]    
    teachers.extend([Float(name) for name in floatNames])

    classroomNames = ["Infants", "Toddlers", "Pre-Primary"]
    classrooms = [Classroom(name) for name in classroomNames]

    return School(teachers, classrooms)


torit = setup()
torit.staffClassrooms()
torit.giveBreaks()
if torit.hasValidSchedule():
    torit.complete()
