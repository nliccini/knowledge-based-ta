"""
NAME: Nick Liccini

@brief: An agent that uses contextual details and knowledge of the
structure of questions to understand the topic of the question and
the object of the question

@detail:
CS4635Context provides one implementation of a Context for the course CS 4635

StudentAgent is the agent that performs tasks using its Knowledge
"""

from grammar import QuestionFrame
from knowledge import Knowledge, Context


class CS4635Context(Context):
    def __init__(self):
        super().__init__()
        self.keywords['DUEDATE'] = ['when', 'what', 'due', 'day', 'date', 'time', 'submit', 'turn', 'until',
                                    'week', 'month', 'dates', 'complete', 'finish', 'upload']
        self.keywords['RELEASEDATE'] = ['how', 'when', 'what', 'time', 'released', 'release', 'announced', 'available',
                                        'access', 'work', 'open', 'start', 'early', 'check', 'day', 'week', 'month',
                                        'date', 'assigned', 'assign', 'dates', 'begin', 'download']
        self.keywords['WEIGHT'] = ['how', 'what', 'worth', 'much', 'grade', 'weight', 'weigh', 'affect', 'effect',
                                   'average', 'distribution', 'important', 'importance']
        self.keywords['PROCESS'] = ['how', 'what', 'where', 'submission', 'submit', 'submitted', 'complete', 'turn',
                                    'site', 'process', 'Canvas', 'upload', 'download', 'uploaded', 'downloaded',
                                    'procedure', 'submitting', 'website', 'webpage', 'class', 'acquire', 'acquired',
                                    'place', 'location']
        self.keywords['DURATION'] = ['how', 'when', 'long', 'time', 'much', 'until', 'work', 'complete', 'turn',
                                     'spend', 'till', 'day', 'week', 'month', 'duration', 'days', 'weeks',
                                     'months', 'longer']

        self.preferences['DUEDATE'] = ['when', 'due', 'complete']
        self.preferences['RELEASEDATE'] = ['when', 'release', 'begin']
        self.preferences['WEIGHT'] = ['what', 'weight', 'worth']
        self.preferences['PROCESS'] = ['how', 'what', 'process', 'site']
        self.preferences['DURATION'] = ['how', 'duration', 'long', 'until']


class StudentAgent:
    def __init__(self, verbose):
        self._verbose = verbose

        self.knowledge = Knowledge()
        self.knowledge.add_to_memory(CS4635Context())

    # Takes in list of words, returns question_object and data_requested
    def input_output(self, word_list):
        context = self.knowledge.infer_context(word_list)

        context.infer_topic(word_list)
        _data_requested = context.topic

        qframe = QuestionFrame(word_list, context)
        _question_object = qframe.object

        return _question_object, _data_requested

