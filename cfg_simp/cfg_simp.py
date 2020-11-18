# Christiano Braga
# Nov, 2020

# Simplifies a CFG by (i) removing useless symbols, (ii) removing
# productions that produce the empty word, (iii) removing productions
# that replace variables by variables.

# The productios of a grammar are represented as a dictionary where
# each item is a set of RHS productions with the same LHS. The key is the
# LHS and the value is a list, whose elements are each RHS of the given
# LHS in the production set.

import pprint
import copy

# Useless symbols simplification

def vars_that_generate_terminals(t, p):
    v1 = set()
    while True:
        size = len(v1)
        for a in p:
            for alpha in p[a]:
                add_a = True
                for x in alpha:
                    if x in t or x in v1:
                        continue
                    else:
                        add_a = False
                        break
                if add_a == False:
                    continue
                else:
                    v1 = v1.union(set(a))
        new_size = len(v1)
        if size == new_size:
            break
    for a in p:
        for alpha in p[a]:
            add_alpha = True
            for x in alpha:
                if x in t or x in v1:
                    continue
                else:
                    add_alpha = False
                    break
            if not add_alpha:
                p[a].remove(alpha)
    return v1, p

def comp_reachable_symbols(v, p, t, s):
    '''
    Computes the set of productions whose symbols are useful.
    '''
    # Productions in p must have been computed by
    # vars_that_generate_terminals(t, p).

    # First we compute the sets of useful symbols either variable or
    # teminal.
    t2 = set()
    v2 = set(s)
    while True:
        size_t2 = len(t2)
        size_v2 = len(v2)
        for x in v2:
            for alpha in p[x]:
                for a in alpha:
                    if a in v:
                        v2 = v2.union(set(a))
                    elif a in t:
                        t2 = t2.union(set(a))
        new_size_t2 = len(t2)
        new_size_v2 = len(v2)
        if size_t2 == new_size_t2 and size_v2 == new_size_v2:
            break

    # Next we eliminate from p those productions that do not refer to
    # symbols in either v2 or t2.
    p2 = {}
    for a in p:
        if a in v2:
            p2.update({a : []})
        for alpha in p[a]:
            alpha_is_good = True
            for x in alpha:
                if x in v2 or x in t2:
                    continue
                else:
                    alpha_is_good = False
                    break
            if alpha_is_good:
                p2[a].append(alpha)
    return p2

# Empty production simplification

def comp_empty_word_var_set(p, v_set):
    '''
    Computes the set of variables that directly or indirectly 
    generate the empty word.
    '''
    # ve is the initial set of variables that directly
    # generate epsilon.
    ve = { a for a in p if ["epsilon"] in p[a] } 
    while True:
        size_ve = len(ve)
        for a in p:
            for alpha in [w for w in p[a] if w != ["epsilon"]]:
                nullable = True
                for x in alpha:
                    if x not in ve and x in v_set:
                        nullable = False
                        break
                if nullable:
                    ve = ve.union(set(a)) 
        new_size_ve = len(ve)
        if size_ve == new_size_ve:
            break
    return ve

def excl_empty_prod(p, ve):
    '''
    Removes (direct and indirect) empty productions.
    '''
    p1 = { a : [] for a in p }
    for a in p:
        for alpha in p[a]:
           if alpha != ["epsilon"]:
               p1[a].append(alpha)
    p1 = { a : p1[a] for a in p1 if p1[a] != [] }
    while True:
        size_p1 = len(p1)
        for a in p1:
            for alpha in p1[a]:
                for x in alpha:
                    if x in ve:
                        idx_x = alpha.index(x)
                        alpha1 = alpha[:idx_x]
                        alpha2 = alpha[idx_x + 1:]
                        alpha3 = alpha1 + alpha2
                        if alpha3 != []:
                            p1[a].append(alpha3)
        new_size_p1 = len(p1)
        if size_p1 == new_size_p1:
            break
    return p1

def add_epsilon(s, p, new_p, ve):
    if ["epsilon"] in p[s]:
        new_p[s].append(["epsilon"])
        return new_p
    else:
        for alpha in p[s]:
            if alpha != []:
                for sym in alpha:
                    if sym in ve:
                        continue
                    else:
                        return new_p
        new_p[s].append(["epsilon"])
        return new_p

# Variable substitution production simplification
    
def comp_var_clos(p, v, v_set):
    p1 = { a : [] for a in p } 
    for a in p:
        for alpha in p[a]:
            if len(alpha) == 1 and alpha[0] in v_set:
                p1[a].append(alpha)
    if p1[v] != []:
        clos = p1[v][0]
    else:
        clos = []
    return clos

def remove_prod_replace_var(p, v_set, clos):
    p1 = { a : [] for a in p }
    for a in p:
        for alpha in p[a]:
            if len(alpha) > 1 or (len(alpha) == 1 and alpha[0] not in v_set):
                p1[a].append(alpha)
            else:
                continue 
    for a in v_set:
        for b in clos[a]:
            if b in p.keys():
                for alpha in p[b]:
                    if len(alpha) > 1 or (len(alpha) == 1 and
                                          alpha[0] not in v_set):
                        p1[a].append(alpha)
    return p1

if __name__ == "__main__":

    pp = pprint.PrettyPrinter()

    print("* Useless symbols simplification example")
    p1 = {"S" : [["a", "A", "a"], ["b", "B", "b"]],
          "A" : [["a"], ["S"]], "C" : [["c"]]}
    v1 = {"S", "A", "B", "C"}
    t1 = {"a", "b", "c"}
    initial1 = "S"
    new_v1, new_p1 = vars_that_generate_terminals(t1, p1)
    print("Original production set")
    pp.pprint(p1)
    print("Production set without useless symbols")
    pp.pprint(comp_reachable_symbols(new_v1, new_p1, t1, initial1))

    print()
    print("* Empty production simplification example")
    p2 = { "S" : [ ["a", "X", "a"], ["b", "X", "b"], ["epsilon"] ],
           "X" : [ ["a"], ["b"], ["Y"] ],
           "Y" : [ ["epsilon"] ] }
    v2 = {"S", "X", "Y"}
    t2 = {"a", "b"}
    initial2 = "S"
    print("Original production set")
    pp.pprint(p2)
    ve = comp_empty_word_var_set(p2, v2)
    new_p2 = excl_empty_prod(p2, ve)
    new_p2 = add_epsilon(initial2, p2, new_p2, ve)
    print("Production set without empty reductions")
    pp.pprint(new_p2)

    print()
    print("* Variable substitution simplification example")
    p3 = {"S" : [["a", "X", "a"], ["b", "X", "b"]], "X" : [["a"], ["b"], ["S"], ["epsilon"]]}
    v3 = {"S", "X"}
    t3 = {"a", "b"}
    initial3 = "S"
    print("Original production set")
    pp.pprint(p3)
    clos = {a : None for a in v3}
    for v in v3:
        clos[v] = comp_var_clos(p3, v, v3)
    print("Production set without variable substitution productions")
    pp.pprint(remove_prod_replace_var(p3, v3, clos))


    
    
