#!/usr/bin/env python3

""" Problem: Simple command line UI with login access

Create a student grading system using Python that has the following functionality:

1.Entering the Grades of a student
2.Removing a student from the system
3.Calculating the average grades of a students

The user should be able to select whether he/she wants to remove a student, enter grades for a
student or find the average grades.

Also perform the following as part of this project:
1. There should be a log-in system to allow only admin access to the grading system.
2. Use dictionaries and lists for storing student’s, admin's data.
3. Use Python functions as much as you can """


from sys import exit
from getpass import getpass
from functools import partial
import statistics
import subprocess


def login(valid_users):
    """
    Basic login functionality using a dictionary.
    :param valid_users: Currently a dictionary for testing purposes!
    :return:
    """
    username = input("Username: ").strip()
    password = getpass()
    if username not in valid_users.keys():
        print("Username not recognised.")
        exit_program(1)
    elif password != valid_users[username]:
        print("Password not correct.")
        exit_program(1)


def yes_no(message):
    """
    Returns True or False for Yes and No respectively
    :param message: Question that requires a yes/no response
    :return: True or False based on response
    """
    response = input("{} (Y/N): ".format(message)).lower().strip()
    if response == 'y':
        return True
    else:
        return False


def display_students(records, out=False):
    """
    Displays or returns the names of the students in the records
    :param records: dictionary of names (tuple) [keys] : list of scores [values]
    :param out: if True, returns an enumerated dictionary of students to work with the UI
    :return:
    """
    if not out:
        print("\nStudents enrolled: ")
        if len(records.keys()) == 0:
            print("None")
        else:
            for name, scores in records.items():
                print("{},{}:\t\t{}".format(name[0].upper(), name[1], scores))
    else:
        student_list = {k: v for k, v in enumerate(records.keys(), 1)}
        return student_list


def add_student(records):
    """
    Adds a student to the records dictionary
    :param records: dictionary of names (tuple) [keys] : list of scores [values]
    :return: none - updates records dictionary
    """
    while True:
        last_name = input("Enter Student's Last name: ").strip()
        first_name = input("Enter Student's First name: ").strip()
        student_name = last_name, first_name

        if not records.get(student_name):
            print("Adding student '{} {}'".format(first_name, last_name))
            records[student_name] = list()
            if not yes_no("Would you like to add another student?"):
                break
        else:
            print("{} {} already exists in the record (I'm currently assuming two of them "
                  "can't exist simultaneously!)\n".format(first_name, last_name))
            continue

    display_students(records)


def remove_student(records):
    """
    Removes student from the records dictionary
    :param records: dictionary of names (tuple) [keys] : list of scores [values]
    :return: none - updates the records dictionary
    """

    names = display_students(records, True)

    while True:
        for k, v in names.items():
            print("[{}] - {},{}".format(k, v[0], v[1]))

        selection = input("Choose the student to remove by number (Enter to exit): ").strip()

        try:
            selection = int(selection)
            if names.get(selection):
                print("Removing '{},{}' from records...".format(names[selection][0], names[selection][1]))
                del(records[names[selection]])
                names = display_students(records, True)
            else:
                raise TypeError
        except (TypeError, ValueError):
            if yes_no("Do you want to stop removing students?"):
                break

    display_students(records)


def stats(vector):
    """
    Calculates mean and stdDev for a given vector using the statistics module
    :param vector: list floats
    :return: tuple (mean, standard deviation)
    """
    mean = statistics.mean(vector)
    stdev = statistics.stdev(vector)
    return mean, stdev


def get_stats(records, type="student"):
    """
    Calculates the mean and std Dev for either each student or the class as a whole
    Bases the class mean on the minimum common number of exams

    :param records: dictionary of names (tuple) [keys] : list of scores [values]
    :param type: indicates whether "student" or "class" stats are required
    :return: none - Prints output to stdout
    """
    if type != "student":
            class_vector = []
            for v in records.values():
                class_vector.append(v)
            r = min([len(l) for l in class_vector])
            class_vector = [l[i] for i in range(r) for l in class_vector]
            results = stats(class_vector)
            print("\nClass Mean:\t\t{:.2f} (Std.Dev: {:.2f})".format(results[0], results[1]))
    else:
        for k, v in records.items():
            results = stats(v)
            print("{},{}:\t\tMean Score {:.2f} (Std.Dev: {:.2f})".format(k[0].upper(), k[1], results[0], results[1]))


def add_score(records, student):
    """
    Adds a user entered score to the dictionary
    :param records: dictionary of names (tuple) [keys] : list of scores [values]
    :param student: tuple (last name, first name) representing student
    :return: none - updates the records dictionary
    """
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
    """
    User picks the student by number from a presented list and adds a new score to their record
    :param records: dictionary of names (tuple) [keys] : list of scores [values]
    :return: none - updates the records dictionary
    """
    names = display_students(records, True)

    while True:
        for k, v in names.items():
            print("[{}] - {},{}".format(k, v[0], v[1]))

        selection = input("Pick a student by number (Enter to skip): ").strip()

        try:
            selection = int(selection)
            if names.get(selection):
                add_score(records, names[selection])
                break
            else:
                raise TypeError
        except (TypeError, ValueError):
            if yes_no("Do you want to stop adding scores to the records?"):
                break

    display_students(records)


def exit_program(status=0):
    print("\nExiting program...")
    exit(status)


def choose_options():
    """
    Basic command line functionality
    :return: none
    """
    while True:
        try:
            print("\nChoose from the following options:{}".format(options))
            key_pressed = getpass(prompt='').strip()
            if key_pressed in [str(i) for i in range(6)]:
                selector[key_pressed](students)
            elif key_pressed == "9":
                selector[key_pressed]()
            else:
                raise KeyError
        except KeyError:
            if not yes_no("Option '{}' not available. Try again?".format(key_pressed)):
                exit_program(0)

# Global structures
students = dict()  # 'database' of students

students["Farah", "June"] = [3.0, 2.7, 3.1]
students["Biggs", "Adam"] = [2.9, 3.1, 3.0]
students["Walton", "Trevor"] = [3.1, 3.5, 3.2]

options = "\n[0] - List Students\n[1] - Add Student\n[2] - Remove Student\n[3] - " \
          "Add Student Score\n[4] - Show Class Average\n[5] - Show Student Averages\n\n" \
          "[9] - Exit\n"

selector = dict()  # selects the user chosen function
selector["0"] = display_students
selector["1"] = add_student
selector["2"] = remove_student
selector["3"] = update_record
selector["4"] = partial(get_stats, type="all")
selector["5"] = get_stats
selector["9"] = exit_program

# Login tests
passwd = dict()    # in lieu of a secure database call!
passwd["alberton"] = "password"
passwd["griffitd"] = "mitzi123"
passwd["eklandr"] = "5yNGh_4L5s"


if __name__ == '__main__':
    login(passwd)
    choose_options()
