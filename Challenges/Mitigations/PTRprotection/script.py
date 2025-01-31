import subprocess
import time

# Esegui lo script 100 volte
iterations = 1000
arg_to_pass = "REMOTE"

win_found = False  # Variabile per indicare se "WIN" è stato trovato

for i in range(iterations):
    print(f"Running iteration {i + 1}...")
    result = subprocess.run(["python", "x.py", arg_to_pass], input="\n", stdout=subprocess.PIPE, text=True)
    
    # Ottieni l'output dal risultato
    output = result.stdout
    
    # Controlla se "WIN" è presente nell'output
    if "WIN" in output:
        print("Trovato 'WIN'. Uscita.")
        win_found = True
        break  # Esci dal loop se trovi 'WIN'
    
    time.sleep(2)  # Ritardo di 1 secondo tra le iterazioni

# Salvataggio del valore di output in un file
with open("output.txt", "w") as file:
    file.write(output)

if win_found:
    print("WIN trovato. L'output è stato salvato in 'output.txt'")
else:
    print("WIN non trovato. L'ultimo output è stato salvato in 'output.txt'")
