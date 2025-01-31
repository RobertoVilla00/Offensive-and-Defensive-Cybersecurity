import subprocess
import os

# Shellcode come sequenza di byte
shellcode_bytes = b"\x48\x31\xC0\x48\x31\xF6\x48\x31\xFF\x48\xC7\xC0\x23\x00\x00\x00\x48\xC7\xC7\x0A\x00\x00\x00\x48\xC7\xC6\x00\x00\x00\x00\x0F\x05"  # Sostituisci con la tua shellcode

# Converti i byte in una rappresentazione esadecimale leggibile
shellcode_hex = ''.join('\\x{:02x}'.format(byte) for byte in shellcode_bytes)

# Componi la shellcode come stringa
shellcode_str = f'"{shellcode_hex}"'

# Componi il comando per eseguire wrapper.py con la shellcode come input
# Aggiungi PYTHONUNBUFFERED=1 come variabile di ambiente
command = f'env PYTHONUNBUFFERED=1 bash -c \'echo -ne {shellcode_str} | python wrapper.py\''

# Esegui il comando usando subprocess
p = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# Stampa l'output e l'errore se presenti
print("Output:", p.stdout)
#print("Error:", p.stderr)
#print("Exit code:", p.returncode)
