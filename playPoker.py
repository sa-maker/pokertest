import sys


#===Global variables============================================================
class Item:
# A database class used to house the name and possible values of a deck of cards
 
    def __init__(self, name, values_array):
        self.name = name
        self.possible_values = values_array

#-------------------------------------------------------------------------------
class CardDeck:
# A database class that stipulates the face and suit values of each card in a
# card deck. 
# In Suits:  s = spades, c = clubs, h = harts, d = diamonds. 
# In Face: j = jack, q = queen, k = king, a = Ace
# * represent a joker. there can only be one Joker and it can only be **
 
    def __init__(self):
        self.face_values = Item("face",["1","2","3","4","5","6","7","8","9","10","j","q","k","a",'*'])
        self.suit_values = Item("suit",["s","c","h","d",'*'])


#We need a deck of cards before we can start playing
card_deck = CardDeck()


#===CLASES======================================================================

class MessageError:
# A state engin that drives the validation of both the cards and the hand. If an
# instance is invalid then the error is set to True. If there is an error in the 
# instance then the reason is set in the message.  

    def __init__(self, message, error):
        self.message = message
        self.error = error
        
    def printMessage(self):
        return self.message
    
    def isError(self):
        return self.error
    
    def setMessageError(self, message, error):
        self.message = message
        self.error = error
    
    def appendMessageError(self, message, error):
        self.message = "%s %s" %(self.message, message)
        self.error = error
    

#-------------------------------------------------------------------------------
class Card(MessageError):
# A poker hand is made up of cards. Cards have a face value and a suit. A card 
# can be a valid card of a invalid card. If the card is invalid then the card's
# error will be set to True and the reason why it is invalid will be set in it's 
# message 
  
    def __init__(self, values):
        MessageError.__init__(self, "Card Dealt %s" %values, False)

        
        try:
            values = values.strip()
            if values.__len__() < 2:
                self.setMessageError("The card values are to small %s"  %values, True)
            if values.__len__() > 3:
                self.setMessageError("The card values are to large %s"  %values, True)    
        
            self.face = values[:-1].lower()
            self.suit = values[-1:].lower()

        except:
            self.setMessageError("An error occured while dealing the card %s"  %values, True)
        if not self.isError():
            self.validateCard()
        

    def __str__(self):
        return "Card: %s%s " % (self.face, self.suit)
    
    def __repr__(self):
        return "Card: %s%s" % (self.face, self.suit)

    def validateCard(self):
    # A validation function to see if the card is in the card deck with the 
    # correct suit and face value
     
        if not self.face in card_deck.face_values.possible_values:
            self.setMessageError("%s is not an acceptible face value, what card deck are you using?" %self.face, True)
        if self.suit not in card_deck.suit_values.possible_values:
            self.setMessageError("%s is not an acceptible suit, what card deck are you using?" %self.suit, True) 
                       
        #joker must be "**", "2*" or "*h" is not allowed 
        if (self.face == "*" and self.suit != "*") or (self.suit == "*" and self.face != "*"):
            self.setMessageError("%s%s is not a acceptible card, what card deck are you using?" %(self.face, self.suit), True)


#-------------------------------------------------------------------------------
class Hand(MessageError):
 
