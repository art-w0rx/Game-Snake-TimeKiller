from tkinter import *
import random
import os


WIDTH = 600
HEIGHT = 500
SEG_SIZE = 25

IN_GAME = False


def create_block():

    global BLOCK
    posx = SEG_SIZE * random.randint(1, (WIDTH - SEG_SIZE) / SEG_SIZE)
    posy = SEG_SIZE * random.randint(1, (HEIGHT - SEG_SIZE) / SEG_SIZE)
    BLOCK = c.create_oval(posx, posy,
                          posx + SEG_SIZE, posy + SEG_SIZE,
                          fill="deeppink")


class Score(object):

    def __init__(self):
        self.score = 0
        self.x = 300
        self.y = 15
        c.create_text(self.x, self.y, text="Счёт: {}".format(self.score), font="Cambria 16",
                      fill="Light steel blue", tag="score", state='hidden')



    def increment(self):
        c.delete("score")
        self.score += 1
        c.create_text(self.x, self.y, text="Cчёт: {}".format(self.score), font="Cambria 16",
                      fill="Light steel blue", tag="score")

        os.chdir('dat')
        fil_open = open('score.nfr')
        res = int(self.score)
        best_res = int(fil_open.read())
        if res > best_res:
            fil_open = open('score.nfr', 'w')
            fil_open.write(str(res))
            fil_open.close()
            os.chdir('..')
        else:
            fil_open.close()
            os.chdir('..')

    def best_score(self):        
        os.chdir('dat')
        fil_open = open('score.nfr')
        best_score_inf = fil_open.read()
        fil_open.close()
        c.create_text(300, 485, text='Лучший счёт: {}'.format(best_score_inf), font="Cambria 16",
                      fill="Light steel blue",tag ="best_score_label", state = 'normal')
        os.chdir('..')


    def best_score_increment(self):
        c.delete('best_score_label')
        os.chdir('dat')
        fil_open = open('score.nfr')
        best_score_inf = fil_open.read()
        fil_open.close()
        c.create_text(300, 485, text='Лучший счёт: {}'.format(best_score_inf), font="Cambria 16",
                      fill="Light steel blue",tag ="best_score_label", state = 'normal')
        os.chdir('..')


    def reset(self):
        c.delete("score")
        self.score = 0
        c.delete("best_score_label")



def main():

    global IN_GAME
    if IN_GAME:
        s.move()

        head_coords = c.coords(s.segments[-1].instance)
        x1, y1, x2, y2 = head_coords

        if x2 > WIDTH or x1 < 0 or y1 < 0 or y2 > HEIGHT:
            IN_GAME = False

        elif head_coords == c.coords(BLOCK):
            s.add_segment()
            c.delete(BLOCK)
            create_block()

        else:
            for index in range(len(s.segments) - 1):
                if head_coords == c.coords(s.segments[index].instance):
                    IN_GAME = False

        root.after(100, main)

    else:
        set_state(restart_text, 'normal')
        set_state(game_over_text, 'normal')
        set_state(close_but, 'normal')

class Segment(object):

    def __init__(self, x, y):
        self.instance = c.create_rectangle(x, y,
                                           x + SEG_SIZE, y + SEG_SIZE,
                                           fill="lime")
                                           
class Snake(object):

    def __init__(self, segments):
        self.segments = segments


        self.mapping = {"Down": (0, 1), "Right": (1, 0),
                        "Up": (0, -1), "Left": (-1, 0)}

        self.vector = self.mapping["Right"]

    def move(self):

        for index in range(len(self.segments) - 1):
            segment = self.segments[index].instance
            x1, y1, x2, y2 = c.coords(self.segments[index + 1].instance)
            c.coords(segment, x1, y1, x2, y2)

        x1, y1, x2, y2 = c.coords(self.segments[-2].instance)
        c.coords(self.segments[-1].instance,
                 x1 + self.vector[0] * SEG_SIZE, y1 + self.vector[1] * SEG_SIZE,
                 x2 + self.vector[0] * SEG_SIZE, y2 + self.vector[1] * SEG_SIZE)

    def add_segment(self):
        score.increment()
        score.best_score_increment()
        last_seg = c.coords(self.segments[0].instance)
        x = last_seg[2] - SEG_SIZE
        y = last_seg[3] - SEG_SIZE
        self.segments.insert(0, Segment(x, y))

    def change_direction(self, event):

        if event.keysym in self.mapping:
            self.vector = self.mapping[event.keysym]


    def reset_snake(self):
        for segment in self.segments:
            c.delete(segment.instance)


def set_state(item, state):
    c.itemconfigure(item, state=state)
    c.itemconfigure(BLOCK, state='hidden')
    s.reset_snake()


def clicked(event):
    global IN_GAME
    s.reset_snake()
    IN_GAME = True
    c.delete(BLOCK)
    score.reset()
    c.itemconfigure(restart_text, state='hidden')
    c.itemconfigure(game_over_text, state='hidden')
    c.itemconfigure(close_but, state='hidden')  
    start_game()


def start_game():
    global s
    create_block()
    s = create_snake()
    c.bind("<KeyPress>", s.change_direction)
    score.best_score()
    main()


def create_snake():
    segments = [Segment(SEG_SIZE, SEG_SIZE),
                Segment(SEG_SIZE * 2, SEG_SIZE),
                Segment(SEG_SIZE * 3, SEG_SIZE)]
    return Snake(segments)


def close_win(self):
    root.quit()
    

root = Tk()
root.title("Змейка")

c = Canvas(root, width=WIDTH, height=HEIGHT, bg="darkolivegreen")
c.grid()


c.focus_set()


game_over_text = c.create_text(WIDTH / 2, HEIGHT / 3, text="МЕНЮ:",
                               font='Cambria 32', fill='Deep sky blue')

                               

restart_text = c.create_text(WIDTH / 2, HEIGHT - HEIGHT / 2,
                             font='Georgia 26',
                             fill='Green2',
                             text="НОВАЯ ИГРА / (ПРОБЕЛ)",
                             state='hidden')


close_but = c.create_text(WIDTH / 2, HEIGHT - HEIGHT / 3, font='Georgia 26',
                          	fill='Red2', 
                          	text="ВЫХОД / (ESC)",
                          	state='hidden')


c.tag_bind(restart_text, "<Button-1>", clicked)
c.tag_bind(close_but, "<Button-1>", close_win)
c.bind("<space>", clicked)
c.bind("<Escape>", lambda event:root.destroy())


score = Score()

start_game()

root.iconphoto(False, PhotoImage(file='dat/snake.png'))

root.resizable(width=False, height=False)

root.mainloop()
