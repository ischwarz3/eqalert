import logging
from unittest.mock import patch
import pytest

from eqa.lib.parsers.spell import SpellParser, SpellParserSaveFileNotFound, SpellParserEQSpellFileNotFound

def test_read_spell_file_invalid():
    logger = logging.getLogger()

    save_file = None
    eq_spell_file = "/invalid/eq_spell_file"

    with pytest.raises(SpellParserSaveFileNotFound):
        _ = SpellParser(logger=logger, save_file=save_file, eq_spell_file=eq_spell_file)

def test_read_spell_file_not_found(mocker):
    mock_exists = mocker.patch('os.path.exists')
    mock_exists.return_value = False

    logger = logging.getLogger()

    save_file = "/file/does/not/exist"
    eq_spell_file = "/file/exists"

    with pytest.raises(SpellParserSaveFileNotFound):
        _ = SpellParser(logger=logger, save_file=save_file, eq_spell_file=eq_spell_file)

    mock_exists.assert_called_once_with(save_file)

def test_read_spell_file_found(mocker):
    mock_exists = mocker.patch('os.path.exists')
    mock_exists.return_value = True

    logger = logging.getLogger()

    expected_save_file = "/file/exists"
    eq_spell_file = "/file/exists"
    with patch.object(SpellParser, "_validate_eq_spell_file", lambda s: None):
        spell_parser = SpellParser(logger=logger, save_file=expected_save_file, eq_spell_file=eq_spell_file)
    
    mock_exists.assert_called_once_with(expected_save_file)
    assert spell_parser.save_file == expected_save_file

def test_read_eq_spell_file_not_found(mocker):
    mock_exists = mocker.patch('os.path.exists')
    mock_exists.return_value = False

    logger = logging.getLogger()

    expected_save_file = "/file/exists"
    eq_spell_file = "/invalid/eq_spell_file"
    with patch.object(SpellParser, "_validate_save_file", lambda s: None):
        with pytest.raises(SpellParserEQSpellFileNotFound):
            _ = SpellParser(logger=logger, save_file=expected_save_file, eq_spell_file=eq_spell_file)

def test_read_eq_spell_file_found(mocker):
    mock_exists = mocker.patch('os.path.exists')
    mock_exists.return_value = True

    logger = logging.getLogger()

    expected_save_file = "/file/exists"
    eq_spell_file = "/invalid/eq_spell_file"
    with patch.object(SpellParser, "_validate_save_file", lambda s: None):
        spell_parser = SpellParser(logger=logger, save_file=expected_save_file, eq_spell_file=eq_spell_file)
        
        mock_exists.assert_called_once_with(eq_spell_file)
        assert spell_parser.eq_spell_file == eq_spell_file
    