# In a poker game there is a hand that exactly contains 5 cards. A card has a face 
# value and a suit. Each card is unique. The hand is constructed from a string 
# of cards. The string is brocken up and each card created from the substring.
# The validity of the Hand is determined by a state engin (MessageError). If a 
# hand is not valid then its error value will be True and the reason will be 
# given in the message. If there is any problem wth any of the cards in the hand 
# then the hand will go in an error state and the card's message will be appended 
# to the hand's message   
 

    def __init__(self, input_str):
        self.input_str = input_str
        MessageError.__init__(self, "\nDealing hand now...", False)
        self.card_list = []
        self.face_dict = {}
        self.suit_dict = {}
        
    #---------------------------------------------------------------------------
    def dealHand(self):
    # The Function that validates and poulated the pocker hand with the corect 
    # number of cards
    
        card_string_list = self.input_str.split(',')
        
        if not card_string_list.__len__() == 5:
            self.setMessageError("\nERROR: A hand must have exactly 5 cards. %s is not 5 cards" %self.input_str, True)
        
        else:
            for card_string in card_string_list:
                card = Card(card_string)
                if self.isUnique(card):
                    if card.isError():
                        self.appendMessageError("\nERROR: Hand could not be dealt: %s" %card.message, True) 
                    else:
                        self.card_list.append(card)
                else:
                    self.appendMessageError("\nERROR: It seems like you have more than one %s%s cards. Mind explaining to the group how that happened?" %(card.face, card.suit), True)
                    
            if not self.isError():
                if self.setDict():
                    self.setMessageError("Hand was dealt, dictionaries compiled" , False)

    #---------------------------------------------------------------------------
    def isUnique(self, card):
    # A validation function to see if the card is unique in the hand
    
        for card_in_hand in self.card_list:
            if card.face == card_in_hand.face and card.suit == card_in_hand.suit:
                return False

        return True
    
    #---------------------------------------------------------------------------
    def setDict(self):
    # An interperator function that builds two dictionaries used to find the 
    # worth of a poker hand. 
    
        for card in self.card_list:
            if card.face in self.face_dict:
                self.face_dict[card.face] += 1
            else:
                self.face_dict[card.face] = 1
        
            if card.suit in self.suit_dict:
                self.suit_dict[card.suit] += 1
            else:
                self.suit_dict[card.suit] = 1
        
        # If there is a joker remove it and add it and add 1 to the only set that 
        # it can work for, the 5 of a kind hand
        if "*" in self.face_dict:
            del self.face_dict["*"]
            for key in self.face_dict:
                if self.face_dict[key] == 4:
                    self.face_dict[key] += 1
                else:
                    self.setMessageError("\nERROR: You can only use a joker in a 5 of a kind. Pick the best value for the joker and use that instead.", True)
                    return False
                
        return True

    #---------------------------------------------------------------------------
    def worth(self, rule_book):
    # The worth of a poker hand can be determined by the grouping of the face 
    # of the cards and the groupings of the suits of the cards
    
        for rule in rule_book.rule_list:
            if rule.isTrue(self.face_dict, self.suit_dict):
                self.setMessageError("Hand was Ruled" , False)
                return rule.description
        
        return rule_book.default.description    
    #---------------------------------------------------------------------------
    def __str__(self):
        return "\nHand: %s " % self.card_list
        
        
