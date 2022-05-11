from Student import *


# Load students data
students = read_students();
# Search for a student
s = student_from_registration(1128, students)
# Displays all student infos
s.studentOverview()
print('_'*88)
print('_'*88)

# Select a subject
sub = subject_from_code('CC1923')

s.enroll(sub)

# Display Matricula
print(s.getComprovant())
print('_'*88)
print('_'*88)
# Unenroll
s.UNenroll(sub)

print(s.getComprovant())
# Display Historico
print(s.getGrades())


new_students = make_new_students()

for stud in new_students:
    new_students.enrolled_classes = subject[:5]
