######################################################################################################
from collections import defaultdict
from copy import deepcopy,copy
global t_dict,alpha,kb,kb_size,alpha_size,index,r_file,input_data,var_count
kb = list(str())
alpha = list(str())
t_dict = dict()
index = defaultdict(list)
kb_size = 0
alpha_size = 0
r_file = open("input.txt", 'r+')
w_file = open("output.txt", 'w+')
input_data = r_file.readlines()

#######################################################################################################

def read_input():


    alpha_size = int(input_data[0])
    kb_size = int(input_data[alpha_size + 1])
    alpha = input_data[1:alpha_size+1]
    kb =  input_data[1+alpha_size+1:1+alpha_size+1+kb_size]
    for i in range(len(kb)):
        kb[i] = kb[i].replace('\n',' ').rstrip(' ')
    for j in range(len(alpha)):
        alpha[j] = alpha[j].replace('\n',' ').rstrip(' ')

    return kb,alpha


def checkprec(a):
    if(a=='~'):
        return 4
    if(a=='&'):
        return 3
    if(a=='|'):
        return 2
    if(a=='>'):
        return 1
    if(a=='('):
        return 0
    if(a==')'):
        return 0
    return 0


def prefix(x):
    s = list()
    prefix_exp = ""
    for i in range(len(x)-1,-1,-1):
        if(x[i]==')'):
            s.append(x[i])
        if(x[i]=='#'):
            j = 0
            while(x[i]):
                j+=1
                if(x[i+j] == '$'):
                    break
            x1 = x[i:i+j+1]
            prefix_exp += x1[::-1]

        if(x[i]=='&' or x[i] == '|' or x[i] == '>' or x[i] == '~'):
            if (not(s)):
                s.append(x[i])
            else:
                prec1 = checkprec(x[i])
                prec2 = checkprec(s[-1])
                if(prec1 > prec2):
                    s.append(x[i])
                else:
                    while(prec1 < prec2 and s):
                        prefix_exp += s.pop()
                        if(s):
                            prec2 = checkprec(s[-1])
                    s.append(x[i])
        if(x[i] == '('):
            while(s[-1] != ')'):
                prefix_exp += s.pop()
            s.pop()
    while(s):
        prefix_exp += s.pop()
    prefix_exp = prefix_exp[::-1]
    return prefix_exp

def remove_impl(a):

    s = list()

    for i in range(len(a)-1,-1,-1):

        if(a[i] =='#'):
            j = 0
            while (a[i]):
                j += 1
                if (a[i + j] == '$'):
                    break
            x1 = a[i:i+j+1]
            s.append(x1)

        if(a[i] =='&' or a[i] =='|'):
            first = s.pop()
            second = s.pop()
            third = first+a[i]+second
            s.append(third)


        if(a[i]=='~'):
            new_first = " "
            first = s.pop()
            first = "~("+first+")"
            s.append(first)


        if(a[i] == '>'):
            first = "~("+s.pop()+")"
            second = s.pop()
            third = first+ "|" +second
            s.append(third)

    return s[-1]

def remove_negation(a):
    s = list()
    for i in range(len(a)-1,-1,-1):
        if(a[i]=='#'):
            j = 0
            while(a[i]):
                j += 1
                if (a[i+j] == '$'):
                    break
            x1 = a[i:j+i+1]
            s.append(x1)

        if(a[i] == '&' or a[i] == '|'):
            first = s.pop()
            second = s.pop()
            third = first+a[i]+second
            s.append(third)

        if (a[i] == '~'):
            newfirst = ""
            first = s.pop()
            j =0
            for j in range(len(first)):
                if (j==0 and first[j] == '#'):
                    newfirst += "~"
                    j_ = 0
                    while (first[j]):
                        j_ += 1
                        if (first[j + j_] == '$'):
                            break
                    newfirst += first[j : j+j_+1]
                elif (first[j] == '|'):
                    newfirst += "&"
                elif (first[j] == '&'):
                    newfirst += "|"
                elif (first[j] == "#"):
                    if (first[j-1] == '~'):
                        j_ = 0
                        while (first[j]):
                            j_+=1
                            if (first[j + j_] == '$'):
                                break
                        newfirst +=first[j:j+j_+1]
                    else:
                        j_=0
                        while(first[j]):
                            j_ += 1
                            if (first[j + j_] == '$'):
                                break
                        newfirst += '~'+first[j:j+j_+1]

            if('&' in newfirst):
                a1 = list(str())
                for a11 in newfirst.split("&"):
                    a11 = "("+ a11 +")"
                    a1.append(a11)
                temp = ""
                for k in a1:
                    temp += k + "&"
                temp = temp[0 : len(temp)-1]
                temp = "(" + temp + ")"
                newfirst = temp

            s.append(newfirst)

    return s[-1]


