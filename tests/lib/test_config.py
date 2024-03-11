from eqa.lib.config import generate_spell_timer_json, generate_new_spell_timer_json
from eqa.lib.consts import VALID_SPELLS

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
    sample_hash = 'abcd1234'
    valid_spells = VALID_SPELLS

    expected = {
    'hash': 'abcd1234',
    'spells': {
        'augmentation': {
            'cast_time': '5.0',
            'duration': '270',
            'formula': '3',
        },
        'cleanse': {
            'cast_time': '0.0',
            'duration': '0',
            'formula': '0',
        },
        'hymn_of_restoration': {
            'cast_time': '3.0',
            'duration': '3',
            'formula': '5',
        },
        'ignite_blood': {
            'cast_time': '4.0',
            'duration': '21',
            'formula': '1',
        },
        'summon_corpse': {
            'cast_time': '5.0',
            'duration': '0',
            'formula': '0',
        },
        'summon_waterstone': {
            'cast_time': '4.0',
            'duration': '0',
            'formula': '0',
        },
        'superior_healing': {
            'cast_time': '4.5',
            'duration': '0',
            'formula': '0',
        },
    },
}
    actual = generate_spell_timer_json(sample_hash, sample_spell_lines, valid_spells)

    assert expected == actual

def test_generate_new_spell_timer_json():
    generate_spell_timer_file = True
    sample_hash = 'abcd1234'
    valid_spells = VALID_SPELLS
    version = "1.0"

    # Notes: 
    #   duration 0 spells are excluded when run in "new" mode
    #   version key added
    expected = {
    'hash': 'abcd1234',
    'spells': {
        'augmentation': {
            'cast_time': '5.0',
            'duration': '270',
            'formula': '3',
        },
        # 'cleanse': {
        #     'cast_time': '0.0',
        #     'duration': '0',
        #     'formula': '0',
        # },
        'hymn_of_restoration': {
            'cast_time': '3.0',
            'duration': '3',
            'formula': '5',
        },
        'ignite_blood': {
            'cast_time': '4.0',
            'duration': '21',
            'formula': '1',
        },
        # 'summon_corpse': {
        #     'cast_time': '5.0',
        #     'duration': '0',
        #     'formula': '0',
        # },
        # 'summon_waterstone': {
        #     'cast_time': '4.0',
        #     'duration': '0',
        #     'formula': '0',
        # },
        # 'superior_healing': {
        #     'cast_time': '4.5',
        #     'duration': '0',
        #     'formula': '0',
        # },
    },
    'version': '1.0',
}
    actual = generate_new_spell_timer_json(generate_spell_timer_file, sample_hash, sample_spell_lines, valid_spells, version)

    assert expected == actual
