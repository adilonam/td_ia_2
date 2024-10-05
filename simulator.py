from tkinter import *
from tkinter.scrolledtext import ScrolledText

# from tkinter.ttk import Style
from tkinter.ttk import Separator


from comparison import Comparison
from vacuum_2d_gui import *
from trivial_vacuum_gui import TrivVacEnv4Gui
from util import  *  
from agents import * 
from trivial_vacuum import  *
from vacuum2d import *

root = Tk()


# root.style = Style()
# ('clam', 'alt', 'default', 'classic')
# root.style.theme_use("classic")

# #########Boolean object used to interrupt agents #########
class Boolean:
    def __init__(self):
        self.b = False

    def get(self):
        return self.b

    def set(self, v):
        self.b = v


interrupted = Boolean()

##########################################################


root.title('Artificial Intelligence, Unit 2')
root.geometry('{}x{}'.format(800, 600))
root.resizable(False, False)  # disable window resizing

# create all of the main containers
top_frame = Frame(root, width=795, height=50, pady=3)
center = Frame(root, width=795, height=450, padx=3, pady=3)
btm_frame = Frame(root, width=795, height=100, pady=3)

# layout all of the main containers
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

top_frame.grid(row=0, sticky="ew")
center.grid(row=1, sticky="nsew")
btm_frame.grid(row=3, sticky="ew")

# create the widgets for the top frame
simulator_label = Label(top_frame, text='Robot vacuum simulator')
separator1 = Separator(top_frame, orient='vertical')
simulator = IntVar()
R1 = Radiobutton(top_frame, text="trivial", variable=simulator, value=0)
R2 = Radiobutton(top_frame, text="2D(4x4)", variable=simulator, value=1)
R3 = Radiobutton(top_frame, text="2D(6x6)", variable=simulator, value=2)
R4 = Radiobutton(top_frame, text="2D(8x8)", variable=simulator, value=3)
R5 = Radiobutton(top_frame, text="2D(10x10)", variable=simulator, value=4)
simulator.set(0)
separator2 = Separator(top_frame, orient='vertical')

# layout the widgets in the top frame
simulator_label.grid(row=0, column=0)
separator1.grid(row=0, column=1, padx=10, pady=10)
R1.grid(row=0, column=2)
R2.grid(row=0, column=3)
R3.grid(row=0, column=4)
R4.grid(row=0, column=5)
R5.grid(row=0, column=6)

# create the center widgets
center.grid_rowconfigure(0, weight=1)
center.grid_columnconfigure(1, weight=1)

ctr_left = Frame(center, width=200, height=450)
ctr_mid = Frame(center, width=500, height=450, padx=3, pady=3)
ctr_right = Frame(center, width=100, height=450, padx=3, pady=3)

# create the widgets for the left frame
agent_label = Label(ctr_left, text="Agent to run:")
btn1 = Button(ctr_left, text='Simple reflex', bd='5')
btn2 = Button(ctr_left, text='Model-based reflex', wraplength=100, justify=LEFT, bd='5')
btn3 = Button(ctr_left, text='Random agent', bd='5')
btn4 = Button(ctr_left, text='Compare all', bd='5')
# btn5 = Button(ctr_left, text='Advanced Model-based', wraplength=100, justify=LEFT, bd='5')

# create the widgets for the right frame

btn_interrupt = Button(ctr_right, text='Interrupt agent', command=lambda: interrupt())
btn_interrupt['state'] = 'disabled'
label_animation = Label(ctr_right, text='Animation speed:')
animation_speed = Scale(ctr_right, from_=2, to=1000, orient=HORIZONTAL)
animation_speed.set(750)
text_score_lbl = Label(ctr_right, text='Score obtained by ', bd='5')
lbl1 = Label(ctr_right, text='Simple reflex', bd='5')
score_lbl1 = Label(ctr_right, text='0', bd='5')
lbl2 = Label(ctr_right, text='Model-based reflex', wraplength=100, justify=LEFT, bd='5')
score_lbl2 = Label(ctr_right, text='0', bd='5')
lbl3 = Label(ctr_right, text='Random agent', bd='5')
score_lbl3 = Label(ctr_right, text='0', bd='5')

# create the widgets for the center frame
canvas = Canvas(ctr_mid, bg='#A39449', width=420, heigh=420)
# create the widgets for the bottom frame
text_box = ScrolledText(btm_frame, wrap=WORD,
                        width=97,
                        height=6,
                        font=("Times New Roman", 15))

text_box.tag_configure('bold_italics', font=('Verdana', 12, 'bold', 'italic'))

