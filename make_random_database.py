# |---------------------------------------------------------------| #
# | The only use for this file is to set up a random database.    | #
# | The execution of this program will stop when the first        | #
# | student becomes of type "Formando".                           | #
# | This way the database will have:                              | #
# |     last indexes: students of type "Calouro"                  | #
# |     first indexes: students of type "Formando"                | #
# |     in the middle: students of type "Continuo or "Individual" | #
# | At every iteration the students will get random grades for    | #
# | the subjects that they are attending and new students         | #
# | (calouros) will enter the database. Based on that they the    | #
# | program automaticlly enrolls them in the new semester.        | #
# |                                                               | #
# | USAGE:                                                        | #
# |     To test this program create an empty file named           | #
# |     "students0.1.txt                                          | #
# |---------------------------------------------------------------| #
from Student import *


def give_random_grades(student):
    # Random grades: if subject is from a semester before the grade is 
    # always above 7 for semplicity reasons
    # The flag sets if a student of type "Calouro" or "Continuo" becames "Individual" 
    flag = 0
    for sub in student.enrolled_classes:
        if type(sub.semester) == str:
            grade = randint(67, 100) / 10
        elif sub.semester < student.semester:
            grade = randint(7, 10)
        else:
            grade = randint(67, 100) / 10
        
        if grade < 7:
            student.type = 'Individual'
        else:
            student.approved_classes.append((sub.code, grade))
    
    student.semester += 1
    student.enrolled_classes = []
    if student.type == 'Calouro':
        student.type = 'Continuo'
    elif len(student.approved_classes) >= 32:
        student.type = 'Formando'






# Enroll a student based on type in a simplistic way
def enroll(student):
    hours = 0
    history = [i[0] for i in student.approved_classes]
    if student.type == 'Calouro':
        student.enrolled_classes = subjects[:5]
        return

    elif student.type == 'Continuo':
        student.enrolled_classes = get_subjects_from_semester(student.semester)
        hours = sum([i.hours for i in student.enrolled_classes])
        

    elif student.type == 'Individual':
        prev_semester = get_subjects_from_semester(student.semester-1) 
        student.enrolled_classes = [i for i in prev_semester if not i.code in history]
     
        this_semester = get_subjects_from_semester(student.semester) 
        student.enrolled_classes = [i for i in this_semester if student.canTakeTheSubject(i)]
        
        hours = sum([i.hours for i in student.enrolled_classes])
    
    counter = 0
    eletivas = [i for i in get_subjects_from_semester('Eletiva') if not i.code in history]
    if len(eletivas):
        while hours < 360 and counter < len(eletivas):
            new_sub = eletivas[counter]
            if student.canTakeTheSubject(new_sub) and not check_conficts(student.enrolled_classes + [new_sub]):
                hours += 72
                student.enrolled_classes.append(new_sub)
            
            counter += 1




if __name__ == '__main__':
    for i in range(8):
        students = read_students()
        new = make_new_students()

        students += new

        for stud in students:
            enroll(stud)
            give_random_grades(stud)

        write_students_to_database(students)

