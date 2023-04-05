import netmiko
import random

def config():
    x = random.randint(0,1)
    if x == 1:
        return "it worked!"
    else: return "it did not work :(s"
