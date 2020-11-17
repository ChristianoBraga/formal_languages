# Christiano Braga Nov. 2020
# Implements the minimization algorithm for finite automata.

# The automaton must be deterministic and its transition function must
# be total.  The transition function is a dictionary whose items are
# inndexed by states and valued by dictionaries indexed by symbols of
# the alphabet whose values are states.  States are labeled by
# strings. The set of states is implemented as a list of strings, and
# so is the set of final states.

# The triangular matrix of potential (non)equivalent states is implemented as a list of state pairs.

import pandas as pd
from tabulate import tabulate
import pprint
#import pygraphviz as pgv
from graphviz import Digraph

def mark_trivial(state_pairs, equiv_states, final):
    for i, s in enumerate(state_pairs):
        k = list(s)
        if (k[0] in final and k[1] not in final) or (k[1] in final and k[0] not in final):
            equiv_states[i] = False

def not_marked(equiv_states, i):
    return equiv_states[i]

def mark_recursive(equiv_states, dep, i):
    l = dep[i]
    for p in l:
        equiv_states[p] = False
        mark_recursive(equiv_states, dep, p)

def mark_non_trivial(sigma, delta, state_pairs, equiv_states, final):
    trace = []
    dep = {i : [] for i in range(len(state_pairs))}
    for i, p in enumerate(state_pairs):
        if not_marked(equiv_states,i):
            trace_step = "Step " + str(i) + "\n"
            l = list(p)
            qu = l[0]
            qv = l[1]
            trace_step += "qu = " + str(qu) + ", qv = " + str(qv) + "\n"
            for s in sigma:
                pu = delta[qu][s]
                pv = delta[qv][s]
                trace_step += "\tSigma = " + str(s) + "\n"
                trace_step += "\t\tpu = " + str(pu) + ", pv = " + str(pv) + "\n"
                if pu == pv:
                    trace_step += "\t\tpu == pv. Skipping to next sigma. \n"
                    continue
                else:
                    pu_pv_idx = state_pairs.index({pu, pv})
                    if not_marked(equiv_states, pu_pv_idx):
                        trace_step += "\t\tpu != pv, and {pu, pv} not marked. \n"
                        trace_step += "\t\tAppending {qu, qv} to the list headed by {pu, pv}. \n"
                        if i not in dep[pu_pv_idx]:
                            dep[pu_pv_idx].append(i)
                        trace_step += "\t\tList headed by " + str({pu, pv}) + " = " + \
                            str([state_pairs[dep[pu_pv_idx][i]] for i in range(len(dep[pu_pv_idx]))]) + "\n"
                        
                    else:
                        trace_step += "\t\tpu != pv and {pu, pv} is marked. \n"
                        trace_step += "\t\tRecursevely marking the list headed by {qu, qv}. \n"
                        trace_step += "\t\tList headed by " + str({qu, qv}) + " = " + \
                            str([state_pairs[dep[i][j]] for j in range(len(dep[i]))]) + "\n"
                        equiv_states[i] = False
                        mark_recursive(equiv_states, dep, i)
        else:
            trace_step = "Step " + str(i) + "\n"
            trace_step += "Pair " + str(p) + " is marked. Skipping to the next pair.\n"
        trace.append(trace_step)
    return trace

def min(sigma, delta, state_pairs, equiv_states, final):
    mark_trivial(state_pairs, equiv_states, final)
    return mark_non_trivial(sigma, delta, state_pairs, equiv_states, final)

def make_state_pairs(states):
    state_pairs = []
    for i, s in enumerate(states):
        for q in states[i+1:]:
            state_pairs.append({s, q})
    return state_pairs

def make_min_afd(states, equiv_states, delta):
    new_states = { s : set(s) for s in states }
    for s in states:
        for t in equiv_states:
            if t.intersection(set(s)) != set():
                new_states[s] = t.union(new_states[s])
    new_states = list(set([frozenset(e) for k, e in new_states.items()]))
    # print(new_states)
    new_graph = {s : {0 : z, 1 : o}
                 for s in new_states
                 for z in new_states
                 for o in new_states if delta[list(s)[0]][0] in z and delta[list(s)[0]][1] in o}
    # print(new_graph)
    return new_graph

def make_digraph(sigma, initial, d, final):
    g = Digraph(format='png')
    g.node("qi", shape="point")
    for s in d.keys():
        if initial in s:
            g.edge("qi", str(set(s)))
        for f in final:
            if f in s:
                g.node(str(set(s)), shape="doublecircle")
        for sym in sigma:
            g.edge(str(set(s)), str(set(d[s][sym])), label=str(sym))
    return g

