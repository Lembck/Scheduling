class Requirement:
    def __init__(self, name, teachers, classrooms, placements, scores):
        self.name = name
        self.teachers = teachers
        self.classrooms = classrooms
        self.placements = placements
        self.scores = scores
        
    def condition(self):
        return False

    def descriptor(self):
        return

    def solver(self):
        return

    def logScores(self):
        self.scores.append(sum(classroom.percentageStaffed() for classroom in self.classrooms) + \
                           sum(teacher.hasBreak() for teacher in self.teachers))

    def createPlacement(self, teacher, location, timeslot):
        #print("teacher", teacher, "location", location, "time", timeslot)
        self.placements.append(Placement(teacher, location, timeslot))
        teacher.assign(location, timeslot)
        if location.isClassroom():
            location.staff(teacher, timeslot)
        self.logScores()

    def groupPlacements(self):
        def convert(x):
            mid = 15 * x + 450
            h = mid // 60
            m = mid % 60
            AMPM = "am" if h < 12 else "pm"
            h = h % 12
            if m == 0:
                m = "00"
            if h == 0:
                h = 12
            return str(h) + ":" + str(m) + AMPM
        def ranges(l):
            ranges = []
            for x in l:
                x = str(x)
                if not ranges:
                    ranges.append([x])
                elif int(x)-prev_x == 1:
                    ranges[-1].append(x)
                else:
                    ranges.append([x])
                prev_x = int(x)
            return ["-".join([convert(int(r[0])), convert(int(r[-1])+1)] if len(r) > 1 else convert(r)) for r in ranges]
        placementsByTeacher = {}
        placementsByTeacherClass = {}
        for placement in self.placements:
            if placement.teacher in placementsByTeacher:
                placementsByTeacher[placement.teacher].append(placement)
            else:
                placementsByTeacher[placement.teacher] = [placement]
                placementsByTeacherClass[placement.teacher] = {}
        for teacher in placementsByTeacher.keys():
            for placement in placementsByTeacher[teacher]:
                if placement.location in placementsByTeacherClass[teacher]:
                    placementsByTeacherClass[teacher][placement.location].append(placement.timeslot)
                else:
                    placementsByTeacherClass[teacher][placement.location] = [placement.timeslot]
        for teacher in placementsByTeacher.keys():
            for location in placementsByTeacherClass[teacher]:
                placementsByTeacherClass[teacher][location] = ranges(placementsByTeacherClass[teacher][location])
        print(placementsByTeacherClass)

class StaffingRequirement(Requirement):
    def condition(self):
        return all(classroom.isFullyStaffed() for classroom in self.classrooms)

    def descriptor(self):
        for classroom in self.classrooms:
            if not classroom.isFullyStaffed():
                print(classroom, "is not fully staffed:", classroom.percentageStaffed()*100, "%")

    def solver(self):
        def staffClassrooms():
            for classroom in self.classrooms:
                if classroom.isFullyStaffed():
                    continue
                for timeslot, t in enumerate(classroom.placements):
                    if classroom.isFullyStaffedAt(timeslot):
                        continue
                    for teacher in self.teachers:
                        if teacher.isAvailableAt(timeslot):
                            self.createPlacement(teacher, classroom, timeslot)
                            break
        staffClassrooms()
        staffClassrooms()

class BreakRequirement(Requirement):
    def condition(self):
        return all(teacher.hasBreak() for teacher in self.teachers)

    def descriptor(self):
        print(", ".join(str(t) for t in self.teachers if not t.hasBreak()), "don't have breaks")

    def solver(self):
        def removePlacement(teacher, location, timeslot):
            toBeRemoved = Placement(teacher, location, timeslot)
            if toBeRemoved in self.placements:
                self.placements.remove(toBeRemoved)# = [p for p in self.placements if p != toBeRemoved]
                teacher.unassign(location, timeslot)
                if location.isClassroom():
                    location.unstaff(teacher, timeslot)

        def onBreak(teacher, timeslot):
            self.createPlacement(teacher, Location("Break"), timeslot)
            #print(teacher, timeslot)

        def findBreakTimeslots(timeslots, teachers, timeslot, teacher):
            for otherTeacher in self.teachers:
                if otherTeacher.isAvailableAt(timeslot):
                    timeslots.append(timeslot)
                    teachers.append(otherTeacher)
                    return timeslots
            return []
        
        for teacher in self.teachers:
            if teacher.hasBreak():
                continue
            breakTimeslots = []
            coveringTeachers = []
            for timeslot in range(30):
                breakTimeslots = findBreakTimeslots(breakTimeslots, coveringTeachers, timeslot, teacher)
                if len(breakTimeslots) == 4:
                    break
            
            for breakTimeslot, coveringTeacher in zip(breakTimeslots, coveringTeachers):
                classroom = teacher.getClassroomAt(breakTimeslot)
                if classroom is not None:
                    removePlacement(teacher, classroom, breakTimeslot)
                    self.createPlacement(coveringTeacher, classroom, breakTimeslot)
                onBreak(teacher, breakTimeslot)

        self.groupPlacements()

