"""
StudentAgent - Project 2 Updated 09/25/2018

DO NOT CHANGE THIS FILE
"""

import StudentAgent

class AgentInterface:
    def __init__(self, verbose):
        self._student_agent = StudentAgent.StudentAgent(verbose)
        return

    def ParseQuestion(self, question):
        return question.lower().split(' ')

    # input_output(question : string) :        response : int
    def input_output(self, question):
        _word_list = self.ParseQuestion(question)
        _intent = self._student_agent.input_output(_word_list)
        return _intent
