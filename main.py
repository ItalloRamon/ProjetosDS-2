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


def menu_ajuste():
    print('''Seleciona a opção que você deseja:
        (1) - Inserir uma disciplia.
        (2) - Remover uma disciplina.
        (3) - Trocar uma disciplina.''')


def choice_subject(student):
    full_calendar()
    print("\nEscolha no mínimo 4 disciplinas, e no máximo 8:")
    print("Para encerrar sua matrícula digite [Q]")
    code_subj = input("Digite o código da disciplina desejada: ").upper()                 
    if code_subj == 'Q' and len(student.enrolled_classes) >= 4:
        return -1
    elif code_subj != 'Q':
        subj = subject_from_code(code_subj)
        # Check sujbect
        if isinstance(subj, str):
            print(f'Não tem disciplina com codigo {subj}.')
        else:
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
#Lembrar que colocar False de volta
matricula_is_finished = False
ajuste_is_finished = False
count_formandos = 0
count_continuos = 0
count_individual = 0

#Calouros
students = read_students()
students_enrolled = []
new_students = make_new_students()
for stud in new_students:
    stud.enrolled_classes = subjects[:5]
    students_enrolled.append(stud)

for s in students_enrolled:
    print(s)


list_inserts = []
list_removes = []
list_changes = []

while should_continue:
    menu()
    choice = input("Digite a opção escolhida: ")
    clear()

    #TODO SALVAR NA BASE DE DADOS
    #TODO VERIFICAR TODAS AS ENTRADAS
    if choice == '1':
        while not matricula_is_finished:
            print("Perído da matrícula em andamento...\n\n\n")
            
            matricula = input("Digite o número da sua matrícula: ")
            student = student_from_registration(int(matricula), students) 
            
            if student:
                #Formandos
                if student.type == 'Formando':
                    while len(student.enrolled_classes) < 8:
                        subject_chosen = choice_subject(student)
                        if subject_chosen == -1:
                            break
                        sleep(3)        # ?
                        clear()
                    count_formandos += 1
                              
                #Padrao
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

                students_enrolled.append(student)
                for s in students_enrolled:
                    print(s)
                # for stud in students:
                #     print(str(stud))
                 
                #Matricula is finished
                if count_formandos == MAX_FORMANDOS and count_individual == MAX_INDIVIDUAL and count_continuos == MAX_CONTINUOS:
                    want_stop_matricula = input("Deseja encerrar o período da matrícula? [S/N] ").upper()
                    if want_stop_matricula == 'S':
                        matricula_is_finished = True
                       # write_students_to_database(students_enrolled)
                        print("Período de matrícula encerrado!")
                        sleep(3) 
            else:
                print("Esse número de matrícula não está cadastrado!")

    #TODO AJUSTE
    elif choice == '2':
        if matricula_is_finished:
            print("Período de ajuste em andamento...\n\n\n")
            
            students = read_students()
            matricula = input("Digite o número da sua matrícula: ")
            student = student_from_registration(int(matricula), students)
            
            if student == -1:
                print("Você não está matriculado!")
                break

            menu_ajuste()
            choice = input("Digite e opção desejada: ")

            if choice == '1': #Insert
                full_calendar()
                code_subj = input("Digite o código da disciplina que você quer inserir: ")
                subj = subject_from_code(code_subj)
                sucess = student.check_enroll(subj)

                if sucess == 200:
                    ins = {
                        "student": (student, subj)
                    }
                    print("Seu pedido foi registrado!")
                    sleep(3)

                    for s in list_changes:
                        if s["student"][1][0].code == ins["student"][1].code:                    
                            #Make the enrollment
                            student_change = s["student"][0]
                            student_change.UNenroll(s["student"][1][0])
                            student_change.enroll(s["student"][1][1])

                            student_insert = ins["student"][0]
                            student_insert.enroll(ins["student"][1])

                            print("Prioridade especial")
                            sleep(3)
                        else:
                            list_inserts.append(ins)
                            print("Prioridade normal")
                            sleep(3)
                else:
                    print("Não pode inserir essa disciplina!")
                    sleep(3)

            elif choice == '2': #Remove
                full_calendar()
                code_subj = input("Digite o código da disciplina que você quer remover: ")
                subj = subject_from_code(code_subj)
                sucess = student.check_UNenroll(subj)

                if sucess == 200:
                    rem = {
                        "student": (student, subj)
                    }
                    print("Seu pedido foi registrado!")
                    sleep(3)

                    for s in list_changes:
                        if s["student"][1][1].code == rem["student"][1].code:                    
                            #Make the enrollment
                            student_remove = rem["student"][0]
                            student_remove.UNenroll(rem["student"][1])

                            student_change = s["student"][0]
                            student_change.UNenroll(s["student"][1][0])
                            student_change.enroll(s["student"][1][1])

                            print("Prioridade especial")
                            sleep(3)
                        else:
                            list_removes.append(rem)
                            print("Prioridade normal")
                else:
                    print("Você não está matriculado nessa matéria")

            elif choice == '3': #Change
                full_calendar()
                code_subj_remove = input("Digite o código da disciplina que você quer remover: ")
                code_subj_insert = input("Digite o código da disciplina que você quer inserir: ")
                #Levando em consideração, que o usuário vai digitar algo válido
                subj_remove = subject_from_code(code_subj_remove) #Check UNenroll
                sucess = student.check_UNenroll(subj_remove)
                if sucess != 200:
                    print("Você não pode remover essa matéria!")
                    break

                subj_insert = subject_from_code(code_subj_insert) #Check enroll
                sucess = student.check_enroll(subj_insert)
                if sucess != 200:
                    print("Você não pode inserir essa matéria!")
                    break
                
                cha = {
                    "student": (student, (subj_remove, subj_insert))
                }
                
                #Check inserts
                for s in list_inserts:
                    if s["student"][1].code == cha["student"][1][0].code:
                        #Make the enrollment
                        student_change = cha["student"][0]
                        student_change.UNenroll(cha["student"][1][0])
                        student_change.enroll(cha["student"][1][1])

                        student_insert = s["student"][0]
                        student_insert.enroll(s["student"][1])

                        print("Prioridade especial")
                        sleep(3)
                    else:
                        list_changes.append(cha)
                        print("Prioridade normal")
                        sleep(3)
                        
                #Check removes
                for s in list_removes:
                    if s["student"][1].code == cha["student"][1][1].code:
                        #Make the enrollment
                        student_remove = s["student"][0]
                        student_remove.UNenroll(s["student"][1])
                        
                        student_change = cha["student"][0]
                        student_change.UNenroll(cha["student"][1][0])
                        student_change.enroll(cha["student"][1][1])

                        print("Prioridade especial")
                        sleep(3)
                    else:
                        list_changes.append(cha)
                        print("Prioridade normal")
                        sleep(3)
                list_changes.append(cha)
                print("Seu pedido foi registrado!")
                sleep(3)
                

        else:
            print("Ainda não começou o período de ajuste.")
            sleep(3)

    #TODO REAJUSTE
    elif choice == '3':
        if matricula_is_finished and ajuste_is_finished:
            print("Período de reajuste em andamento...\n\n\n")
        else:
            print("Período de reajuste ainda não começou.")
            sleep(3)

    elif choice == '99':
        should_continue = False
