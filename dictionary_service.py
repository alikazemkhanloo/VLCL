import requests
from PyQt6.QtCore import QThread, pyqtSignal

class DictionaryService:
    def __init__(self):
        self.cache = {}

    def normalize(self, entry):
        if not entry:
            return None

        word = entry.get("word", "")

        meanings = entry.get("meanings", [])
        definition = ""

        if meanings:
            defs = meanings[0].get("definitions", [])
            if defs:
                definition = defs[0].get("definition", "")

        phonetics = entry.get("phonetics", [])
        audio = ""

        for p in phonetics:
            if p.get("audio"):
                audio = p["audio"]
                break

        return {
            "word": word,
            "definition": definition,
            "audio": audio
        }
    

    def lookup(self, word):
        if word in self.cache:
            return self.cache[word]

        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        r = requests.get(url, timeout=5)
        print('r',r)
        if r.status_code != 200:
            return {
                'status': 'error',
                'error_code': r.status_code,
            }

        data = r.json()
        normalized_data = self.normalize(data[0])
        print('d', data, normalized_data)
        return {
            'status': 'success',
            'data': normalized_data
        } if data else None
       
        
        

class DictionaryWorker(QThread):
    result = pyqtSignal(object)

    def __init__(self, service, word):
        super().__init__()
        self.service = service
        self.word = word

    def run(self):
        data = self.service.lookup(self.word)
        self.result.emit(data)