def distributivity(a):
    s = list(str())
    for i in range(len(a)-1,-1,-1):
        if(a[i]=='#'):
            j_ = 0
            while (a[i]):
                j_ +=1
                if (a[i + j_] == '$'):
                    break
            s.append(a[i:i+j_+1])

        if(a[i]=='&'):
            first= s.pop()
            second= s.pop()
            third=first+a[i]+second
            s.append(third)

        if(a[i]=='~'):
            newfirst=""
            first= s.pop()
            newfirst="~"+first
            s.append(newfirst)

        if(a[i]=='|'):
            first= s.pop()
            second=s.pop()
            third=""
            one = list(str())
            two = list(str())
            if('&' in first):
                for d in  first.split("&"):
                    one.append(d)

            if ('&' in second):
                for d in second.split("&"):
                    two.append(d)

            if(not(one) and not(two)):
                third+=first+"|"+second

            if(not(one) and two):
                for ee in two:
                    third+=first+"|"+ee
                    third+="&"

            if(one and not(two)):
                for ee in one:
                    third+=second+"|"+ee
                    third+="&"

            if(one and two):
                for ee in one:
                    for ee2 in two:
                        third+=ee+"|"+ee2
                        third+="&"
            if(third[len(third)-1]=='&'):
                third=third[0:len(third)-1]
            s.append(third)

    return s[-1]

def clean_clause(clause):
    clause = clause.replace(' ','')
    clause = clause.replace('=>','>')
    return clause

def map_pred(clause):
    clause_ = clause
    Pred_map  = dict()
    count = 0
    i = 0
    while i<len(clause_):
        ch = clause_[i]
        if(ch.isupper()):
            j = 0
            while (clause_[i]):
                j+=1
                if (clause_[i+j] == ')'):
                    break
            p_map = "#"+str(count)+"$"
            Pred_map[p_map] = []
            Pred_map[p_map] = (clause_[i:i+j+1])
            clause_ = clause_.replace(clause_[i:i+j+1],p_map)
            count+=1
        i=i+1
    return Pred_map,clause_

def to_cnf(clause):
    clause_ = clause
    clause_ = clean_clause(clause_)
    Pred_map,clause_ = map_pred(clause_)
    clause_ = prefix(clause_)
    clause_ = remove_impl(clause_)
    clause_ = prefix(clause_)
    clause_ = remove_negation(clause_)
    clause_ = prefix(clause_)
    clause_ = distributivity(clause_)
    i=0
    final_clause = ""
    while i < len(clause_):
        if (clause_[i] == '#'):
            j = 0
            while (clause_[i]):
                j += 1
                if (clause_[i + j] == '$'):
                    break
            final_clause += Pred_map[clause_[i:i+j+1]]
            i+= j
        else:
            final_clause += clause_[i]
            i += 1
    return final_clause.replace('$','').split("&")

def literals(clause):
    if('(' in clause):
        return len(clause.split('|'))
    return 0

def op(clause):
    if((clause[0].islower()) or clause[0] == '#'):
        return clause
    if(literals(clause) == 1):
        if(clause[0] == '~'):
            return '~'
        j = 0
        while(clause[j]):
            j += 1
            if(clause[j] == '('):
                break
        if( '(' in clause):
            j+=1
        return clause[:j-1]

    return '|'

def args(clause):
    clause = clean_clause(clause)
    arg = list(str())
    if((clause[0].islower()) or clause[0] == '#'):
        return arg
    if(literals(clause) == 1):
        if(clause[0] == '~'):
            arg.append(clause[1:len(clause)])
            return arg
        if('(' in clause):
            return clause[clause.find('(')+1 : len(clause)-1].split(',')
    if('|' not in clause):
        arg.append(clause)
        return arg
    clause1 = clause[::-1]
    ind = len(clause1) - clause1.find('|')
    clause1 = clause1[::-1]
    arg.append(clause1[:ind -1])
    arg.append(clause1[ind:])
    return arg

def is_var(s):
    if (s[0].islower() or s[0] == '#'):
        return True
    else:
        return False

def repr(op_, arg):
    if(len(arg) == 0):
        return op(op_)
    elif(not(is_var(op_)) and (op_[0].isupper())):
        s = ""
        i=0
        for i in range(len(arg)):
            s += (arg[i] + ",")
        s = s[:len(s) - 1]
        return op_+"("+s+")"
    elif(len(arg) ==1):
        return (op_+arg[0])
    else:
        s = ""
        i=0
        for i in range(len(arg)):
            s += (arg[i]+op_)
        s = s[:len(s)-1]
        return s
