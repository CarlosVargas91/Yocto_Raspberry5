#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(void)
{
    printf("========================================\n");
    printf("  Hello from meta-homeai layer!\n");
    printf("  Raspberry Pi 5 - Custom Yocto Linux\n");
    printf("  Carlos Vargas - Embedded AI Project\n");
    printf("========================================\n");

    printf("\nKernel version:\n");
    system("uname -a");

    printf("\nCPU Info:\n");
    system("cat /proc/cpuinfo | grep 'Model'");

    printf("\nMemory:\n");
    system("free -h");

    printf("\nLayer is working correctly!\n");

    return 0;
}