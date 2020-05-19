# Project 1: Understanding
Name: Nick Liccini

## Contents
#### `AgentGrader.py`

UNEDITIED: Given file from class.

#### `AgentInterface.py`

UNEDITIED: Given file from class.

#### `common.py`

UNEDITIED: Given file from class.

#### `StudentAgent.py` 

This is the main driver class of the agent.
The specific CS 4635 context is defined here and the question topic
and object are parse/output here.

#### `knowledge.py`

This is an interface for an agent's knowledge base.
Here the `Context` and `Knowledge` interfaces are defined.

#### `understanding.py`

This is an interface for frames and thematic roles that
the agent will use to employ grammar rules.

#### `grammar.py`

This is where all the grammar rules and vocabulary
are defined for the agent. Here all the relevant 
frames, parsing functions, constraints, and grammar
constructs are defined.

To expand the agent's vocabulary, the `GrammarRules`
class would be edited. 

#### `utils.py`

There are some useful data structures defined here.

#### `ExampleQuestions.json`

Some questions used when testing the agent.

#### `requirements.txt`

Result of `>> pip3 freeze` to list all dependencies this project used.

Should be an empty text file because only the core Python 3 library is used.

## Instructions
Run the AgentGrader.py normally. Use whatever questions file desired

`>> python3 AgentGrader.py -f <questions>.json `
