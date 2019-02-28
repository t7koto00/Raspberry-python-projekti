import time
import random
from graphics import *
import google.cloud.storage

storage_client = google.cloud.storage.Client.from_service_account_json('/home/pi/Documents/hangman.json')
bucket = storage_client.get_bucket('hangman-words')
blob = bucket.get_blob("wordlist2.txt")
pokimen = blob.download_as_string()


win = GraphWin('Hangman', 900, 450) 
message = Text(Point(win.getWidth()/2, 20), 'What is your name?')
message.draw(win)

textEntry = Entry(Point(win.getWidth()/2,100),20)
textEntry.draw(win)
x = " "
while x != "Return":
        x = win.getKey()
#win.getMouse()
textEntry.undraw()
name = textEntry.getText()
message.undraw()
viesti = "Hello", name
message = Text(Point(win.getWidth()/2, 20), viesti)
message.draw(win)
message = Text(Point(win.getWidth()/2, 40), "Time to play hangman!")
message.draw(win)
time.sleep(1)
turns = 10
word = ""
score = 0

def game():
    message = Text(Point(win.getWidth()/2, 60), "Start guessing...")
    message.draw(win)
    time.sleep(0.5)
    words = pokimen.split()
    wordIndex = random.randint(0, len(words) - 1)
    word = words[wordIndex]
    word = word.decode('utf-8')
    guesses = ''
    global turns
    while turns > 0:         

        empty = 0             
        x = 0
        for char in word:
            if char in guesses:    
                message = Text(Point(win.getWidth()/2 -48 + x, 100), char)
                message.draw(win)
                x = x+12
            else:
                message = Text(Point(win.getWidth()/2 -48 + x, 100), "_")
                message.draw(win)
                x = x+12
                empty += 1    

        if empty == 0:
            print ("")
            win.delete("all")
            message = Text(Point(win.getWidth()/2, 140), "Correct!")
            message.draw(win)
            global score
            score += 1
            pisteet = ("Your score is: {}").format(score)
            message = Text(Point(win.getWidth()/2, 160), pisteet)
            message.draw(win)
            sana = ("The word was: {}").format(word)
            message2 = Text(Point(win.getWidth()/2,180),sana)
            message2.draw(win)
            turns = turns + 5
            game()
            break

        guess = win.getKey()
        win.delete("all")
        if len(guess) != 1:
            message = Text(Point(win.getWidth()/2, 140), "Your guess must have only one character!")
            message.draw(win)
        else: 
            guesses += guess                    

            if guess not in word:  
                turns -= 1        
                viesti = ("Your have {}"
                          " more guesses").format(turns)
                message = Text(Point(win.getWidth()/2, 140), "Wrong")
                message.draw(win)
                message = Text(Point(win.getWidth()/2, 160), viesti)
                message.draw(win)

                if turns == 0:
                    win.delete("all")
                    message = Text(Point(win.getWidth()/2, 40), "Game Over!")
                    message.draw(win)
                    viesti =("The correct word was: {}").format(word)
                    message = Text(Point(win.getWidth()/2, 60), viesti)
                    message.draw(win)
                    viesti =("Your final score was: {}").format(score)
                    message = Text(Point(win.getWidth()/2, 80), viesti)
                    message.draw(win)
                
                    tulos = name + "___" +str(score)
                    
                    blob2 = bucket.get_blob("pisteet.txt")
                    tulokset = blob2.download_as_string()
                    tulokset = tulokset.decode('utf-8')
                    tulokset = tulokset + " " + tulos
                    blob2.upload_from_string(tulokset)
                    
                    tulokset = tulokset.split()
                    i = 0
                    for x in tulokset:
                        points = tulokset[i]
                        message = Text(Point(win.getWidth()/2, 120+i*20), points)
                        message.draw(win)
                        i = i +1
game()