/* 
 * Decode RGB led serial bitstream
 * p. brier
 * timing based on GCC compiler for LPC1768 using MBED library
 */

#include "mbed.h"

DigitalOut led1(LED1);
DigitalOut led2(LED2);
DigitalOut led3(LED3);
DigitalOut led4(LED4);

DigitalIn data(p30);

char bitdata[256];
int bitlen=0;


Serial pc(USBTX, USBRX);

static inline bool datapin()
{
  return (LPC_GPIO0->FIOPIN & (1<<4));    
}


int main() 
{
    Timer t;
    t.start();
    
    pc.baud(115200);
      
    while(0)  // echo state to led
    {
      if ( datapin() )
        led1 = 1;
      else
        led1 = 0;    
    }
    
    while(0) // measure histogram
    {
      volatile int j = 0;
      int hist[100];

      for(int i=0; i<100; i++) hist[i]=0;
      for(int i=0; i<10000; i++)
      { 
        while( datapin() ) j++;
        hist[j]++;
        while( ! datapin() ) j = 0; 
      }
 
      for(int i=0; i<20; i++) 
        printf("%d %d\n", i, hist[i]);
    }
    
    volatile int bitlen = 0;
    volatile int j = 0;
    volatile char bitdata[256];
    printf("\n\rcompiled: " __DATE__  " " __TIME__ "\n\r");
    
    while(1) { // decode bits
      j = 0;
      while( !datapin()  ) 
      {
        if ( j++ > 100 ) // latch
        {
            if ( bitlen ) // there is data
            {
              led1 = 1;
              printf("%d %d %s\n", (int)t.read_us(), (int)bitlen, bitdata);
              bitlen = 0;
              led1 = 0;
            }
        }
      }
      j = 0;
      while( datapin() ) j++;
      bitdata[bitlen++] = (j> 3 ? '1' : '0');    
    }
}
