"""
Agent helper function V083118

DO NOT CHANGE THIS FILE
"""


# Please read project directions before importing anything


#
# Common classes
#
class Frame:
    # qobject = the object of the question
    # datarequested = the data about the object, the question is asking
    def __init__(self, question, qobject, datarequested):
        self._question = question
        self._qobject = qobject
        self._datarequested = datarequested
        self._frame_dictionary = {
                                    'question': self._question,
                                    'object': self._qobject,
                                    'data_requested': self._datarequested
                                 }
        self.CheckDataType()

    @classmethod
    def fromDict(cls, frameDict):
        return cls(frameDict['question'],
                   frameDict['object'],
                   frameDict['data_requested'])

    def print(self, what='all'):
        if 'all' in what:
            output = self._question+"|"+self._qobject+"|"+self._datarequested
        if 'qd' in what:
            output = "|"+self._qobject+"|"+self._datarequested
        return output

    def CheckDataType(self):
        data_types = GetListOfRequestTypes()
        if self._datarequested not in data_types:
            raise ValueError('INVALID data type')

    def GetDictionary(self): return self._frame_dictionary

    def GetData(self):
        return self._question, self._qobject, self._datarequested

    def CompareQObject(self, qobject):
        if qobject == self._qobject:
            return 1.0
        return 0.0

    def CompareDataRequested(self, datarequested):
        if datarequested == self._datarequested:
            return 1.0
        return 0.0

    # Call this function to compare dictionaries
    def CompareDicts(self, frameDict):
        qobject_score = self.CompareQObject(frameDict['object'])
        dr_score = self.CompareDataRequested(frameDict['data_requested'])
        return ((qobject_score, dr_score))

    # Call this function to compare Frame Objects
    def CompareObject(self, frameObject):
        return self.CompareDicts(frameObject.GetDictionary())

    # Generic comapare
    def Compare(self, frame):
        try:
            a = frame['qobject']
            return self.CompareDicts(frame)
        except TypeError:
            return self.CompareObject(frame)


#
# Common functions
#

# datarequested = the data about the object, the question is asking
def GetListOfRequestTypes():
    return ['DUEDATE', 'RELEASEDATE', 'WEIGHT', 'PROCESS', 'DURATION']


def ParseQuestion(question):
    return question.lower().split(' ')
