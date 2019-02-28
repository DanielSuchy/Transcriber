class Transcriber(object):

  Segments = {
    'á': 'aː',
    'e': 'ɛ',
    'é': 'ɛː',
    'ě': 'ɛ',
    'í': 'iː',
    'i': 'ɪ',
    'y': 'ɪ',
    'ý': 'iː',
    'ó': 'oː',
    'ú': 'uː',
    'ů': 'uː',
    'c': 't͡s',
    'č': 't͡ʃ',
    'ď': 'ɟ',
    'h': 'ɦ',
    'ch': 'x',
    'ň': 'ɲ',
    #q
    'ř': 'r̝',
    'š': 'ʃ',
    'ť': 'c',
    'w': 'v',
    'ž': 'ʒ' 
  }

  def __init__(self, text):
    self.text = text
    self.transcription = ""
    self.transcribe_text(text)

  def transcribe_text(self, text):
    words = text.split()
    text_len = len(words)
    i = 0
    for word in words:
      self.transcription += self.transcribe_word(word)
      if i != text_len-1:
        self.transcription += " "

      i+= 1

  def transcribe_word(self, word):
    new_word = ""
    for letter in word:
      elif letter in self.Segments:
        segment = self.Segments[letter]
      else:
        segment = letter

      new_word += segment

    return new_word
    
  def __str__(self):
    return self.transcription