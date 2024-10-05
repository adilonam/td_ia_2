# =======Default mazes=======
import copy
from tkinter import CENTER

from PIL import Image, ImageTk

from vacuum_2d import VacuumEnvironment, Action, Direction, Dirt, Wall

maze4x4 = ["######",
           "#A   #",
           "#*##*#",
           "#  # #",
           "#*  *#",
           "######"]

maze6x6 = ["########",
           "#A #*  #",
           "#*##*  #",
           "#  ### #",
           "#* ## *#",
           "#*  #  #",
           "#*  *  #",
           "########"]

maze8x8 = ["##########",
           "#A #*    #",
           "#*##*    #",
           "#    # # #",
           "#*  * *  #",
           "#* #  * *#",
           "#* #  * *#",
           "#*  *  # #",
           "#*  *  #*#",
           "##########"]

maze10x10 = ["############",
             "#A #*   *  #",
             "#*##*      #",
             "#*##*      #",
             "#    # #   #",
             "#*  *#  *  #",
             "#*   #  * *#",
             "#*   #  * *#",
             "#*    * *  #",
             "#*  *   #  #",
             "#*  *  *#  #",
             "############"]
# =======End default mazes=======
mazes = {1: maze4x4, 2: maze6x6, 3: maze8x8, 4: maze10x10}


def build_vacuum_env(maze, agent_factory):
    env = VacuumEnvironment(len(maze[0]), len(maze))
    for i in range(1, len(maze) - 1):
        for j in range(1, len(maze[i])):
            if maze[i][j] == '#':
                env.add_thing(Wall(), (j, i))
            elif maze[i][j] == '*':
                env.add_thing(Dirt(), (j, i))
            elif maze[i][j] == 'A':
                env.add_thing(agent_factory(), (j, i))
    return env


global current_robot_img


