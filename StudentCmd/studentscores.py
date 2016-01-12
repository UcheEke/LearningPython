#!/usr/bin/env python3

from sys import exit
from getpass import getpass


def login(valid_users):
    username = input("Username: ").strip()
    password = getpass()
    if username not in valid_users.keys():
        print("Username not recognised.")
        exit_program(1)
    elif password != valid_users[username]:
        print("Password not correct.")
        exit_program(1)


def yes_no(message):
    response = input("{} (Y/N): ".format(message)).lower().strip()
    if response == 'y':
        return True
    else:
        return False


def display_students(records, out=False):
    if not out:
        print("\nStudents enrolled: ")
        for name, scores in records.items():
            print("{},{}: {}".format(name[0].upper(), name[1], scores))
    else:
        student_list = {k: v for k, v in enumerate(records.keys(), 1)}
        return student_list


def add_student(records):
    while True:
        last_name = input("Enter Student's Last name: ").strip()
        first_name = input("Enter Student's First name: ").strip()
        student_name = last_name, first_name

        if not records.get(student_name):
            print("Adding student '{} {}'".format(first_name, last_name))
            records[student_name] = list()
            if yes_no("Would you like to add another student?"):
                continue
            else:
                break
        else:
            print("{} {} already exists in the record (I'm currently assuming two of them "
                  "can't exist simultaneously!)\n".format(first_name, last_name))
            continue

    display_students(records)


def remove_student(records):
    # 1. By enumeration (for small class sizes)
    names = display_students(records, True)

    while True:
        for k, v in names.items():
            print("{}. {},{}".format(k, v[0], v[1]))

        selection = input("Choose the student to remove by number: ").strip()

        try:
            selection = int(selection)
            if names.get(selection):
                print("Removing '{},{}' from records...".format(names[selection][0], names[selection][1]))
                del(records[names[selection]])
            else:
                raise TypeError
        except (TypeError, ValueError):
            if not yes_no("Invalid choice. Try again?"):
                break

    display_students(records)


def get_stats(records):
    print("Adding grades...")


def add_score(records, student):
    while True:
        try:
            score = input("Enter current score for '{},{}': ".format(student[0], student[1])).strip()
            score = float(score)
            break
        except TypeError:
            if not yes_no("Invalid Score. Try again?"):
                break

    records[student].append(score)


def update_record(records):
    names = display_students(records, True)

    while True:
        for k, v in names.items():
            print("{}. {},{}".format(k, v[0], v[1]))

        selection = input("Pick a student by number (Enter to skip): ").strip()

        try:
            selection = int(selection)
            if names.get(selection):
                add_score(records, names[selection])
                break
            else:
                raise TypeError
        except (TypeError, ValueError):
            if not yes_no("Invalid choice. Try again?"):
                break

    display_students(records)


def exit_program(status=0):
    print("\nExiting program...")
    exit(status)


def choose_options():
    while True:
        key_pressed = input("\nChoose from the following options:{}".format(options)).strip()
        if key_pressed in [str(i) for i in range(5)]:
            selector[key_pressed](students)
        elif key_pressed == "5":
            selector[key_pressed]()
        else:
            print("Option '{}' not available.Try again".format(key_pressed))

students = dict()  # 'database' of students

options = "\n[0] - List Students\n[1] - Add Student\n[2] - Remove Student\n[3] - " \
          "Update Records\n[4] - Show Class Average\n[5] - Exit\n\n"

selector = dict()  # selects the user chosen function
selector["0"] = display_students
selector["1"] = add_student
selector["2"] = remove_student
selector["3"] = update_record
selector["4"] = get_stats
selector["5"] = exit_program

passwd = dict()    # in lieu of a secure database call
passwd["alberton"] = "password"
passwd["griffitd"] = "mitzi123"
passwd["eklandr"] = "5yNGh_4L5s"


if __name__ == '__main__':
    login(passwd)
    choose_options()
