"""
==================================
Autograder - Version student083118


usage: -f <json containing dictionary frames>
       -l <path/filename to log file>
       -v verbose output to console
       -h this message to console
==================================
"""


# standard library
import sys, getopt, json, traceback
from contextlib import redirect_stdout

# local libraries
import common
from AgentInterface import AgentInterface


class Grader:
    def __init__(self):
        self._stats = {'object': {'count': 0, 'match': 0},
                       'datatype': {'count': 0, 'match': 0}}

    def grade(self, groundtruth_frame, student_frame):
        _result = groundtruth_frame.Compare(student_frame)
        self._stats['object']['count'] += 1
        self._stats['datatype']['count'] += 1
        self._stats['object']['match'] += _result[0]
        self._stats['datatype']['match'] += _result[1]

    def header_string(self):
        retval = "count,object,datatype"
        return retval

    def result_string(self):
        result = '|' + str(self._stats['object']['count']) + '|'
        result += str(self._stats['object']['match']) + '|'
        result += str(self._stats['datatype']['match'])
        return result


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
            print(msg)

    def logclose(self):
        self._log_file.write("\n\n")
        self._result_file.write("\n\n")
        self._log_file.close()


def AgentAutograder(parameters):
    _frame_filename = parameters['frames']
    _verbose = parameters['verbose']
    print("Opening frames: " + _frame_filename)
    try:
        with open(_frame_filename, encoding='utf-8') as json_data:
            _ground_truth_frames = json.load(json_data)
    except Exception as e:
        print("Failure opening or reading frames: " + str(e))
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
        for _ground_truth_dict in _ground_truth_frames:
            _ground_truth_frame = common.Frame.fromDict(_ground_truth_dict)
            _result_str = _ground_truth_frame.print('all')
            with redirect_stdout(redirect):
                _agent_frame = _agent.input_output(_ground_truth_dict['question'])
            _result_str += _agent_frame.print('qd')
            _grader.grade(_ground_truth_frame, _agent_frame)
            _result_str += _grader.result_string()
            _logger.logmsg(_result_str)
            _logger.logmsg("\n")

        _logger.logmsg("\n\n")
        _logger.logmsg(_grader.header_string())
        _logger.logmsg("\n"+_grader.result_string()+"\n")
        _logger.resultmsg("\n\n"+_grader.header_string())
        _logger.resultmsg("\n"+_grader.result_string())

    except Exception as e:
        _logger.logmsg("Error during grading: " + str(e))
        _logger.logmsg(traceback.print_exc(file=sys.stdout))
    finally:
        _logger.logclose()
        return 1


def main(argv):

    parameters = {
                    'verbose': False,
                    'frames': "ExampleQuestions.json",
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
        elif opt in ("-f"):  # -f <json containing dictionary frames>
            parameters['frames'] = arg
        elif opt in ("-l"):  # -l <path/filename to log file>
            parameters['log'] = arg

    return AgentAutograder(parameters)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
