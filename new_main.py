from Student import *
import sys
from os import system
from time import sleep


INTERVAL = 2 # second to sleep

MAX_FORMANDOS = 1
MAX_CONTINUOS = 1
MAX_INDIVIDUAL = 1

COUNT_FORMANDOS = 0
COUNT_CONTINUOS = 0
COUNT_INDIVIDUAL = 0

MATRICULA_IS_FINISHED = False
AJUSTE_IS_FINISHED = False
REAJUSTE_IS_FINISHED = False

LIST_REMOVES = []
LIST_INSERTS = []
LIST_CHANGES = []


def clear():
    if sys.platform == 'linux' or sys.platform == 'darwin':
        system('clear')
    else:
        system('cls')


def main_menu():    
    clear()
    print('''
    ------MATRICULA------

    [1] - Matrícula
    [2] - Ajuste
    [3] - Reajuste
    [0] - Encerrar o programa 
    
    ''')


def menu_ajuste():
    print('''

    ------SELECIONE UMA OPCAO:-----

    [1] - Inserir uma disciplia
    [2] - Remover uma disciplina
    [3] - Trocar uma disciplina

    ''')


# Check if there are new students (type Calouro) in a list of students
def new_students_check(students):
    for stud in students:
        if stud.type == 'Calouro':
            return 1
    return 0


# Create some new Calouros and enrolls them in the first semester subjects
def enroll_new_students():
    students = make_new_students()

    for stud in students:
        stud.enrolled_classes = subjects[:5]
    
    return students


# Ask for user registration, return student if student is found
def ask_registration(students):
    matricula = input("Digite o número da sua matrícula: ")
    # Prevent ValueError converting str to int
    if matricula.isdigit():
        student = student_from_registration(int(matricula), students) 
    else:
        student = 0
        print("Esse número de matrícula não está cadastrado!")
        sleep(2)

    return student


# |------------------------------------| #
# |     Phase 1 simple enrollment      | #
# |------------------------------------| #
def choose_subjects(student):   
    while len(student.enrolled_classes) < 8:
        full_calendar()
        print("\nEscolha no mínimo 4 disciplinas, e no máximo 8:")
        print("Para encerrar sua matrícula digite [Q]")
        
        code_subj = input("Digite o código da disciplina desejada: ").upper()

        if code_subj == 'Q' and len(student.enrolled_classes) >= 4:
            return
            
        elif code_subj != 'Q':
            subj = subject_from_code(code_subj)
            
            # Resolve bad input
            if isinstance(subj, str):
                print(f'Não tem disciplina com codigo {subj}.')
            else:
                sucess = student.enroll(subj)
                history = [i[0] for i in student.approved_classes]
                if sucess == 0:
                    print("Você já pagou essa disciplina :(")
                elif sucess == -1:
                    print("Você não tem os pré-requisitos para pagar essa disciplina.")
                elif sucess == 1:
                    print("Esta disciplina está dando choque de horário com alguma outra.")
                elif sucess == 2:
                    print("Esta disciplina não tem mais vagas!")
                else:
                    print(f"Matrícula realizada com sucesso na disciplina {subj}.")
            
            
        sleep(2)
        clear()
    print("Você està matriculado em 8 materias")


# Matricula Normal
def matriculation(student):
    global COUNT_FORMANDOS
    global COUNT_CONTINUOS
    global COUNT_INDIVIDUAL
    global MAX_FORMANDOS
    global MAX_CONTINUOS
    global MAX_INDIVIDUAL
    global MATRICULA_IS_FINISHED

    if len(student.enrolled_classes):
        print("Sua matrícula jà foi realizada")
        return 0

    elif student.type == 'Formando' and COUNT_FORMANDOS < MAX_FORMANDOS:
        choose_subjects(student)
        COUNT_FORMANDOS += 1

    elif student.type == 'Continuo' and COUNT_FORMANDOS == MAX_FORMANDOS and COUNT_CONTINUOS < MAX_CONTINUOS:
        choose_subjects(student) 
        COUNT_CONTINUOS += 1

    elif student.type == 'Individual' and COUNT_FORMANDOS == MAX_FORMANDOS and COUNT_CONTINUOS == MAX_CONTINUOS:
        choose_subjects(student)
        COUNT_INDIVIDUAL += 1

    # Close Marticula period
    elif COUNT_FORMANDOS == MAX_FORMANDOS and COUNT_CONTINUOS == MAX_CONTINUOS and COUNT_INDIVIDUAL == MAX_INDIVIDUAL:
        MATRICULA_IS_FINISHED = True

    else:
        print("Ainda não está na sua hora.")
        sleep(3)



