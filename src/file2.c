#include <stdio.h>

int target_func2(char *buf, int size) {

  switch (buf[0]) {

    case 1:
      if (buf[1] == '\x22') {

        puts("null ptr deference");
        *(char *)(0) = 1;

      }

      break;
    case 0xff:
      if (buf[2] == '\x28') {

        if (buf[1] == '\x41') {

          puts("crash....");
          *(char *)(0xdeadbeef) = 1;

        }

      }

      break;
    default: puts("default action"); break;

  }

  return 1;

}


