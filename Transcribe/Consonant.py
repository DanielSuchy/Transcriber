class Consonant(object):

  possible_place = ['bilabial', 'labiodental', 'dental', 'alveolar', 'postalveolar', 'retroflex', 'palatal', 'velar', 'uvular', 'pharyngeal', 'glottal']
  possible_manner = ['stop', 'fricative', 'africate', 'tap', 'flap', 'tap/flap', 'aproximant', 'nasal', 'trill']
  def __init__(self, is_voiced, place, manner):
    self.place = self.get_place(place)
    self.manner = self.get_manner(manner)

    if self.manner in ['stop', 'fricative', 'africate']:
      self.is_obstruent = True
    else:
      self.is_obstruent = False

    self.is_voiced = self.get_voicing(is_voiced) 


  def get_place(self, place):
    if place in self.possible_place:
      return place
    else:
      raise(Exception('IncorrectPlace'))

  def get_manner(self, manner):
    if manner == 'tap' or manner == 'flap':
      return 'tap/flap'
    elif manner in self.possible_manner:
      return manner
    else:
      raise(Exception('IncorrectManner'))

  def get_voicing(self, is_voiced):
    if is_voiced == False and self.is_obstruent == False:
      #only obstruents can be voiceless
      raise(Exception('IncorrectVoicing'))
    else:
      return is_voiced