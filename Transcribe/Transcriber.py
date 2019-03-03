from Alphabet import Alphabet
from Segment import Segment

class Transcriber(object):

  def __init__(self, text):
    self.alphabet = Alphabet()
    self.text = text
    self.transcription = ""
    self.transcribe_text(text)

  def transcribe_text(self, text):
    i = 0
    text_length = len(text)
    get_next_letter = lambda next_letter: text[i+1] if i < text_length - 1 else '' #return '' not OutOfRange

    while i < text_length:
      letter = text[i]
      next_letter = get_next_letter(i)
      next_assimilation = self.get_last_consonant(text, i)
      self.transcription += self.transcribe_letter(letter, next_letter, next_assimilation,i)

      if letter == 'c' and next_letter == 'h':
        i += 1 # grapheme 'ch' defaults to 'x'

      i += 1

  def transcribe_letter(self, letter, next_letter, next_assimilation,i):
    if letter == 'c' and next_letter == 'h':
      segment = 'x'
    elif next_letter == 'ě':
      segment = self.handle_soft_e(letter)
    elif (letter == ' ' and next_letter in 'aeiouáéíóúů'):
      segment = ' ʔ'
    elif (i == 0 and letter in 'aeiouáéíóúů'):
      segment = 'ʔ' + letter
    elif next_letter == 'i':
      segment = self.handle_i_palatalization(letter)
    else:
      segment = self.alphabet.get_phonetic_representation(letter)
      segment = self.apply_assimilation(segment, next_letter, next_assimilation)

    if letter == 'o' and next_letter == 'u':
      segment += '͡'

    return segment

  def handle_i_palatalization(self, letter):
    segment = self.alphabet.get_phonetic_representation(letter)
    segment_desc = self.alphabet.get_phonetic_description(letter)

    if segment_desc.place == 'alveolar' and segment_desc.manner in ('stop', 'nasal'):
      new_segment = Segment(segment_desc.is_consonant, segment_desc.is_voiced, 'palatal', segment_desc.manner, '', '', False, False)
      return self.alphabet.get_symbol_by_phoneme(new_segment)

    return segment

  def handle_soft_e(self, letter):
    segment = self.alphabet.get_phonetic_representation(letter)
    segment_desc = self.alphabet.get_phonetic_description(letter)
    
    if segment_desc.place == 'alveolar':
      new_segment = Segment(segment_desc.is_consonant, segment_desc.is_voiced, 'palatal', segment_desc.manner, '', '', False, False)
      return self.alphabet.get_symbol_by_phoneme(new_segment)
    elif segment == 'm':
      segment += 'ɲ'
    else:
      segment += 'j'

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

  def get_last_consonant(self, text, i):
    for i in range(i, len(text)+1):
      next_letter = text[i]
      next_segment = self.alphabet.get_phonetic_description(next_letter)
      if next_segment.is_obstruent == False and next_letter != ' ':
        return text[i-1]
      elif (i == len(text) - 1):
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

  # transcriber = Transcriber('tip hlásky')
  # print(transcriber.get_last_consonant('tip hlásky', 2))
  # print(transcriber)