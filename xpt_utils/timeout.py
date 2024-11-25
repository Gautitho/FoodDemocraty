import signal

def alarm_handler(signum, frame):
  raise TimeoutExpired

def input_with_timeout(prompt, timeout):
  signal.signal(signal.SIGALRM, alarm_handler)
  signal.alarm(timeout)

  try:
    input(prompt)
  except:
    pass
  finally:
    signal.alarm(0) # cancel alarm
