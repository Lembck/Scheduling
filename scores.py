class School:
    def __init__(self, teacher, classroom):
        self.teacher = teacher
        self.classroom = classroom

    def checkRestrictionOne(self):
        if self.classroom.isStaffed:
            return 1
        return 0

    def solveRestrictionOne(self):
        if not self.classroom.isStaffed() and self.teacher.isAvailable():
            self.classroom.staffClassroom()
            self.teacher.assignTeacher()
            return True
        return False

    def solveSchedule(self):
        #check if already solved
        if self.checkRestrictionOne() == 1:
            return True
        else:
            return self.solveRestrictionOne()

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

montessori = School(teacherBob, classroomPreK)

print(montessori.solveSchedule())

class Restrictions:
    AllClassesFullyStaffed = 1
