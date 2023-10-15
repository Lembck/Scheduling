AbbyHourlyAvailability = [True, True, True, True, True, True, True, True, True] # 7-3pm
InfantRoomStaffed = [False, False, False, False, False, False, False, False]

class Teacher:
    def __init__(self, name):
        self.name = name
        self.availability = [True, True, True, True, True, True, True, True]


class Classroom:
    def __init__(self, name):
        self.name = name
        self.staffed = [False, False, False, False, False, False, False, False]

def checkValidity(teachers, classrooms):
    always_staffed = all([all(classroom.staffed) for classroom in classrooms])
    #one_place_at_once = 
    return always_staffed

def anyAvailability(teachers):
    return any([any(teacher.staffed) for teacher in teachers])

teachers = [Teacher("Abby")]
classrooms = []#[Classroom("Infants")]

while not checkValidity(teachers, classrooms):
    if not anyAvailability(teachers):
        print("No solution possible")
        break
    
print("Solution found")
