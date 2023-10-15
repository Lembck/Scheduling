class Teacher:
    def __init__(self, name):
        self.name = name
        self.availability = [True, True, True, True, True, True, True, True]
        self.placements = [None, None, None, None, None, None, None, None]

    def has_availability(self):
        return any(self.availability)

    def when_available(self):
        return [i for i in range(len(self.availability)) if self.availability[i]]

class Classroom:
    def __init__(self, name):
        self.name = name
        self.staffed = [False, False, False, False, False, False, False, False]
        self.placements = [None, None, None, None, None, None, None, None]

    def is_staffed(self):
        return all(self.staffed)

    def when_unstaffed(self):
        return [i for i in range(len(self.staffed)) if not self.staffed[i]]

def checkValidity(teachers, classrooms):
    always_staffed = all([classroom.is_staffed() for classroom in classrooms])
    #one_place_at_once = 
    return always_staffed

def anyAvailability(teachers):
    return any([teacher.has_availability for teacher in teachers])

def assignTeacherToClassroom(teacher, classroom, times):
    for time in times:
        teacher.availability[time] = False
        teacher.placements[time] = classroom.name
        classroom.staffed[time] = True
        classroom.placements[time] = teacher.name

def main():
    teachers = [Teacher("Abby")]
    classrooms = [Classroom("Infants")]

    while not checkValidity(teachers, classrooms):
        if not anyAvailability(teachers):
            print("No solution possible")
            break
        for classroom in classrooms:
            if classroom.is_staffed():
                continue
            times_unstaffed = classroom.when_unstaffed()
            for teacher in teachers:
                if not teacher.has_availability():
                    continue
                times_available = teacher.when_available()
                times_aligned = set(times_unstaffed).intersection(set(times_available))
                assignTeacherToClassroom(teacher, classroom, times_aligned)
                if checkValidity(teachers, classrooms):
                    print("Solution found")
                    print(teacher.placements)
                    print(classroom.placements)
                    return

main()
