from Student import *
from sys import platform
from os import system
from time import sleep

MAX_FORMANDOS = 1
MAX_CONTINUOS = 1
MAX_INDIVIDUAL = 1

LIST_INSERTS = []  # (Student, subject_ins)
LIST_REMOVES = []  # (Student, subject_rem)
LIST_CHANGES = []  # (Student, subject_ins, subject_rem)

LIST_REAJUSTMENTS = [] # Ordered list containing request of remove, insert, change


def clear():
    if platform == 'linux' or platform == 'darwin':
        system('clear')        
    elif platform == 'win32':
        system('cls')


def menu():
    
    clear()
    print('''
    ------MATRICULA------

    [1] - Matrícula
    [2] - Ajuste
    [3] - Reajuste
    [0]- Encerrar o programa 
    
    ''')


def menu_ajuste():
    print('''

    ------SELECIONE UMA OPCAO:-----
        
    [1] - Inserir uma disciplia
    [2] - Remover uma disciplina
    [3] - Trocar uma disciplina   
    
    ''')




# Ask for user registration, return student if student is found
def ask_registration(students):
    matricula = input("Digite o número da sua matrícula: ")
    # Prevent ValueError converting str to int
    if matricula.isdigit():
        student = student_from_registration(int(matricula), students) 
    else:
        student = 0

    return student


# |------------------------------------| #
# |     Phase 1 simple enrollment      | #
# |------------------------------------| #
def choose_subjects(student):
    
    while len(student.enrolled_classes) < 8:
        full_calendar()
        print(student.getGrades()) 
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
                else:
                    print(f"Matrícula realizada com sucesso na disciplina {subj}.")
            
        sleep(3)
        clear()


# |-------------------------------------------------------| #
# |     Pahse 2 Adjustments (insert, remove, change)      | #
# |-------------------------------------------------------| #
# Used for requesting to insert or remove a subject
def adjustments(student, remove=False): 

    full_calendar()
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
        sleep(3)


# Used to request a subject replacement
def adjustments_replace(student):
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
    
    sleep(3)

# |-------------------------------------------------------------------| #
# |     Check priority for subject changes, insertion end remove      | #
# |-------------------------------------------------------------------| #
def check_priority(student, subj_insert, subj_remove):
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





    ''' 
        aluno com solicitacao de ajuste --> op(inserir, remover e trocar)

        X alunos 

        ajuste: OPCODE ---> cod de operacao
                {disciplina: OPCODE}

        
    ---------------------------------------------------------------------
        OPCODE 1: remove disciplina
        remover[] ---> fazer de uma vez
            materias removidas/vagas disponiveis[] ---> 

        
        OPCODE 2: inserir 
        inserir[]
            remover[qtd vagas] ---> inserir[de acordo com as vagas]
            prioridade de insercao

        OPCODE 3: trocar 
        trocar[] ---> checar se h'a materia nas vagas disponiveis de remover[]
            prioridade de troca

    -----------------------------------------------------------------------

        Depois das 3 listas finalizadas 


        CHECAR A PRIORIDADE DE SOLUCAO 

        X Y Z --> qual esta mais perto da formacao 

    y > x > x

    '''


should_continue = True

# Lembrar que colocar False
matricula_is_finished = False
ajuste_is_finished = False

count_formandos = 0
count_continuos = 0
count_individual = 0

# Calouros
students = read_students()
students_enrolled = []
new_students = make_new_students()

for stud in new_students:
    stud.enrolled_classes = subjects[:5]
    students_enrolled.append(stud)

for s in students_enrolled:
    print(s)


while should_continue:
    menu()
    choice = input("Digite a opção escolhida: ")
    clear()

    #TODO SALVAR NA BASE DE DADOS
    #TODO VERIFICAR TODAS AS ENTRADAS
    if choice == '1':
        
        while not matricula_is_finished:
            print("Perído da matrícula em andamento...\n\n\n")
            
            student = ask_registration(students)

            if student:
                
                #Formandos
                if student.type == 'Formando':
                    choose_subjects(student)
                    count_formandos += 1
                              
                #Padrao
                elif student.type == 'Continuo' and count_formandos == MAX_FORMANDOS:
                    student.enrolled_classes = get_subjects_from_semester(student.semester)
                    choose_subjects(student)    
                    count_continuos += 1
                    
                #Individual
                elif student.type == 'Individual' and count_formandos == MAX_FORMANDOS and count_continuos == MAX_CONTINUOS:   
                    choose_subjects(student)
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
        
        if matricula_is_finished and not ajuste_is_finished:
            print("Período de ajuste em andamento...\n\n\n")
            
            student = ask_registration(students)
            if student:
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
                                
                want_finish_adjustment = input("Você desejar encerrar o período de ajuste? [S/N] ").upper()
                if want_finish_adjustment == 'S':
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
            
            else:
                print("Você não está matriculado!")

                
        else:
            print("Ainda não começou o período de ajuste.")
            sleep(3)

    #TODO REAJUSTE
    elif choice == '3':
        if matricula_is_finished and ajuste_is_finished:
            print("Período de reajuste em andamento...\n\n\n")

            students = read_students()
            matricula = input("Digite o número da sua matrícula: ")

            # Prevent ValueError converting str to int
            if matricula.isdigit():
                student = student_from_registration(int(matricula), students) 
            else:
                student = 0
            
            if not student:
                print("Você não está matriculado!")
                break

            full_calendar()
            code_subj = input("Digite o código da disciplina que você quer inserir: ")
            subj = subject_from_code(code_subj)
            sucess = student.check_enroll(subj)
            
            if sucess == 200:
                
                ins = {
                    "student": (student,subj)
                }
                print("Seu pedido foi registrado!")
                list_readjust.append(ins)
                sleep(3)
            else:
                print("Erro: Falha ao realizar o pedido dessa disciplina.")
                sleep(3)
            
            want_finish_readjustment = input("Você desejar encerrar o período de reajuste? [S/N] ").upper()
            if want_finish_readjustment == 'S':
                #Realizar as matrículas dos normais
                #Changes, removes and inserts
                
                for i in range(0, len(list_readjust)-1):
                    for j in range(0, len(list_readjust)-1):
                        if list_readjust[j]["student"][0].coefficent < list_readjust[j+1]["student"][0].coefficent:
                            temp = list_readjust[j]
                            list_readjust[j] = list_readjust[j+1]
                            list_readjust[j+1] = list_readjust[j] 

            
            
                for s in list_readjust:
                    if s["student"][1].enrolled_students < s["student"][1].class_capacity:
                        s["student"][0].enroll(s["student"][1])
                        coef = s["student"][0].coefficent
                        print(f"Coeficiente: {coef}")
                        #print (s["student"][0].coefficent
                        name_print = s["student"][0]
                        print(f"{name_print} conseguiu sua matéria.")
                        sleep(10)
                    else:
                        print(f"{name_print} , não foi possivel realizar a matrícula, a disciplina escolhida não tinha mais vagas.")
                        sleep(10)



                        


        else:
            print("Período de reajuste ainda não começou.")
            sleep(3)

    elif choice == '0':
        should_continue = False





'''
    #TODO REAJUSTE
     elif choice == '3':
        if matricula_is_finished and ajuste_is_finished:
            print("Período de reajuste em andamento...\n\n\n")
            
            student = ask_registration(students)
            if student:
                # Ask if he whants to remove, add, change
                # Insert in a list ordered by Student.coefficient
                # Close reajuste and resolve requests
                pass

            else:
                print("Você não está matriculado!")

        else:
            print("Período de reajuste ainda não começou.")
            sleep(3)

    elif choice == '0':
        should_continue = False'''
