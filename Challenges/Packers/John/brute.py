import subprocess
import random
import string
# Scarica le parole dell'alfabeto inglese (una sola volta)
#import nltk
#nltk.download('words')

def generate_random_english_word(length):
    characters = string.ascii_letters + string.digits + "_-"
    return ''.join(random.choice(characters) for _ in range(length))


if __name__ == "__main__":
    flag_trovato = False

    for _ in range(1000):
        if flag_trovato:
            break

        # Genera una nuova parola inglese di 7 lettere
        random_word = generate_random_english_word(1)

        # Crea l'input completo con la nuova parola
        input_string = f"flag{{packer-4o3-1{random_word}37&-annoying__}}"

        print(f"Tentativo: {random_word}")

        # Esegui il programma john con l'input e verifica l'output
        command = ["./john", input_string]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, text=True)

        try:

            # Leggi l'output dalla stdout del processo
            output = process.stdout.read()

            # Controlla se l'output contiene la stringa desiderata
            if "\x1b[1;37mYou got the flag" in output:
                flag_trovato = True
                print(f"Flag trovato! Input: {input_string}")

        except Exception as e:
            print(f"Errore: {e}")

        finally:
            # Chiudi la stdin del processo
            process.wait()

    print(f"Niente")
