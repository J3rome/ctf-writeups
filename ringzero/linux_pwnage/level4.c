#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
int main(int argc, char **argv) {
   // printf() displays the string inside quotation
   time_t cur = time(NULL);
   //printf("%s\n", ctime(&cur));
   srand(cur);
   char key = (unsigned char)(rand());
   fprintf(stderr, "--\\%02hhx--\n\n", (unsigned char) key);
   //printf("key is %c\n", key);
   //printf("Input is %s\n", argv[1]);
   
   char buf[1024];
   strncpy(buf, argv[1], 1024);
    
   int size = strlen(buf);

   for(int i=0; i < size; i++){
       buf[i] = (char) buf[i] ^ key;
   }
   //printf("Encoded is %s\n", buf);
   printf("%s", buf);

   /*for(int i=0; i < size; i++){
       buf[i] = (char) buf[i] ^ key;
   }

   printf("Decoded is %s\n", buf);
   */
   return 0;
}

