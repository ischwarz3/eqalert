import logging
from pathlib import Path

import pytest
from eqa.lib.config import (
    combine_config_files,
    generate_spell_timer_json,
    SpellTimerJSON,
    SpellTimer,
    read_config_file,
    read_config_files,
    read_line_alert_files,
)
from eqa.lib.struct import config_file, configs
from eqa.lib.util import JSONFileHandler
from eqa.const.validspells import VALID_SPELLS
from eqa.models.config import (
    CharacterState,
    Characters,
    CharacterLog,
    EncounterParsing,
    LastState,
    LocalTTS,
    MobTimer,
    PlayerData,
    RaidMode,
    SettingData,
    Settings,
    Speech,
    SpellTimerConfig,
    SpellTimerFilter,
    SystemPaths,
    Timers,
    Zone,
    Zones,
)
from eqa.models.util import BaseFlag, Location

sample_spell_lines = [
    "0^^BLUE_TRAIL^^^^^^^0^0^0^0^0^0^0^7^65^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^-1^-1^-1^-1^1^1^1^1^-1^-1^-1^-1^100^100^100^100^100^100^100^100^100^100^100^100^0^0^0^0^254^254^254^254^254^254^254^254^254^254^254^254^2^0^52^-1^0^0^255^255^255^255^255^255^255^255^255^255^255^255^255^255^255^255^44^13^0^-1^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^100^0^161^0^0^-150^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^100^0^0^0^0^0^0^0^0^0^0^0^0^0^-150^100^-150^-99^7^65^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^1^0^0^0^0^0^0^-1^0^0^0^1^0^0^1^1^^0",
    "3^Summon Corpse^PLAYER_1^^^^^^^10000^0^0^0^5000^2250^12000^0^0^0^700^70^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^2512^2106^17355^-1^-1^-1^1^1^1^1^-1^-1^-1^-1^100^100^100^100^100^100^100^100^100^100^100^100^0^1^0^0^91^254^254^254^254^254^254^254^254^254^254^254^6^20^14^-1^0^0^255^255^255^255^255^255^255^255^255^255^39^255^255^255^255^255^43^0^0^4^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^100^0^35^83^0^0^0^0^0^0^0^0^0^0^0^64^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^5^101^49^52^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^1^0^0^0^0^0^-1^0^0^0^1^0^0^1^1^!Expansion:Jan2001^8478",
    "4^Summon Waterstone^PLAYER_1^^^^^^^0^0^0^0^4000^2250^2250^0^0^0^40^10342^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^2512^2106^-1^-1^-1^-1^1^1^1^1^-1^-1^-1^-1^109^100^100^100^100^100^100^100^100^100^100^100^0^1^0^0^32^254^254^254^254^254^254^254^254^254^254^254^6^25^14^-1^0^0^255^255^255^255^255^255^255^255^255^255^255^255^20^255^255^255^43^0^0^4^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^100^0^35^83^0^0^0^0^0^0^0^0^0^0^0^109^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^5^101^20^61^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^1^0^0^0^0^0^-1^0^0^0^1^0^0^1^1^^0",
    "5^Cloak^PLAYER_1^^^^^ shimmers.^^100^0^0^0^5000^2250^0^3^200^0^50^1^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^2502^2115^-1^-1^-1^-1^1^1^1^1^-1^-1^-1^-1^100^100^100^100^100^100^100^100^100^100^100^100^0^1^0^0^90^254^254^254^254^254^254^254^254^254^254^254^14^25^18^-1^0^0^255^255^255^255^255^255^255^255^255^255^255^255^255^255^255^255^42^0^0^9^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^100^0^138^95^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^100^0^-99^3^200^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^1^1^0^0^0^0^0^-1^0^0^0^1^0^0^1^1^^0",
    "6^Ignite Blood^PLAYER_1^^^^Your blood ignites.^'s blood ignites.^Your blood cools.^200^0^0^0^4000^2500^2250^1^21^0^250^-56^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^2503^2119^-1^-1^-1^-1^1^1^1^1^-1^-1^-1^-1^100^100^100^100^100^100^100^100^100^100^100^100^0^0^0^2^0^254^254^254^254^254^254^254^254^254^254^254^5^25^5^-1^0^0^255^255^255^255^255^255^255^255^255^255^49^255^255^255^255^255^44^13^0^20^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^100^0^142^89^0^-100^0^0^0^0^0^0^0^0^0^38^0^0^-1^-1^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^-12^133^-157^129^1^21^0^0^0^0^2^106^0^0^0^0^0^0^0^0^0^0^1^0^0^0^0^0^0^-1^0^0^0^1^0^0^1^1^^0",
    "7^Hymn of Restoration^PLAYER_1^^^^Your wounds begin to heal.^^^0^30^0^0^3000^0^0^5^3^0^0^1^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^2510^2007^-1^-1^-1^-1^1^1^1^1^-1^-1^-1^-1^110^100^100^100^100^100^100^100^100^100^100^100^0^1^0^0^0^254^254^254^254^254^254^254^254^254^254^254^41^15^49^-1^0^0^255^255^255^255^255^255^255^6^255^255^255^255^255^255^255^255^40^0^0^6^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^67^1^0^0^0^0^0^0^0^0^0^0^0^43^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^5^101^13^25^5^3^0^0^1^0^0^0^0^0^0^0^0^0^0^0^0^0^0^1^0^0^0^0^0^-1^0^0^0^1^0^0^1^1^^0",
    "8^Cleanse^PLAYER_1^^^^You feel cleansed.^^^0^0^0^0^0^0^0^0^0^0^0^-1^-1^5^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^2510^2051^-1^-1^-1^-1^1^1^1^1^-1^-1^-1^-1^100^100^100^100^100^100^100^100^100^100^100^100^0^1^0^0^36^35^0^254^254^254^254^254^254^254^254^254^6^0^5^-1^0^0^255^255^255^255^255^255^255^255^255^255^255^255^255^255^255^255^43^0^0^50^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^100^0^25^97^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^100^0^-99^0^0^0^0^0^1^0^0^0^0^0^0^0^0^0^0^0^0^0^1^0^0^0^0^0^-1^0^0^0^1^0^0^1^1^^0",
    "9^Superior Healing^PLAYER_1^^^^You feel much better.^ feels much better.^^100^0^0^0^4500^2500^2250^0^0^0^250^463^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^583^0^0^0^0^0^0^0^0^0^0^0^2510^2051^-1^-1^-1^-1^1^1^1^1^-1^-1^-1^-1^104^100^100^100^100^100^100^100^100^100^100^100^0^1^0^0^0^254^254^254^254^254^254^254^254^254^254^254^5^25^5^-1^0^0^255^34^57^255^255^53^255^255^255^53^255^255^255^255^255^255^43^0^0^1^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^100^0^131^73^0^0^0^0^0^0^0^0^0^0^0^42^0^0^0^0^0^100^0^0^0^0^0^0^0^0^0^0^0^0^0^5^101^47^20^0^0^0^0^0^0^5^583^0^0^0^0^0^0^0^0^0^0^0^1^0^0^0^0^0^-1^0^0^0^1^0^0^1^1^!Expansion:Feb2001^8631",
    "10^Augmentation^PLAYER_1^^^^You feel your body pulse with energy.^'s body pulses with energy.^The pulsing energy fades.^100^0^0^0^5000^2250^2250^3^270^0^90^115^5^5^-2^1^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^128^30^30^0^100^0^0^0^0^0^0^0^2518^2124^-1^-1^-1^-1^1^1^1^1^-1^-1^-1^-1^109^101^101^100^203^100^100^100^100^100^100^100^0^1^0^0^11^6^1^24^148^254^254^254^254^254^254^254^5^25^5^-1^0^0^255^255^255^255^255^255^255^255^255^255^255^255^255^29^255^255^43^0^0^7^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^100^0^132^88^0^0^0^0^0^0^0^0^0^0^0^41^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^5^101^24^202^3^270^0^0^0^0^3^230^0^0^0^0^0^0^0^0^0^0^1^1^0^0^0^0^0^-1^0^0^0^1^0^0^1^1^^0",
]


