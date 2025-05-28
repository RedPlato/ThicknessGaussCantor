class Segment:
    def __init__(self, left, right):
        if left <= right:
            self.left = left
            self.right = right
            self.length = right-left
        else:
            raise ValueError("left_bound is greater than right_bound")


#GAB stands for Gaps And Bridges
class GAB:
    def __init__(self, left_bound, right_bound, gap):
        self.left_bound = left_bound
        self.right_bound = right_bound
        self.gap = gap
        if gap!=None:
            self.thickness = min(gap.left_bound-left_bound, right_bound - gap.right_bound)/(gap.length)
        else:
            self.thickness = None

def create_gap_in_segment(segment, gap):
    s_left = segment.left
    s_right = segment.right
    return GAB(s_left,s_right, gap)

def gap_compare(gap1, gap2):
    r"""RETURNS
            True if gap1 is at the left of gap2
            False if gap1 is at the right of gap2
            Raise a ValueError if the two gaps are intertwined"""
    if gap1.right<gap2.left:
        return True
    elif gap2.right<gap1.left:
        return False
    else:
        raise ValueError("Gaps are intertwined and cannot be compared")
    
class SegmentBinaryTree:
    def __init__(self, left_bound, right_bound):
        self.gab = GAB(left_bound,right_bound,None)
        self.left_tree = None
        self.right_tree = None
        self.thickness_tree = None

    def insert_recursive(self, gap_to_insert):
        if gap_to_insert.left < self.gab.left_bound or gap_to_insert.right > self.gab.right_bound:
            raise ValueError('gap_to_insert out of the bounds the tree')
        
        elif self.gab.gap == None:
            self.gab.gap = gap_to_insert
            self.gab.thickness = min(self.gab.gap.left-self.gab.left_bound, self.gab.right_bound - self.gab.gap.right)/(self.gab.gap.length)
            self.left_tree = SegmentBinaryTree(self.gab.left_bound,self.gab.gap.left)
            self.right_tree = SegmentBinaryTree(self.gab.gap.right,self.gab.right_bound)

        else:
            if gap_compare(self.gab.gap,gap_to_insert):
                self.right_tree.insert_recursive(gap_to_insert)
            else:
                self.left_tree.insert_recursive(gap_to_insert)
                

    def string_tree_recursive(self):
         if self.gab.gap==None:
            return("["+str(int(1000*self.gab.left_bound)/1000)+","+str(int(1000*self.gab.right_bound)/1000)+"]")
         else:
            return self.left_tree.string_tree_recursive() + "--" + self.right_tree.string_tree_recursive()


    def __str__(self):
        return self.string_tree_recursive()
    
    
    def thickness_recursive_tree(self):
        if self.left_tree.gab.thickness == None and self.right_tree.gab.thickness == None:
            self.thickness_tree = self.gab.thickness
        elif self.left_tree.gab.thickness == None:
            self.thickness_tree = min(self.gab.thickness, self.right_tree.thickness_recursive_tree())
        elif self.right_tree.gab.thickness == None:
            self.thickness_tree = min(self.gab.thickness, self.left_tree.thickness_recursive_tree())
        else:
            self.thickness_tree = min(self.gab.thickness, self.left_tree.thickness_recursive_tree(), self.right_tree.thickness_recursive_tree())

        return self.thickness_tree
       
    
