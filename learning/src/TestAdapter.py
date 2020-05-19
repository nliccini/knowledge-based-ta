'''
This adapter is for prototyping classifiers
'''


class TestAdapter:
    """ Test adapter """
    def __init__(self, training_data):
        self._engine_name = "Project3"
        self._training_data = training_data

    def get_engine(self):
        """ Get engine name """
        return self._engine_name

    def ask_question(self, question):
        """
            returns {
                        'question':question,
                        'label':confidence
                    }
        """
        d_of_intents_confidence = {'question':question}
        label,confidence = self._your_classifier(question)
        d_of_intents_confidence[label] = confidence
        return d_of_intents_confidence

    def _your_classifier(self, question):
        """
        :param question: A question to analyze
        :return: label, confidence tuple representing the inferred label and confidence score of that label
        """
        '''Score how well the question matches each concept'''
        scores = dict()
        for label, concept in self._training_data.items():
            score = concept.classify(question)
            scores[label] = score

        '''Get the label with highest confidence'''
        result = 'UNKNOWN'
        confidence = 0.0
        for label, score in scores.items():
            if score > confidence:
                result = label
                confidence = score

        return result, confidence
