"""
NAME: Nick Liccini

@brief: The domain knowledge for CS4635

@detail: The domain knowledge consists of an understanding component
given by 'keywords' and 'preferences', and a classification component
given by 'knowledge' which is made up of experience and reference
information, both of which are subclasses of Case
"""

from knowledge import Context
from cognition import Case
from grammar import GrammarTools
from utils import compare_words, convert_numerals, remove_numerals


class CS4635Experience(Case):
    def __init__(self, label, question, answer, obj, category):
        super().__init__()
        self.label = label
        self.question = GrammarTools.str2words(question)
        self.answer = answer
        self.object = obj
        self.category = category

    def compare(self, to_comp):
        question, obj, category = to_comp

        # Convert the input to a comparable format
        object_words = GrammarTools.str2words(obj)
        my_object_words = GrammarTools.str2words(self.object)
        object_words = convert_numerals(object_words)
        my_object_words = convert_numerals(my_object_words)

        # Compare the objects
        obj_score = compare_words(object_words, my_object_words)

        # Compare the categories
        # If the category is GENERAL, it doesn't matter what the input is
        if self.category == 'GENERAL' or self.category == category:
            cat_score = 1.0
        else:
            cat_score = 0.0

        # Return the comparison result
        match = False
        similarity_score = obj_score*0.50 + cat_score*0.50
        if obj_score > 0.51 and cat_score == 1.0:
            match = True
        return match, similarity_score


class CS4635Information(Case):
    def __init__(self, label, subject, releasedate, duedate, duration, weight, process, banned):
        super().__init__()
        self.label = label
        self.subject = convert_numerals(subject.split(' '))
        self.duedate = duedate
        self.releasedate = releasedate
        self.duration = duration
        self.process = process
        self.weight = weight
        self.banned = banned
        self.everything = subject + ' ' + releasedate + ' ' + duedate + ' ' + duration + ' ' + weight + ' ' + process
        self.everything = self.everything.split(' ')

        self.labels = {'RELEASEDATE': label, 'DUEDATE': label+8, 'DURATION': label+16,
                       'WEIGHT': label+24, 'PROCESS': label+32}

        # Infer how long the subject is open
        words = releasedate.split(' ')
        runits = 'weeks'
        if 'day' in words or 'days' in words:
            runits = 'days'
        start = 0
        for word in words:
            if word.isnumeric():
                start = int(word)
                break

        words = duration.split(' ')
        dunits = 'weeks'
        if 'day' in words or 'days' in words:
            dunits = 'days'
        delta = 0
        for word in words:
            if word.isnumeric():
                delta = int(word)
                break

        end = start
        if runits == 'weeks' and dunits == 'weeks':
            end = start + delta
        elif runits == 'weeks' and dunits == 'days':
            end = start + 7*delta
        elif runits == 'days' and dunits == 'weeks':
            end = int(start/7) + delta
        elif runits == 'days' and dunits == 'days':
            end = int(start/7) + 7*delta

        self.weeks_available = list()
        for i in range(int(start), int(end)):
            self.weeks_available.append(i)
        self.weeks_available.append(end)

        self.releasedate = self.weeks_available[0]
        self.duedate = self.weeks_available[len(self.weeks_available)-1]

        # Add this range to self.everything
        for i in self.weeks_available:
            self.everything.append(str(i))

    def compare(self, to_comp):
        """
        Function to compare this information case to query data. Uses procedural knowledge
        rules to evaluate the similarity of query data to this case

        :param to_comp: query case: (question <list<str>>, object <list<str>>, category <str>)
        :return: (match, similarity_score)
        """
        question, obj, category = to_comp
        question = convert_numerals(question)
        obj = convert_numerals(obj.split(' '))

        # Check if there are any banned words for this case
        for word in question:
            if word in self.banned:
                return False, 0.0

        # Check if the object is the subject
        subject_similarity = compare_words(obj, self.subject)

        # If the object is not similar enough to the subject, check the rest of the question for relevance
        absolute_relevance = 0.0
        if subject_similarity < 0.51:
            # If this subject is in the question, there is a match
            for word in remove_numerals(self.subject):
                if word in question:
                    subject_similarity = len(self.subject) / len(question)
                    break
            # If the object is in any way related to this case, there is reason to continue comparing
            if subject_similarity < 0.51:
                for word in obj:
                    if word in self.everything:
                        absolute_relevance = 1 / len(self.everything)
                        break
        else:
            self.label = self.labels[category]
            return True, subject_similarity

        # If there is absolutely no relevance between this case and the query, skip it
        if subject_similarity == 0.0 and absolute_relevance == 0.0:
            return False, 0.0

        # Compute the subscore for each category
        # Get the week that the question is querying
        query = 0
        for i in range(len(question) - 1):
            if question[i] == 'week':
                if question[i-1].isnumeric():
                    query = int(question[i-1])
                    break
                if question[i+1].isnumeric():
                    query = int(question[i+1])
                    break

        subscores = []
        subscore_types = ['RELEASEDATE', 'DUEDATE', 'DURATION', 'WEIGHT', 'PROCESS']
        for subscore in subscore_types:
            similarity_score = 0.0
            if subscore == 'RELEASEDATE':
                if category == 'DUEDATE':
                    similarity_score = 0.0
                elif 'download' in question:
                    if self.releasedate == query:
                        similarity_score = 1.0
                elif self.releasedate <= query <= self.duedate:
                    similarity_score = 1.0
            elif subscore == 'DUEDATE':
                if category == 'RELEASEDATE':
                    similarity_score = 0.0
                elif query == self.duedate:
                    similarity_score = 1.0
            elif subscore == 'DURATION':
                duration_query = 0
                for i in range(len(question)):
                    if question[i] == 'week' or question[i] == 'weeks':
                        if question[i-1].isnumeric():
                            duration_query = int(question[i-1])
                            break
                if duration_query == len(self.weeks_available)-1:
                    similarity_score = 1.0
            elif subscore == 'WEIGHT':
                similarity_score = compare_words(obj, self.weight.split(' '))
            else:
                similarity_score = compare_words(obj, self.process.split(' '))
            subscores.append(similarity_score)

        similarity_score = max(subscores)

        # Return the comparison result (match, max(subscores))
        self.label = self.labels[category]
        if similarity_score > 0.51:
            return True, similarity_score
        return False, similarity_score


