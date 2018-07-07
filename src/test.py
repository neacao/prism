#!/usr/bin/env python

# Python code to demonstrate naive
# method to compute gcd ( Euclidean algo )
 
 
def computeGCD(x, y):
 
   while(y):
       x, y = y, x % y
 
   return x
 
# prints 12
print (computeGCD(570570,7106))
print (computeGCD(255255, 78))

