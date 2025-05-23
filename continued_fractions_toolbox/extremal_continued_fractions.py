def word_check(test_word, forbidden_words, bad_word = False):
    r"""Checks that the test word does not contain any forbidden words."""
    if bad_word:
        for check_word in forbidden_words:
            if check_word in test_word:
                return (False,check_word)
        return (True,'')
    else:
        for check_word in forbidden_words:
            if check_word in test_word:
                return False
        return True

def subshift_symmetrization(forbidden_words):
    r"""Add the transposes to the forbidden_words set.
    Additionally, deletes forbidden words if a subword is already on the set."""
    forbidden_words = set(forbidden_words)
    F_T = set()
    for w in forbidden_words:
        F_T.add(w[::-1])
    forbidden_words = set(sorted(forbidden_words.union(F_T)))
    F = forbidden_words.copy()
    for w in forbidden_words:
        for eta in forbidden_words:
            if w != eta and w in eta:
                if eta in F:
                    F.remove(eta)
    return F


def extending_algorithm(beggining,max_alph,forbidden_words,boolean,bad_words=False):
    r"""Given a finite continued fraction [a_0;a_1,...,a_n] and a finite
    list of forbidden words of size at most M such that n + 1 \geq M,

    it finds the minimal or maximal continued fraction 
    [a_0;a_1,...,a_n,b_{n+1},...,b_{m},(c_1,...,c_h)]

    where all a_i,b_i,c_i belong to [1,...,max_alph] such that

    the continuation does not containing forbidden words.
    If bad_words = True it will return the forbidden words used.
    boolean = 0 is for minimizing, boolean = 1 is for maximizing """
    
    max_seq_len = max(len(word) for word in forbidden_words)

    parity = (len(beggining) + boolean) % 2
    if parity == 0:
        letters = range(max_alph,0,-1)
    else:
        letters = range(1,max_alph+1)

    
    curr_cont_fraction = beggining[:]
    testing_window = ''.join(str(x) for x in curr_cont_fraction[-max_seq_len:])
    length_before_windows = len(curr_cont_fraction)
    
    past_testing_windows = []
    past_testing_windows.append(testing_window)
    
    forbidden_words_used = set()
    extend = True
    while extend:
        parity = (parity + 1) % 2
        letters = letters[::-1]
        for i in letters:
            if bad_words:
                (allowable,fw) = word_check(testing_window+str(i),forbidden_words,True)
            else:
                allowable = word_check(testing_window+str(i),forbidden_words)
            if allowable:
                testing_window = testing_window[1:]+str(i)
                curr_cont_fraction.append(i)
                if (testing_window,parity) in past_testing_windows:
                    extend = False
                else:
                    past_testing_windows.append((testing_window,parity))
                break
            else:
                if bad_words:
                    forbidden_words_used.add(fw)
        
        
    beggining_of_period = past_testing_windows.index((testing_window,parity))+length_before_windows
    period = tuple(curr_cont_fraction[beggining_of_period:])
    curr_preperiod = curr_cont_fraction[:beggining_of_period]
        
    simplify = True
    while simplify:
        if len(curr_preperiod) > 1 and curr_preperiod[-1] == period[-1]:
            curr_preperiod.pop()
            period = (period[-1],)+period[:-1]
        else:
            simplify = False
    if bad_words:
        return (curr_preperiod+[period],forbidden_words_used)
    else:
        return curr_preperiod+[period]

def preperiod_extension(beggining,max_alph,forbidden_words,boolean,bad_words=False):
    r"""Given a finite continued fraction [a_0;a_1,...,a_n] and a finite

    list of forbidden words, it finds the minimal or maximal continued 

    fraction [a_0;a_1,...,a_n,b_{n+1},...,b_{m},(c_1,...,c_h)]

    where all a_i,b_i,c_i belong to [1,...,max_alph] such that

    the continuation does not containing forbidden words.

    If bad_words = True it will return the forbidden words used.

    boolean = 0 is for minimizing, boolean = 1 is for maximizing """

    max_seq_len = max(len(word) for word in forbidden_words)
    
    parity = (len(beggining) + boolean) % 2
    if parity == 0:
        letters = range(max_alph,0,-1)
    else:
        letters = range(1,max_alph+1)
    
    curr_cont_fraction = beggining[:]
    
    r"""We extend the current beginning until we obtain a continued

    fraction of the size of the longest forbidden word."""
    
    forbidden_words_used = set()
    str_curr_cont_fraction = ''.join(str(x) for x in curr_cont_fraction)
    while len(curr_cont_fraction)<max_seq_len+1:
        parity = (parity + 1) % 2
        letters = letters[::-1]
        for i in letters:
            if bad_words:
                (allowable,fw) = word_check(str_curr_cont_fraction+str(i),forbidden_words,True)
            else:
                allowable = word_check(str_curr_cont_fraction+str(i),forbidden_words)

            if allowable:
                curr_cont_fraction.append(i)
                str_curr_cont_fraction = str_curr_cont_fraction+str(i)
                break
            else:
                if bad_words:
                    forbidden_words_used.add(fw)
    if bad_words:
        return [curr_cont_fraction,forbidden_words_used]
    else:
        return curr_cont_fraction

def minimize_continued_fraction(beggining,max_alph,forbidden_words,bad_words=False):
    if bad_words:
        (beggining_ext,fwu1) = preperiod_extension(beggining,max_alph,forbidden_words,0,True)
        (final_ext,fwu2) = extending_algorithm(beggining_ext,max_alph,forbidden_words,0,True)
        return (final_ext,fwu1.union(fwu2))
    else:    
        beggining_ext = preperiod_extension(beggining,max_alph,forbidden_words,0)
        return extending_algorithm(beggining_ext,max_alph,forbidden_words,0)
def maximize_continued_fraction(beggining,max_alph,forbidden_words,bad_words=False):
    if bad_words:
        (beggining_ext,fwu1) = preperiod_extension(beggining,max_alph,forbidden_words,1,True)
        (final_ext,fwu2) = extending_algorithm(beggining_ext,max_alph,forbidden_words,1,True)
        return (final_ext,fwu1.union(fwu2))
    else:
        beggining_ext = preperiod_extension(beggining,max_alph,forbidden_words,1)
        return extending_algorithm(beggining_ext,max_alph,forbidden_words,1)


