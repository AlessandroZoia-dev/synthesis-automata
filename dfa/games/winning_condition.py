from pythomata import SimpleDFA

dfa_game = None


def init_dfa_game(dfa_game_aut: SimpleDFA):
    """
        Initialize DFA Game using intersection automata.
    """
    global dfa_game
    dfa_game = dfa_game_aut


def get_dfa_game():
    """
        Returns the DFA Game
        :return: SimpleDFA object
    """
    return dfa_game


def prec(states):
    """
        Build the PreC set given the input states.
        :return: PreC set
    """
    dfa_states = dfa_game.states
    prec_set = set()
    for s in dfa_states:
        transitions = dfa_game.get_transitions_from(s)
        explored_actions = set()
        for transition in transitions:
            letter = transition[1]
            action = letter.split()[0]
            next_state = transition[2]
            if action not in explored_actions and next_state in states:
                to_add = True
                other_transitions = transitions.copy()
                other_transitions.discard(letter)
                for other_transition in other_transitions:
                    other_letter = other_transition[1]
                    other_action = other_letter.split()[0]
                    other_next_state = transition[2]
                    if action == other_action and other_next_state not in states:
                        to_add = False
                        break
                if to_add:
                    prec_set.add(s)
                    continue
            explored_actions.add(action)
    return prec_set


def winnning_states(final_states):
    """
        Compute the set Win of winning states.
        :return: A list of set of winning states
    """
    win_list = []
    win = final_states
    win_list.append(win)
    finish = False
    while not finish:
        win_next = win.union(prec(win))
        if win_next != win:
            win_list.append(win_next)
            win = win_next
        else:
            finish = True
    return win_list
