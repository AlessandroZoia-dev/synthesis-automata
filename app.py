from flloat.parser.ltlf import LTLfParser
from problem.dfa.automata import problem_dfa, intersection
from dfs.nested_dfs import emptiness_check
from problem.planner.plan import extract_plan_from_witness
from robot.cozmo.plan_execution import *
import cozmo


def cozmo_application(robot: cozmo.robot.Robot):
    init_robot_world(robot)
    problem_automaton = problem_dfa()
    problem_automaton.to_graphviz().render("problem_automata")

    parser = LTLfParser()
    #formula = "(G !vs_w2) & F (vs_w1 & X G(!at_h))"
    formula = "F (vs_w1 & X vs_w2 & X G(at_h))"
    parsed_formula = parser(formula)

    # from LTLf formula to DFA : deterministic minimized automaton
    dfa = parsed_formula.to_automaton()
    dfa.to_graphviz().render("ltl_automata")
    automaton_intersection = intersection(problem_automaton, dfa)
    automaton_intersection.to_graphviz().render("intersection_automata")

    check, witness, seed = emptiness_check(automaton_intersection)

    if not check:
        print("Problem unsolvable")
    else:
        print("Solution found")

    print("Seed:" + seed)

    #print(check)
    #while not witness.empty():
        #print(witness.get())
        #print(" ")

    print("Extracting plan from witness ... ")
    plan = extract_plan_from_witness(witness, seed, automaton_intersection)

    print("Plan:")
    while not plan.empty():
        action = plan.get().split(",")[0]
        print(action)
        action_list[action](robot)


cozmo.run_program(cozmo_application)