class CS4635Domain:
    def __init__(self):
        self.keywords = dict()
        self.keywords['RELEASEDATE'] = ['how', 'when', 'what', 'time', 'released', 'release', 'announced', 'available', 'access', 'work', 'open', 'start', 'early', 'check', 'day', 'week', 'month', 'date', 'assigned', 'assign', 'dates', 'begin', 'download', 'submissions', 'open', 'beginning', 'start', 'starting', 'beginning']
        self.keywords['DUEDATE'] = ['when', 'what', 'due', 'day', 'date', 'time', 'submit', 'turn', 'until', 'week', 'month', 'dates', 'complete', 'finish', 'upload', 'submissions', 'need', 'submitted', 'completed', 'close', 'required', 'require']
        self.keywords['WEIGHT'] = ['how', 'what', 'worth', 'much', 'grade', 'weight', 'weigh', 'affect', 'effect', 'average', 'distribution', 'important', 'importance']
        self.keywords['PROCESS'] = ['how', 'what', 'where', 'submission', 'submit', 'submitted', 'complete', 'turn', 'site', 'process', 'Canvas', 'upload', 'download', 'uploaded', 'downloaded', 'procedure', 'submitting', 'website', 'webpage', 'acquire', 'acquired', 'place', 'location']
        self.keywords['DURATION'] = ['how', 'when', 'long', 'time', 'much', 'until', 'work', 'complete', 'turn', 'spend', 'till', 'day', 'week', 'month', 'duration', 'days', 'weeks', 'months', 'longer']

        self.preferences = dict()
        self.preferences['RELEASEDATE'] = ['when', 'release', 'begin']
        self.preferences['DUEDATE'] = ['when', 'due', 'complete']
        self.preferences['WEIGHT'] = ['what', 'weight', 'worth']
        self.preferences['PROCESS'] = ['how', 'what', 'where', 'process', 'site']
        self.preferences['DURATION'] = ['how', 'duration', 'long', 'until']

        self.reaction = CS4635Experience(0, 'when will assignment 4 be released', 'i do not know', '', '')

        self.knowledge = set()
        self.knowledge.add(self.reaction)
        self.knowledge.add(CS4635Experience(1, 'when will assignment 1 be released', 'assignment 1 will be available in the second week', 'assignment 1', 'RELEASEDATE'))
        self.knowledge.add(CS4635Experience(2, 'when can we begin working on​ project 1', 'You can download project 1 during week 3', 'project 1', 'RELEASEDATE'))
        self.knowledge.add(CS4635Experience(3, 'when can we start on ​assignment 2', 'assignment 2 will be released on week 6', 'assignment 2', 'RELEASEDATE'))
        self.knowledge.add(CS4635Experience(4, 'what week is the ​midterm', 'the midterm occurs in week 7', 'midterm', 'RELEASEDATE'))
        self.knowledge.add(CS4635Experience(5, 'when can i download​ project 2', 'Project 2 will be distributed in week 8', 'project 2', 'RELEASEDATE'))
        self.knowledge.add(CS4635Experience(6, 'What week does ​assignment 3​​ start', 'Assignment 3 starts in week 11', 'assignment 3', 'RELEASEDATE'))
        self.knowledge.add(CS4635Experience(7, 'when can we begin working on ​project 3', 'Project 3 will be available in week 13', 'project 3', 'RELEASEDATE'))
        self.knowledge.add(CS4635Experience(8, 'when will the​ final​​ open', 'The final occurs in week 16', 'final', 'RELEASEDATE'))
        self.knowledge.add(CS4635Experience(9, 'when is ​assignment 1 ​​due', 'Assignment 1 is due at the start of week 3', 'assignment 1', 'DUEDATE'))
        self.knowledge.add(CS4635Experience(10, 'when will ​project 1​​ need to be submitted', 'Project 1 must be turned in at the beginning of week 6', 'project 1', 'DUEDATE'))
        self.knowledge.add(CS4635Experience(11, 'when will i need to submit ​assignment 2', 'Assignment 2 must be submitted at the start of week 7', 'assignment 2', 'DUEDATE'))
        self.knowledge.add(CS4635Experience(12, 'when is the ​midterm​​ due', 'The midterm must be completed by the end of week 7', 'midterm', 'DUEDATE'))
        self.knowledge.add(CS4635Experience(13, 'when should we have ​project 2​​ completed by', 'Project 2 must be submitted by the end of week 11', 'project 2', 'DUEDATE'))
        self.knowledge.add(CS4635Experience(14, 'when do I need to turn in​ assignment 3', 'Assignment 3 is due by the end of week 12', 'assignment 3', 'DUEDATE'))
        self.knowledge.add(CS4635Experience(15, 'when will submissions close for ​project 3', 'Project 3 must be submitted by the end of week 16', 'project 3', 'DUEDATE'))
        self.knowledge.add(CS4635Experience(16, 'when do I need to turn in the ​final', 'The final is due at the end of week 16', 'final', 'DUEDATE'))
        self.knowledge.add(CS4635Experience(17, 'how much time is there for submitting ​assignment 1', '1 week', 'assignment 1', 'DURATION'))
        self.knowledge.add(CS4635Experience(18, 'how long do we have to complete​ project 1', '3 weeks', 'project 1', 'DURATION'))
        self.knowledge.add(CS4635Experience(19, 'how long do we have to finish ​assignment 2', '1 week', 'assignment 2', 'DURATION'))
        self.knowledge.add(CS4635Experience(20, 'how long do we have to complete the ​midterm', '1 week', 'midterm', 'DURATION'))
        self.knowledge.add(CS4635Experience(21, 'how long do we have to do ​project 2', '3 weeks', 'project 2', 'DURATION'))
        self.knowledge.add(CS4635Experience(22, 'how many weeks to write​ assignment 3', '1 week', 'assignment 3', 'DURATION'))
        self.knowledge.add(CS4635Experience(23, 'how many weeks to code ​project 3', '3 weeks', 'project 3', 'DURATION'))
        self.knowledge.add(CS4635Experience(24, 'how many weeks to complete the​ final', '1 week', 'final', 'DURATION'))
        self.knowledge.add(CS4635Experience(25, 'what percentage of my grade is ​assignment 1 ​​worth', '4% of final grade', 'assignment 1', 'WEIGHT'))
        self.knowledge.add(CS4635Experience(26, 'how much is​ project 1​​ worth', '15% of final grade', 'project 1', 'WEIGHT'))
        self.knowledge.add(CS4635Experience(27, 'what is the weight of ​assignment 2', '4% of final grade', 'assignment 2', 'WEIGHT'))
        self.knowledge.add(CS4635Experience(28, 'how much will the ​midterm​​ be worth', '15% of final grade', 'midterm', 'WEIGHT'))
        self.knowledge.add(CS4635Experience(29, 'what percentage of the total grade is ​project 2', '15% of final grade', 'project 2', 'WEIGHT'))
        self.knowledge.add(CS4635Experience(30, 'how much does ​assignment 3​​ contribute to my grade', '4% of final grade', 'assignment 3', 'WEIGHT'))
        self.knowledge.add(CS4635Experience(31, 'how much is​ project 3​​ contributing to my grade', '15% of final grade', 'project 3', 'WEIGHT'))
        self.knowledge.add(CS4635Experience(32, 'how much is the​ final​​ worth', '20% of grade', 'final', 'WEIGHT'))
        self.knowledge.add(CS4635Experience(33, 'what is the process for submitting ​assignment 1', 'Turn in to Canvas as PDF', 'assignment 1', 'PROCESS'))
        self.knowledge.add(CS4635Experience(34, 'what is the process of submitting ​project 1', 'Turn in code as zip file, and report as pdf into Canvas', 'project 1', 'PROCESS'))
        self.knowledge.add(CS4635Experience(35, 'where do i turn in ​assignment 2', 'Turn in to Canvas as PDF', 'assignment 2', 'PROCESS'))
        self.knowledge.add(CS4635Experience(36, 'where do i turn in my​ midterm', 'Turn in to Canvas as PDF', 'midterm', 'PROCESS'))
        self.knowledge.add(CS4635Experience(37, 'How do I turn in ​project 2', 'Turn in code as zip file, and report as pdf into Canvas', 'project 2', 'PROCESS'))
        self.knowledge.add(CS4635Experience(38, 'where do i submit ​assignment 3', 'Turn in to Canvas as PDF', 'assignment 3', 'PROCESS'))
        self.knowledge.add(CS4635Experience(39, 'where do i submit ​project 3', 'Turn in code as zip file, and report as pdf into Canvas', 'project 3', 'PROCESS'))
        self.knowledge.add(CS4635Experience(40, 'what is the procedure for submitting the ​final', 'Turn in to Canvas as PDF', 'final', 'PROCESS'))
        self.knowledge.add(CS4635Experience(41, 'where do i go to get class announcements', 'Announcements, question answering and discussions: We will use the Piazza forum for announcements, question answering, discussions, and collaboration. It is important that you log into Piazza regularly and frequently (at least two or three times a week, daily if possible)', 'class announcements', 'GENERAL'))
        self.knowledge.add(CS4635Experience(41, 'where do i go to get class announcements', 'Announcements, question answering and discussions: We will use the Piazza forum for announcements, question answering, discussions, and collaboration. It is important that you log into Piazza regularly and frequently (at least two or three times a week, daily if possible)', 'announcements', 'GENERAL'))
        self.knowledge.add(CS4635Experience(42, 'what are the primary learning goals for the class', 'The class is organized around three primary learning goals. First, this class teaches the concepts, methods, and prominent issues in knowledge-based artificial intelligence. Second, it teaches the specific skills and abilities needed to apply those concepts to the design of knowledge-based AI agents. Third, it teaches the relationship between knowledge-based artificial intelligence and the study of human cognition.', 'learning goals', 'GENERAL'))
        self.knowledge.add(CS4635Experience(42, 'what are the primary learning goals for the class', 'The class is organized around three primary learning goals. First, this class teaches the concepts, methods, and prominent issues in knowledge-based artificial intelligence. Second, it teaches the specific skills and abilities needed to apply those concepts to the design of knowledge-based AI agents. Third, it teaches the relationship between knowledge-based artificial intelligence and the study of human cognition.', 'goals', 'GENERAL'))

        self.knowledge.add(CS4635Information(1, 'assignment 1', 'week 2', 'week 3', '1 week', '4%', 'Turn in to Canvas as PDF', ['code', 'project']))
        self.knowledge.add(CS4635Information(2, 'project 1', 'week 3', 'week 6', '3 weeks', '15%', 'Turn in code as zip file, and report as pdf into Canvas', ['assignment']))
        self.knowledge.add(CS4635Information(3, 'assignment 2', 'week 6', 'week 7', '1 week', '4%', 'Turn in to Canvas as PDF', ['code', 'project']))
        self.knowledge.add(CS4635Information(4, 'midterm', 'week 7', 'week 8', '1 week', '15%', 'Turn in to Canvas as PDF', ['code', 'project', 'assignment']))
        self.knowledge.add(CS4635Information(5, 'project 2', 'week 8', 'week 11', '3 weeks', '15%', 'Turn in code as zip file, and report as pdf into Canvas', ['assignment']))
        self.knowledge.add(CS4635Information(6, 'assignment 3', 'week 11', 'week 12', '1 week', '4%', 'Turn in to Canvas as PDF', ['code', 'project']))
        self.knowledge.add(CS4635Information(7, 'project 3', 'week 13', 'week 16', '3 weeks', '15%', 'Turn in code as zip file, and report as pdf into Canvas', ['assignment']))
        self.knowledge.add(CS4635Information(8, 'final', 'week 16', 'week 17', '1 week', '20%', 'Turn in to Canvas as PDF', ['code', 'project', 'assignment']))


class CS4635Context(Context):
    def __init__(self):
        super().__init__()
        self.name = 'CS4635'
        domain = CS4635Domain()

        # Understanding component
        self.keywords = domain.keywords
        self.preferences = domain.preferences

        # Domain knowledge (information/experience)
        self.knowledge = domain.knowledge
        self.reaction = domain.reaction

    def clarify(self, input):
        # If referring to the final week or final <object>, replace 'final' accordingly
        if 'final' in input:
            ind = input.index('final')
            if 0 < ind < len(input)-1:
                if input[ind+1] == 'week':
                    input[ind] = 'week'
                    input[ind+1] = '17'
                if input[ind+1] in ['assignment', 'project']:
                    input[ind] = input[ind+1]
                    input[ind+1] = '3'
        return input
