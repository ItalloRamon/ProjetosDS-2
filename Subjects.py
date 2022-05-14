DAYS = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex']
HOURS = ['7:30', '8:20', '9:20', '10:10', '11:10', '12:00', '13:30', '14:20', '15:20', '16:10', '17:00']
MAX_CAPACITY = 40

class Subject:
    def __init__(self, name, semester, code, hours, schedule, pre_requisite=None):
        self.name = name
        self.semester = semester
        self.code = code
        self.hours = hours
        self.pre_requisite = pre_requisite
        self.class_capacity = MAX_CAPACITY
        self.enrolled_students = 0 # Could be a list of Student
        self.schedule = schedule


    def __str__(self):
        return self.code + '\t\t' + self.name# + '\t\t' + str(self.pre_requisite)

    def getClassesSchedule(self):
        return '\n'.join(DAYS[int(i[0])] + ' ' + HOURS[int(i[1:])] for i in self.schedule)

    def addStudent(self):
        self.enrolled_students+=1
    
    # Checks conflicts in the schedule of this Subject with another Subject object
    # outputs:  1 -> there is conflict in the schedule of the two subjects (overlapping)
    #           0 -> there is no conflict in the schedule
    def scheduleConflict(self, other):
        for t in self.schedule:
            if t in other.schedule:
                return 1
        return 0



# |-------------------------------| #
# |         More Functions        | #
# |-------------------------------| #
# Read subjects from file
def read_subjects():
    with open('subjects.txt', 'r') as f:
        raw_data = [i.split('\n') for i in f.read().split('\n\n')]
    
    if raw_data[-1][-1] == '':
        raw_data[-1] = raw_data[-1][:-1]
    
    subjects = []
    for i, s in enumerate(raw_data):
        if i == len(raw_data) - 1:
            p = 'Eletiva'
        else:
            p = i+1
        for j in s:
            try:
                name, hours, code, schedule, pre_req = j.split('; ')
                pre_req = pre_req.split('&')
            except ValueError: 
                name, hours, code, schedule = j.split('; ')
                pre_req = None

            schedule = schedule.split('&')
            subjects.append(Subject(name, p, code, int(hours), schedule, pre_requisite=pre_req))

    return subjects



# Return Subject object from code
# Code should be "CC1901" for single subject 
def subject_from_code(code):
    global subjects
    first = 1901
    last = 1940
    if len(code) == 6:
        try:
            c = int(code[2:])
            # Avoid index error
            if c >= first and c <= last:
                return subjects[c - first]
        except ValueError:
            # Return the code if the user messes up
            return code
    return code

# This part of the function is not being used  i'll keep it there eventually i'll delete it
#    elif len(code) > 6:
#        c = [int(i) for i in code[2:].split('-')]
#        start = c[0] - first
#        stop = c[1] - first + 1
#        return subjects[start: stop] 


def code_from_subject(name):
    global subjects
    for sub in subjects:
        if sub.name.lower() == name.lower():
            return sub.code


# Returns all subjects for a given semester
def get_subjects_from_semester(semester):
    global subjects
    return [i for i in subjects if i.semester == semester]


# Check if there are conflicts in a list of Subject objects
# output:   1 -> there is conflict on the schedule (overlapping)
#           0 -> no conflict
def check_conficts(subjects):
    for i in range(len(subjects)-1):
        for j in range(i+1, len(subjects)):
            if subjects[i].scheduleConflict(subjects[j]):
                return 1
    # No conflicts found in schedule
    return 0



# Makes a formatted calendar from a list of subjects
def calendar(subjects):
    if len(subjects) == 16:
        # Calendar for "Eletivas" is two calendars
        return calendar(subjects[:8]) + '\n' + '_'*88+'\n' + calendar(subjects[8:])

    calendar_arr = [['-', '-', '-', '-', '-'] for i in range(len(HOURS))] 
    subjects_str = '\n'
    for s in subjects:
        subjects_str += '\n' + str(s)
        for t in s.schedule:
            calendar_arr[int(t[1:])][int(t[0])] = s.code

    header = '\t|\t' + '\t|\t'.join(i for i in DAYS) + '\t|'
    calendar_s = '\n' + '-' * 8 + '|' + '---------------|'*5
    for i in range(len(calendar_arr)):
        calendar_s += '\n' + HOURS[i] + '\t|\t'
        calendar_s += '\t|\t'.join(c for c in calendar_arr[i]) + '\t|'
        calendar_s += '\n' + '-' * 8 + '|' + '---------------|'*5
          

    return header + calendar_s + subjects_str


# Print formatted calendar for all semesters
def full_calendar():
    print(('\n'+'_'*88 + '\n').join(calendar(get_subjects_from_semester(i)) for i in range(1, 8)))
    print('\n'+'_'*88 + '\n' + calendar(get_subjects_from_semester('Eletiva')))



subjects = read_subjects()
