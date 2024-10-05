from tkinter import CENTER

from PIL import Image, ImageTk

from trivial_vacuum import *


class TrivVacEnv4Gui(TrivialVacuumEnvironment):
    def __init__(self, agent, canvas, animation_speed, interrupted, score_lbl, done_observer):
        super().__init__()
        self.agent = agent
        self.add_thing(agent)
        self.canvas = canvas
        self.speed = animation_speed
        self.score_lbl = score_lbl
        self.done_observer = done_observer
        self.interrupted = interrupted
        self.steps = 1000
        self.locations = {loc_A: (1, 1), loc_B: (2, 1)}
        self.maze = ["####", "#**#", "####"]
        self.agent_img = Image.open("images/vac.png")
        # flip the image around a vertical axis
        # for horizontal axis use: Image.FLIP_TOP_BOTTOM
        self.agent_img_flip = self.agent_img.transpose(Image.FLIP_LEFT_RIGHT)
        self.robot_img = None
        self.robot_img_flip = None

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
            self.canvas.create_rectangle(0, 0, width, height, fill="black")
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

        maze_height = len(self.maze)

        self.canvas.create_line(width / 2, height / maze_height,
                                width / 2, (2 * height / maze_height),
                                fill="black", width=2)

        for loc in self.locations.keys():
            if self.status.get(loc) == Dirty:
                x, y = self.locations.get(loc)
                self.draw(x, y, 'gray', Dirty)

        x, y = self.locations.get(self.agent.location)

        self.draw(x, y, '', 'agent')

    def is_wall(self, x, y):
        return self.maze[y][x] == '#'

    def draw_wall(self, x, y):
        self.draw(x, y, "black")

    def draw(self, x, y, color, thing=None):
        maze_height = len(self.maze)
        maze_width = len(self.maze[0])
        height = self.canvas.winfo_height() / maze_height
        width = self.canvas.winfo_width() / maze_width

        x1, y1 = (x * width, y * height)
        x2, y2 = (x1 + width, y1 + height)

        if thing is None:
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)
        elif thing == Dirty:
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)
        else:
            if self.robot_img is None:
                width, height = self.agent_img.size
                if width > x2 - x1:
                    image = self.agent_img.resize((int(x2 - x1), int(y2 - y1)), Image.NEAREST)
                    self.robot_img = ImageTk.PhotoImage(image)
                    image = self.agent_img_flip.resize((int(x2 - x1), int(y2 - y1)), Image.NEAREST)
                    self.robot_img_flip = ImageTk.PhotoImage(image)
                else:
                    self.robot_img = ImageTk.PhotoImage(self.agent_img)
                    self.robot_img_flip = ImageTk.PhotoImage(self.agent_img_flip)

            self.canvas.create_image((x1 + x2) / 2,
                                     (y1 + y2) / 2,
                                     image=self.get_robot_img(),
                                     anchor=CENTER)

    def get_robot_img(self):
        if self.agent.location == loc_A:
            return self.robot_img
        else:
            return self.robot_img_flip
