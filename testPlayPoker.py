import unittest
import playPoker

#-------------------------------------------------------------------------------
class TestMessageError(unittest.TestCase):
    
    def setUp(self):
        self.message_error = playPoker.MessageError('Test message', False)

    def test_printMessage(self):
        self.assertEqual(self.message_error.printMessage(), 'Test message')
        
    def test_isError(self):
        self.assertFalse(self.message_error.isError())
        
    def test_setMessageErrorError(self):
        self.message_error.setMessageError("new Test", True)
        self.assertTrue(self.message_error.error)

    def test_setMessageErrorMessage(self):
        self.message_error.setMessageError("new Test", True)
        self.assertEqual(self.message_error.message, 'new Test')

    def test_appendMessageErrorError(self):
        self.message_error.appendMessageError("new Test", True)
        self.assertTrue(self.message_error.error)

    def test_appendMessageErrorMessage(self):
        self.message_error.appendMessageError("new Test", True)
        self.assertEqual(self.message_error.message, 'Test message new Test')        

#-------------------------------------------------------------------------------
class TestCard(unittest.TestCase):
    
        
    def test_Correct(self):
        card = playPoker.Card("4h")
        self.assertFalse(card.error)
        
    def test_WrongSuit(self):
        card = playPoker.Card("4f")
        self.assertTrue(card.error)

    def test_WrongFace(self):
        card = playPoker.Card("40h")
        self.assertTrue(card.error)
    
    def test_SmallFormat(self):
        card = playPoker.Card("h")
        self.assertTrue(card.error)

    def test_LargeFormat(self):
        card = playPoker.Card("3412h")
        self.assertTrue(card.error)

#-------------------------------------------------------------------------------
class TestHand(unittest.TestCase):
        

            
    def test_Correct(self):
        hand = playPoker.Hand("AS, 10C, 6d, 5h, kh")
        hand.dealHand()
        self.assertFalse(hand.error)
        
    def test_NotEnough(self):
        hand = playPoker.Hand("10C, 6d, 5h, kh")
        hand.dealHand()
        self.assertTrue(hand.error)
        
    def test_TooMany(self):
        hand = playPoker.Hand("AS, 10C, 6d, 5h, kh, qd")
        hand.dealHand()
        self.assertTrue(hand.error)

    def test_Duplicate(self):
        hand = playPoker.Hand("AS, 10C, 6d, 5h, 5h")
        hand.dealHand()
        self.assertTrue(hand.error)        

    def test_setFaceDictHighcard(self):
        hand = playPoker.Hand("AS, 10C, 6d, 5h, kh")
        hand.dealHand()
        self.assertDictEqual(hand.face_dict, {'a': 1, "10":1, "6":1, "5":1, "k":1})
        
    def test_setSuitDictHighCard(self):
        hand = playPoker.Hand("AS, 10C, 6d, 5h, kh")
        hand.dealHand()
        self.assertDictEqual(hand.suit_dict, {'s': 1, "c":1, "d":1, "h":2})

    def test_setSuitDictFlush(self):
        hand = playPoker.Hand("AS, 10S, 6S, 5S, kS")
        hand.dealHand()
        self.assertDictEqual(hand.suit_dict, {'s': 5})

#-------------------------------------------------------------------------------
class TestRulebook(unittest.TestCase):
    def setUp(self):
        self.rule_book = playPoker.Rulebook()
    
    def test_FiveOfAKind(self):
        hand = playPoker.Hand("5S, 5H, 5D, 5c, **")
        hand.dealHand()
        self.assertEqual(hand.worth(self.rule_book), 'Five of a kind')
    
    def test_StraightFlush(self):
        hand = playPoker.Hand("7S, 8S, 9S, 10S, JS")
        hand.dealHand()
        self.assertEqual(hand.worth(self.rule_book), 'Straight flush')    
        
    def test_FourOfAKind(self):
        hand = playPoker.Hand("7S, 7D, 7C, 7H, JS")
        hand.dealHand()
        self.assertEqual(hand.worth(self.rule_book), 'Four of a kind')

    def test_FullHouse(self):
        hand = playPoker.Hand("7S, 7D, 4C, 4H, 4S")
        hand.dealHand()
        self.assertEqual(hand.worth(self.rule_book), 'Full house')
 
    def test_Flush(self):
        hand = playPoker.Hand("3S, 7S, 9S, AS, 2S")
        hand.dealHand()
        self.assertEqual(hand.worth(self.rule_book), 'Flush')  

    def test_Sraight(self):
        hand = playPoker.Hand("3S, 4D, 7C, 6H, 5H")
        hand.dealHand()
        self.assertEqual(hand.worth(self.rule_book), 'Straight')

    def test_ThreeOfAKind(self):
        hand = playPoker.Hand("3S, 3H, 5H, 6H, 3D")
        hand.dealHand()
        self.assertEqual(hand.worth(self.rule_book), 'Three of a kind')

    def test_TwoPair(self):
        hand = playPoker.Hand("3S, 3H, 5H, 6H, 5D")
        hand.dealHand()
        self.assertEqual(hand.worth(self.rule_book), 'Two pair')

    def test_OnePair(self):
        hand = playPoker.Hand("3S, 3H, 5H, 6H, 4D")
        hand.dealHand()
        self.assertEqual(hand.worth(self.rule_book), 'One pair')

    def test_HighCard(self):
        hand = playPoker.Hand("3S, KH, 5H, 6H, 4D")
        hand.dealHand()
        self.assertEqual(hand.worth(self.rule_book), 'High card')

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()