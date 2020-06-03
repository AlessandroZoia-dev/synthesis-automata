import queue

plan = queue.Queue()


def extract_plan_from_witness(witness, seed, automaton):
    """
    Extract a plan from witness
    :param witness: accepting lasso witness
    :param seed: seed in the emptiness check
    :param automaton: input automaton
    :return: a plan
    """
    states = []
    while not witness.empty():
        states.append(witness.get())

    for i in range(len(states)-1):
        state_label = states[i][0]
        next_state_label = states[i+1][0]
        transitions = automaton.get_transitions_from(state_label)
        for transition in transitions:
            if transition[2] == next_state_label:
                plan.put(transition[1])
                break
        if next_state_label == seed:
            break
    return plan
