from pwn import *

context.update(arch='amd64', os='linux')
context.terminal = ['tmux', 'splitw', '-h']

if "REMOTE" not in args:
    p = process("./leaked_license")
    gdb.attach(p, """
    b* 0x00101169
    b* 0x001012b5

    """)
else:
    p = remote("bin.training.offdef.it", null)


p.interactive()
