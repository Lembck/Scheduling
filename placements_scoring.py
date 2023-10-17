class School:
    def __init__(self, teachers, locations):
        self.teachers = teachers
        self.locations = locations
        self.classrooms = [location for location in locations if location.isClassroom()]
        self.placements = []
        self.scores = []
        self.solve()

    def logScores(self):
        self.scores.append(sum(classroom.percentageStaffed() for classroom in self.classrooms))

    def solved(self):
        return all(classroom.isFullyStaffed() for classroom in self.classrooms) and all(teacher.hasBreak() for teacher in self.teachers)

    def solve(self):
        while not self.solved():
            if not all(classroom.isFullyStaffed() for classroom in self.classrooms):
                if all(teacher.fullyBooked() for teacher in self.teachers):
                    print("Not enough people")
                    break
                print("staffing classrooms")
                self.staffClassrooms()
                self.staffClassrooms()
                print(list(zip(self.placements, self.scores)))
            if not all(teacher.hasBreak() for teacher in self.teachers):
                print("breaking teachers")
                self.breakTeachers()

        #print(list(zip(self.placements, self.scores)))

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
            toBeRemoved = Placement(teacher, location, timeslot)
            print("a", len(self.placements))
            self.placements = [p for p in self.placements if p != toBeRemoved]
            print("b", len(self.placements))

        def onBreak(teacher, timeslot):
            self.createPlacement(teacher, Location("Break"), timeslot)
        
        for teacher in self.teachers:
            if teacher.hasBreak():
                continue
            timeslots = []
            teachers = []
            for timeslot in range(30):
                print(timeslot)
                for otherTeacher in self.teachers:
                    #print(otherTeacher)
                    if teacher != otherTeacher and otherTeacher.isAvailableAt(timeslot):
                        timeslots.append(timeslot)
                        teachers.append(otherTeacher)
                        #print(timeslots)
                        #print(teachers)
                        break
                timeslots = []
                if len(timeslots) == 4:
                    for timeslot in timeslots:
                        classroom = teacher.getClassroomAt(timeslot)
                        removePlacement(teacher, classroom, timeslot)
                        onBreak(teacher, timeslot)
                        self.createPlacement(otherTeacher, classroom, timeslot)
                    break
            
                    
    
class Placement:
    def __init__(self, teacher, location, timeslot):
        self.teacher = teacher
        self.location = location
        self.timeslot = timeslot

    def __str__(self):
        return self.teacher.name + " in " + self.location.name + " at " + str(self.timeslot)

    def __repr__(self):
        return self.teacher.name + " in " + self.location.name + " at " + str(self.timeslot)


class Teacher:
    def __init__(self, name):
        self.name = name
        self.placements = [None] * 30

    def assign(self, location, timeslot):
        self.placements[timeslot] = location

    def fullyBooked(self):
        return all(x != None for x in self.placements)

    def isAvailableAt(self, timeslot):
        return self.placements[timeslot] == None

    def hasBreak(self):
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
    
class Classroom(Location):
    def __init__(self, name):
        super().__init__(name)
        self.placements = [[] for i in range(30)] #7:30am - 3:00pm
   
    def staff(self, teacher, timeslot):
        self.placements[timeslot].append(teacher)

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
