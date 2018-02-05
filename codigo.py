"""
Reading and learning from the snake code - January - Frebruary 2018
"""

"""
Python with OOP Course from Udemy - Started with this code at 31-01-2018
Teachers Marcos Castro and Thomas William
"""

"""
First improvement - the dot will start in a random position
"""

"""
Second improvement - now you can also play with keyboard and walk in the diagonal direction
 Mapped keys qwe,ad,zxc to make the snake walk in these directions directions
 
 The new keys will make snake walk in these directions 
 q ↖ 
 w ↑ 
 e ↗ 
 a ←
 d → 
 z ↙
 x ↓ 
 c ↘ 
 
 Making this analogy with the Numeric Keyboard:
     ↑ 
↖ q  w  e ↗ 
← a     d → 
↙ z  x  c ↘ 
     ↓ 
"""

"""
Started coding a final improvement: 2 players will make this game a lot of fun
02-02-2018
"""

#Imports
import sys
import random
from PIL import Image, ImageTk
from tkinter import Tk, Frame, Canvas, ALL, NW


"""
Static variables that holds game settings
Size of the board and others
"""

WIDTH = 600
HEIGHT = 600
DOT_SIZE = 10
DELAY = 100
RAND_POS = 27
 
 
class Board(Canvas):
    """
    Inherits from Canvas this class holds elements of the game
    """
    def __init__(self, parent):
        super().__init__(width= WIDTH, height=HEIGHT, 
            background='black', highlightthickness=0)
 
        self.parent = parent
        self.ini_game()
        self.pack()
 
    def ini_game(self):
        """
        Initialize the game
        """
        #Old keyboard arrows movement
        self.left = False
        self.right = True
        self.up = False
        self.down = False
        
        #New keyboard movement
        #Added in 01-02-2018
        self.z = False
        self.x = False
        self.c = False
        self.a = False
        self.d = False
        self.q = False
        self.w = False
        self.e = False


        #Second Player
        #Added in 02-02-2018
        self.one = False
        self.two = False
        self.three = False
        self.four = False
        self.six = True
        self.seven = False
        self.eight = False
        self.nine = False
        
        #Trying to add Score to the game
        self.score = 0
        
        #Second player score
        self.score2 = 0
        
        self.in_game = True
        
        #First improvement - now the first dot will get a random position at the start of the game
        # The 2 while loops is to avoid the dot to born in the same position as the head
        #Added in 01-02-2018
        r = random.randint(0, RAND_POS)
        xdotini = r * DOT_SIZE
        while xdotini > 29 and xdotini < 51:
            r = random.randint(0, RAND_POS)
            xdotini = r * DOT_SIZE
            print (xdotini)

        self.dot_x = xdotini 

        ydotini = r * DOT_SIZE
        while ydotini > 49 and ydotini < 60:
            r = random.randint(0, RAND_POS)
            ydotini = r * DOT_SIZE
            print (ydotini)        
        self.dot_y = ydotini
        #self.dot_x = 100
        #self.dot_y = 190
 
        #Object Image loding for the dot and snake head and body

        try:
            self.ibody = Image.open('body.png')
            self.body = ImageTk.PhotoImage(self.ibody)
            self.ihead = Image.open('head.png')
            self.head = ImageTk.PhotoImage(self.ihead)
            self.idot = Image.open('dot.png')
            self.dot = ImageTk.PhotoImage(self.idot)
            
            #Second player loading images
            self.ibody2 = Image.open('body2.png')
            self.body2 = ImageTk.PhotoImage(self.ibody2)
            self.ihead2 = Image.open('head2.png')
            self.head2 = ImageTk.PhotoImage(self.ihead2)
            
        except IOError as e:
            print(str(e))
            sys.exit(1)
 
        # Canvas Methods that wii fire events on runtime
        # focus_get to get the focus of the Canvas
        # 
        # bind_all control method that eveytime we touch a key on keyboard fires the event --> on_key_press
        # after method fires the event (on_time) every DELAY ms, event
        self.focus_get()
        self.create_objects()
        self.bind_all('<Key>', self.on_key_press)
        self.after(DELAY, self.on_time)
 
    def create_objects(self):
        """
        Creates the objects on the game - dot and snake's body and head
        Canvas method create image (cordinate x, cordinate x, relative position (NORTHWEST) and the tag )
        """
        self.create_image(self.dot_x, self.dot_y, image=self.dot, anchor=NW, tag='dot')
        self.create_image(50, 50, image=self.head, anchor=NW, tag='head')
        self.create_image(40, 50, image=self.body, anchor=NW, tag='body')
        self.create_image(30, 50, image=self.body, anchor=NW, tag='body')
        
        #Creating Second Snake
        self.create_image(150, 150, image=self.head2, anchor=NW, tag='head2')
        self.create_image(140, 150, image=self.body2, anchor=NW, tag='body2')
        self.create_image(130, 150, image=self.body2, anchor=NW, tag='body2')

    def check_dot(self):
        """
        Check that snake's head overlaps the food (dot)
        find_wtihtag will return tuple that returns id of objects with that tag
        """
        dot = self.find_withtag('dot')
        head = self.find_withtag('head')
        
        #Player 2 Head tag
        head2 = self.find_withtag('head2')
        
        #This is only to understand the touple
        #body = self.find_withtag('body')
        #print (body)
      
        #bbox is the coordinates of the bound box of the object - in this case head
        x1, y1, x2, y2 = self.bbox(head)
        
        #Player2 Cordinates bound of the head
        x3, y3, x4, y4 = self.bbox(head2)
        
        #To check if overlap of objects happened and returns a tuple
        overlap = self.find_overlapping(x1, y1, x2, y2)
        overlap2 = self.find_overlapping(x3, y3, x4, y4)
        
        
        #From the overlap tuple check if the dot element is one of the elements in overlap
        #If it is means dot is eaten so the snake will grow - create image and locate_dot
        for ovr in overlap:
            if dot[0] == ovr:
                x, y = self.coords(head)
                self.create_image(x, y, image=self.body, anchor=NW, tag='body')
                self.delete("score")
                self.score += 1
                self.locate_dot()

        for ovr in overlap2:
            if dot[0] == ovr:
                x22, y22 = self.coords(head2)
                self.create_image(x22, y22, image=self.body2, anchor=NW, tag='body2')
                self.delete("score")
                self.score2 += 1
                self.locate_dot()
                


    def locate_dot(self):
        #The dot was founded so we got to delete it and randomize another dot
        dot  = self.find_withtag('dot')
        self.delete(dot[0])

        r = random.randint(0, RAND_POS)
        self.dot_x = r * DOT_SIZE
        r = random.randint(0, RAND_POS)
        self.dot_y = r * DOT_SIZE

        self.create_image(self.dot_x, self.dot_y, image=self.dot, anchor=NW,  tag='dot')

    def do_move(self):
        #Here we define how the snake moves

        #Again the touples now head id and body parts ids
        bodys = self.find_withtag('body')
        head = self.find_withtag('head')
        
        #PLayer2 movement
        bodys2 = self.find_withtag('body2')
        head2 = self.find_withtag('head2')

        items = bodys + head

        items2 = bodys2 + head2
        
        k = 0
        while( k < len(items) - 1):
            c1 = self.coords(items[k])
            c2 = self.coords(items[k+1])
            self.move(items[k], c2[0]-c1[0], c2[1]-c1[1])
            k += 1

        
        k2 = 0
        while( k2 < len(items2) - 1):
            c12 = self.coords(items2[k2])
            c22 = self.coords(items2[k2+1])
            self.move(items2[k2], c22[0]-c12[0], c22[1]-c12[1])
            k2 += 1
            

        #The ifs below will make the snake move to the direction you pressed
        #Changed in 01-02-2018
        if self.left:
            self.move(head, -DOT_SIZE, 0)

        if self.right:
            self.move(head, DOT_SIZE, 0)

        if self.up:
            self.move(head, 0, -DOT_SIZE)

        if self.down:
            self.move(head, 0, DOT_SIZE)

        if self.z:
            self.move(head, -DOT_SIZE, DOT_SIZE)

        if self.x:
            self.move(head, 0, DOT_SIZE)

        if self.c:
            self.move(head, DOT_SIZE, DOT_SIZE)

        if self.a:
            self.move(head, -DOT_SIZE, 0)

        if self.d:
            self.move(head, DOT_SIZE, 0)

        if self.q:
            self.move(head, -DOT_SIZE, -DOT_SIZE)

        if self.w:
            self.move(head, 0, -DOT_SIZE)

        if self.e:
            self.move(head, DOT_SIZE, -DOT_SIZE)
       
        #PLayer2 movemnts
        if self.one:
            self.move(head2, -DOT_SIZE, DOT_SIZE)

        if self.two:
            self.move(head2, 0, DOT_SIZE)

        if self.three:
            self.move(head2, DOT_SIZE, DOT_SIZE)

        if self.four:
            self.move(head2, -DOT_SIZE, 0)

        if self.six:
            self.move(head2, DOT_SIZE, 0)

        if self.seven:
            self.move(head2, -DOT_SIZE, -DOT_SIZE)

        if self.eight:
            self.move(head2, 0, -DOT_SIZE)

        if self.nine:
            self.move(head2, DOT_SIZE, -DOT_SIZE)



    def check_collisions(self):
        """
        This method checks 2 cases:
            The snake goes beyond Canvas limits
            The snake collides with itself
        """
        
        #Tuples of bodys and head ID
        
        bodys = self.find_withtag('body')
        head = self.find_withtag('head')

        #Adding player2
        bodys2 = self.find_withtag('body2')
        head2 = self.find_withtag('head2')
        
        #Coordinates of the head
        x1, y1, x2, y2 = self.bbox(head)
        overlap = self.find_overlapping(x1, y1, x2, y2)

        #Adding player2
        x12, y12, x22, y22 = self.bbox(head2)
        overlap2 = self.find_overlapping(x12, y12, x22, y22)
        
        #If a collision body head happened then the game is over
        for body in bodys:
            for ovr in overlap:
                if body == ovr:
                    self.in_game = False


        #If a collision body head happened then the game is over for player2
        for body2 in bodys2:
            for ovr2 in overlap2:
                if body2 == ovr2:
                    self.in_game = False        
        
        #Need to do body of snake 1 x snake 2
        #Trying that on 05-02-2018
        
        
        #Body of player 1 cant be on body of player 2
        for body in bodys:
            for ovr in overlap:
                for body2 in bodys2:
                    for ovr2 in overlap2:
                        if body == ovr2:
                            self.in_game = False
        
        #Body of player 2 cant be on body of player 1
        for body in bodys:
            for ovr in overlap:
                for body2 in bodys2:
                    for ovr2 in overlap2:
                        if body2 == ovr:
                            self.in_game = False
        
        #Collision trough walls also terminate the game
        #Change here to get a place to put your score - Not done
        #Trying to change here so the game doesnt end in the walls
        """
        Old code walls kill you when out of bound
        if x1 < 0:
            self.in_game = False

        if x1 > WIDTH - DOT_SIZE:
            self.in_game = False

        if y1 < 0:
            self.in_game = False

        if y1 > HEIGHT - DOT_SIZE:
            self.in_game = False
        """
        #New code walls doesnt kill you when out of bound
        if x1 < 0:
            self.move(head, WIDTH - DOT_SIZE, 0)

        if x1 > WIDTH - DOT_SIZE:
            self.move(head, DOT_SIZE - WIDTH, 0)

        if y1 < 0:
            self.move(head, 0, HEIGHT - DOT_SIZE)

        if y1 > HEIGHT - DOT_SIZE:
            self.move(head, 0, DOT_SIZE- HEIGHT)
            
        #New code palyer2 get out of bound
        if x12 < 0:
            self.move(head2, WIDTH - DOT_SIZE, 0)

        if x12 > WIDTH - DOT_SIZE:
            self.move(head2, DOT_SIZE - WIDTH, 0)

        if y12 < 0:
            self.move(head2, 0, HEIGHT - DOT_SIZE)

        if y12 > HEIGHT - DOT_SIZE:
            self.move(head2, 0, DOT_SIZE- HEIGHT)

    def on_key_press(self, e):
        #This method will make the control what key is pressed so the variables will define behavior
        #This part was changed 01-02-2018 so now we can control in diagonals and in the keyboard also
        key = e.keysym

        if key == 'Left' and not (self.right or self.d):
            self.left = True
            self.up = False
            self.down = False
            self.z = False
            self.x = False
            self.c = False
            self.a = False
            self.d = False
            self.q = False
            self.w = False
            self.e = False

        if key == 'Right' and not (self.left or self.a):
            self.right = True
            self.up = False
            self.down = False
            self.z = False
            self.x = False
            self.c = False
            self.a = False
            self.d = False
            self.q = False
            self.w = False
            self.e = False

        if key == 'Up' and not (self.down or self.x):
            self.up = True
            self.left = False
            self.right = False
            self.z = False
            self.x = False
            self.c = False
            self.a = False
            self.d = False
            self.q = False
            self.w = False
            self.e = False

        if key == 'Down' and not (self.up or self.w):
            self.down = True
            self.left = False
            self.right = False
            self.z = False
            self.x = False
            self.c = False
            self.a = False
            self.d = False
            self.q = False
            self.w = False
            self.e = False
        
        if key == 'z' and not self.e:
            self.down = False
            self.left = False
            self.right = False
            self.z = True
            self.x = False
            self.c = False
            self.a = False
            self.d = False
            self.q = False
            self.w = False
            self.e = False

        if key == 'x' and not (self.w or self.up):
            self.down = False
            self.left = False
            self.right = False
            self.z = False
            self.x = True
            self.c = False
            self.a = False
            self.d = False
            self.q = False
            self.w = False
            self.e = False

        if key == 'c' and not self.q:
            self.down = False
            self.left = False
            self.right = False
            self.z = False
            self.x = False
            self.c = True
            self.a = False
            self.d = False
            self.q = False
            self.w = False
            self.e = False

        if key == 'a' and not (self.d or self.right):
            self.down = False
            self.left = False
            self.right = False
            self.z = False
            self.x = False
            self.c = False
            self.a = True
            self.d = False
            self.q = False
            self.w = False
            self.e = False

        if key == 'd' and not (self.a or self.left):
            self.down = False
            self.left = False
            self.right = False
            self.z = False
            self.x = False
            self.c = False
            self.a = False
            self.d = True
            self.q = False
            self.w = False
            self.e = False

        if key == 'q' and not self.c:
            self.down = False
            self.left = False
            self.right = False
            self.z = False
            self.x = False
            self.c = False
            self.a = False
            self.d = False
            self.q = True
            self.w = False
            self.e = False

        if key == 'w' and not (self.x or self.down):
            self.down = False
            self.left = False
            self.right = False
            self.z = False
            self.x = False
            self.c = False
            self.a = False
            self.d = False
            self.q = False
            self.w = True
            self.e = False

        if key == 'e' and not self.z:
            self.down = False
            self.left = False
            self.right = False
            self.z = False
            self.x = False
            self.c = False
            self.a = False
            self.d = False
            self.q = False
            self.w = False
            self.e = True
        
        #Stating to map second player's key entry
        if key == 'KP_1' and not self.nine:
            self.one = True
            self.two = False
            self.three = False
            self.four = False
            self.six = False
            self.seven = False
            self.eight = False
            self.nine = False

        if key == 'KP_2' and not self.eight:
            self.one = False
            self.two = True
            self.three = False
            self.four = False
            self.six = False
            self.seven = False
            self.eight = False
            self.nine = False

        if key == 'KP_3' and not self.seven:
            self.one = False
            self.two = False
            self.three = True
            self.four = False
            self.six = False
            self.seven = False
            self.eight = False
            self.nine = False
            
        if key == 'KP_4' and not self.six:
            self.one = False
            self.two = False
            self.three = False
            self.four = True
            self.six = False
            self.seven = False
            self.eight = False
            self.nine = False
            
        if key == 'KP_6' and not self.four:
            self.one = False
            self.two = False
            self.three = False
            self.four = False
            self.six = True
            self.seven = False
            self.eight = False
            self.nine = False
            
        if key == 'KP_7' and not self.three:
            self.one = False
            self.two = False
            self.three = False
            self.four = False
            self.six = False
            self.seven = True
            self.eight = False
            self.nine = False
            
        if key == 'KP_8' and not self.two:
            self.one = False
            self.two = False
            self.three = False
            self.four = False
            self.six = False
            self.seven = False
            self.eight = True
            self.nine = False
            
        if key == 'KP_9' and not self.z:
            self.one = False
            self.two = False
            self.three = False
            self.four = False
            self.six = False
            self.seven = False
            self.eight = False
            self.nine = True


    def on_time(self):
        """
        Method after call this one, after 100 MS this method will be called
        Here you'll have to change if you want to add score and other funcionalitys
        """
        
        #We start checking if the game is True so we start
        # checking collisions, check if the snake ate a dot
        # make a move and call this method again recursively
        if self.in_game:
            self.check_collisions()
            self.check_dot()
            self.do_move()
            #Add the score here
            self.create_text(self.winfo_width()/2, self.winfo_height()*9/10, text=str(self.score) + " <-> " + str(self.score2), fill='White',
                             tag="score")
            self.after(DELAY, self.on_time)
            if self.score > 30:
                self.victory()
        else:
            self.game_over()

    def game_over(self):
        """
        Game over is called if in_game is False
        """
        self.delete(ALL)
        self.create_text(self.winfo_width()/2, self.winfo_height()/2, text='Game Over', fill='White')
    
    def victory(self):
        """
        Game over is called if in_game is False
        """
        self.delete(ALL)
        self.create_text(self.winfo_width()/2, self.winfo_height()/3, text='30 dots! You WON! See you next time', fill='White')




class Snake(Frame):

    def __init__(self, parent):
        super().__init__(parent)
        parent.title('Snake')
        self.board = Board(parent)
        self.pack()

def main():
    root = Tk()
    snake = Snake(root)
    root.mainloop()

if __name__ == '__main__':
    main()

