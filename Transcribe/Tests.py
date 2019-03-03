import unittest
from os import listdir, path
from FileIO import FileIO
from Text import Text
from Segment import Segment
from Transcriber import Transcriber
from Alphabet import Alphabet

class TestFileIO(unittest.TestCase):

  def test_current_directory(self):
    file_IO = FileIO()
    self.assertEqual(file_IO.current_directory, 'C:\\Users\\user1\\py\\Transcribe')

  def test_relevant_files(self):
    file_IO = FileIO()
    for file in file_IO.relevant_files:
      self.assertTrue('.docx' in file or '.txt' in file)

  def test_new_names(self):
    file_IO = FileIO()
    current_directory = path.dirname(path.realpath(__file__))
    files_in_dir = listdir(current_directory)
    if 'Documentation.txt' in file_IO.relevant_files:
      self.assertTrue('Documentation_transcribed.txt' in files_in_dir)

    if 'Documentation.docx' in file_IO.relevant_files:
      self.assertTrue('Documentation_transcribed.docx' in files_in_dir)

  # def test_translate_single_file(self):
  #   file_IO = FileIO(translate_single_file=True)
  #   if 'C:\\Users\\user1\\py\\Transcribe\\tests\\test1.txt' in file_IO.relevant_files:
  #     files_in_dir = listdir('C:\\Users\\user1\\py\\Transcribe\\tests')
  #     self.assertTrue('test1_transcribed.txt' in files_in_dir)
      
class TestText(unittest.TestCase):

  def test_equal_files(self):
    # assert equal files???
    text = Text('C:\\Users\\user1\\py\\Transcribe\\tests\\test1.txt')
    file = open('C:\\Users\\user1\\py\\Transcribe\\tests\\test1.txt', 'r',encoding='utf8')
    file.close()

  def test_file_to_words(self):
    text = Text('C:\\Users\\user1\\py\\Transcribe\\tests\\test1.txt')
    text.file_to_words()

class TestSegment(unittest.TestCase):

  def test_create_segment(self):
    segment = Segment(True, False, 'bilabial', 'stop', '', '', False, False)
    self.assertEqual(segment.is_consonant, True)
    self.assertEqual(segment.is_voiced, False)
    self.assertEqual(segment.place, 'bilabial')
    self.assertEqual(segment.manner,  'stop')

    segment = Segment(False, True, '', '', 'close', 'front', False, False)
    self.assertEqual(segment.is_consonant, False)
    self.assertEqual(segment.is_voiced, True)
    self.assertEqual(segment.height, 'close')
    self.assertEqual(segment.backness, 'front')

  def test_rename_segment(self):
    segment = Segment(True, True, 'alveolar', 'tap', '', '', False, False)
    self.assertEqual(segment.manner, 'tap/flap')

    segment = Segment(True, True, 'alveolar', 'flap', '', '', False, False)
    self.assertEqual(segment.manner, 'tap/flap')


  def test_incorrect_segment(self):
    with self.assertRaises(Exception):
      Segment(True, True, 'test', 'stop', '', '', False, False)

    with self.assertRaises(Exception):
      Segment(True, True, 'bilabial', 'test', '', '', False, False)

    with self.assertRaises(Exception):
      Segment(False, True, '', '', 'close', 'test', False, False)

    with self.assertRaises(Exception):
      Segment(False, True, '', '', 'test', 'front', False, False)

class TestAlphabet(unittest.TestCase):

  def test_get_phonetic_representation(self):
    a = Alphabet()
    
    phon = a.get_phonetic_representation('á')
    self.assertEqual(phon, 'aː')

    phon = a.get_phonetic_representation('c')
    self.assertEqual(phon, 't͡s')

  def test_get_phonetic_description(self):
    a = Alphabet()

    test_segment = Segment(True, False, 'velar', 'fricative', '', '', False, False)
    phon = a.get_phonetic_description('ch')
    self.assertEqual(vars(phon), vars(test_segment))

    test_segment = Segment(False, True, '', '', 'open', 'front', False, True)
    phon = a.get_phonetic_description('á')
    self.assertEqual(vars(phon), vars(test_segment))

  def test_get_textual_representation(self):
    a = Alphabet()

    letter = a.get_textual_representation('t͡s')
    self.assertEqual(letter, 'c')

    letter = a.get_textual_representation('aː')
    self.assertEqual(letter, 'á')

  def test_get_symbol_by_phoneme(self):
    a = Alphabet()
    k = a.get_symbol_by_phoneme(Segment(True, False, 'velar', 'stop', '', '', False, False))
    self.assertEqual(k, 'k')

    r = a.get_symbol_by_phoneme(Segment(True, True, 'alveolar', 'trill', '', '', False, False))
    self.assertEqual(r, 'r')

    a_long = a.get_symbol_by_phoneme(Segment(False, True, '','', 'open', 'front', False, True))
    self.assertEqual(a_long, 'aː')

