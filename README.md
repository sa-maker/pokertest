This project is a test to see the coding skills of a developer.

### PROBLEM DEFINITION ####

For this program, you will be taking a text input of playing cards and 
evaluating what the best poker hand could be constructed with the cards. 

 
For example, given a string input of: 
'AS, 10C, 10H, 3D, 3S' 
(the cards above are ace of spades, 10 of clubs, 10 of hearts, 3 of diamonds and 3 of spades) 
 
Output would be: 'Two Pair' 
 
Use whatever language you are most comfortable in, however preferably Java if 
you are familiar with it. We are looking for evidence of good:  
- Object Oriented programming    
- design  
- test rather than language skills. 
 
We are interested in seeing how you prioritize features. 
For us to see that progress, please provide a git commit history. 
 
For reference, the ten possible poker hands can be found at: 
https://en.wikipedia.org/wiki/List_of_poker_hand_categories 
 
Please provide your program as a zipped file of the directory ensuring that the 
git history file is included.

### SOLUTION ###

The solution consists of 2 python script files
- A single page python file that contains the classes and the instantiating 
scripts that will take the given string and print the result on screen.
- A unit test file that can be run to ensure that any changes made does not break
the code.

According to the Wiki page there can be a joker in the mix. To add a joker to 
the card string use **. there can only be one joker and he can only be used to 
make a 5 of a kind hand. 

### INSTALLING AND RUNNING THE SOLUTION ###
On a windows PC:
- install python on the pc 
- ensure that python is on your environment path
- unzip the code

To run playPocker
- Open a Powershell or CMD window in the code directory
- type in:  
	python playPoker.py "AS, 10C, 10H, 3D, 3S"
- Hit enter
- try diffrent combinations of cards

To run the unit tests
- Open a Powershell or CMD window in the code directory
- type in:  
	python testPlayPoker.py
- Hit enter









 

  

