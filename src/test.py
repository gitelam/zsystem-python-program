import time
import psutil
import os
import platform
import random


#main thar reicieves args and it stop until with the arg = "stop"
def randomNum():
    return random.randint(1, 100)

if __name__ == '__main__':
    randomNum()