# |-------------------------------------------------------| #
# |     Phase 2 Adjustments (insert, remove, change)      | #
# |-------------------------------------------------------| #
# Used for requesting to insert or remove a subject (Ajuste, reajuste)
def adjustments(student, remove=False):
    global LIST_REMOVES
    global LIST_INSERTS
    global AJUSTE_IS_FINISHED
    
    # Print calendario normal
    if not AJUSTE_IS_FINISHED:
        full_calendar()
    else:
        # Print calendario das materias a mais
        pass

    if remove:
        code_subj = input("Digite o código da disciplina que você quer remove: ")
    
    else:
        code_subj = input("Digite o código da disciplina que você quer inserir: ")

    subj = subject_from_code(code_subj)
    # Resolve bad input
    if isinstance(subj, str):
        print(f'Não tem disciplina com codigo {subj}.')
        return

    if remove:
        sucess = student.check_UNenroll(subj)
    else:
        sucess = student.canTakeTheSubject(subj)

    if sucess == 200:

        print("Seu pedido foi registrado!")
        sleep(3)


        if remove:
            LIST_REMOVES.append((student, subj))
        else:
            LIST_INSERTS.append((student, subj))

    else:
        print("Não pode inserir esta disciplina!")
        sleep(2)


# Used to request a subject replacement
def adjustments_replace(student):
    global LIST_CHANGES
    full_calendar()
    code_subj_insert = input("Digite o código da disciplina que você quer inserir: ")
    code_subj_remove = input("Digite o código da disciplina que você quer remover: ")

    subj_remove = subject_from_code(code_subj_remove)
    subj_insert = subject_from_code(code_subj_insert)
    # Return if bad input
    if isinstance(subj_remove, str) or isinstance(subj_insert, str):
        print('O codigo de uma das disciplinas està errado!')
        return

    # Subjects -> All right!
    # Checks enroll and UNenroll
    success = student.checkChange(subj_insert, subj_remove)
    # Bad input
    if sucess != 200:
        print("Você não pode realizar essa troca!")
        return

    # Priority check
    priority = check_priority(student, subj_insert, subj_remove)
    if priority:
        print('Seu pedido foi realizado com sucesso!')
    # - Low priority
    else:
        LIST_CHANGES.append((student, subj_insert, subj_remove))
        print("Seu pedido foi registrado!")

    sleep(2)


# First step of adjustment
def matriculation_adjust(student):
    menu_ajuste()
    choice = input("Digite e opção desejada: ")
    # | Insert and removes are low priority while replacement check for a possible high | #
    # | prority situation, if none is found it goes to low priority and is then checked | #
    # | when adjustment period is closed                                                | #
    if choice == '1':
        adjustments(student, remove=False)
    # Remove 
    elif choice == '2':
        adjustments(student, remove=True)
    # Change
    elif choice == '3':
       adjustments_replace(student) 
    

# Last step of adjustemnts
def resolve_adjustments():
    global LIST_CHANGES
    global LIST_REMOVES
    global LIST_INSERTS
    global AJUSTE_IS_FINISHED

    close_adjustment = input("Você desejar encerrar o período de ajuste? [S/N] ").upper()
    if close_adjustment == 'S':
        # Priority
        for stud_change in LIST_CHANGES:
            priority = check_priority(stud_change[0], stud_change[1], stud_change[2])
            if priority:
                LIST_CHANGES.remove(stud_change)

        # Normal
        for s in LIST_REMOVES:
            s[0].UNenroll(s[1])

        for s in LIST_INSERTS:
            s[0].enroll(s[1])

        for s in LIST_CHANGES:
            s[0].UNenroll(s[2])
            s[0].enroll(s[1])
        AJUSTE_IS_FINISHED = True




