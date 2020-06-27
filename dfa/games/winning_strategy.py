from pythomata import SimpleDFA

winning_states = []
dfa_game = None


def init_winning_condition(winning_states_list, dfa_game_aut: SimpleDFA):
    """
        Initialize winning condition.
    """
    global winning_states
    global dfa_game
    winning_states = winning_states_list
    dfa_game = dfa_game_aut


def omega_function(state):
    """
        Realize the omega function w:S->2^A to compute
        winning strategy
        :return: an action
    """
    for i in range(0, len(winning_states)-1):
        difference = winning_states[i+1].difference(winning_states[i])
        if state in difference:
            transitions = dfa_game.get_transitions_from(state)
            for transition in transitions:
                letter = transition[1]
                action = letter.split()[0]
                next_state = transition[2]
                if next_state in winning_states[i]:
                    other_transitions = transitions.copy()
                    other_transitions.discard(letter)
                    omega_check = True
                    for other_transition in other_transitions:
                        other_letter = other_transition[1]
                        other_action = other_letter.split()[0]
                        other_next_state = transition[2]
                        if action == other_action and other_next_state not in winning_states[i]:
                            omega_check = False
                            break
                    if omega_check:
                        return action.split(",")[0]
    return None
