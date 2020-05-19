"""
-------------------------------------------------------------
"""

import sys
import getopt
from TestAdapter import TestAdapter
from NaturalLanguageProcessing import NLPAgent


def _train_agent(training_raw):
    """
    Build a model from the raw training data

    :param training_raw:
    :return:
    """
    agent = NLPAgent()
    for row in training_raw:
        '''Extract the training data'''
        label = row[0]
        question = row[1]

        '''Induce some rules from the input'''
        rules = agent.induce(question)

        '''Incrementally update the concept using these rules'''
        agent.learn(label, rules)

    agent.reflect()
    model = agent.get_model()
    return model


def main(argv):
    """
        This is your test main. This main WILL NOT be used by the autograder.
        When grading your agent, we will call _train_agent() and _train_agent() from our autograder.
        DO NOT MAKE ANY CHANGES IN THIS FUNCTION THAT ARE REQUIRED BY YOUR AGENT TO FUNCTION.
    """
    print(__doc__)

    train_test_filename = argv[0]
    training_questions = []
    test_questions = []
    header = True
    print("Opening test file: " + train_test_filename)
    try:
        with open(train_test_filename, "r", encoding='ascii', errors='backslashreplace') as data:
            for line in data:
                if header:
                    header = False
                    continue
                line = line.split(',')
                training_questions.append([line[0].lower().strip(), line[1].lower().strip()])
                test_questions.append([line[0].lower().strip(), line[2].lower().strip()])
    except IOError as err:
        print("Failure opening or reading test questions filename: " + str(err))
        sys.exit(-1)

    print("\nTraining...")
    training_data = _train_agent(training_questions)
    jw_adapter = TestAdapter(training_data)
    print("\nTesting...")
    total_questions = 0
    correct_answers = 0
    results = {}
    for row in test_questions:
        label = row[0]
        test_question = row[1]
        result_dict = jw_adapter.ask_question(test_question)
        del result_dict['question']
        result_label = list(result_dict.keys())[0]
        print(test_question+"\n\tGround Truth: "+label+"\n\tResult: "+result_label)
        results.update({'test_question':test_question, 'label':label, 'result_label':result_label})
        total_questions += 1
        if label == result_label:
            correct_answers += 1
        print("\t"+str(label==result_label).upper())
    print("\nResults:")
    print("\tTotal Questions: "+str(total_questions))
    print("\tCorrect Answers: "+str(correct_answers))
    sys.exit(0)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
