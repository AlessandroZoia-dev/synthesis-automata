from pythomata import SimpleDFA
from flloat.parser.ltlf import LTLfParser

"""
DFA Automaton for domain problem
and intersection between the automaton
and the LTL formula automaton
"""

# Propositions for states
propositions = {'s0': {'at_h': True},
                's1': {'at_h': True, 'vs_w1': True},
                's2': {'at_h': True, 'vs_w2': True},
                's3': {'vs_w1': True, 'vs_w2': True},
                's4': {'at_h': True, 'vs_w1': True, 'vs_w2': True},
                's5': {'vs_w1': True},
                's6': {'vs_w2': True},
                's_init': {}
                }


def problem_dfa():
    """
    Create DFA for problem domain.
    :return: SimpleDFA object
    """
    alphabet = {"wait,s0", "wait,s1", "wait,s2", "wait,s3", "wait,s4", "wait,s5", "wait,s6",
                "mov_hw1,s5", "mov_hw2,s6", "mov_w1w2,s3", "mov_w1h,s1",
                "mov_w2h,s2", "mov_w2w1,s3", "mov_w12h,s4", "start,s0"}
    states = {"s0", "s1", "s2", "s3", "s4", "s5", "s6", 's_init'}
    initial_state = "s_init"
    accepting_states = {"s0", "s1", "s2", "s3", "s4", "s5", "s6"}
    transition_function = {
        "s_init": {
            "start,s0": "s0",
        },
        "s0": {
            "mov_hw1,s5": "s5",
            "mov_hw2,s6": "s6",
            "wait,s0": "s0"
        },
        "s5": {
            "mov_w1w2,s3": "s3",
            "mov_w1h,s1": "s1",
            "wait,s5": "s5"
        },
        "s6": {
            "mov_w2w1,s3": "s3",
            "mov_w2h,s2": "s2",
            "wait,s6": "s6"
        },
        "s3": {
            "mov_w12h,s4": "s4",
            "wait,s3": "s3"
        },
        "s1": {
            "wait,s1": "s1"
        },
        "s2": {
            "wait,s2": "s2"
        },
        "s4": {
            "wait,s4": "s4"
        }
    }
    dfa = SimpleDFA(states, alphabet, initial_state, accepting_states, transition_function)
    return dfa


def intersection(prb_dfa, ltl_dfa):
    """
    Build the intersection DFA automaton between
    problem DFA and LTL DFA.
    :param prb_dfa: problem DFA
    :param ltl_dfa: LTL formula DFA
    :return: SimpleDFA object
    """
    parser = LTLfParser()
    alphabet = prb_dfa.alphabet
    states = set({})
    initial_state = "[" + prb_dfa.initial_state + "," + str(ltl_dfa.initial_state) + "]"
    accepting_states = set({})
    transition_function = {}
    explore = {(prb_dfa.initial_state, str(ltl_dfa.initial_state))}

    while len(explore) is not 0:
        state = explore.pop()
        state_intersection = "[" + state[0] + "," + state[1] + "]"
        states.add(state_intersection)
        if prb_dfa.is_accepting(state[0]) and ltl_dfa.is_accepting(int(state[1])):
            accepting_states.add(state_intersection)
        for letter in alphabet:
            successor = prb_dfa.get_successors(state[0], letter)
            if len(successor) is not 0:
                prob_state = successor.pop()
                ltl_state = state[1]
                props = [propositions[prob_state]]
                transitions = ltl_dfa.get_transitions_from(int(state[1]))
                for transition in transitions:
                    formula = ltl_extract_formula(transition)
                    if parser(str(formula).replace("~", "!")).truth(props, 0):
                        ltl_state = str(ltl_extract_next_state(transition))
                        break
                new_state_intersection = "[" + prob_state + "," + ltl_state + "]"
                if new_state_intersection not in states:
                    explore.add((prob_state, ltl_state))
                if state_intersection not in transition_function:
                    transition_function[state_intersection] = {letter: new_state_intersection}
                else:
                    transition_function[state_intersection][letter] = new_state_intersection

    return SimpleDFA(states, alphabet, initial_state, accepting_states, transition_function)


def ltl_extract_formula(transition):
    """ Returns the transition formula
    """
    return transition[1]


def ltl_extract_next_state(transition):
    """ Returns the next state for this transition
    """
    return transition[2]
