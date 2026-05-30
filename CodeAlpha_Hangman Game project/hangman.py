import random
words=['apple','mango',"banana","guawa","peach",'pear','grapes']

word= random.choice(words)


blanks=["_"]*len(word)
lives=6
# alredy guessed letters
already_guessed=[]
print('-_-_-_-_-_-_-_-WELCOME TO HANGMAN GAME-_-_-_-_-_-_-_-')

print('guess the word')
# space
print(" ".join(blanks))

# logic part

while lives >0 and '_' in blanks:
    
    user_guess=input('\n Enter the letter:  ').lower()
    
    if not user_guess.isalpha() or len(user_guess)!= 1:
        print('please only enter  one alphabet letter')
        continue
    
    if user_guess in already_guessed:
        print('\n you alreday guessed that letter')
        continue
    already_guessed.append(user_guess)        
    

    if user_guess in word:
        print('Correct') 
        for i in range(len(word)):
            if word[i]==user_guess:
                blanks[i]=user_guess
        print(" ".join(blanks)) 
    else:
         lives-=1
         print("Wrong letter ! Lives Left:",lives)
         print(' '.join(blanks))
     
if "_" not in blanks:
    
    print('Congratulates! you gussed it right')
    print('The word was',word)