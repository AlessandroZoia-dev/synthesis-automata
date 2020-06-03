import queue

"""
Nested DFS with Witness algorithm
"""

states = {}
success = False
accepting_lasso = queue.LifoQueue()
seed = None
not_empty = False


def emptiness_check(automaton):
    """
    Emptiness check
    :param automaton: input automata
    :return: emptiness check, witness and seed
    """
    initial_state = automaton.initial_state
    dfs1(initial_state, automaton)
    return not_empty, accepting_lasso, seed


def dfs1(state, automaton):
    """
    DFS1 phase. Updates global variables
    :param state: current state
    :param automaton: input automaton
    :return: nothing
    """
    global seed
    if state not in states:
        states[state] = {"bit1": 1, "bit2": 0}
    else:
        states[state]["bit1"] = 1
    transitions = automaton.get_transitions_from(state)
    for transition in transitions:
        next_state = extract_next_state(transition)
        if (next_state not in states) or states[next_state]["bit1"] == 0:
            dfs1(next_state, automaton)
        if success:
            accepting_lasso.put((state, 1))
            return
    if state in automaton.accepting_states:
        seed = state
        dfs2(state, automaton)
        if success:
            accepting_lasso.put((state, 1))
    return


def dfs2(state, automaton):
    """
    DFS2 phase. Updates global variables
    :param state: current state
    :param automaton: input automaton
    :return: nothing
    """
    global seed
    global not_empty
    global success
    if state not in states:
        states[state] = {"bit1": 0, "bit2": 1}
    else:
        states[state]["bit2"] = 1
    transitions = automaton.get_transitions_from(state)
    for transition in transitions:
        next_state = extract_next_state(transition)
        if (next_state not in states) or states[next_state]["bit2"] == 0:
            dfs2(next_state, automaton)
        if success:
            accepting_lasso.put((state, 2))
            return
        if next_state == seed:
            not_empty = True
            success = True

    return


def extract_next_state(transition):
    """
    Returns the next state for this transition
    :param transition: current transition
    :return: next state for this transition
    """
    return transition[2]
