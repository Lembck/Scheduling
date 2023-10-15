class School:
    def __init__(self, teachers=[], classrooms=[]):
        self.teachers = teachers
        self.classrooms = classrooms

    def hasInvalidSchedule(self):
        always_staffed = all([classroom.is_staffed() for classroom in self.classrooms])
        return not always_staffed

    def teachersHaveNoAvailability(self):
        return not any([teacher.has_availability for teacher in self.teachers])

    def assignTeacherToClassroom(self, teacher, classroom, times):
        for time in times:
            teacher.assign_classroom(classroom.name, time)
            classroom.assign_teacher(teacher.name, time)

    def teachersByAgePreference(self, age):
        return sorted(self.teachers, key=lambda teacher: abs(teacher.age_preference - age))

    def noSolutionPossible(self):
        print("No Solution Possible")
        print(self)

    def complete(self):
        print("Solution Found")
        print(self)

    def __str__(self):
        return "\n".join([teacher.__str__() for teacher in self.teachers]) + "\n" + "-" * 30 + "\n" + "\n".join([classroom.__str__() for classroom in self.classrooms])

class Teacher:
    def __init__(self, name, age_preference):
        self.name = name
        self.availability = [True, True, True, True, True, True, True, True]
        self.placements = [None, None, None, None, None, None, None, None]
        self.age_preference = age_preference

    def has_availability(self):
        return any(self.availability)

    def when_available(self):
        return [i for i in range(len(self.availability)) if self.availability[i]]

    def assign_classroom(self, classroom, time):
        self.availability[time] = False
        self.placements[time] = classroom

    def __str__(self):
        return self.name + "'s schedule: " + ", ".join([str(p) for p in self.placements])

class Classroom:
    def __init__(self, name, age):
        self.name = name
        self.staffed = [False, False, False, False, False, False, False, False]
        self.placements = [None, None, None, None, None, None, None, None]
        self.age = age

    def is_staffed(self):
        return all(self.staffed)

    def when_unstaffed(self):
        return [i for i in range(len(self.staffed)) if not self.staffed[i]]

    def assign_teacher(self, teacher, time):
        self.staffed[time] = True
        self.placements[time] = teacher

    def __str__(self):
        return self.name + "'s schedule: " + ", ".join([str(p) for p in self.placements])


def main():
    teacher_names = ["Abby", "Beatrice", "Charlotte", "Danielle"]
    teacher_age_preferences = [6, 1, 4, 2]
    teachers = [Teacher(name, age) for name, age in zip(teacher_names, teacher_age_preferences)]

    classroom_names = ["Infants", "Toddlers", "Pre-school", "Elementary"]
    classroom_ages = [1, 2, 4, 6]
    classrooms = [Classroom(name, age) for name, age in zip(classroom_names, classroom_ages)]

    torit = School(teachers, classrooms)
    
    while torit.hasInvalidSchedule():
        if torit.teachersHaveNoAvailability():
            torit.noSolutionPossible()
            break
        for classroom in torit.classrooms:
            if classroom.is_staffed():
                continue
            
            times_unstaffed = classroom.when_unstaffed()
            for teacher in torit.teachersByAgePreference(classroom.age):
                if not teacher.has_availability():
                    continue
                
                times_available = teacher.when_available()
                times_aligned = set(times_unstaffed).intersection(set(times_available))
                torit.assignTeacherToClassroom(teacher, classroom, times_aligned)

                if not torit.hasInvalidSchedule():
                    return torit

                if classroom.is_staffed():
                    break
                

torit = main()
torit.complete()
