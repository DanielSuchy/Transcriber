from Alphabet import Alphabet
from Segment import Segment

class Transcriber(object):

  def __init__(self, text):
    self.alphabet = Alphabet()
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
    i = 0
    word_length = len(word)
    get_next_letter = lambda next_letter: word[i+1] if i < word_length - 1 else ' ' #return ' ' not OutOfRange
    
    while i < word_length:
      letter = word[i]
      next_letter = get_next_letter(i)
      next_assimilation = self.get_last_consonant(word, i)
      new_word += self.transcribe_letter(letter, next_letter, next_assimilation)

      if letter == 'c' and next_letter == 'h':
        i += 1 # grapheme 'ch' defaults to 'x'

      i += 1

    return new_word

  def transcribe_letter(self, letter, next_letter, next_assimilation):
    if letter == 'c' and next_letter == 'h':
        segment = 'x'
    elif letter in self.alphabet.Segments:
      segment = self.alphabet.get_phonetic_representation(letter)
      segment = self.apply_assimilation(segment, next_letter, next_assimilation)
    else:
      segment = letter

    return segment

  def apply_assimilation(self, letter, next_letter, next_assimilation):
    letter = self.apply_place_assimilation(letter, next_letter)
    letter = self.apply_voicing_assimilation(letter, next_assimilation)
    return letter

  def apply_place_assimilation(self, letter, next_letter):
    next_segment = self.alphabet.get_phonetic_description(next_letter)

    if letter == 'n' and next_segment.place == 'velar':
      letter = 'ŋ'
    elif letter == 'm' and next_segment.place == 'labiodental':
      letter = 'ɱ'

    return letter

  def apply_voicing_assimilation(self, letter, next_letter):
    current_segment = self.alphabet.get_phonetic_description(letter)

    if next_letter == ' ' and current_segment.is_obstruent == True:
      new_segment = Segment(current_segment.is_consonant, False, current_segment.place, current_segment.manner, '', '', False, False)
      letter = self.alphabet.get_symbol_by_phoneme(new_segment)
      return letter
      
    next_segment = self.alphabet.get_phonetic_description(next_letter)

    if (current_segment.is_obstruent == True
        and next_segment.is_consonant == True
        and next_segment.is_obstruent == True
       ):
      new_segment = Segment(current_segment.is_consonant, next_segment.is_voiced, current_segment.place, current_segment.manner, '','',False, False)
      letter = self.alphabet.get_symbol_by_phoneme(new_segment)
    return letter

  def get_last_consonant(self, word, i):
    for i in range(i, len(word)+1):
      next_letter = word[i]
      next_segment = self.alphabet.get_phonetic_description(next_letter)
      if next_segment.is_obstruent == False:
        return word[i-1]
      elif (i == len(word) - 1):
        return ' '

    raise(Exception("SegmentNotFound"))
    
  def __str__(self):
    return self.transcription

if __name__ == '__main__':

  transcriber = Transcriber('')
  # transcriber.get_next_assimilation('ch', 0)
  # transcriber.get_next_assimilation('pes', 0)
  # t = transcriber.apply_voicing_assimilation('d', 'k')
  # print(t)

  # t = transcriber.apply_voicing_assimilation('k', 'r')
  # print(t)

  # t = transcriber.apply_voicing_assimilation('z', 'k')
  # print(t)

  # t = Transcriber('věštba')
  # print(str(t))

  # transcriber = Transcriber('blb')
  # print(transcriber)

