import sys
from Transcriber import Transcriber

class IOWrapper(object):

  def __init__(self):
    self.text = ""
    self.get_text()
    self.get_transcription()

  def get_transcription(self):
    t = Transcriber(self.text)
    print("\n\nvýsledek transkripce:\n" + str(t))

  def get_text(self):
    self.text = input("Prosím vložte text:\n")

if __name__ == '__main__':
  io = IOWrapper()