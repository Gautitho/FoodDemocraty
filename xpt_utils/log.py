import xpt_utils

# Change these values in your application main
DISPLAYED_LOG_TYPE = ["MISC", "INFO_BLUE", "SUCCESS", "INFO", "DEBUG", "WARNING", "ERROR"] # Not displayed : []
LOG_DIR = "."

def to_string(obj, separator=" "):
  if (type(obj) is list):
    s = ""
    for elem in obj:
      s += to_string(elem) + separator
    s = s[:-len(separator)]
  elif (type(obj) is dict):
    s = ""
    for key in list(obj.keys()):
      s += str(key) + " : " + to_string(obj[key]) + separator
    s = s[:-len(separator)]
  else:
    s = str(obj)
  return s

def format_log(msg, type="MISC", print_enable=True, file_path=None, write_mode="a", format="LIGHT"):
  if (type in xpt_utils.DISPLAYED_LOG_TYPE):
    if (type == "ERROR"):
      s = '\033[31m' + "ERROR: " + str(msg) + '\033[0m'
    elif (type == "WARNING"):
      s = '\033[36m' + "WARNING: " + str(msg) + '\033[0m'
    elif (type == "INFO_BLUE"):
      s = '\033[34m' + "INFO: " + str(msg) + '\033[0m'
    elif (type == "SUCCESS"):
      s = '\033[32m' + "INFO: " + str(msg) + '\033[0m'
    elif (type == "INFO"):
      s = "INFO: " + str(msg)
    else:
      s = str(msg)

    if (print_enable):
      print(s)

    if (file_path != None):
      fd = open(xpt_utils.LOG_DIR + "/" + file_path, write_mode)
      fd.write(s + "\n")
      fd.close()

    return s

  else:
    return ""
