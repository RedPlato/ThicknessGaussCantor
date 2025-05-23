import numpy as np
from continued_fractions_basics import ordering
from extremal_continued_fractions import minimize_continued_fraction, maximize_continued_fraction
from tqdm import tqdm

#assuming alphabet is a set of letters (1 character)

def presence(transition,added_letter,word):
    if added_letter == transition[0]:
        L = len(transition)
        if len(word)>=L-1:
            comparing_part = word[:L-1]
            return comparing_part==transition[1:]                  
        else:
            return False
    else:
        return False
    
def simplify_forbidden_transitions(forbidden_transition,alphabet):
    forbidden_transition = set(forbidden_transition)
    alphabet = set(alphabet)

    suppressing = True
    
    while suppressing: #we want to check for further simplifications each time we delete a new word
        forbidden_transition_simplified = forbidden_transition.copy()
        suppressing = False
        for word in forbidden_transition:
            L = len(word)
            prefix = word[:L-1]
            list_of_suffix = set()
            candidates_to_suppression = set()

            #we search all transitions that start like prefix and have only one letter afterward
            for comparing_word in forbidden_transition:
                if len(comparing_word)==L:
                    if comparing_word[:L-1]==prefix:
                        list_of_suffix.add(comparing_word[L-1])
                        candidates_to_suppression.add(comparing_word)
            
            if list_of_suffix == alphabet:
                suppressing = True
                for deleting_word in candidates_to_suppression:
                    forbidden_transition_simplified.discard(deleting_word)
                forbidden_transition_simplified.add(prefix)
            

        forbidden_transition = forbidden_transition_simplified.copy()

    return forbidden_transition_simplified


        
            


def gauss_cantor_forbidden_words(ordered_alphabet, forbidden_transition, n):
    if n==1:
        return [[letter] for letter in ordered_alphabet[::-1]]
    
    else:
        N = len(ordered_alphabet)
        C_prev = gauss_cantor_forbidden_words(ordered_alphabet, forbidden_transition, n-1)
        C_next = N*C_prev

        if n%2==0:
            using_alphabet = ordered_alphabet
        else:
            using_alphabet = ordered_alphabet[::-1]

        index = 0
        print("Generating Cantor set at rank",n)
        for word in tqdm(C_prev):
            for letter in using_alphabet:
                check_letter = True
                for transition in forbidden_transition:
                    if presence(transition, letter, word):
                        check_letter = False
                        break
                if check_letter:        
                    C_next[index] = [letter] + word
                    index = index+1
                
        C_next = C_next[:index]
        return C_next
    
def list_to_string(L):
    s = ""
    for x in L:
        s = s + str(x)
    return s

def string_to_list(s):
    L = []
    for charac in s:
        L = L + [int(charac)]
    return L
    
def segments_cantor_sets_forbidden_words(alphabet,forbidden_transition,n,k):
    cantor_points = gauss_cantor_forbidden_words(alphabet,forbidden_transition,n)
    segments_cantor = []

    forbidden_transition_string = []
    for transition in forbidden_transition:
        forbidden_transition_string.append(list_to_string(transition))

    print("forbidden transitions created")

    print("Finding segments extremities")
    for point in tqdm(cantor_points):
        point = list(point)
        data_min = minimize_continued_fraction(point,alphabet[-1],forbidden_transition_string)
        data_max = maximize_continued_fraction(point,alphabet[-1],forbidden_transition_string)

        period_min = list(data_min[-1])
        period_max = list(data_max[-1])
        preperiod_min = data_min[:-1]
        preperiod_max = data_max[:-1]

        point_min = preperiod_min + k*period_min
        point_max = preperiod_max + k*period_max

        segments_cantor.append(point_min)
        segments_cantor.append(point_max)

    return segments_cantor