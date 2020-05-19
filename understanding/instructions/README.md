## Projects for CS-4635-A AND CS-7637-A AND CS-4635-O01 AND CS-7637-O

### Requirements

Python 3.6 or above

### Files

| File | Change? | Description |
| ---- | ------- | ----------- |
| ExampleQuestions.json | YES | Add your manually generated frames into this file |
| StudentAgent.py | YES | Add your code here |
| AgentInterface.py | NO | Autograder to agent interface |
| AgentGrader.py | NO | The autograder will test your agent and output a result |
| common.py | NO | Helper functions |


## To run grader

```
python AgentGrader.py

==================================
Autograder - Version student083118


usage: -f <json containing dictionary frames>
       -l <path/filename to log file>
       -v verbose output to console
       -h this message to console
==================================

Opening frames: ExampleQuestions.json
Redirecting to file: results.out
Logging to file: results.log

```

## Autograder Output

```
in results.log
---------------

when is the project due|project|DUEDATE|project|DUEDATE1|1.0|1.0
when is the project released|project|RELEASEDATE|project|DUEDATE2|2.0|1.0
how much is the project worth|project|WEIGHT|project|DUEDATE3|3.0|1.0
where do I turn in my project|project|PROCESS|project|DUEDATE4|4.0|1.0
where is the project specification|project|PROCESS|project|DUEDATE5|5.0|1.0
how long do we have to complete a project|project|DURATION|project|DUEDATE6|6.0|1.0

count,object,datatype
6|6.0|1.0
------------------------------------------------------------------------------------------------------
 
 | is a delimiter. 

count,object,datatype
6       |   6.0   |  1.0

count = total # of questions
object = # of correct object matches
datatype = # of correct datatype matches

                          |     ground truth        |   student agent     |
question                  |  object   |  requested  |  object | requested | question # | object match | request match
when is the project due   |  project  |  DUEDATE    | project | DUEDATE   |     1      |      1.0     |     1.0
```


