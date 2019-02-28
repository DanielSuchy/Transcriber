class Vocal(object):

  possible_height = ['close', 'near-close', 'close-mid', 'mid', 'open-mid', 'near-open', 'open']
  possible_backness = ['front', 'central', 'back']
  def __init__(self, is_voiced, vowel_height, vowel_backness, is_rounded, is_long):
    self.is_voiced = bool(is_voiced)
    self.backness = self.get_backness(vowel_backness)
    self.height = self.get_height(vowel_height)
    self.is_long = is_long
    self.is_rounded = is_rounded

  def get_backness(self, vowel_backness):
    if vowel_backness in self.possible_backness:
      return vowel_backness
    else:
      raise(Exception('IncorrectBackness'))

  def get_height(self, vowel_height):
    if vowel_height in  self.possible_height:
      return vowel_height
    else:
      raise(Exception('IncorrectHeight'))