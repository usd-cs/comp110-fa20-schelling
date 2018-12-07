"""
Module: segregation

Implementation of Schelling's Model of Segregation
"""
import random
from tkinter import *
from tkinter.font import Font
from time import sleep

SATISFACTION_LEVEL = 0.5

class Agent:
    """
    An agent in our world. Has a type and a location.
    """

    def __init__(self, agent_type, location):
        self.x = location[0]
        self.y = location[1]
        self.type = agent_type

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
        return percent_similar >= SATISFACTION_LEVEL

    def move_to(self, x, y):
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
        # step 1: add agent's current location to open_spots
        # step 2: update grid so agent is located at new spot
        # step 3: update grid so agent's old location is cleared (None)
        # step 4: update agent's location using its move_to method
        return

    def display_turn(self):
        """ Updates our GUI to show where agents are located now. """
        fonty = Font(family="Times", size=-40)
        self.canvas.delete(ALL) # erase all old drawings

        for y in range(self.height):
            for x in range(self.width):
                val = self.grid[y][x]
                if val is not None:
                    self.canvas.create_text(50*x+25, 50*y+25, text=val.type,
                                            font=fonty)

    def print_world(self, turn_number):
        """ Print out the world. """
        print("\nTurn: " + str(turn_number))
        for y in range(self.height):
            for x in range(self.width):
                val = self.grid[y][x]
                if val is not None:
                    print(val.type, end='')
                else:
                    print(" ", end='')
            print()
        print()


def create_window():
    """ Returns a new GUI window. """
    root = Tk()
    root.title("Schelling's Model of Segregation")

    # make sure this pops in front of all other windows
    root.lift()
    root.attributes("-topmost", True)
    return root


def simulate(num_turns, world_width, world_height, num_agents):
    """ Perform simulation of a world with num_agents for num_turns turns. """

    top = create_window()

    world = World(world_width, world_height, top)

    # create and randomly place agents. Assume half of each type.
    for i in range(num_agents):
        if i < num_agents * 0.75:
            agent_type = "X"
        else:
            agent_type = "O"

        agent_loc = world.get_open_spot()
        agent = Agent(agent_type, agent_loc)
        world.add_agent(agent, agent_loc)

    # perform all turns of the simulation
    for turn in range(num_turns):
        #world.print_world(turn)
        world.display_turn()
        for agent in world.agents:
            if not agent.is_satisfied(world):
                x, y = world.get_open_spot()
                world.move_agent(agent, x, y)

        # redraw window and wait for 250 ms so we can see each turn
        top.update_idletasks()
        top.update()
        sleep(0.25)

    #print(len(world.open_spots))
    top.mainloop()

if __name__ == "__main__":
    simulate(30, 10, 10, 75)
