import os

class Importer:
    def __init__(self, file, text):
        self.file = file
        self.text = text

    def run(self):
        path = os.path.dirname(self.file.name)
        lines = self.text.split('\n')

        for i, line in enumerate(lines):
            if '#import ' in line:
                importSplit = line.split(' ')
                importFile = importSplit[1].replace('\'', '') + '.owpy'
                f = open(os.path.join(path, importFile))
                importText = f.read()
                importer = self.__class__(f, importText)
                lines[i] = importer.run()

        return '\n'.join(lines)