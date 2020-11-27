# Christiano Braga
# Nov. 2020

# This module implements a pushdown automaton simulator.

import pprint 

def delta(w, stack, rhs):
    '''
    Applies the rhs of a transition to word w in state q with stack stack.
    Pre-condition: (rhs[0] == w[0] or rhs[0] == "epsilon") and (rhs[1] == stack[-1])
    Returns w_prime, q_prime, stack_prime
    '''
    w_prime = w[1:]
    q_prime = rhs[3]
    stack_prime = stack.copy()

    if rhs[0] == "?":
        if len(w) == 0:
            if rhs[1] == "?":
                if len(stack) == 0:
                    if rhs[2] == "epsilon":
                        return w, q_prime, stack_prime
                    else:
                        stack_prime.pop()
                        stack_prime.append(rhs[2])
                        return w, q_prime, stack_prime
                else:
                    raise Exception("Rhs " + str(rhs) + " does not apply to " + str(w))
        else:
            raise Exception("Rhs " + str(rhs) + " does not apply to " + str(w))            

    if rhs[0] != "epsilon":
        if len(w) == 0:
            raise Exception("Rhs " + str(rhs) + " does not apply to " + str(w))
        else:
            if rhs[0] != w[0]:
                raise Exception("Rhs " + str(rhs) + " does not apply to " + str(w))                
    else:
        w_prime = w        
            
    if rhs[1] == "epsilon": # Does not care about the top of the stack.
        if rhs[2] != "epsilon": # Writes to the stack.
            stack_prime.append(rhs[2])
        # else:
        #   rhs[2] == "epsilon" => Stack remains the same.
            
    else:
        # Checks if 2nd prj. of the transition equals the top
        # of the stack.
        top = stack_prime.pop()
        if rhs[1] == top: 
            if rhs[2] != "epsilon": # Writes to the stack.
                stack_prime.append(rhs[2])
            # else:
            #   rhs[2] == "epsilon" => Stack remains the same.
        else:
            raise Exception("Rhs " + str(rhs) + " 2nd projection " + str(rhs[1]) +
                                " differs from stack's top" + str(top))                
    # Consumes the first symbol of w, steps to transitions
    # target state with stack_prime.
    return w_prime, q_prime, stack_prime

def delta_clos(w, q, stack, t_dict):
    if q in t_dict.keys():
        w_prime = w[1:]
        q_prime = None
        stack_prime = None
        reachable = []
        rhs_list = t_dict[q]
        for rhs in rhs_list:
            if len(w) > 0:
                sigma_guard = rhs[0] == "epsilon" or (w[0] == rhs[0])
            else:
                if rhs[0] != "epsilon":
                    if rhs[0] != "?":
                        continue
                sigma_guard = True
            if len(stack) > 0:
                stack_guard = rhs[1] == "epsilon" or rhs[1] == stack[-1]
            else:
                stack_guard = rhs[1] == "epsilon" or rhs[1] == "?"
            if sigma_guard and stack_guard:
                print(w, q, stack)
                print("==["+str(rhs)+"]==>")
                w_prime, q_prime, stack_prime = delta(w, stack, rhs)
                print(w_prime, q_prime, stack_prime)
                print()
                reachable.append((w_prime, q_prime, stack_prime))
        if reachable == []:
            return [(w, q, stack)]
        else:
            return reachable
    else:
        return [(w, q, stack)]

def lifted_delta_clos(w_q_stack_list, t_dict):
    levels = [w_q_stack_list.copy()]
    while True:
        levels_size = len(levels)
        level = []
        # print(levels[-1])
        for w, q, s in levels[-1]:
            w_q_stack_list_prime = delta_clos(w, q, s, t_dict)
            if [(w, q, s)] != w_q_stack_list_prime:
                level += w_q_stack_list_prime
        if len(level) > 0:
            levels.append(level)
        if len(w) == 0:
            level = []
            t_final = {}
            for k,v_list in t_dict.items():
                for v in v_list:
                    if v[0] == "?" or v[1] == "?":
                        if k not in t_final.keys():
                            t_final.update({k : []})
                        t_final[k].append(v)
            for w, q, s in levels[-1]:
                w_q_stack_list_prime = delta_clos(w, q, s, t_final)
                if [(w, q, s)] != w_q_stack_list_prime:
                    level += w_q_stack_list_prime
            if len(level) > 0:
                levels.append(level)
        new_levels_size = len(levels)
        if levels_size == new_levels_size:
            return levels
    
if __name__ == "__main__":
    pp = pprint.PrettyPrinter()
    print("PDA for {a^nb^n}")
    Sigma = {"a", "b"}
    Q = {"q0", "q1", "qf"}
    q0 = "q0"
    F = {"qf"}
    V = {"B"}
    delta1 = { "q0" : [("a", "epsilon", "B", "q0"), ("b", "B", "epsilon", "q1"), ("?", "?", "epsilon", "qf")],
               "q1" : [("b", "B", "epsilon", "q1"), ("?", "?", "epsilon", "qf")] }
    w = "aabb"
    pp.pprint(lifted_delta_clos([(w, "q0",[])], delta1))
    print()
    print("PDA for {ww^r}")
    Sigma = {"a", "b"}
    Q = {"q0", "q1", "qf"}
    q0 = "q0"
    F = {"qf"}
    V = {"a", "b"}
    delta1 = { "q0" : [("a", "epsilon", "a", "q0"), ("b", "epsilon", "b", "q0"),
                       ("epsilon", "epsilon", "epsilon", "q1")],
               "q1" : [("a", "a", "epsilon", "q1"), ("b", "b", "epsilon", "q1"),
                       ("?", "?", "epsilon", "qf")] }
    M = (Sigma, Q, delta1, q0, F, V)
    w = "abba"
    pp.pprint(lifted_delta_clos([(w, "q0", [])], delta1))
    
