import time
import unittest

from eqa.lib.parser import check_melee, determine


class TestCheckMelee(unittest.TestCase):
    def setUp(self):
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print('%s: %.5f' % (self.id(), t))

    def testCheckMeleeMin(self):
        text = "Soanso hits you for 10 points of damage."
        assert check_melee(text) == "combat_you_receive_melee"

    def testCheckMeleeMax(self):
        text = "A glimmering drake kicks you."
        assert check_melee(text) == "combat_ranger_drake"

    def testCheckMeleeNotFound(self):
        text = "ffffff"
        assert check_melee(text) is None 

    def testDetermineFail(self):
        text = "ffffff"
        assert determine(text) == "undetermined"

    def testDetermineQuickMelee(self):
        text = "Soanso hits you for 10 points of damage."
        assert determine(text) == "combat_you_receive_melee"
    
    def testDetermineSlowMelee(self):
        text = "A glimmering drake kicks you."
        assert determine(text) == "combat_ranger_drake"

