"""
TESTS is a dict with all you tests.
Keys for this will be categories' names.
Each test is dict with
    "input" -- input data for user function
    "answer" -- your right answer
    "explanation" -- not necessary key, it's using for additional info in animation.
"""

#This is very basic and verbose solution. You need to compress this code as much as possible (in compiled form).
def fibgolf_basic(sequence, num):
    if sequence == 'fibonacci':
        i = 2
        a = 0
        b = 1
        while True:
            nxt = a + b
            if i == num: return nxt
            a = b
            b = nxt
            i += 1
    if sequence == 'tribonacci':
        i = 3
        a = 0
        b = 1
        c = 1
        while True:
            nxt = a + b + c
            if i == num: return nxt
            a = b
            b = c
            c = nxt
            i += 1
    if sequence == 'lucas':
        i = 2
        a = 2
        b = 1
        while True:
            nxt = a + b
            if i == num: return nxt
            a = b
            b = nxt
            i += 1
    if sequence == 'jacobsthal':
        i = 2
        a = 0
        b = 1
        while True:
            nxt = 2 * a + b
            if i == num: return nxt
            a = b
            b = nxt
            i += 1
    if sequence == 'pell':
        i = 2
        a = 0
        b = 1
        while True:
            nxt = a + 2 * b
            if i == num: return nxt
            a = b
            b = nxt
            i += 1
    if sequence == 'perrin':
        i = 3
        a = 3
        b = 0
        c = 2
        while True:
            nxt = a + b
            if i == num: return nxt
            a = b
            b = c
            c = nxt
            i += 1
    if sequence == 'padovan':
        i = 3
        a = 0
        b = 1
        c = 1
        while True:
            nxt = a + b
            if i == num: return nxt
            a = b
            b = c
            c = nxt
            i += 1


TESTS = {}
import random

category = ['fibonacci', 'tribonacci', 'lucas', 'jacobsthal', 'pell', 'perrin', 'padovan']
for i, e in enumerate(category):
    TESTS[str(i + 1) + '. ' + e] = []
    for n in random.sample(range(10, 400), 8):
        TESTS[str(i + 1) + '. ' + e].append({"input": [e, n], "answer": fibgolf_basic(e, n)})