# |----------------------------------------------------------------------------| #
# |     Check priority for subject changes, insertion end remove (AJUSTE)      | #
# |----------------------------------------------------------------------------| #
def check_priority(student, subj_insert, subj_remove):
    global LIST_INSERTS
    global LIST_REMOVES
    global LIST_CHANGES

    for stud_insert in LIST_INSERTS:
        if stud_insert[1] == subj_remove:
            stud_insert[0].enroll(subj_remove)
            student.UNenroll(subj_remove)
            students.enroll(subj_insert)
            LIST_INSERTS.remove(subj_insert)
            # Priority satisfied
            return 1

    for stud_remove in LIST_REMOVES:
        if stud_remove[1] == subj_insert:
            stud_remove[0].UNenroll(subj_insert)
            student.UNenroll(subj_remove)
            students.enroll(subj_insert)
            LIST_REMOVES.remove(subj_remove)
            # Priority satisfied
            return 1
    # No priority
    return 0



# |-------------------------------| #
# |     Resolve for REAJUSTE      | #
# |-------------------------------| #
# Last step of REAJUSTE
def resolve_readjustments():
    global LIST_INSERTS
    global REAJUSTE_IS_FINISHED
    close_re_adjustment = input("Você desejar encerrar o período de reajuste? [S/N] ").upper()
    if want_finish_readjustment == 'S':
        LIST_INSERTS = sorted(LIST_INSERTS, key=lambda x:x[0].cofficent, reverse=True)
        for insert in LIST_INSERTS:
            insert[0].enroll(insert[1])
        
        REAJUSTE_IS_FINISHED = True




# |------------------------| #
# |     GOD HAVE MERCY     | #
# |------------------------| #
def main():
    global MATRICULA_IS_FINISHED
    global AJUSTE_IS_FINISHED
    global REAJUSTE_IS_FINISHED

    # Read database
    students = read_students()

    main_menu()
    choice = input("Digite a opção escolhida: ")
    # ! Exit (might resolve to saving data and then exit)
    if choice == '0':
        clear()
        print("Exiting Program")
        sys.exit()
    
    if choice == '1':
        # |------------------|
        # |     MATRICULA    |
        # |------------------|
        # Step 1: check that there aren't Students of type calouro and enroll new students
        #         and saves them to database
        if not new_students_check(students):
            new_students = enroll_new_students()
            students += new_students
            #write_students_to_database(students)
            

        while not MATRICULA_IS_FINISHED:
            # Step 2: ask for a registration number to get and start with the process
            student = ask_registration(students)
            print("Periodo de Matricula em andamento\n\n\n")
            if student:
                # Continue and save once student has finished
                matriculation(student)
                #write_students_to_database(students)
        
        if MATRICULA_IS_FINISHED:
            print("Periodo de Matricula encerrado\n\n\n")
            

    elif choice == '2' and MATRICULA_IS_FINISHED:
        # |------------------|
        # |     AJUSTE       |
        # |------------------|
        while not AJUSTE_IS_FINISHED:
            # Step 1: ask for registration number to start
            student = ask_registration(students)
            print("Período de ajuste em andamento...\n\n\n")
            if student:
                matriculation_adjust(student) # Step 2: Start reajuste
                resolve_adjustments() # Step 3: Ask to close AJUSTE
                # Save data once the AJUSTE is closed
                if AJUSTE_IS_FINISHED:
                    pass
                    #write_students_to_database(students)
        
        if AJUSTE_IS_FINISHED:
            print("Período de ajuste em encerrado...\n\n\n")
            
    

    elif choice == '3' and MATRICULA_IS_FINISHED and AJUSTE_IS_FINISHED:
        # |------------------|
        # |     REAJUSTE     |
        # |------------------|
        while not REAJUSTE_IS_FINISHED:
            # Step 1: ask for registration number to start
            student = ask_registration(students)
            print("Período de ajuste em andamento...\n\n\n")
            if student:
                adjustments(student)  # Step 2: ask for subject to make the new insertion
                resolve_adjustments() # Step 3: ask to close REAJUSTE than save
                if AJUSTE_IS_FINISHED:
                    pass
                    #write_students_to_database(students)
        
        if REAJUSTE_IS_FINISHED:
            print("Período de reajuste em encerrado...\n\n\n")


    # ! Invalid option
    else:
        clear()
        print("Input invalido!")
        sleep(2)
        return main()

    clear()



main()
