#!/usr/bin/env python3

""" fizzbuzz.py

    write a program that prints out the numbers from 1 to 100.
    But for multiples of  print 'Fizz' instead of the number and for
    multiples of five print 'Buzz'. For multiples of both 5 and 3 print
    "FizzBuzz"

"""

def fizzBuzz(num):
    if (num % 3 == 0) & (num % 5 == 0):
        print("FizzBuzz")
    elif (num % 3 == 0):
        print("Fizz")
    elif (num % 5 == 0):
        print("Buzz")
    else:
        print(num)

