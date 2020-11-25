# Christiano Braga
# Nov. 2020
# Grammar transformation to Greibach normal form.
# The productios of a grammar are represented as a dictionary where
# each item is a set of RHS productions with the same LHS. The key is the
# LHS and the value is a list, whose elements are each RHS of the given
# LHS in the production set.

# Given a grammar G = (V, T, P, S), all symbols are strings, V is
# implemented as a list and so is T. S is a string and P is as
# described above.

import pprint
from termcolor import colored
import copy
import itertools

def sort_variables(v):
    v_set = set(v)
    v_list = list(v_set)
    return v_list

def r_lte_s(v, p_0):
    p = copy.deepcopy(p_0)
    for a_r in v:
        for a_s in v: 
            if v.index(a_s) < v.index(a_r):
                rhs_list = p[a_r]
                for rhs in rhs_list:
                    if rhs[0] == a_s:
                        for beta in p[a_s]:
                            beta_copy = beta.copy()
                            beta_copy.extend(rhs[1:]) # beta alpha
                            p[a_r].append(beta_copy)
                        p[a_r].remove(rhs)
    return p

def left_recursion_elimination(v, p_0):
    p = copy.deepcopy(p_0)
    excluded = []
    new_p = {}
    for a_r in p:
        for i, rhs in enumerate(p[a_r]):
            if rhs[0] == a_r:
                rhs_copy = rhs.copy()
                b_r = rhs_copy[0] + "_rr"
                v = v.append(b_r)
                alpha = rhs_copy[1:]
                alpha_x = alpha.copy()
                alpha_x.append(b_r)
                new_p.update({ b_r : [alpha, alpha_x] })
                p[a_r].remove(rhs)
                excluded += a_r
    p.update(new_p)
    for a_r in excluded:
        rhs_list = copy.deepcopy(p[a_r])
        for rhs in rhs_list:
            rhs_copy = rhs.copy()
            rhs_copy.append(a_r + "_rr")
            p[a_r].append(rhs_copy)
    return p

def begin_with_terminal(p):
    pass

def terminal_followed_by_word_of_variables(p):
    pass

def print_prod(p):
    for key in p.keys():
        print(colored(key, 'magenta') + colored(" → ", 'white', attrs=['bold']) + colored(" ".join(p[key][0]), 'cyan'))
        for rhs in p[key][1:]:
            print(colored(" | ", 'white', attrs=['bold']) + colored(" ".join(rhs), 'cyan'))
    
def mk_example(ex_num, v_0, p_0):
    pp = pprint.PrettyPrinter(indent=4)
    print(colored("Example " + str(ex_num), attrs=['bold']))
    print("Original production set.")
    print_prod(p_0)
    
    for i, v in enumerate(list(itertools.permutations(v_0))):
        print(colored("Example "+ str(ex_num) + "." + str(i), 'green', attrs=['bold']))
        
        # First step: grammar simplification
        print(colored("Second step: sort variables", 'blue'))
        v = list(v)
        pp.pprint(v)

        # Third and fourth steps: production set transformation to
        # A_r → A_s α, where r ≤ s and removal of productions of the form
        # Ar → Arα.
        
        print(colored("Production set transformation to A_r → A_s α, where r ≤ s.", 'blue'))
        p_i = r_lte_s(v, p_0)
        print_prod(p_i)
        print(colored("Production set elimination of A_r → A_r α.", 'blue'))    
        p_i = left_recursion_elimination(v, p_i)
        print_prod(p_i)
        print(colored("Each production begining with a terminal.", 'grey'))
        p_i = begin_with_terminal(p_i)
        pp.pprint("TO DO!")    
        print(colored("Each production begining with a terminal followed by a word of variables.", 'grey'))
        p_i = terminal_followed_by_word_of_variables(p_i)
        pp.pprint("TO DO!")
    
if __name__ == "__main__":
    print(colored("Examples of transformations from CFG to Greibach normal form", attrs=['bold']))

    ### Example 1
    v_0 = ["A", "S"]
    t = ["a", "b"]
    p_0 = { "S" : [["A", "A"], ["a"]], "A" : [["S", "S"], ["b"]] }
    s  = "S"
    mk_example(1, v_0, p_0)

    ### Example 2
    v1 = ["A", "B", "C"]
    t1 = ["a", "b"]
    p1 = { "A" : [["B", "C"]], "B" : [["C", "A"], ["b"]], "C" : [["A", "B"], ["a"]] }
    s1  = "A"
    mk_example(2, v1, p1)
    
