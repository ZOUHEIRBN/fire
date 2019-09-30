from mesa import Agent, Model
from mesa.time import RandomActivation
import sys
sys.path.append('..')
from video import Server
import time

class AlertAgent(Agent):
    """An agent with fixed initial wealth."""
    def __init__(self, unique_id, model, threshold_lv=.5):
        super(AlertAgent, self).__init__(unique_id, model)
        self.safety_factor = 50
        self.safety_threshold = threshold_lv
        self.message = ''

    def fetch(self):
        a = self.model.server.RTData.state
        self.safety_factor = int(a["Fire"])
        #print(self.safety_factor)

    def set_threshold(self, threshold):
        self.safety_threshold = threshold

    def step(self):
        self.fetch()
        d = self.safety_factor
        if d < self.safety_threshold:
            self.message = "This is agent no: {:04} signaling danger!".format(self.unique_id)


class FetchAgent(AlertAgent):
    def __init__(self,unique_id, model, func, threshold_lv=.5, dng_classes=3):
        super(FetchAgent, self).__init__(unique_id, model, threshold_lv)
        self.fetch_func = func
        self.message = ''
        self.dng_classes = dng_classes

    def fetch(self):
        self.safety_factor = self.fetch_func()

    def step(self):
        #Classifier here
        self.fetch()
        d = int(self.safety_factor/(100/self.dng_classes))
        if d == 0:
            self.message = ''
        else:
            self.message = 'DECLARED CLASS {:02} DANGER!! '.format(d)
        time.sleep(1)

class DialAgent(AlertAgent):
    def __init__(self,unique_id, model, threshold_lv=.5):
        super(DialAgent, self).__init__(unique_id, model, threshold_lv)
        self.emergency_num = '0645538791'

    def reflex(self):
        print("Calling {} ...".format(self.emergency_num))

class AlertSystem(Model):
    """A model with some number of agents."""

    def __init__(self, server=None):
        self.agents = [AlertAgent, DialAgent]
        self.schedule = RandomActivation(self)
        if server is not None:
            self.server = server
        else:
            self.server = Server(system=self)
        # Create agents
        for i, ag in enumerate(self.agents):
            a = ag(i, self)
            self.schedule.add(a)

    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()

