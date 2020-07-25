#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <time.h>
#define BUFFER_MAX_SIZE 1024

typedef struct __INPUT {
        char output[BUFFER_MAX_SIZE / 4];
} INPUT;

void parse_buffer(char *buffer) {
    srand(time(NULL));
    char key = (unsigned char)(rand());
    int i, size = strlen(buffer);
    for(i = 0; i < size; i++) {
        buffer[i] = (char)buffer[i] ^ key;
    }
}

int main(int argc, char **argv) {
    char buff[BUFFER_MAX_SIZE];
    memset(buff, 0, 256);
    INPUT input;
    char out[BUFFER_MAX_SIZE / 4];
    char in[BUFFER_MAX_SIZE];
    memset(out, 0, BUFFER_MAX_SIZE / 4);
    if(argc != 2) {
        printf("Usage: %s buffer\n", argv[0]);
        exit(0);
    }
    printf("processing input\n");
    strncpy(in, argv[1], BUFFER_MAX_SIZE - 1);
    printf("in : %ld, argv %ld\n", strlen(in), strlen(argv[1]));
    parse_buffer(in);
    strncpy(out, in, BUFFER_MAX_SIZE - 1);
    strncpy(input.output, out, BUFFER_MAX_SIZE - 1);
    printf("output: %s\n", input.output);
    return 0;
}

