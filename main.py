from Student import *
from sys import platform
from os import system
from time import sleep

MAX_FORMANDOS = 1
MAX_CONTINUOS = 1
MAX_INDIVIDUAL = 1

def clear():
    if platform == 'linux' or platform == 'darwin':
        system('clear')        
    elif platform == 'win32':
        system('cls')

def menu():
    clear()
    print("#-#-#-#- MENU -#-#-#-#")
    print('''
    (1) - Matrícula
    (2) - Ajuste
    (3) - Reajuste
    (99) - Encerrar o programa''')

def choice_subject(student):
    full_calendar()
    print("\nEscolha no mínimo 4 disciplinas, e no máximo 8:")
    print("Para encerrar sua matrícula digite [Q]")
    code_subj = input("Digite o código da disciplina desejada: ").upper()                 
    if code_subj == 'Q' and len(student.enrolled_classes) >= 4:
        return -1
    elif code_subj != 'Q':
        subj = subject_from_code(code_subj)
        sucess = student.enroll(subj)
        if sucess == 0:
            print("Você já pagou essa disciplina :(")
        elif sucess == -1:
            print("Você não tem os pré-requisitos para pagar essa disciplina.")
        elif sucess == 1:
            print("Esta disciplina está dando choque de horário com alguma outra.")
        else:
            print(f"Matrícula realizada com sucesso na disciplina {subj}.")

should_continue = True
matricula_is_finished = False
ajuste_is_finished = False
count_formandos = 0
count_continuos = 0
count_individual = 0

while should_continue:
    menu()
    choice = input("Digite a opção escolhida: ")
    clear()

    #Matrícula
    #TODO SALVAR NA BASE DE DADOS
    #TODO VERIFICAR TODAS AS ENTRADAS
    if choice == '1':
        while not matricula_is_finished:
            print("Perído da matrícula em andamento...\n\n\n")
            
            students = read_students()

            #Calouros
            new_students = make_new_students()
            for stud in new_students:
                stud.enrolled_classes = subjects[:5]
            students.extend(new_students)

            matricula = input("Digite o número da sua matrícula: ")
            student = student_from_registration(int(matricula), students) 
            
            if student:
                #Formandos
                if student.type == 'Formando':
                    while len(student.enrolled_classes) < 8:
                        subject_chosen = choice_subject(student)
                        if subject_chosen == -1:
                            break
                        sleep(3)
                        clear()
                    count_formandos += 1           
                #Padrão
                elif student.type == 'Continuo':
                    if count_formandos == MAX_FORMANDOS:
                        student.enrolled_classes = get_subjects_from_semester(student.semester)
                        while len(student.enrolled_classes) < 8:
                            subject_chosen = choice_subject(student)
                            if subject_chosen == -1:
                                break
                            elif subject_chosen == 0:
                                pass
                            sleep(3)
                            clear()
                        count_continuos += 1 
                    else:
                        print("Ainda não está na sua hora.")
                        sleep(3)
                #Individual
                elif student.type == 'Individual':
                    if count_formandos == MAX_FORMANDOS and count_continuos == MAX_CONTINUOS:   
                        while len(student.enrolled_classes) < 8:
                            subject_chosen = choice_subject(student)
                            if subject_chosen == -1:
                                break
                            sleep(3)
                            clear()
                        count_individual += 1 
                    else:
                        print("Ainda não está na sua hora.")
                        sleep(3)

                #Matricula is finished
                if count_formandos == MAX_FORMANDOS and count_individual == MAX_INDIVIDUAL and count_continuos == MAX_CONTINUOS:
                    want_stop_matricula = input("Deseja encerrar o período da matrícula? [S/N] ").upper()
                    if want_stop_matricula == 'S':
                        matricula_is_finished = True
                        print("Período de matrícula encerrado!")
                        sleep(3) 
            else:
                print("Esse número de matrícula não está cadastrado!")

    #TODO AJUSTE
    elif choice == '2':
        if matricula_is_finished:
            print("Período de ajuste iniciado!")
        else:
            print("Ainda não começou o período de ajuste.")
            sleep(3)

    #TODO REAJUSTE
    elif choice == '3':
        if matricula_is_finished and ajuste_is_finished:
            print("Período de reajuste iniciado!")
        else:
            print("Período de reajuste ainda não começou.")
            sleep(3)

    elif choice == '99':
        should_continue = False
