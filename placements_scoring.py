class School:
    def __init__(self, teachers, classrooms):
        self.teachers = teachers
        self.classrooms = classrooms
        self.placements = []
        self.scores = []
        self.unsolvable = False
        self.solve()

    def logScores(self):
        self.scores.append(sum(classroom.percentageStaffed() for classroom in classrooms))

    def unsolved(self):
        return not all(classroom.isFullyStaffed() for classroom in self.classrooms)

    def solve(self):
        while self.unsolved() and not self.unsolvable:
            if not all(classroom.isFullyStaffed() for classroom in self.classrooms):
                if all(teacher.fullyBooked() for teacher in self.teachers):
                    print("here")
                    break
                #else:
                    #print(teachers[0].placements)
                self.staffClassrooms()
            #if not all(teacher.hasBreak() for teacher in self.teachers):
            #    self.breakTeachers()

        print(list(zip(self.placements, self.scores)))

    def staffClassrooms(self):
        #print("staffing")
        def createPlacement(teacher, classroom, timeslot):
            #print("creating placement")
            self.placements.append(Placement(teacher, classroom, timeslot))
            teacher.assign(classroom, timeslot)
            classroom.staff(teacher, timeslot)
            self.logScores()

        for classroom in self.classrooms:
            if classroom.isFullyStaffed():
                print("class is fully staffed")
                continue
            for timeslot, t in enumerate(classroom.placements):
                if classroom.isFullyStaffedAt(timeslot):
                    print("timeslot full " + str(timeslot))
                    continue
                #print(self.teachers)
                for teacher in self.teachers:
                    #print(teacher)
                    if teacher.isAvailableAt(timeslot):
                        createPlacement(teacher, classroom, timeslot)
                        break

    #def breakTeachers(self):
    #    for teacher in self.teachers:
     #       if teacher.hasBreak():
     #           continue
     #       #find four placements in a row when someone is available, all in the same classroom
     #       for timeslot in range(30):
                

class Placement:
    def __init__(self, teacher, classroom, timeslot):
        self.teacher = teacher
        self.classroom = classroom
        self.timeslot = timeslot

    def __str__(self):
        return self.teacher.name + " in " + self.classroom.name + " at " + str(self.timeslot)

    def __repr__(self):
        return self.teacher.name + " in " + self.classroom.name + " at " + str(self.timeslot)


class Teacher:
    def __init__(self, name):
        self.name = name
        self.placements = [None] * 30

    def assign(self, classroom, timeslot):
        self.placements[timeslot] = classroom

    def fullyBooked(self):
        return all(x != None for x in self.placements)

    def isAvailableAt(self, timeslot):
        return self.placements[timeslot] == None

    def hasBreak(self):
        return list(filter(lambda slot: slot == "Break", self.placements))

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

class Classroom:
    def __init__(self, name):
        self.name = name
        self.placements = [[] for i in range(30)] #7:30am - 3:00pm
   
    def staff(self, teacher, timeslot):
        self.placements[timeslot].append(teacher)

    def isFullyStaffed(self):
        return all(len(placement) == 2 for placement in self.placements)

    def isFullyStaffedAt(self, timeslot):
        return len(self.placements[timeslot]) == 2

    def percentageStaffed(self):
        return sum(map(lambda x: len(x), self.placements)) / 60

teachers = [Teacher("Alison"), Teacher("Judy"), Teacher("Kristin"), Teacher("Molly"), Teacher("John")]
classrooms = [Classroom("Pre-K"), Classroom("K")]
school = School(teachers, classrooms)
