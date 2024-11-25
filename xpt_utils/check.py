import xpt_utils

# If condition is not valid : exit on error, raise an exception or print a warning. Else do nothing
def check_condition(condition, msg, severity="DEFAULT", exception_type="DEV"):
  if not(condition):
    xpt_utils.handle_error(msg, severity=severity, exception_type=exception_type)

# If a key is not in the dict : exit on error, raise an exception or print a warning. Else do nothing
def check_key_presence(dic, dic_name, key, severity="DEFAULT", default="", exception_type="DEV"):
  if not(key in dic):
    xpt_utils.handle_error(f"Missing [{key}] in {dic_name} ! Set to the default value ({default}).", severity=severity, exception_type=exception_type)
    dic[key] = default

# Check if args object from argparse python module contains some arguments
def check_args(args, mandatory_arg_list, optionnal_arg_list):
  for arg in mandatory_arg_list:
    if (getattr(args, arg) == None):
      val = input('\033[93m' + f"WARNING: Missing mandatory argument [{arg}] for command [{args.cmd}]. Choose it now : "  + '\033[0m')
      setattr(args, arg, val)
  for arg in optionnal_arg_list:
    if (getattr(args, arg) == None):
      val = xpt_utils.input_with_timeout('\033[93m' + f"WARNING: The optionnal argument [{arg}] for command [{args.cmd}] has not been chosen. Choose it now or skip (Auto skip in 20 seconds) : "  + '\033[0m', 20)
      if (val != "" and val != None):
        setattr(args, arg, val.split())