class TestTranscriber(unittest.TestCase):

  def test_simple_words(self):
    t = Transcriber('pes')
    self.assertEqual(str(t), 'pɛs')

    t = Transcriber('čaj')
    self.assertEqual(str(t), 't͡ʃaj')

    t = Transcriber('pes pije')
    self.assertEqual(str(t), 'pɛs pɪjɛ')

    t = Transcriber('pes pije vodu')
    self.assertEqual(str(t), 'pɛs pɪjɛ vodu')

  def test_ch(self):
    t = Transcriber('ch')
    self.assertEqual(str(t), 'x')

    t = Transcriber('hroch chrochtá')
    self.assertEqual(str(t), 'ɦrox xroxtaː')

  def test_apply_place_assimilation(self):
    t = Transcriber('banka')
    velar_n = t.apply_place_assimilation('n', 'k')
    self.assertEqual(velar_n, 'ŋ')
    self.assertEqual(str(t), 'baŋka')

    t = Transcriber('tango')
    velar_n = t.apply_place_assimilation('n', 'g')
    self.assertEqual(velar_n, 'ŋ')
    self.assertEqual(str(t), 'taŋgo')

    t = Transcriber('tramvaj')
    labiodental_m = t.apply_place_assimilation('m', 'v')
    self.assertEqual(labiodental_m, 'ɱ')

  def test_apply_voicing_assimilation_segments(self):
    transcriber = Transcriber('')
    t = transcriber.apply_voicing_assimilation('d', 'k')
    self.assertEqual(t, 't')

    d = transcriber.apply_voicing_assimilation('t', 'g')
    self.assertEqual(d, 'd')

    k = transcriber.apply_voicing_assimilation('k', 'r')
    self.assertEqual('k', k)

    p = transcriber.apply_voicing_assimilation('b', 'k')
    self.assertEqual('p', p)

    p = transcriber.apply_voicing_assimilation('p', 'k')
    self.assertEqual('p', p)

    s = transcriber.apply_voicing_assimilation('z', 'k')
    self.assertEqual('s', s) 

  def test_get_last_consonant(self):
    transcriber = Transcriber('')
    k = transcriber.get_last_consonant('lebka', 2)
    self.assertEqual(k, 'k')

    b = transcriber.get_last_consonant('věždba', 2)
    self.assertEqual(b, 'b')

    p = transcriber.get_last_consonant('prst', 0)
    self.assertEqual(p, 'p')

    k = transcriber.get_last_consonant('odkráčet', 1)
    self.assertEqual(k, 'k')

    h = transcriber.get_last_consonant('typ hlásky', 2)
    self.assertEqual(h, 'h')

  def test_enword_voicing(self):
    transcriber = Transcriber('')
    p = transcriber.apply_voicing_assimilation('b', ' ')
    self.assertEqual(p, 'p')

    transcriber = Transcriber('blb')
    self.assertEqual(str(transcriber), 'blp')

    transcriber = Transcriber('chlup')
    self.assertEqual(str(transcriber), 'xlup')

  def test_apply_voicing_assimilation_words(self):
    transcriber = Transcriber('lebka')
    self.assertEqual(str(transcriber), 'lɛpka')

    transcriber = Transcriber('odkráčet')
    self.assertEqual(str(transcriber), 'otkraːt͡ʃɛt')

    transcriber = Transcriber('rozkrojit')
    self.assertEqual(str(transcriber), 'roskrojɪt')

    transcriber = Transcriber('kdo')
    self.assertEqual(str(transcriber), 'gdo')

    transcriber = Transcriber('sblížit se')
    self.assertEqual(str(transcriber), 'zbliːʒɪt sɛ')

    transcriber = Transcriber('věštba')
    self.assertEqual(str(transcriber), 'vjɛʒdba')

    transcriber = Transcriber('švédský')
    self.assertEqual(str(transcriber),  'ʃvɛːtskiː')

  def test_multiple_word_assimilation(self):
    transcriber = Transcriber('typ hlásky')
    self.assertEqual(str(transcriber), 'tɪb ɦlaːskɪ')

    transcriber = Transcriber('hod kladivem')
    self.assertEqual(str(transcriber), 'ɦot kladɪvɛm')

    transcriber = Transcriber('hod diskem')
    self.assertEqual(str(transcriber), 'ɦod dɪskɛm')

  def test_handle_soft_e(self):
    transcriber = Transcriber('')
    
    vj = transcriber.handle_soft_e('v')
    self.assertEqual('vj', vj)

    mn = transcriber.handle_soft_e('m')
    self.assertEqual('mɲ', mn)

    d = transcriber.handle_soft_e('d')
    self.assertEqual('ɟ', d)

    c = transcriber.handle_soft_e('t')
    self.assertEqual('c', c)

    transcriber = Transcriber('době')
    self.assertEqual(str(transcriber), 'dobjɛ')

    transcriber = Transcriber('kromě')
    self.assertEqual(str(transcriber), 'kromɲɛ')

    transcriber = Transcriber('silně')
    self.assertEqual(str(transcriber), 'sɪlɲɛ')

    transcriber = Transcriber('těmi')
    self.assertEqual(str(transcriber), 'cɛmɪ')

    transcriber = Transcriber('měděně')
    self.assertEqual(str(transcriber), 'mɲɛɟɛɲɛ')

    transcriber = Transcriber('uměnovědě')
    self.assertEqual(str(transcriber), 'umɲɛnovjɛɟɛ')


if __name__ == "__main__":
	unittest.main()