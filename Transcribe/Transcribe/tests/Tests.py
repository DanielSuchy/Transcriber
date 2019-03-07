import unittest
from os import listdir, path
from FileIO import FileIO
from Text import Text
from Segment import Segment
from Transcriber import Transcriber

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

class TestTranscriber(unittest.TestCase):

  def test_simple_words(self):
    t = Transcriber('pes')
    self.assertEqual(str(t), 'pɛs')

    t = Transcriber('pes pije')
    self.assertEqual(str(t), 'pɛs pɪjɛ')

    t = Transcriber('pes pije vodu')
    self.assertEqual(str(t), 'pɛs pɪjɛ vodu')

  def test_double_grapheme(self):
    t = Transcriber('hroch')
    self.assertEqual(str(t), 'ɦrox')

if __name__ == "__main__":
	unittest.main()