##class LeadTeacherRequirement(Requirement):
##    def condition(self):
##        return all(class.lead
##
##    def descriptor(self):
##        return
##
##    def solver(self):
##        return

class School:
    def __init__(self, teachers, locations):
        self.teachers = teachers
        self.locations = locations
        self.classrooms = [location for location in self.locations if location.isClassroom()]
        self.placements = []
        self.scores = []
        self.setUpRequirements()
        self.solve()
        
    def setUpRequirements(self):
        self.requirements = [StaffingRequirement("S", self.teachers, self.classrooms, self.placements, self.scores),
                             BreakRequirement("B", self.teachers, self.classrooms, self.placements, self.scores)]
        

    def solved(self):
        return all(classroom.isFullyStaffed() for classroom in self.classrooms) and all(teacher.hasBreak() for teacher in self.teachers)

    def solve(self):
        while not self.solved():
            for requirement in self.requirements:
                if not requirement.condition():
                    requirement.descriptor()
                    requirement.solver()
                    

        print("Solved")
        self.groupPlacements()
        print(max(self.scores))

    def groupPlacements(self):
        def ranges(l):
            ranges = []
            for x in l:
                x = str(x)
                if not ranges:
                    ranges.append([x])
                elif int(x)-prev_x == 1:
                    ranges[-1].append(x)
                else:
                    ranges.append([x])
                prev_x = int(x)
            return ["-".join([r[0], r[-1]] if len(r) > 1 else r) for r in ranges]
        placementsByTeacher = {}
        placementsByTeacherClass = {}
        for placement in self.placements:
            if placement.teacher in placementsByTeacher:
                placementsByTeacher[placement.teacher].append(placement)
            else:
                placementsByTeacher[placement.teacher] = [placement]
                placementsByTeacherClass[placement.teacher] = {}
        for teacher in placementsByTeacher.keys():
            for placement in placementsByTeacher[teacher]:
                if placement.location in placementsByTeacherClass[teacher]:
                    placementsByTeacherClass[teacher][placement.location].append(placement.timeslot)
                else:
                    placementsByTeacherClass[teacher][placement.location] = [placement.timeslot]
        for teacher in placementsByTeacher.keys():
            for location in placementsByTeacherClass[teacher]:
                placementsByTeacherClass[teacher][location] = ranges(placementsByTeacherClass[teacher][location])
        print(placementsByTeacherClass)
            
class Class:
    def __init__(self, leadTeachers=[], students=[], classroom=None):
        self.leadTeachers = leadTeachers
        self.students = students
        self.classroom = classroom

class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age            
    
class Placement:
    def __init__(self, teacher, location, timeslot):
        self.teacher = teacher
        self.location = location
        self.timeslot = timeslot

    def __str__(self):
        return self.teacher.name + " in " + self.location.name + " at " + str(self.timeslot)

    def __repr__(self):
        return self.teacher.name + " in " + self.location.name + " at " + str(self.timeslot)

    def __eq__(self, other):
        if isinstance(other, Placement):
            return self.teacher == other.teacher and \
                   self.location == other.location and \
                   self.timeslot == other.timeslot

class Teacher:
    def __init__(self, name):
        self.name = name
        self.placements = [None] * 30

    def assign(self, location, timeslot):
        self.placements[timeslot] = location

    def unassign(self, location, timeslot):
        self.placements[timeslot] = None

    def fullyBooked(self):
        return all(x != None for x in self.placements)

    def isAvailableAt(self, timeslot):
        return self.placements[timeslot] == None

    def hasBreak(self):
        breakTimes = ([time for time, location in enumerate(self.placements) if location == Location("Break")])
        if breakTimes:
            breakStart = min(breakTimes)
            if [b - breakStart for b in breakTimes] == list(range(4)):
                return True
        return False
        return list(filter(lambda location: location == Location("Break"), self.placements))

    def getClassroomAt(self, timeslot):
        return self.placements[timeslot]

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, Teacher):
            return self.name == other.name

    def __hash__(self):
        return hash(self.name)
        
class Location:
    def __init__(self, name):
        self.name = name

    def isClassroom(self):
        return False

    def __eq__(self, other):
        if isinstance(other, Location):
            return self.name == other.name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)
    
class Classroom(Location):
    def __init__(self, name):
        super().__init__(name)
        self.placements = [[] for i in range(30)] #7:30am - 3:00pm
        self.squareFootage = None
   
    def staff(self, teacher, timeslot):
        self.placements[timeslot].append(teacher)

    def unstaff(self, teacher, timeslot):
        self.placements[timeslot] = [t for t in self.placements[timeslot] if t != teacher]

    def isFullyStaffed(self):
        return all(len(placement) == 2 for placement in self.placements)

    def isFullyStaffedAt(self, timeslot):
        return len(self.placements[timeslot]) == 2

    def percentageStaffed(self):
        return sum(map(lambda x: len(x), self.placements)) / 60

    def isClassroom(self):
        return True

    def __hash__(self):
        return hash(self.name)

teachers = [Teacher("Alison"), Teacher("Judy"), Teacher("Kristin"), Teacher("Molly"), Teacher("John")]
locations = [Classroom("Pre-K"), Classroom("K")]
school = School(teachers, locations)