class VacEnv4Gui(VacuumEnvironment):
    def __init__(self, agent, canvas, animation_speed, interrupted, score_lbl, maze_index, done_observer):
        super().__init__(len(mazes.get(maze_index)[0]), len(mazes.get(maze_index)))
        self.maze = copy.deepcopy(mazes.get(maze_index))
        for i in range(1, len(self.maze) - 1):
            for j in range(1, len(self.maze[i])):
                if self.maze[i][j] == '#':
                    self.add_thing(Wall(), (j, i))
                elif self.maze[i][j] == '*':
                    self.add_thing(Dirt(), (j, i))
                elif self.maze[i][j] == 'A':
                    self.add_thing(agent, (j, i))
        self.agent = agent
        self.canvas = canvas
        self.speed = animation_speed
        self.score_lbl = score_lbl
        self.interrupted = interrupted
        self.done_observer = done_observer
        self.steps = 1000
        self.agent_img_bump = Image.open("images/vac_bump.png")
        self.agent_img_r = Image.open("images/vac.png")
        self.agent_img_l = self.agent_img_r.transpose(Image.FLIP_LEFT_RIGHT)
        self.agent_img_u = self.agent_img_r.transpose(Image.ROTATE_90)
        self.agent_img_d = self.agent_img_r.transpose(Image.ROTATE_270)
        self.robot_img_bump = None
        self.robot_img_r = None
        self.robot_img_l = None
        self.robot_img_u = None
        self.robot_img_d = None

    def delete_thing(self, thing):
        super().delete_thing(thing)
        if isinstance(thing, Dirt):
            x, y = thing.location
            self.maze[y] = self.maze[y][:x] + ' ' + self.maze[y][x + 1:]

    def run(self, steps=1000):
        """Run the Environment for given number of time steps."""
        self.steps = steps
        self.start()

    def start(self):
        self.draw_maze()
        self.steps = self.steps - 1
        if not self.is_done() and not self.interrupted.get() and self.steps > 0:
            self.step()
            self.canvas.after(self.speed.get(), self.start)
        else:
            self.score_lbl['text'] = str(self.agent.performance)
            self.agent.alive = False
            height = self.canvas.winfo_height()
            width = self.canvas.winfo_width()
            # self.canvas.create_rectangle(0, 0, width, height, fill="#000")
            self.done_observer()

    def draw_maze(self):
        self.canvas.delete('all')
        height = self.canvas.winfo_height()
        width = self.canvas.winfo_width()
        self.canvas.create_rectangle(0, 0, width, height, fill="white")
        for y, row in enumerate(self.maze):
            for x, ch in enumerate(row):
                if self.is_wall(x, y):
                    self.draw_wall(x, y)
                elif self.is_dirty(x, y):
                    self.draw_dirty(x, y)
                else:
                    self.draw_rec(x, y, "white")
        self.draw_agent()

    def is_wall(self, x, y):
        return self.maze[y][x] == '#'

    def is_dirty(self, x, y):
        return self.maze[y][x] == '*'

    def draw_wall(self, x, y):
        self.draw_rec(x, y, "#000")

    def draw_dirty(self, x, y):
        self.draw_rec(x, y, "gray")

    def draw_rec(self, x, y, color):
        x1, y1, x2, y2 = self.convert(x, y)
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)
        self.canvas.create_rectangle(x1, y1, x2, y2, outline="black")

    def convert(self, x, y):
        maze_height = len(self.maze)
        maze_width = len(self.maze[0])
        height = self.canvas.winfo_height() / maze_height
        width = self.canvas.winfo_width() / maze_width
        x1, y1 = (x * width, y * height)
        x2, y2 = (x1 + width, y1 + height)
        return x1, y1, x2, y2

    def draw_agent(self):
        x, y = self.agent.location
        maze_height = len(self.maze)
        maze_width = len(self.maze[0])
        height = self.canvas.winfo_height() / maze_height
        width = self.canvas.winfo_width() / maze_width
        x1, y1 = (x * width, y * height)
        x2, y2 = (x1 + width, y1 + height)

        if self.robot_img_r is None:
            width, height = self.agent_img_r.size
            if width > x2 - x1:
                image = self.agent_img_r.resize((int(x2 - x1), int(y2 - y1)), Image.NEAREST)
                self.robot_img_r = ImageTk.PhotoImage(image)
                image = self.agent_img_l.resize((int(x2 - x1), int(y2 - y1)), Image.NEAREST)
                self.robot_img_l = ImageTk.PhotoImage(image)
                image = self.agent_img_u.resize((int(x2 - x1), int(y2 - y1)), Image.NEAREST)
                self.robot_img_u = ImageTk.PhotoImage(image)
                image = self.agent_img_d.resize((int(x2 - x1), int(y2 - y1)), Image.NEAREST)
                self.robot_img_d = ImageTk.PhotoImage(image)
                image = self.agent_img_bump.resize((int(x2 - x1), int(y2 - y1)), Image.NEAREST)
                self.robot_img_bump = ImageTk.PhotoImage(image)
            else:
                self.robot_img_r = ImageTk.PhotoImage(self.agent_img_r)
                self.robot_img_l = ImageTk.PhotoImage(self.agent_img_l)
                self.robot_img_u = ImageTk.PhotoImage(self.agent_img_u)
                self.robot_img_d = ImageTk.PhotoImage(self.agent_img_d)
                self.robot_img_bump = ImageTk.PhotoImage(self.agent_img_bump)

        global current_robot_img
        current_robot_img = self.get_robot_img()
        self.canvas.create_image((x1 + x2) / 2,
                                 (y1 + y2) / 2,
                                 image=current_robot_img,
                                 anchor=CENTER)

    def get_robot_img(self):
        if self.agent.bump:
            return self.robot_img_bump
        return {Direction(Direction.L): self.robot_img_l,
                Direction(Direction.R): self.robot_img_r,
                Direction(Direction.U): self.robot_img_u,
                Direction(Direction.D): self.robot_img_d}.get(self.agent.direction)
