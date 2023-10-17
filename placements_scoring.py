class School:
    def __init__(self, teachers, locations):
        self.teachers = teachers
        self.locations = locations
        self.classrooms = [location for location in locations if location.isClassroom()]
        self.placements = []
        self.scores = []
        self.solve()

    def logScores(self):
        self.scores.append(sum(classroom.percentageStaffed() for classroom in self.classrooms) + \
                           sum(teacher.hasBreak() for teacher in self.teachers))

    def solved(self):
        return all(classroom.isFullyStaffed() for classroom in self.classrooms) and all(teacher.hasBreak() for teacher in self.teachers)

    def solve(self):
        while not self.solved():
            if not all(classroom.isFullyStaffed() for classroom in self.classrooms):
                print("Staffing Classrooms")
                if all(teacher.fullyBooked() for teacher in self.teachers):
                    print("Not enough people")
                    break
                
                for c in self.classrooms:
                    if not c.isFullyStaffed():
                        print(c, "is not fully staffed:", c.percentageStaffed()*100, "%")
                        
                self.staffClassrooms()
                self.staffClassrooms()
                
            if not all(teacher.hasBreak() for teacher in self.teachers):
                print("breaking teachers")
                print(", ".join(str(t) for t in self.teachers if not t.hasBreak()), "don't have breaks")
                self.breakTeachers()
            else:
                print("All teachers have breaks")

        print("Solved")
        print(self.placements)
        print(max(self.scores))

    def createPlacement(self, teacher, location, timeslot):
        self.placements.append(Placement(teacher, location, timeslot))
        teacher.assign(location, timeslot)
        if location.isClassroom():
            location.staff(teacher, timeslot)
        self.logScores()

    def staffClassrooms(self):
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

    def breakTeachers(self):
        print("Breaking teachers")
        def removePlacement(teacher, location, timeslot):
            #print("removing", teacher, "from", location, "at", timeslot)
            toBeRemoved = Placement(teacher, location, timeslot)
            if toBeRemoved in self.placements:
                self.placements = [p for p in self.placements if p != toBeRemoved]
                teacher.unassign(location, timeslot)
                if location.isClassroom():
                    location.unstaff(teacher, timeslot)
                #print("removed", teacher, "from", location, "at", timeslot)

        def onBreak(teacher, timeslot):
            self.createPlacement(teacher, Location("Break"), timeslot)

        def findBreakTimeslots(timeslots, teachers, timeslot, teacher):
            for otherTeacher in self.teachers:
                if otherTeacher.isAvailableAt(timeslot):
                    #print(otherTeacher, "can cover at", timeslot)
                    timeslots.append(timeslot)
                    teachers.append(otherTeacher)
                    return timeslots
            return []
        
        for teacher in self.teachers:
            #print("Trying to find a break for", teacher)
            if teacher.hasBreak():
                #print(teacher, "already had a break")
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

teachers = [Teacher("Alison"), Teacher("Judy"), Teacher("Kristin"), Teacher("Molly"), Teacher("John")]
locations = [Classroom("Pre-K"), Classroom("K")]
school = School(teachers, locations)
