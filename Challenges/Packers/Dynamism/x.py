from pwn import *

context.update(arch='amd64', os='linux')
context.terminal=['tmux','splitw','-h']
#context.log_level = 'debug'

if "REMOTE" in args:
    
    p=remote("bin.training.offdef.it", 4010)

else:
    p=process(["./dynamism", "flag{aaa}"])
    gdb.attach(p,"""
    #b* 0x00401d33
    
    """)



p.interactive()


first (data)
0x7ffff7ffa000:	mov    rdi,QWORD PTR [rdi]
0x7ffff7ffa003:	jmp    0x7ffff7ffa027
0x7ffff7ffa005:	pop    rsi
0x7ffff7ffa006:	mov    r12,0x9
0x7ffff7ffa00d:	cmp    r12,0x0
0x7ffff7ffa011:	je     0x7ffff7ffa026
0x7ffff7ffa013:	mov    r13,QWORD PTR [rsi]
0x7ffff7ffa016:	mov    QWORD PTR [rdi],r13
0x7ffff7ffa019:	add    rsi,0x8
0x7ffff7ffa01d:	add    rdi,0x8
0x7ffff7ffa021:	dec    r12
0x7ffff7ffa024:	jmp    0x7ffff7ffa00d
0x7ffff7ffa026:	ret    
0x7ffff7ffa027:	call   0x7ffff7ffa005

0x7ffff7ffa02c:	0x4827c3baaa35c7cc	0x2648a0c1cd54abaa
0x7ffff7ffa03c:	0x3c46afcfde54b5ab	0x3178e2e5d05ba8a5
0x7ffff7ffa04c:	0x3c78b7d5cd6ab2a3	0x1740a2d6cc6aa2a4
0x7ffff7ffa05c:	0x265ea7e5c75ab5aa	0x3c4e9cc9cb4298ed
0x7ffff7ffa06c:	0x35189cded854af93	0x0000000000000000



second (prepare input)
0x7ffff7ffa000:	mov    rsi,QWORD PTR [rdi+0x8]    rdi
0x7ffff7ffa004:	mov    rdi,QWORD PTR [rdi]
0x7ffff7ffa007:	mov    rdx,rsi
0x7ffff7ffa00a:	add    rdx,0x100	
0x7ffff7ffa011:	mov    rsi,QWORD PTR [rsi]
0x7ffff7ffa014:	mov    r12,0x8		
0x7ffff7ffa01b:	cmp    r12,0x0
0x7ffff7ffa01f:	je     0x7ffff7ffa037
0x7ffff7ffa021:	mov    rcx,QWORD PTR [rdi]
0x7ffff7ffa024:	xor    rcx,rsi			
0x7ffff7ffa027:	mov    QWORD PTR [rdx],rcx
0x7ffff7ffa02a:	add    rdx,0x8
0x7ffff7ffa02e:	add    rdi,0x8
0x7ffff7ffa032:	dec    r12
0x7ffff7ffa035:	jmp    0x7ffff7ffa01b
0x7ffff7ffa037:	ret





third (check)
0x7ffff7ffa000:	mov    rdi,QWORD PTR [rdi]
0x7ffff7ffa003:	mov    rsi,rdi
0x7ffff7ffa006:	add    rsi,0x100
0x7ffff7ffa00d:	add    rdi,0x8
0x7ffff7ffa011:	mov    rcx,0x9
0x7ffff7ffa018:	cmp    rcx,0x0
0x7ffff7ffa01c:	je     0x7ffff7ffa03e
0x7ffff7ffa01e:	mov    r10,QWORD PTR [rdi]
0x7ffff7ffa021:	mov    r11,QWORD PTR [rsi]
0x7ffff7ffa024:	add    rdi,0x8
0x7ffff7ffa028:	add    rsi,0x8
0x7ffff7ffa02c:	cmp    r10,r11 
0x7ffff7ffa02f:	jne    0x7ffff7ffa036
0x7ffff7ffa031:	dec    rcx
0x7ffff7ffa034:	jmp    0x7ffff7ffa018
0x7ffff7ffa036:	mov    rax,0x0
0x7ffff7ffa03d:	ret    
0x7ffff7ffa03e:	mov    rax,0x1
0x7ffff7ffa045:	ret



0x4827c3baaa35c7cc

flag{congratulationz_!_you_got_the_flag_from_dyn!_was_it_hard_?}

x/40gx 0x5555555596c0

b* 0x555555555574