var_count = 0
def std_clause(clause):
    global var_count
    disjuncts = clause.split('|')
    std = []
    for dis in disjuncts:
        p = dis[:dis.find('(')]
        p+= '('
        ar = args(dis[1:]) if (dis[0] == '~') else (args(dis))
        for i in range(len(ar)):
            if(is_var(ar[i])):
                if ar[i] in t_dict:
                    ar[i] = t_dict[ar[i]]
                else:
                    var_count = (var_count) + 1
                    t_dict[ar[i]] = '#' + str(var_count)
                    ar[i] = t_dict[ar[i]]
        i=0
        for i in range(len(ar)):
            p+= ar[i] + ','
        p = p[:len(p)-1] + ")"
        std.append(p)
    ans = ""
    i=0
    for i in range(len(std)):
        ans += std[i] + '|'
    ans = ans[:len(ans)-1]
    return ans

def subst(clause, theta):

    if(is_var(clause)):

        if clause in theta:
            return theta[clause]
        else:
            return clause
    elif(not(is_var(clause)) and (literals(clause)==0)):
        return clause
    else:
        ar = list(str())
        for i in args(clause):
            ar.append(subst(i,theta))
        return repr(op(clause), ar)

def index_KB(kb):
    m = defaultdict(list)
    for clause in kb:
        disjuncts = clause.split('|')
        for pred in disjuncts:
            j = pred.find('(')
            m[pred[:j]].append(clause)
    return m

def can_unify(args1,args2):
    count = 0
    for i in range(len(args1)):
        if (is_var(args1[i]) and is_var(args2[i])):
            count+=1
        elif (is_var(args1[i]) and not(is_var(args2[i]))):
            count+=1
        elif (not(is_var(args1[i])) and is_var(args2[i])):
            count+=1
        elif (args1[i] == args2[i]):
            count+=1
    if(count == len(args1)):
        return True
    return False

def resolution(query,inf_count):
    global index
    while(len(query)>0):
        lit = query.pop()
        if(lit[0] == '~'):
            lit = lit[1:]
        else:
            lit = "~"+lit
        query_pred = lit[:lit.find('(')]
        query_args = args(lit[1:]) if (lit[0] == '~') else args(lit)

        if query_pred in index:
            clauses = index[query_pred]
            new_query = list()
            for clause in clauses:
                if(inf_count > (2*len(index))):
                    return "FALSE"
                disjuncts = clause.split('|')
                found_pred = str()
                m_1 = 0
                match = 0
                for p in disjuncts:
                    m_1 += 1
                    if(query_pred in p):
                        found_pred = p
                        match = m_1
                found_args = args(found_pred[1:]) if (found_pred[0] =='~') else args(found_pred)
                if(can_unify(query_args,found_args)):
                    theta = dict()
                    for i in range(len(query_args)):
                        theta[found_args[i]] = query_args[i]
                    new_query = copy(query)
                    m_1 = 0
                    for resolvent in disjuncts:
                        m_1 +=1
                        resolvent = subst(resolvent,theta)
                        resolvent_pred = resolvent[:resolvent.find("(")]
                        if(resolvent_pred != query_pred or ((resolvent_pred == query_pred) and m_1 != match)):
                            new_query.append(resolvent)
                    if(resolution(new_query,inf_count+1) == "TRUE"):
                        return "TRUE"
            return "FALSE"
        else:
            return "FALSE"
    return "TRUE"

def main():
    global kb,alpha,index
    to_outfile = ""
    kb,alpha = read_input()
    kb_ = list(str())
    for clause in kb:
        conjuncts = to_cnf(clause)
        for i in conjuncts:
            kb_.append(i)
    kb = copy(kb_)
    del kb_[:]
    kb_ = list(str())

    for i in kb:
        t_dict.clear()
        kb_.append(std_clause(i))

    t_dict.clear()
    kb = copy(kb_)
    del kb_[:]

    index = index_KB(kb)
    index_copy = copy(index)

    for query in alpha:
        index.clear()
        index = deepcopy(index_copy)
        index[query[1:query.find('(')] if query[0]=='~' else '~'+query[:query.find('(')]].append(query[1:] if query[0]=='~' else "~"+query)
        alpha_stack = list(str())
        query = clean_clause(query)
        if(query[0] == '~'):
            alpha_stack.append(query[1:])
        else:
            alpha_stack.append("~"+ query)
        out_file = resolution(alpha_stack,0)
        print out_file
        to_outfile += out_file + "\n"
    
    w_file.write(to_outfile)
    w_file.close()
    return 0

if __name__ == "__main__":
    main()
    

















