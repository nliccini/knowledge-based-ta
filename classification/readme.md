# Project 2: Classification
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
There is a function `input_output` which takes in the question and
outputs the intent of the question.

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

#### `cognition.py`

This is where the cognitive architecture for the agent is defined.
Here the agent uses its knowledge to classify the input and produce
an output.

#### `cs4635context.py`

This is the domain knowledge for a particular topic, here CS 4635.
This includes the constraints (in the form of categories), keywords,
preferences, prior experiences, and preloaded information.

This is an example of one `Context` that the agent may have knowledge
about.

#### `utils.py`

There are some useful data structures and methods defined here.

#### `vocabulary.txt`

This is the list of words that the agent is able to interpret.
Anything outside of this list will be disregarded as unintelligible.

#### `ExampleQuestions.json`

Some questions used when testing the agent.

#### `requirements.txt`

Result of `>> pip3 freeze` to list all dependencies this project used.

Should be an empty text file because only the core Python 3 library is used.

## Instructions
Run the AgentGrader.py normally. Use whatever questions file desired

`>> python3 AgentGrader.py -f <questions>.json `
