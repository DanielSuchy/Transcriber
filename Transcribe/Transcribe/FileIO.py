from os import listdir, path
from shutil import copyfile

class FileIO(object):

  TEXT_FILE = '.txt'
  DOC_FILE = '.docx'
  def __init__(self, translate_single_file=False):
    if translate_single_file == True:
      self.relevant_files = []
      self.relevant_files.append(self.get_file_path())
      self.create_new_files()
    else:
      self.current_directory = path.dirname(path.realpath(__file__))
      self.relevant_files = self.get_relevant_files()
      self.create_new_files()

  def get_file_path(self):
    file_path = input("Vložte cestu k souboru, nebo nechte prazdné pro přeložení souborů v aktuální složce: ")
    
    if path.isfile(file_path):
      return file_path
    elif file_path == "":
      self.current_directory = path.dirname(path.realpath(__file__))
      self.relevant_files = self.get_relevant_files()
      self.create_new_files()
    else:
      print("Soubor nebyl nalezen")
      self.get_file_path()


  def create_new_files(self):
    for file in self.relevant_files:
      if '_transcribed' in file:
        break

      new_file = self.get_new_filename(file)
      copyfile(file, new_file)


  def get_new_filename(self, file):
      dot = file.find('.')
      new_name = file[0:dot] + '_transcribed'

      if self.is_text_file(file):
        new_name += FileIO.TEXT_FILE
      else:
        new_name += FileIO.DOC_FILE

      return new_name

  def get_relevant_files(self):
    files_in_dir = listdir(self.current_directory)
    return [file for file in files_in_dir if self.is_text_file(file) or self.is_doc_file(file)]

  def is_text_file(self, file):
    if FileIO.TEXT_FILE in file:
      return True
    return False

  def is_doc_file(self, file):
    if FileIO.DOC_FILE in file:
      return True
    return False

if __name__ == '__main__':
  file_IO = FileIO(translate_single_file=True)
  input()