if __name__ == "__main__":
    # states = ["q0", "A", "NA", "AandB", "NAandB", "AandNB", "NAandNB", "d"]
    # state_pairs = make_state_pairs(states)
    # delta = {"q0" : {0 : "NA" , 1: "A"},
    #          "A" : {0 : "AandNB", 1: "AandB"},
    #          "NA" : {0 : "NAandNB", 1: "NAandB"},
    #          "NAandB" : {0 : "d", 1 : "d"},
    #          "AandNB" : {0 : "d", 1 : "d"},
    #          "NAandNB" : {0 : "d", 1 : "d"},
    #          "d" : {0: "d", 1: "d"}
    #          }
    # final = ["AandB"]
    # sigma = {0, 1}
    # equiv_states = [True] * len(state_pairs)
    # trace = min(sigma, delta, state_pairs, equiv_states, final)
    # l = [p for i, p in enumerate(state_pairs) if equiv_states[i] == True]
    # pp = pprint.PrettyPrinter()
    # pp.pprint(l)
    # for e in trace:
    #     print(e)

    # states2 = ["q0", "q1", "q2", "q3", "q4", "q5"]
    # state_pairs2 = make_state_pairs(states2)
    # final2 = ["q0", "q4", "q5"]
    # delta2 = {
    #     "q0" : {"a" : "q2", "b" : "q1"},
    #     "q1" : {"a" : "q1", "b" : "q0"},
    #     "q2" : {"a" : "q4", "b" : "q5"},
    #     "q3" : {"a" : "q5", "b" : "q4"},
    #     "q4" : {"a" : "q3", "b" : "q2"},
    #     "q5" : {"a" : "q2", "b" : "q3"}
    # }
    # sigma2 = {"a", "b"}
    # equiv_states2 = [True] * len(state_pairs2)
    # trace2 = min(sigma2, delta2, state_pairs2, equiv_states2, final2)
    # l2 = [p for i, p in enumerate(state_pairs2) if equiv_states2[i] == True]
    # #pp = pprint.PrettyPrinter()    
    # pp.pprint(l2)
    # for e in trace2:
    #     print(e)
    
    states3 = ["A", "B", "C", "D"]
    state_pairs3 = make_state_pairs(states3)
    initial = "A"
    final3 = ["D"]
    delta3 = {
        "A" : {0 : "B", 1 : "A"},
        "B" : {0 : "B", 1 : "C"},
        "C" : {0 : "D", 1 : "A"},
        "D" : {0 : "B", 1 : "C"}
    }
    sigma3 = {0, 1}
    equiv_states3 = [True] * len(state_pairs3)
    trace3 = min(sigma3, delta3, state_pairs3, equiv_states3, final3)
    l3 = [p for i, p in enumerate(state_pairs3) if equiv_states3[i] == True]
    pp = pprint.PrettyPrinter()    
    pp.pprint(l3)
    print("2020.1 - Avaliação Minimização AFD - Questão 1")
    for e in trace3:
        print(e)

    G = Digraph(format='png')
    G.node("_q0", shape="point")    
    G.edge("_q0", "A")
    G.node("D", shape="doublecircle")
    for src in delta3.keys():
        for sym in sigma3:
            G.edge(src, delta3[src][sym], label=str(sym))
    G.render("questao1.png")
    
    states4 = ["A", "B", "C", "D", "E", "F", "G", "H"]
    state_pairs4 = make_state_pairs(states4)
    initial4 = "A"
    final4 = ["B", "E"]
    delta4 = {
        "A" : {0 : "E", 1 : "D"},
        "B" : {0 : "A", 1 : "C"},
        "C" : {0 : "G", 1 : "B"},
        "D" : {0 : "E", 1 : "A"},
        "E" : {0 : "H", 1 : "C"},
        "F" : {0 : "C", 1 : "B"},
        "G" : {0 : "F", 1 : "E"},
        "H" : {0 : "B", 1 : "H"}        
    }
    sigma4 = {0, 1}
    equiv_states_bool4 = [True] * len(state_pairs4)
    trace4 = min(sigma4, delta4, state_pairs4, equiv_states_bool4, final4)
    equiv_states4 = [p for i, p in enumerate(state_pairs4) if equiv_states_bool4[i] == True]

    print("2020.1 - Avaliação Minimização AFD - Questão 2")
    for e in trace4:
        print(e)
    
    orig_graph = Digraph(format='png')
    orig_graph.node("_q0", shape="point")
    orig_graph.node("B", shape="doublecircle")
    orig_graph.node("E", shape="doublecircle")
    orig_graph.edge("_q0", "A")
    orig_graph.render("questao2-aut.png")
    for src in delta4.keys():
        for sym in sigma4:
            orig_graph.edge(src, delta4[src][sym], label=str(sym))
        
    min_graph = make_digraph(sigma4, initial4, make_min_afd(states4, equiv_states4, delta4), final4)
    min_graph.render("questao2-aut-min.png")
    
