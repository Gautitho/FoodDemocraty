import sys
import traceback
import xpt_utils

# Change these values in your application main to change handle_error default behavior
ERROR_SEVERITY    = "FATAL"   # Available values : FATAL, EXCEPTION, WARNING, IGNORED
ERROR_PRINT_TRACE = True

def handle_error(msg, severity="DEFAULT", print_trace="DEFAULT", exception_type="DEV"):
  severity    = severity if severity != "DEFAULT" else xpt_utils.ERROR_SEVERITY
  print_trace = print_trace if print_trace != "DEFAULT" else xpt_utils.ERROR_PRINT_TRACE
  if (severity == "FATAL"):
    exit_on_error(msg, print_trace=print_trace)
  elif (severity == "EXCEPTION"):
    except_on_error(msg, print_trace=print_trace, exception_type=exception_type)
  elif (severity == "WARNING"):
    warning_on_error(msg, print_trace=print_trace)
  elif (severity == "IGNORED"):
    pass
  else:
    exit_on_error(f"severity ({severity}) must be in [FATAL, EXCEPTION, WARNING, IGNORED] !")

def exit_on_error(msg, print_trace=True):
  if (print_trace):
    traceback.print_stack(file=sys.stdout)
  xpt_utils.format_log(msg, type="ERROR")
  sys.exit(1)

def except_on_error(msg, print_trace=True, exception_type="DEV"):
  if (print_trace):
    with open("error_trace.log", "w") as f:
      traceback.print_stack(file=f)
  if (exception_type == "USER"):
    raise xpt_utils.UserException(msg)
  else:
    raise xpt_utils.DevException(msg)

def warning_on_error(msg, print_trace=True):
  if (print_trace):
    with open("error_trace.log", "w") as f:
      traceback.print_stack(file=f)
  xpt_utils.format_log(msg, type="WARNING")
