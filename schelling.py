"""
Module: schelling

Implementation of Schelling's Model of Segregation

Author: Sat Garcia (sat@sandiego.edu)... and YOU?
"""
import random
from tkinter import *
from tkinter.font import Font
from time import sleep

class Agent:
    """
    An agent in our world. Has a type, location, and satisfaction level.
    """

    def __init__(self, agent_type, location, satisfaction):
        self.x = location[0]
        self.y = location[1]
        self.type = agent_type
        self.satisfaction_level = satisfaction

    def is_satisfied(self, world):
        """
        Returns True if this agent is satisfied, False otherwise.
        An agent is considered satisfied if at least n% of its neighbors have
        the same type.
        """
        num_same = 0
        num_diff = 0

        for i in range(-1, 2):
            for j in range(-1, 2):
                # check for neighbors, avoid invalid world locations and
                # our self
                if (self.x + i) in range(0, world.width) \
                and (self.y + j) in range(0, world.height) \
                and (i, j) != (0, 0):
                    neighbor = world.get_agent((self.x+i, self.y+j))
                    if neighbor is not None:
                        if neighbor.type == self.type:
                            num_same += 1
                        else:
                            num_diff += 1

        # calculate the percentage of neighbors that are similar to this
        # agent.
        num_neighbors = num_same + num_diff
        if num_neighbors == 0:
            percent_similar = 1.0
        else:
            percent_similar = num_same / (num_same + num_diff)
        return percent_similar >= self.satisfaction_level

    def set_location(self, x, y):
        """ Changes the location of this agent. """
        self.x = x
        self.y = y

    def get_location(self):
        """ Returns the (x, y) location of this agent. """
        return (self.x, self.y)


class World:
    """
    Representation of a 2D grid world containing agents.
    """

    def __init__(self, width, height, window):
        self.width = width
        self.height = height
        self.grid = [[None] * width for _ in range(height)]

        # start with no agents and every spot in the world is open
        self.agents = []
        self.open_spots = [(x, y) for x in range(width)
                           for y in range(height)]

        # creates a GUI for us to draw our world on
        self.window = window
        self.canvas = Canvas(window, bg="green", height=(50*height),
                             width=(50*width), bd=0, relief='sunken',
                             highlightthickness=0)
        self.canvas.pack()

    def get_open_spot(self):
        """ Returns a random open spot in the world. """
        location = random.choice(self.open_spots)
        self.open_spots.remove(location)
        return location

    def add_agent(self, agent, location):
        """ Places a new agent in the world at the given location. """
        self.agents.append(agent)
        self.grid[location[1]][location[0]] = agent

    def get_agent(self, location):
        """ Returns the agent at the given location, or None if one isn't
        there. """
        return self.grid[location[1]][location[0]]

    def move_agent(self, agent, new_x, new_y):
        """ Moves the given agent from their corrent location to their new,
        given location, (new_x, new_y). """

        # TODO: Implement this function.

        # Step 1: Append agent's current location this world's (i.e. self's)
        # open_spots. Note: You can use the agent's get_location method as 
        # part of your solution.

        pass # replace this line with step 1's implementation

        # Step 2: Assign agent to new_x, new_y in this world's grid.
        # Caution: Make sure you get the order of new_x and new_y right.

        pass # replace this line with step 2's implementation

        # Step 3: Update this world's grid so agent's old location is cleared
        # (i.e. set to None). Note: agent.x and agent.y are the agent's old
        # location.

        pass # replace this line with step 3's implementation

        # Step 4: Update agent's location using its set_location method.

        pass # replace this line with step 4's implementation


    def display_turn(self, turn_number):
        """ Updates our GUI to show where agents are located now. """
        fonty = Font(family="Times", size=-40)
        self.canvas.delete(ALL) # erase all old drawings
        self.window.title("Schelling's Segregation Simulator (Turn: " + str(turn_number) + ")")

        for y in range(self.height):
            for x in range(self.width):
                val = self.grid[y][x]
                if val is not None:
                    self.canvas.create_text(50*x+25, 50*y+25, text=val.type,
                                            font=fonty)


def create_window():
    """ Returns a new GUI window. """
    root = Tk()
    root.title("Schelling's Segregation Simulator")

    # make sure this pops in front of all other windows
    root.lift()
    root.attributes("-topmost", True)
    return root


def create_and_place_agents(world, num_agents, satisfaction_level):
    """ Creates agents and randomly places them in the world. """
    for i in range(num_agents):
        if i < num_agents * 0.5:
            agent_type = "X"
        else:
            agent_type = "O"

        agent_loc = world.get_open_spot()
        agent = Agent(agent_type, agent_loc, satisfaction_level)
        world.add_agent(agent, agent_loc)


def simulate(num_turns, world_width, world_height, num_agents,
             satisfaction_level):
    """ Perform simulation of a world with num_agents for num_turns turns. """

    top = create_window()

    # create world and randomly place agents in the world
    world = World(world_width, world_height, top)
    create_and_place_agents(world, num_agents, satisfaction_level)

    # perform all turns of the simulation
    for turn in range(num_turns):
        world.display_turn(turn)
        for agent in world.agents:
            if not agent.is_satisfied(world):
                x, y = world.get_open_spot()
                world.move_agent(agent, x, y)

        # redraw window and wait for 250 ms so we can see each turn
        top.update_idletasks()
        top.update()
        sleep(0.25)

    top.mainloop()

def get_validated_number(prompt, min_val, max_val):
    """ Returns a user-inputted integer between the min_val and max_val. """
    val = int(input(prompt))

    while val < min_val or val > max_val:
        print("Invalid input. Try again.")
        val = int(input(prompt))

    return val

if __name__ == "__main__":
    num_agents = get_validated_number("Enter the number of agents (1 - 100): ", 1, 100)
    level = get_validated_number("Enter satisfaction_level (0 - 100): ", 0, 100)

    # run 10x10 world simulation for 100 turns
    simulate(50, 10, 10, num_agents, level/100)