def test_generate_spell_timer_json():
    sample_hash = "abcd1234"
    valid_spells = VALID_SPELLS
    version = "1.0"
    spells = {
        "augmentation": SpellTimer("5.0", "270", "3"),
        "hymn_of_restoration": SpellTimer("3.0", "3", "5"),
        "ignite_blood": SpellTimer("4.0", "21", "1"),
    }
    expected = SpellTimerJSON(hash=sample_hash, version=version, spells=spells)

    actual = generate_spell_timer_json(
        sample_hash, sample_spell_lines, valid_spells, version
    )

    # Compare the parent classes (does not check the spells)
    assert expected == actual

    # Compare that all the expected spells are present
    assert sorted(expected.spells.keys()) == sorted(actual.spells.keys())


def test_read_config_files():

    read_result = '{ "foo": { "bar": "baz" }}'

    class TestJSONFileHandler(JSONFileHandler):
        def read(self):
            # Short circuiting the file read operation
            return self.deserialize(read_result)

    test_file_path = Path("whatever")

    expected = {
        "test_valid": config_file(
            "test_valid", "whatever/test_valid.json", {"foo": {"bar": "baz"}}
        )
    }
    actual = read_config_files(test_file_path, TestJSONFileHandler)

    assert actual == expected


character_file_contents = r"""{
  "char_logs": {
    "SOANDSO_P1999Green": {
      "char": "SOANDSO",
      "char_state": {
        "bind": "Lake of Ill Omen",
        "class": "Druid",
        "direction": "East",
        "encumbered": false,
        "guild": null,
        "level": 60,
        "location": {
          "x": -2554.12,
          "y": 1947.01,
          "z": -6.19
        },
        "zone": "Everfrost"
      },
      "character": "SOANDSO",
      "disabled": false,
      "file_name": "eqlog_SOANDSO_P1999Green.txt",
      "server": "P1999Green"
    },
    "FULANO_P1999Green": {
      "char": "FULANO",
      "char_state": {
        "bind": null,
        "class": "Necromancer",
        "direction": "North",
        "encumbered": false,
        "guild": "Redacted",
        "level": 1,
        "location": {
          "x": 0.0,
          "y": 0.0,
          "z": 0.0
        },
        "zone": "Kurn's Tower"
      },
      "character": "FULANO",
      "disabled": false,
      "file_name": "eqlog_FULANO_P1999Green.txt",
      "server": "P1999Green"
    }
  },
  "version": "3.7.2"
}
"""
character_file_parsed = Characters(
    **{
        "char_logs": {
            "SOANDSO_P1999Green": CharacterLog(
                **{
                    "char": "SOANDSO",
                    "char_state": CharacterState(
                        **{
                            "bind": "Lake of Ill Omen",
                            "class": "Druid",
                            "direction": "East",
                            "encumbered": False,
                            "guild": None,
                            "level": 60,
                            "location": Location(
                                **{"x": -2554.12, "y": 1947.01, "z": -6.19}
                            ),
                            "zone": "Everfrost",
                        }
                    ),
                    "character": "SOANDSO",
                    "disabled": False,
                    "file_name": "eqlog_SOANDSO_P1999Green.txt",
                    "server": "P1999Green",
                }
            ),
            "FULANO_P1999Green": CharacterLog(
                **{
                    "char": "FULANO",
                    "char_state": CharacterState(
                        **{
                            "bind": None,
                            "class": "Necromancer",
                            "direction": "North",
                            "encumbered": False,
                            "guild": "Redacted",
                            "level": 1,
                            "location": Location(**{"x": 0.0, "y": 0.0, "z": 0.0}),
                            "zone": "Kurn's Tower",
                        }
                    ),
                    "character": "FULANO",
                    "disabled": False,
                    "file_name": "eqlog_FULANO_P1999Green.txt",
                    "server": "P1999Green",
                }
            ),
        }
    }
)
settings_file_contents = r"""{
  "last_state": {
    "afk": false,
    "character": "FULANO",
    "group": false,
    "leader": false,
    "raid": false,
    "server": "P1999Green"
  },
  "settings": {
    "character_mention_alert": {
      "enabled": true
    },
    "consider_eval": {
      "enabled": true
    },
    "debug_mode": {
      "enabled": false
    },
    "detect_character": {
      "enabled": true
    },
    "encounter_parsing": {
      "allow_player_target": false,
      "auto_save": false,
      "enabled": true
    },
    "mute": {
      "enabled": false
    },
    "paths": {
      "data": "/home/somedude/.eqa/data/",
      "eqalert_log": "/home/somedude/.eqa/log/",
      "everquest_files": "/home/somedude/.wine/drive_c/Program Files/Sony/EverQuest/",
      "everquest_logs": "/home/somedude/.wine/drive_c/Program Files/Sony/EverQuest/Logs/",
      "sound": "/home/somedude/.eqa/sound/",
      "tmp_sound": "/tmp/eqa/sound/"
    },
    "player_data": {
      "persist": true
    },
    "raid_mode": {
      "auto_set": true
    },
    "speech": {
      "expand_lingo": true,
      "gtts_lang": "en",
      "gtts_tld": "com",
      "local_tts": {
        "enabled": false,
        "model": "tts_models/en/ljspeech/tacotron2-DDC_ph"
      }
    },
    "timers": {
      "mob": {
        "auto": true,
        "auto_delay": 10
      },
      "spell": {
        "consolidate": true,
        "delay": 24,
        "filter": {
          "by_list": false,
          "filter_list": {
            "spirit_of_wolf": false
          },
          "guild_only": false,
          "yours_only": false
        },
        "guess": false,
        "other": true,
        "self": true,
        "zone_drift": true
      }
    }
  },
  "version": "3.7.2"
}"""
settings_file_parsed = Settings(
    **{
        "last_state": LastState(
            **{
                "afk": False,
                "character": "FULANO",
                "group": False,
                "leader": False,
                "raid": False,
                "server": "P1999Green",
            }
        ),
        "settings": SettingData(
            **{
                "character_mention_alert": BaseFlag(**{"enabled": True}),
                "consider_eval": BaseFlag(**{"enabled": True}),
                "debug_mode": BaseFlag(**{"enabled": False}),
                "detect_character": BaseFlag(**{"enabled": True}),
                "encounter_parsing": EncounterParsing(
                    **{
                        "allow_player_target": False,
                        "auto_save": False,
                        "enabled": True,
                    }
                ),
                "mute": BaseFlag(**{"enabled": False}),
                "paths": SystemPaths(
                    **{
                        "data": "/home/somedude/.eqa/data/",
                        "eqalert_log": "/home/somedude/.eqa/log/",
                        "everquest_files": "/home/somedude/.wine/drive_c/Program Files/Sony/EverQuest/",
                        "everquest_logs": "/home/somedude/.wine/drive_c/Program Files/Sony/EverQuest/Logs/",
                        "sound": "/home/somedude/.eqa/sound/",
                        "tmp_sound": "/tmp/eqa/sound/",
                    }
                ),
                "player_data": PlayerData(**{"persist": True}),
                "raid_mode": RaidMode(**{"auto_set": True}),
                "speech": Speech(
                    **{
                        "expand_lingo": True,
                        "gtts_lang": "en",
                        "gtts_tld": "com",
                        "local_tts": LocalTTS(
                            **{
                                "enabled": False,
                                "model": "tts_models/en/ljspeech/tacotron2-DDC_ph",
                            }
                        ),
                    }
                ),
                "timers": Timers(
                    **{
                        "mob": MobTimer(**{"auto": True, "auto_delay": 10}),
                        "spell": SpellTimerConfig(
                            **{
                                "consolidate": True,
                                "delay": 24,
                                "filter": SpellTimerFilter(
                                    **{
                                        "by_list": False,
                                        "filter_list": {"spirit_of_wolf": False},
                                        "guild_only": False,
                                        "yours_only": False,
                                    }
                                ),
                                "guess": False,
                                "other": True,
                                "self": True,
                                "zone_drift": True,
                            }
                        ),
                    }
                ),
            }
        ),
        "version": "3.7.2",
    }
)
zones_file_contents = r"""{
  "zones": {
    "An Arena (PVP) Area": {
      "indoors": false,
      "raid_mode": false,
      "timer": 0
    },
    "Befallen": {
      "indoors": false,
      "raid_mode": false,
      "timer": 1120
    }
  },
  "version": "3.7.2"
}"""
zones_file_parsed = Zones(
    **{
        "zones": {
            "An Arena (PVP) Area": Zone(
                **{"indoors": False, "raid_mode": False, "timer": 0}
            ),
            "Befallen": Zone(**{"indoors": False, "raid_mode": False, "timer": 1120}),
        }
    }
)


