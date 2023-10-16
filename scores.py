RestrictionAlreadySolved =  " was already solved"
RestrictionFailed = " Failed: "
RestrictionNowSolved = " is now solved"
RestrictionCannotBeSolved = " cannot be solved in this state"

R1FailureMessage = "The following classrooms were unstaffed: "

class Restrictions:
    AllClassesFullyStaffed = 1

class Log:
    def __init__(self):
        self.log = []
        self.failureDetails = {"R1" : None}
        self.failureMessages = {"R1" : R1FailureMessage}
    def add(self, *msg):
        self.log.extend(msg)
    def print(self):
        print("\n".join(self.log))
    def assigningTeacherToClassroom(self, teacher, classroom):
        self.add("Assigning " + teacher + " to " + classroom)
    def restrictionAlreadySolved(self, restriction):
        self.add(restriction + RestrictionAlreadySolved)
    def restrictionFailed(self, restriction):
        message = self.failureMessages[restriction] + self.failureDetails[restriction]
        self.add(restriction + RestrictionFailed + message)
    def restrictionNowSolved(self, restriction):
        self.add(restriction + RestrictionNowSolved)
    def restrictionCannotBeSolved(self, restriction):
        self.add(restriction + RestrictionCannotBeSolved)
    def updateFailureDetails(self, restriction, details):
        self.failureDetails[restriction] = details
    

class School:
    def __init__(self, teacher, classrooms):
        self.teacher = teacher
        self.classrooms = classrooms
        self.log = Log()

    def restrictionOnePassed(self):
        unstaffedClassrooms = []
        def restrictionOneFailed():
            return len(unstaffedClassrooms) > 0
        
        for classroom in self.classrooms:
            if not classroom.isStaffed():
                unstaffedClassrooms.append(classroom.name)
        if restrictionOneFailed():
            self.log.updateFailureDetails("R1", ", ".join(unstaffedClassrooms))
            return False

    def solveRestrictionOne(self):
        for classroom in self.classrooms:
            if classroom.isStaffed():
                continue
            if self.teacher.isAvailable():
                self.log.assigningTeacherToClassroom(self.teacher.name, classroom.name)
                classroom.staffClassroom()
                self.teacher.assignTeacher()
            else:
                return False
        return True

    def solveSchedule(self):
        if self.restrictionOnePassed():
            self.log.restrictionAlreadySolved("R1")
            return True
        self.log.restrictionFailed("R1")
        if self.solveRestrictionOne():
            self.log.restrictionNowSolved("R1")
            return True
        else:
            self.log.restrictionCannotBeSolved("R1")

    def printLog(self):
        self.log.print()
            

class Teacher:
    def __init__(self, name):
        self.name = name
        self.available = True

    def assignTeacher(self):
        self.available = False

    def isAvailable(self):
        return self.available

class Classroom:
    def __init__(self, name):
        self.name = name
        self.staffed = False
        
    def staffClassroom(self):
        self.staffed = True

    def isStaffed(self):
        return self.staffed

teacherBob = Teacher("Bob")
classroomPreK = Classroom("PreK")
classroomK = Classroom("K")
classrooms = [classroomPreK]

montessori = School(teacherBob, classrooms)

montessori.solveSchedule()
montessori.printLog()
