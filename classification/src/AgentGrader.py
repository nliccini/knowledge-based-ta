"""
============================================
Autograder - Version Project 2 student092518


usage: -q <json containing questions/intents>
       -l <path/filename to log file>
       -v verbose output to console
       -h this message to console
============================================
"""


# standard library
import sys, getopt, json, traceback
from contextlib import redirect_stdout

# local libraries
from AgentInterface import AgentInterface


def format_string(list_of_words, start=False):
    deli = ' | '
    retstr = ""
    if start: retstr += deli
    for word in list_of_words:
        retstr += (word + deli)
    return retstr


class Grader:
    def __init__(self):
        self._stats = {'intent': {'count': 0, 'match': 0}}

    def grade(self, groundtruth, student):
        self._stats['intent']['count'] += 1
        if groundtruth == student:
            self._stats['intent']['match'] += 1

    def header_string(self):
        retval = ["count","match"]
        return retval

    def result_string(self):
        return [str(self._stats['intent']['count']), str(self._stats['intent']['match'])]


class Logger:
    def __init__(self, logname, verbose):
        self._verbose = verbose
        print("Logging to file: " + logname + ".log")
        self._log_file = open(logname + ".log", "w")
        self._result_file = open(logname + ".result", "w")

    def logmsg(self, msg):
        self._log_file.write(msg)
        if self._verbose:
            print(msg, end='')

    def resultmsg(self, msg):
        self._result_file.write(msg)
        if self._verbose:
            print(msg, end='')

    def logclose(self):
        self._log_file.write("\n\n")
        self._result_file.write("\n\n")
        self._log_file.close()


def AgentAutograder(parameters):
    retval = 0
    _questions_filename = parameters['questions']
    _verbose = parameters['verbose']
    print("Opening questions: " + _questions_filename)
    try:
        with open(_questions_filename, encoding='utf-8') as json_data:
            _ground_truth_dicts = json.load(json_data)
    except Exception as e:
        print("Failure opening or reading questions: " + str(e))
        return 1

    print("Redirecting to file: " + parameters['log'] + ".out")
    try:
        redirect = open(parameters['log'] + ".out", "w")
    except:
        print("Failed to open redirection file")
        return 1

    _logger = Logger(parameters['log'], _verbose)

    try:
        _grader = Grader()
        print("\n\nInstantiating student agent")
        _agent = AgentInterface(parameters['verbose'])

        print("\n\nStarting test")
        _head = ["question","intent","guessed intent","correct?","count","# correct"]
        _logger.logmsg(format_string(_head,True))
        _logger.logmsg("\n")
        for _ground_truth_dict in _ground_truth_dicts:
            _ground_truth_question = _ground_truth_dict['question']
            _ground_truth_intent = _ground_truth_dict['intent']

            with redirect_stdout(redirect):
                _student_agent_intent = _agent.input_output(_ground_truth_question)

            _grader.grade(_ground_truth_intent, _student_agent_intent)

            _result =   [
                _ground_truth_question,
                str(_ground_truth_intent),
                str(_student_agent_intent),
                str(_student_agent_intent == _ground_truth_intent).upper()
            ]
            _logger.logmsg(format_string(_result,False))
            _logger.logmsg(format_string(_grader.result_string(), False))
            _logger.logmsg("\n")

        # log file
        _logger.logmsg("\n\n" + format_string(_grader.header_string(), False))
        _logger.logmsg("\n"+format_string(_grader.result_string(), False))

        # results file
        _logger.resultmsg("\n\n"+format_string(_grader.header_string(), False))
        _logger.resultmsg("\n"+format_string(_grader.result_string(), False))

    except Exception as e:
        _logger.logmsg("Error during grading: " + str(e))
        _logger.logmsg(traceback.print_exc(file=sys.stdout))
        retval = 1

    _logger.logmsg("\n\nInvalid inputs: \n")
    invalids = list()
    for question in _agent._student_agent.invalid_list:
        deli = ' '
        q = ""
        for word in question:
            q += (word + deli)
        invalids.append(q)
        _logger.logmsg(q)
        _logger.logmsg('\n')

    print("\nDone")
    _logger.logclose()
    return retval


def main(argv):

    parameters = {
                    'verbose': False,
                    'questions': "ExampleQuestions.json",
                    'log': "results"
                 }

    print(__doc__)
    try:
        opts, args = getopt.getopt(argv, "vf:l:")
    except getopt.GetoptError:
        sys.exit(1)
    for opt, arg in opts:
        if opt in ("-v"):  # -v verbose
            parameters['verbose'] = True
        elif opt in ("-q"):  # -f <json containing dictionary frames>
            parameters['questions'] = arg
        elif opt in ("-l"):  # -l <path/filename to log file>
            parameters['log'] = arg

    return AgentAutograder(parameters)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
