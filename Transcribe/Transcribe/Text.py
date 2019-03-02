class Text(object):

  TEXT_FILE = '.txt'
  DOC_FILE = '.docx'
  def __init__(self, path_to_file):
    self.file = self.extract_text(path_to_file)
    self.words = []
    self.file.close()


  def file_to_words(self):
    return []
    

  def extract_text(self, path_to_file):
    if self.is_doc_file(path_to_file) == True:
      pass # word documents will be implemented later
    else:
      return open(path_to_file, 'r',encoding='utf8')


  def is_doc_file(self, file):
    if Text.DOC_FILE in file:
      return True
    return False