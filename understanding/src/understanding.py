"""
NAME: Nick Liccini

@brief: Frames and thematic roles are one way to design an agent
that can understand

@detail:
ThematicFrame is an interface for identifying roles in sentences
"""


class ThematicFrame:
    def __init__(self):
        self.slots = {'verb': '',
                      'agent': '',
                      'beneficiary': '',
                      'source': '',
                      'instrument': '',
                      'location': '',
                      'conveyance': '',
                      'duration': '',
                      'destination': '',
                      'thematic_object': ''
                      }
        self.constraints = {'by': ['agent', 'conveyance', 'location'],
                            'for': ['beneficiary', 'duration'],
                            'from': ['source'],
                            'with': ['coagent', 'instrument'],
                            'to': ['destination']
                            }

