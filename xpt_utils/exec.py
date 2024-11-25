import os

import xpt_utils

def exec_cmd(cmd, type="MISC", print_enable=False, file_path=None):
  xpt_utils.format_log(cmd, type, print_enable, file_path)
  ret_val = os.system(cmd)
  if (ret_val != 0):
    xpt_utils.handle_error(f"Execution of this command terminate with an error :\n{cmd}\n")
