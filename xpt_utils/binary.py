import xpt_utils

def int_to_2_complement(a, size):
  if (a < 0):
    if (a < -pow(2, size)):
      xpt_utils.handle_error("Value (" + str(a) + ") out of range (" + str(-pow(2, size)) + ") !")
    else:
      return pow(2, size) + a
  else:
    if (a > pow(2, size) - 1):
      xpt_utils.handle_error("Value (" + str(a) + ") out of range (" + str(pow(2, size) - 1) + ") !")
    else:
      return a

def complement_2_to_int(a, size):
  if (a < 0):
    xpt_utils.handle_error("Value (" + str(a) + ") must be positive !\n")
  else:
    if (a > pow(2, size) - 1):
      xpt_utils.handle_error("Value (" + str(a) + ") out of range (" + str(pow(2, size) - 1) + ") !")
    elif (a > pow(2, size-1) - 1):
      return a - pow(2, size)
    else:
      return a

def assign_bit_vector(vector, vector_size, val, start, end):
  if (end >= vector_size or start > end):
    xpt_utils.handle_error("Parameters must follow this order : start(" + str(start) + ") <= end (" + str(end) + ") < size (" + str(vector_size) + ") !\n")

  vec_2_comp  = int_to_2_complement(vector, vector_size)
  val_2_comp  = int_to_2_complement(val, end - start + 1)
  bin_val     = eval('"{:0' + str(end -start + 1) + 'b}".format(' + str(val_2_comp) + ')')
  bin_vector  = eval('"{:0' + str(vector_size) + 'b}".format(' + str(vec_2_comp) + ')')

  bin_vector = eval('bin_vector[:' + str(vector_size - 1 - end) + '] + bin_val + bin_vector[' + str(vector_size - 1 - start + 1) + ':]')

  return int(bin_vector, 2)

def get_bit_vector(vector, vector_size, start, end):
  if (end >= vector_size or start > end):
    xpt_utils.handle_error("Parameters must follow this order : start(" + str(start) + ") <= end (" + str(end) + ") < size (" + str(vector_size) + ") !\n")

  vec_2_comp  = int_to_2_complement(vector, vector_size)
  str_end     = vector_size - 1 - end
  str_start   = vector_size - start
  bin_vector = eval('"{:0' + str(vector_size) + 'b}".format(vec_2_comp)[str_end:str_start]')
  return int(bin_vector, 2)
