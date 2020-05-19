"""
NAME: Nick Liccini

@brief: Frames and thematic roles are one way to design an agent
that can understand

@detail:
ThematicFrame is an interface for identifying roles in sentences
"""

from common import Frame
from grammar import GrammarTools, QuestionFrame


class Understanding:
    def __init__(self):
        pass

    @staticmethod
    def understand(question, context):
        question = context.clarify(question)

        # Infer the topic of the question
        context.infer_topic(question)
        data_requested = context.topic

        # Infer the object of the question
        question_frame = QuestionFrame(question, context)
        question_object = question_frame.object

        # Generalize the question based on the object
        # generalized_question = GrammarTools.extract_object(question, question_object)
        generalized_question = question

        # Return the working memory frame
        frame = Frame(generalized_question, question_object, data_requested)
        return frame
