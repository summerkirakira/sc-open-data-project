from pathlib import Path
from typing import Optional

current_dir = Path(__file__).parent

global_path_data = current_dir / 'data' / 'localization'


class Localizer:
    def __init__(self, language='english'):
        self.language = language
        self.path = global_path_data / f'{self.language}.ini'
        self.data = {}
        self.load()

    def load(self):
        with open(self.path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f.readlines():
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.replace(',P', '')
                    self.data[key] = value.strip()

    def get(self, key, default=None) -> str:
        if key.startswith('@'):
            key = key[1:]

        if key in self.data:
            return self.data[key]
        else:
            return default or key


localizer_en = Localizer()
localizer_cn = Localizer('chinese')

if __name__ == '__main__':
    print(localizer_en.get('@ATC_OutpostTerraMills'))



