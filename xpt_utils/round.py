import math

def div_ceil(a, b):
  return int(math.ceil(float(a)/float(b)))

def ceil_multiple(a, m):
  return int(math.ceil(float(a)/float(m))*float(m))

def div_floor(a, b):
  return int(math.floor(float(a)/float(b)))

def floor_multiple(a, m):
  return int(math.floor(float(a)/float(m))*float(m))