# layout the widgets in the left frame
agent_label.grid(row=0, column=0, sticky=W + E)
btn1.grid(row=1, column=0, sticky=W + E)
btn2.grid(row=2, column=0, sticky=W + E)
btn3.grid(row=3, column=0, sticky=W + E)
# btn4.grid(row=4, column=0, sticky=W + E)
btn4.grid(row=5, column=0, sticky=W + E)

# layout the widgets in the right frame


btn_interrupt.grid(row=0, column=0, sticky=W + E)
label_animation.grid(row=1, column=0, sticky=W + E)
animation_speed.grid(row=2, column=0, sticky=W + E)
text_score_lbl.grid(row=3, column=0, sticky=W + E)
lbl1.grid(row=4, column=0, sticky=W + E)
score_lbl1.grid(row=5, column=0, sticky=W + E)
lbl2.grid(row=6, column=0, sticky=W + E)
score_lbl2.grid(row=7, column=0, sticky=W + E)
lbl3.grid(row=8, column=0, sticky=W + E)
score_lbl3.grid(row=9, column=0, sticky=W + E)

# layout the widgets in the center frame
canvas.grid(row=0, column=0)

# layout the widgets in the bottom frame
text_box.grid(row=0, column=0, sticky="nsew")

ctr_left.grid(row=0, column=0, sticky="ns")
ctr_mid.grid(row=0, column=1, sticky="nsew")
ctr_right.grid(row=0, column=2, sticky="ns")


# Widget Event Processing
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def trace_agent(agent):
    old_program = agent.program

    def new_program(perception):
        action = old_program(perception)
        if hasattr(agent, 'name'):
            text_box.insert(END,
                            ("%s percepts %s, and act by %s\n" %
                             (agent.name, perception, action)))
        else:
            text_box.insert(END,
                            ("%s percepts %s, and act by %s\n" %
                             (agent, perception, action)))
        return action

    agent.program = new_program


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


def run_env(agent, env):
    trace_agent(agent)
    env.run()


def interrupt():
    global interrupted
    interrupted.set(True)
    enable_btns()


def disable_btns():
    canvas.delete('all')
    interrupted.set(False)
    btn1['state'] = 'disabled'
    btn2['state'] = 'disabled'
    btn3['state'] = 'disabled'
    btn4['state'] = 'disabled'
    btn_interrupt['state'] = 'normal'


def enable_btns():
    btn1['state'] = 'normal'
    btn2['state'] = 'normal'
    btn3['state'] = 'normal'
    btn4['state'] = 'normal'
    btn_interrupt['state'] = 'disabled'
    text_box.delete('1.0', END)


def run_s_reflex_agent(event=None):
    disable_btns()
    if simulator.get() == 0:
        agent = TrivialReflexVacuumAgent()
        env = TrivVacEnv4Gui(agent, canvas, animation_speed, interrupted, score_lbl1, enable_btns)
    else:
        agent = ReflexVacuumAgent()
        env = VacEnv4Gui(agent, canvas, animation_speed, interrupted, score_lbl1, simulator.get(), enable_btns)
    run_env(agent, env)


btn1.bind('<Button-1>', run_s_reflex_agent)
btn_interrupt.bind('<Button-1>', run_s_reflex_agent)


def run_mb_reflex_agent(event=None):
    disable_btns()

    if simulator.get() == 0:
        agent = TrivialModelbasedReflexVacuumAgent()
        env = TrivVacEnv4Gui(agent, canvas, animation_speed, interrupted, score_lbl2, enable_btns)
    else:
        agent = ModelBasedVacuumAgent()
        env = VacEnv4Gui(agent, canvas, animation_speed, interrupted, score_lbl2, simulator.get(), enable_btns)
    run_env(agent, env)


btn2.bind('<Button-1>', run_mb_reflex_agent)


def run_random_agent(event=None):
    disable_btns()
    if simulator.get() == 0:
        agent = TrivialRandomAgent()
        env = TrivVacEnv4Gui(agent, canvas, animation_speed, interrupted, score_lbl3, enable_btns)
    else:
        agent = RandomVacuumAgent()
        env = VacEnv4Gui(agent, canvas, animation_speed, interrupted, score_lbl3, simulator.get(), enable_btns)
    run_env(agent, env)


btn3.bind('<Button-1>', run_random_agent)


def run_compare(event=None):
    disable_btns()
    comp = Comparison(canvas, interrupted, enable_btns)
    comp.run()


btn4.bind('<Button-1>', run_compare)

root.mainloop()
