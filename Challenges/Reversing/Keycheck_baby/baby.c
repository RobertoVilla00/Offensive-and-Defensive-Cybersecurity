#include <stdio.h>

void findFlag() {
    char magic1[] = {0xEB, 0x51, 0xB0, 0x13, 0x85, 0xB9, 0x1C, 0x87, 0xB8, 0x26, 0x8D, 0x07};
    char flag[13]; // 13 bytes come specificato

    // Inizializza tmp a -0x45
    char tmp = -0x45;

    // Calcola la flag
    for (int i = 0; i < 12; i++) {
        flag[i] = magic1[i] - tmp;
        tmp = tmp + flag[i];
    }

    // Terminatore di stringa
    flag[12] = '\0';

    // Stampa la flag trovata
    printf("Flag: %s\n", flag);
}

int main() {
    findFlag();
    return 0;
}
