import os
import sys

# back to the basics baby
print(sys.path)
help("modules")
days_of_the_week = 7

def say_hello(recipient):
    print("hello world! hello {}". format(recipient))
    return recipient