#-------------------------------------------------------------------------------
class Rule():
# A controller class that houses the logic for determinaing if a pokerhand is 
# adhears to a set of paramaters 

    def __init__(self, description, face_int_1, face_int_2, face_follow, suit_same ):
    # The initiating of parameters is loaded into the Rule and will be used to 
    # determine if the poker hand ahears to it 
    
        self.description = description
        self.face_int_1 = face_int_1
        self.face_int_2 = face_int_2
        self.face_follow = face_follow
        self.suit_same = suit_same
        
    #---------------------------------------------------------------------------
    def isTrue(self, face_dict, suit_dict):
    # A function that recieves two formatted dictionaries that represents the 
    # poker handand returns True if it adhears to the initiating rule parameters
    # Otherwise it returns False
      
        ret_face1 = None
        ret_face2 = None
        used_keys = []
        
        ret_suit = None
        ret_follow = None
        
        # Here we build the parameters that must be true for the rule to be true
        
        # Is there a rule parameter?
        if self.face_int_1: 
            ret_face1 = False
            
            # is that parametr True?
            for key in face_dict:
                if key not in used_keys:
                    if face_dict[key] == self.face_int_1:
                        ret_face1 = True
                        #This key has been counted now remove it
                        used_keys.append(key)
                        break

        # Is there a rule parameter?            
        if self.face_int_2:
            ret_face2 = False
            
            # is that parametr True?
            for key in face_dict:
                if key not in used_keys:
                    if face_dict[key] == self.face_int_2:
                        ret_face2 = True
                        #This key has been counted now remove it
                        used_keys.append(key)
                        break
                    
        # Is there a rule parameter?
        if self.suit_same:
            ret_suit = False
            # is that parametr True?
            if suit_dict.__len__() == 1:
                ret_suit = True
                
        # Is there a rule parameter?
        if self.face_follow:
            ret_follow = False
            # is that parametr True?
            if face_dict.__len__() == 5:
                ret_follow = self.doesNumbersFollow(face_dict)
        
        response = False
        
        # Here we collect all the Rule's parameters 
        # The moment it becomes aparent that a required paramenter was broken, 
        # return False else continue until it is proven to be true
        
        if ret_face1 is not None:
            if ret_face1 == False:
                return False
            else:
                response = True
        
        if ret_face2 is not None:
            if ret_face2 == False:
                return False
            else:
                response = True
        
        if ret_suit is not None:
            if ret_suit == False:
                return False
            else:
                response = True
                
        if ret_follow is not None:
            if ret_follow == False:
                return False
            else:
                response = True
        
        return response
    
    #---------------------------------------------------------------------------
    def doesNumbersFollow(self, face_dict):
    # A helper function that determine if all the face values in a dictionary 
    # follow one another
    
        cards = []
        for face in face_dict:
            try:
                val = int(face)
                cards.append(val)
            except ValueError:
                if face =="j":
                    cards.append(11)
                elif face =="q":
                    cards.append(12)
                elif face =="k":
                    cards.append(13)
                elif face =="a":
                    cards.append(14)
         
        cards.sort()
        test_val = cards[0] - 1
        for val in cards:
            if (test_val + 1) != val:
                return False
            test_val = val
        return True    
       
#-------------------------------------------------------------------------------
class Rulebook():
# A database class that houses a list of the rules that a poker hand can be worth
    def __init__(self):
        self.rule_list = []
        self.rule_list.append(Rule("Five of a kind", 5, "", False, False))
        self.rule_list.append(Rule("Straight flush",  "",     "",     True,   True))
        self.rule_list.append(Rule("Four of a kind",  4,      "",     False,  False))
        self.rule_list.append(Rule("Full house",      3,      2,      False,  False))
        self.rule_list.append(Rule("Flush",           "",     "",     False,  True))
        self.rule_list.append(Rule("Straight",        "",     "",     True ,  False))
        self.rule_list.append(Rule("Three of a kind", 3,      "",     False,  False))
        self.rule_list.append(Rule("Two pair",        2,      2,      False,  False))
        self.rule_list.append(Rule("One pair",        2,      "",     False,  False))
        
        self.default = Rule("High card",        "",      "",     False,  False)
        self.rule_list.append(self.default)
        


#---MAIN FUNCTION---------------------------------------------------------------
def main():
# The main function that takes the Input string, creates a hand and pass the 
# input string to it. Prints out any errors that happend as the hand was created
# Instantiates a rulebook and pass it to the hand that uses it to reports on 
# what the hand is worth 

    input_str = ""
    try:
        input_str = sys.argv[1]
    except IndexError as e:
        print("Please enter a string after the playPoker.py Something like \"AS, 10C, 10H, 3D, 3S\"")
    
    
    if input_str:
        print("Lets play poker with %s" % input_str)
        
        #Lets deal a hand from the deck
        hand = Hand(input_str)
        hand.dealHand()
        
        #The hand is dealt, lets take look 
        if hand.isError():
            print(hand.printMessage())
            print("\n")
        else:
            #well what does the rule book say it is worth?
            rule_book = Rulebook()
            print(hand.worth(rule_book))
            print("\n")


#===BASH FUNCTION===============================================================
# This is the main function that gets the variable from the bash line and send 
# it through to the main(input_str) function
# The format of the variable is a string. the following bash code will work 
# from with in the project folder  
# python playPoker.py "AS, 10C, 10H, 3D, 3S"
  
if __name__ == "__main__": main()
