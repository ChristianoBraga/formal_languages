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
import copy

def sort_variables(v):
    v_set = set(v)
    v_list = list(v_set)
    return v_list

def r_lte_s(v, p):
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

def left_recursion_elimination(v, p):
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

if __name__ == "__main__":
    pp = pprint.PrettyPrinter()
    
    v = ["S", "A"]
    t = ["a", "b"]
    p = { "S" : [["A", "A"], ["a"]], "A" : [["S", "S"], ["b"]] }
    s  = "S"

    print("Original production set.")
    pp.pprint(p)
    
    # First step: grammar simplification
    print("Second step: sort variables")
    v = sort_variables(v)
    print(v)

    # Third and fourth steps: production set transformation to
    # A_r → A_s α, where r ≤ s and removal of productions of the form
    # Ar → Arα.

    print("Production set transformation to A_r → A_s α, where r ≤ s.")
    p = r_lte_s(v, p)
    pp.pprint(p)
    print("Production set elimination of A_r → A_r α.")    
    p = left_recursion_elimination(v, p)
    pp.pprint(p)
    print("Each production begining with a terminal.")
    p = begin_with_terminal(p)
    pp.pprint("TO DO!")    
    print("Each production begining with a terminal followed by a word of variables.")
    p = terminal_followed_by_word_of_variables(p)
    pp.pprint("TO DO!")    
