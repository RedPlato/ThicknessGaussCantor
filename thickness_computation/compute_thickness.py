import numpy as np
from simple_gauss_cantor import C, segments_cantor
from tqdm import tqdm

def gaps_lengths(segments_list):
    L = segments_list.shape[0]
    gaps = np.zeros(L-1)
    segment_right = segments_list[0]

    for i in range(1,L):
        segment_left = segment_right
        segment_right = segments_list[i]
        gaps[i-1] = segment_right[0] - segment_left[1]

    return gaps



def remove_gap(segments, left_bound_gap, right_bound_gap):
    S = segments.shape[0] #number of segments
    new_segments = np.zeros((S+1,2))

    k = 0                                             #finding where to insert the gap
    while k<S-1 and segments[k+1][0]<left_bound_gap:
        k = k+1
    
    for i in range(k):                              #the first segments before the inserted gap stay the same
        new_segments[i] = segments[i]

    new_segments[k]   = np.array([segments[k][0],left_bound_gap])  #splitting the k-th segment in 2
    new_segments[k+1] = np.array([right_bound_gap,segments[k][1]]) 

    for i in range(k+1,S):
        new_segments[i+1] = segments[i]                #the following segments stay the same

    return new_segments, k


def thickness_ordered_gaps(all_segments):
    gaps = gaps_lengths(all_segments)
    ordering = np.argsort(gaps)[::-1] #indices of the gaps inn the decreasing order of their lengths

    segments = np.array([[np.min(all_segments), np.max(all_segments)]]) #convex hull of the cantor set

    local_thickness = np.zeros((gaps.size,2))

    for index in tqdm(ordering):
        left_bound_gap  = all_segments[index][1]
        right_bound_gap = all_segments[index+1][0]

        segments, k = remove_gap(segments, left_bound_gap, right_bound_gap)
        left_bridge  = segments[k][1]   - segments[k][0]
        right_bridge = segments[k+1][1] - segments[k+1][0]

        local_thickness[index] = np.array([left_bridge/gaps[index], right_bridge/gaps[index]])
        
    return np.min(local_thickness)