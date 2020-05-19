"""
StudentAgent - Updated 08/31/2018

DO NOT CHANGE THIS FILE
"""

import common
import StudentAgent


class AgentInterface:

    def __init__(self, verbose):
        self._student_agent = StudentAgent.StudentAgent(verbose)
        return

    # input_output(question : string) :        response : string
    #      question  =  string from user (will not have ? at end)(no case guarantee)
    #      response = agent.ReturnDictionary
    def input_output(self, question):
        _word_list = common.ParseQuestion(question)
        _qobject, _data_requested = self._student_agent.input_output(_word_list)
        return common.Frame(question, _qobject, _data_requested)
