import tkinter as tk
from PIL import Image,ImageTk
import random
MOVE_INCREMENT = 20
moves_per_second=15
GAME_SPEED=1000//moves_per_second


class Snake(tk.Canvas):

    def __init__(self):
        super().__init__(width=620, height=600, background="black", highlightthickness=0)
        self.score = 0
        self.snake_positions = [(100, 100), (80, 100), (60, 100)]
        self.food_positions = self.set_new_food_positions()
        self.direction = "Right"
        self.bind_all("<Key>", self.on_key_press)
        self.load_assets()
        self.create_objects()
        self.after(75, self.perform_action)


    def load_assets(self):
        try:
            self.snake_body_image=Image.open("snake.png")
            self.snake_body=ImageTk.PhotoImage(self.snake_body_image)

            self.food_image = Image.open("food.png")
            self.food = ImageTk.PhotoImage(self.food_image)

        except IOError as error:
            print(error)
            root.destroy()

    def create_objects(self):
        self.create_text(
            45, 12, text=f"Score:{self.score}", fill="#fff", font=("TkDefaultFont", 14), tag="score"
        )

        for x_position, y_position in self.snake_positions:
            self.create_image(x_position, y_position, image=self.snake_body, tag="snake")
        self.create_image(*self.food_positions, image=self.food, tag="food")
        self.create_rectangle(5, 2, 615, 595, outline="#fff")


    def move_snake(self):
        head_x_position, head_y_position=self.snake_positions[0]
        if self.direction == "Right":
            new_head_position=(head_x_position+MOVE_INCREMENT, head_y_position)
        elif self.direction=="Left":
            new_head_position = (head_x_position - MOVE_INCREMENT, head_y_position)
        elif self.direction=="Down":
            new_head_position = (head_x_position , head_y_position+MOVE_INCREMENT)
        elif self.direction=="Up":
            new_head_position = (head_x_position, head_y_position-MOVE_INCREMENT)

        self.snake_positions = [new_head_position] + self.snake_positions[:-1]

        for segment, position in zip(self.find_withtag('snake'), self.snake_positions):
            self.coords(segment, position)


    def perform_action(self):
        if self.check_collision():
            return self.game_over()
        self.food_collision()
        self.move_snake()
        self.after(GAME_SPEED, self.perform_action)



    def check_collision(self):
        head_x_position, head_y_position = self.snake_positions[0]
        return(
            head_x_position in (0, 600) or
            head_y_position in (20, 620)
            or (head_x_position, head_y_position) in self.snake_positions[1:]

            )

    def on_key_press(self, e):
        new_direction=e.keysym
        all_directions = {'Up', 'Down', 'Left', 'Right'}
        opposite_directions = ({'Up', 'Down'}, {'Left', 'Right'})
        if (new_direction in all_directions and
                {self.direction,new_direction} not in opposite_directions):
            self.direction=new_direction


    def food_collision(self):
        if self.snake_positions[0]==self.food_positions:
            self.score+=1
            self.snake_positions.append(self.snake_positions[-1])
            if self.score%5==0:
                global moves_per_second
                moves_per_second+=1



            self.create_image(
                *self.snake_positions[-1], image=self.snake_body, tag='snake'
            )

            self.food_positions = self.set_new_food_positions()
            self.coords(self.find_withtag("food"), self.food_positions)

            score = self.find_withtag("score")
            self.itemconfigure(score, text=f"Score:{self.score}", tag="score")

    def set_new_food_positions(self):
        while True:
            x_position = random.randint(20, 28) * MOVE_INCREMENT
            y_position = random.randint(3, 25) * MOVE_INCREMENT
            food_position = (x_position, y_position)

            if food_position not in self.snake_positions:
                return food_position

    def game_over(self):
        self.delete(tk.ALL)
        self.create_text(
            310, 300, text=f"GAME OVER...you scored {self.score}", fill="#fff", font=("TkDefaultFont", 14), tag="score"
        )



root = tk.Tk()
root.title("Worm")
root.resizable(False, False)

board = Snake()
board.pack()


root.mainloop()

