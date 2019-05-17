import signal


class GracefulKiller(object):
  """gracefully shutdown indicator"""
  kill_now = False

  def __init__(self):
    signal.signal(signal.SIGINT, self.exit_gracefully)
    signal.signal(signal.SIGTERM, self.exit_gracefully)

  def exit_gracefully(self, _signum, _frame):
    self.kill_now = True
