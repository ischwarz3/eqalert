from dataclasses import dataclass
from logging import Logger
import os


@dataclass
class SpellTimerJSON:
    spells: dict
    hash: str
    version: str


class SpellParserSaveFileNotFound(Exception):
    def __init__(self, save_file, message="Could not find existing spell file to parse"):
            self.save_file = save_file
            self.message = message
            super().__init__(self.message)


class SpellParserEQSpellFileNotFound(Exception):
    def __init__(self, save_file, message="Could not find EQ spell file to parse"):
            self.save_file = save_file
            self.message = message
            super().__init__(self.message)


class SpellParser:
    logger: Logger
    save_file: str
    eq_spell_file: str
    version: str
    hash: str
    spell_timer: SpellTimerJSON

    def __init__(self, logger: Logger, save_file:str, eq_spell_file:str) -> None:
        self.logger = logger
        self._read_save_file(save_file)

        self.eq_spell_file = eq_spell_file
        self._validate_eq_spell_file()

    def _read_save_file(self, save_file: str) -> None:
        self.save_file = save_file
        self._validate_save_file()

    def _validate_save_file(self):
        if self.save_file is None or not os.path.exists(self.save_file):
            raise SpellParserSaveFileNotFound(self.save_file)
        
    def _validate_eq_spell_file(self):
        if self.eq_spell_file is None or not os.path.exists(self.eq_spell_file):
            raise SpellParserEQSpellFileNotFound(self.eq_spell_file)