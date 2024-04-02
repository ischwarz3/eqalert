from pathlib import Path
from typing import Dict, Optional

from pydantic import BaseModel

from eqa.models.util import BaseFlag, Location


class CharacterState(BaseModel):
    bind: str | None
    char_class: str | None
    direction: str | None
    encumbered: bool
    guild: str | None
    level: int | None
    location: Location
    zone: str | None


class CharacterLog(BaseModel):
    char: str
    char_state: CharacterState
    character: str
    disabled: bool
    filename: str
    server: str


class Characters(BaseModel):
    character_logs: Optional[Dict[str, CharacterLog]]


class LastState(BaseModel):
    afk: bool
    character: str
    group: bool
    leader: bool
    raid: bool
    server: str


class EncounterParsing(BaseFlag):
    allow_player_target: bool
    auto_save: bool


class SystemPaths(BaseModel):
    data: str | Path
    eqalert_log: str | Path
    everquest_files: str | Path
    everquest_logs: str | Path
    sound: str | Path
    tmp_sound: str | Path


class PlayerData(BaseModel):
    persist: bool


class RaidMode(BaseModel):
    auto_set: bool


class LocalTTS(BaseFlag):
    model: str


class Speech(BaseModel):
    expand_lingo: bool
    gtts_lang: str
    gtts_tld: str
    local_tts: LocalTTS


class MobTimer(BaseModel):
    auto: bool
    auto_delay: int


class SpellTimerFilter(BaseModel):
    by_list: bool
    guild_only: bool
    yours_only: bool
    filter_list: Optional[Dict[str, BaseFlag]]


class SpellTimer(BaseModel):
    """Generic Spell Timer data to config the behavior of the Spell Timer in EQA"""

    consolidate: bool
    delay: int
    spell_timer_filter: SpellTimerFilter
    guess: bool
    other: bool
    self: bool
    zone_drift: bool


class Timers(BaseModel):
    mob: MobTimer
    spell: SpellTimer


class SettingData(BaseModel):
    character_mention_alert: BaseFlag
    consider_eval: BaseFlag
    debug_mode: BaseFlag
    detect_character: BaseFlag
    encounter_parsing: EncounterParsing
    mute: BaseFlag
    paths: SystemPaths
    player_data: PlayerData
    raid_mode: RaidMode
    speech: Speech
    timers: Timers


class Settings(BaseModel):
    last_state: LastState
    settings: SettingData
    version: str


class Zone(BaseModel):
    indoors: bool
    raid_mode: bool
    timer: int


class Zones(BaseModel):
    zones: Optional[Dict[str, Zone]]


class LineAlert(BaseModel):
    reaction: str
    sound: bool
    alert: Optional[Dict[str, str]]


class LineAlerts(BaseModel):
    line: Optional[Dict[str, LineAlert]]


class LineAlertFile(BaseModel):
    line_alert: LineAlerts


class Config(BaseModel):
    characters: Optional[Characters]
    settings: Optional[Settings]
    zones: Optional[Zones]
    line_alerts: Optional[Dict[str, LineAlertFile]]
