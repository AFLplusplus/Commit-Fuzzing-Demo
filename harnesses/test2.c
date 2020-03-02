#include "../include/header.h"
#include <stdio.h>
#include <unistd.h>

int main() {

  char buf[1024*10];
  
  size_t l = read(0, buf, 1024*10);
  
  if(target_func2(buf, l)) target_func3(buf, l);

}
