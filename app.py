from flloat.parser.ltlf import LTLfParser
from problem.dfa.automata import problem_dfa, intersection
from dfa.games import winning_condition
from dfa.games import winning_strategy
from robot.cozmo.actions import *
import cozmo


def cozmo_application(robot: cozmo.robot.Robot):
    init_robot_world(robot)
    print("Problem DFA Automaton ...")
    problem_automaton = problem_dfa()
    problem_automaton.to_graphviz().render("problem_automata")

    parser = LTLfParser()
    formula = "(G !vs_w2) & F (vs_w1 & X G(!at_h))"
    #formula = "F(vs_w1 & vs_w2 & X G(at_h))"
    parsed_formula = parser(formula)

    # From LTLf formula to DFA : deterministic minimized automaton
    print("LTL formula DFA Automaton ...")
    dfa = parsed_formula.to_automaton()
    dfa.to_graphviz().render("ltl_automata")

    # DFA intersection
    print("DFA intersection Automaton ...")
    automaton_intersection = intersection(problem_automaton, dfa)
    automaton_intersection.to_graphviz().render("intersection_automata")

    # DFA Game
    #print("Robot task: visit  way point 1, way point 2 and back to home")
    print("Robot task: visit  way point 1 and remain there")
    print("LTL formula:" + formula)

    print("-----------------------")
    print("Start DFA Game")
    print("-----------------------")
    winning_condition.init_dfa_game(automaton_intersection)
    dfa_game = winning_condition.get_dfa_game()
    print("Winning states waiting ....")
    winning_states = winning_condition.winnning_states(automaton_intersection.accepting_states)

    print("Winning states:")
    print(winning_states)

    print("Winning strategy waiting ...")
    winning_strategy.init_winning_condition(winning_states, automaton_intersection)

    print("Start winning strategy:")
    state = dfa_game.initial_state
    final = dfa_game.accepting_states
    last_env_state = "s_init"
    while state not in final:
        print("-----------------------")
        print("Current state:" + state)
        omega_action = winning_strategy.omega_function(state)
        if omega_action is None:
            print("No action from winning strategy: problem unsolvable")
            return
        print("Current action:" + omega_action)
        print("-----------------------")
        print("Send action to the robot ...")
        env_state = action_list[omega_action](robot)
        if env_state != "err":
            if env_state is None:
                print("Environment state after the action execution:" + last_env_state)
                env_state = last_env_state
            else:
                last_env_state = env_state
                print("Environment state after the action execution:" + env_state)
            action = omega_action + "," + env_state
            transitions = dfa_game.get_transitions_from(state)
            for transition in transitions:
                if transition[1] == action:
                    state = transition[2]
                    break
        else:
            print("Error from environment")
            return
        print("-----------------------")
    print("DFA Game completed successfully")


cozmo.run_program(cozmo_application)