@pytest.mark.parametrize(
    "config_type, file_contents, expected",
    [
        (Characters, character_file_contents, character_file_parsed),
        (Zones, zones_file_contents, zones_file_parsed),
        (Settings, settings_file_contents, settings_file_parsed),
    ],
)
def test_read_config_file(config_type, file_contents, expected):
    class TestJSONFileHandler(JSONFileHandler):
        def read(self):
            # Short circuiting the file read operation
            return self.deserialize(file_contents)

    actual = read_config_file(Path("foo"), "whatever", config_type, TestJSONFileHandler)

    assert actual == expected


def test_read_config_file_validation_error(caplog):
    class TestJSONFileHandler(JSONFileHandler):
        def read(self):
            # Short circuiting the file read operation
            return self.deserialize('{ "foo": { "bar": "baz" }}')

    with caplog.at_level(logging.INFO):
        actual = read_config_file(
            Path("foo"), "NoWhammies", Characters, TestJSONFileHandler
        )

    assert actual is None  # Error should get handled by error handler
    assert "NoWhammies" in caplog.text  # Error is registered to the logger


@pytest.mark.parametrize(
    "file_handler_result, expected",
    [
        (
            '{ "line": {"foo": { "bar": "baz" }}}',
            {"line": {"foo": {"bar": "baz"}}, "version": None},
        ),
        (
            '{ "line": {"foo": { "bar": "baz" }}, "version": "1.2.3"}',
            {"line": {"foo": {"bar": "baz"}}, "version": "1.2.3"},
        ),
    ],
)
def test_read_line_alert_files(file_handler_result, expected):

    class TestJSONFileHandler(JSONFileHandler):
        def read(self):
            # Short circuiting the file read operation
            return self.deserialize(file_handler_result)

    test_file_path = Path("whatever")
    test_config_files = ["test_valid"]

    actual = read_line_alert_files(
        test_file_path, test_config_files, TestJSONFileHandler
    )

    assert actual == expected


def test_combine_config_files():

    configs_data = {
        "characters": config_file(
            "characters", "whatever/characters.json", {"foo": {"bar": "baz"}}
        ),
        "settings": config_file(
            "settings", "whatever/characters.json", {"foo": {"bar": "baz"}}
        ),
        "zones": config_file(
            "zones", "whatever/characters.json", {"foo": {"bar": "baz"}}
        ),
    }

    line_alerts = {"line": {"foo": {"bar": "baz"}}, "version": "1.2.3"}
    line_alerts_config = config_file(
        "line-alerts",
        None,
        line_alerts,
    )

    expected = configs(
        configs_data["characters"],
        configs_data["settings"],
        configs_data["zones"],
        line_alerts_config,
    )

    actual = combine_config_files(configs_data, line_alerts)

    assert actual == expected
