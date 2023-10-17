class School:
    def __init__(self, teacher, classrooms):
        self.teacher = teacher
        self.classrooms = classrooms
        self.log = Log()
        self.notSolvedYet = True

    def solveSchedule():
        while self.notSolvedYet:
            #classrooms need to be staffed
            if not all(classroom.isStaffed for classroom in classrooms):
                self.staffClassrooms()
                    
            #teachers need to have a break

    def staffClassrooms():
        def assignTeacherToClassroom(teacher, classroom, times):
            teacher.assignTeacher(classroom, times)
            classroom.staffClassroom(teacher, times)

        for classroom in classrooms:
            if classroom.isStaffed:
                continue
            
            timesAvailable = set(teacher.whenAvailable())
            timesUnstaffed = set(classroom.whenUnstaffed())
            timesAligned = timesUnstaffed.intersection(timesAvailable)
            assignTeacherToClassroom(teacher, classroom, timesAligned)

    def printLog(self):
        self.log.print()
        

class Teacher:
    def __init__(self, name):
        self.name = name
        self.available = True
        self.availability = [None] * 30

    def assignTeacher(self, classroom, times):
        for time in times:
            self.availability[time] = classroom
        self.setAvailable()

    def setAvailable(self):
        self.available = not [slot for slot in self.availability if slot is not None]

    def isAvailable(self):
        return self.available

    def whenAvailable(self):
        return [i for i in range(30) if self.availability[i]]

class Classroom:
    def __init__(self, name):
        self.name = name
        self.staffed = False
        self.placements = [None] * 30 #7:30am - 3:00pm

    def percentageStaffed(self):
        def calculatePercentage():
            return len(filter(lambda x: x != None , self.placements)) / len(self.placements)
        return self.staffed or calculatePercentage()
        
    def staffClassroom(self):
        self.staffed = True

    def isStaffed(self):
        return self.staffed

    def whenUnstaffed(self):
        return [i for i in range(30) if self.placements[i] == None]

teacherBob = Teacher("Bob")
classroomPreK = Classroom("PreK")
classroomK = Classroom("K")
classrooms = [classroomPreK]

montessori = School(teacherBob, classrooms)

montessori.solveSchedule()
montessori.printLog()
