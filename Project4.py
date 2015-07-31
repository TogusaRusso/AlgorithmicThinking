"""
Student code for Project 4
Computing alignments of sequences
Dmitry Akentyev
Student will implement four functions:

build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score)
compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag)
compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix)
compute_local_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix)
"""

def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
    """
    Takes as input a set of characters alphabet and three scores diag_score,
    off_diag_score, and dash_score. The function returns a dictionary
    of dictionaries whose entries are indexed by pairs of characters in
    alphabet plus '-'. The score for any entry indexed by one or more dashes
    is dash_score. The score for the remaining diagonal entries is diag_score.
    Finally, the score for the remaining off-diagonal entries is off_diag_score.
    """
    scoring_matrix = {'-' : {'-' : dash_score}}
    for x_i in alphabet:
        scoring_matrix['-'][x_i] = dash_score
        scoring_matrix[x_i]= {'-' : dash_score}
        for y_j in alphabet:
            if x_i == y_j:
                scoring_matrix[x_i][y_j] = diag_score
            else:
                scoring_matrix[x_i][y_j] = off_diag_score
    return scoring_matrix

def compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag):
    """
    Takes as input two sequences seq_x and seq_y whose elements share
    a common alphabet with the scoring matrix scoring_matrix. The function
    computes and returns the alignment matrix for seq_x and seq_y as described
    in the Homework. If global_flag is True, each entry of the alignment matrix
    is computed using the method described in Question 8 of the Homework.
    If global_flag is False, each entry is computed using the method described
    in Question 12 of the Homework.
    """
    l_x = len(seq_x)
    l_y = len(seq_y)
    a_m = [[-1 for _ in xrange(l_y + 1)] for _ in xrange(l_x + 1)]
    a_m[0][0] = 0
    for x_i in xrange(1, l_x + 1):
        a_m[x_i][0] = scoring_matrix[seq_x[x_i - 1]]['-'] + a_m[x_i - 1][0]
        if not global_flag:
            a_m[x_i][0] = max(0, a_m[x_i][0])
    for y_j in xrange(1, l_y + 1):
        a_m[0][y_j] = scoring_matrix['-'][seq_y[y_j - 1]] + a_m[0][y_j - 1]
        if not global_flag:
            a_m[0][y_j] = max(0, a_m[0][y_j])
    for x_i in xrange(1, l_x + 1):
        for y_j in xrange(1, l_y + 1):
            a_m[x_i][y_j] = max(a_m[x_i - 1][y_j - 1] 
                                + scoring_matrix[seq_x[x_i - 1]][seq_y[y_j - 1]],
                                a_m[x_i - 1][y_j] 
                                + scoring_matrix[seq_x[x_i - 1]]['-'],
                                a_m[x_i][y_j - 1] 
                                + scoring_matrix['-'][seq_y[y_j - 1]])
            if not global_flag:
                a_m[x_i][y_j] = max(0, a_m[x_i][y_j])           
    return a_m

def compute_global_alignment(seq_x, seq_y, 
                             scoring_matrix, 
                             alignment_matrix):
    """
    Takes as input two sequences seq_x and seq_y whose elements share
    a common alphabet with the scoring matrix scoring_matrix. This function
    computes a global alignment of seq_x and seq_y using the global alignment matrix
    alignment_matrix.
    The function returns a tuple of the form (score, align_x, align_y) where score
    is the score of the global alignment align_x and align_y. Note that
    align_x and align_y should have the same length and may include
    the padding character '-'.
    """
    x_i = len(seq_x)
    y_j = len(seq_y)
    score = alignment_matrix[x_i][y_j]
    align_x = ""
    align_y = ""
    while x_i > 0 and y_j > 0:
        if (alignment_matrix[x_i][y_j] == alignment_matrix[x_i - 1][y_j - 1] 
            + scoring_matrix[seq_x[x_i - 1]][seq_y[y_j - 1]]):
            align_x = seq_x[x_i - 1] + align_x
            align_y = seq_y[y_j - 1] + align_y
            x_i -= 1
            y_j -= 1
        elif (alignment_matrix[x_i][y_j] == alignment_matrix[x_i - 1][y_j] 
              + scoring_matrix[seq_x[x_i - 1]]['-']):
            align_x = seq_x[x_i - 1] + align_x
            align_y = '-' + align_y
            x_i -= 1
        else:
            align_x = '-' + align_x
            align_y = seq_y[y_j - 1] + align_y
            y_j -= 1
    while x_i > 0:
        align_x = seq_x[x_i - 1] + align_x
        align_y = '-' + align_y
        x_i -= 1
    while y_j > 0:
        align_x = '-' + align_x
        align_y = seq_y[y_j - 1] + align_y
        y_j -= 1
    return (score, align_x, align_y)

def compute_local_alignment(seq_x, seq_y,
                            scoring_matrix, 
                            alignment_matrix):
    """
    Takes as input two sequences seq_x and seq_y whose
    elements share a common alphabet with the scoring
    matrix scoring_matrix. This function computes
    a local alignment of seq_x and seq_y using
    the local alignment matrix alignment_matrix. 
    The function returns a tuple of the form
    (score, align_x, align_y) where score is the score
    of the optimal local alignment align_x and align_y.
    Note that align_x and align_y should have
    the same length and may include the padding character '-'.
    """
    maximum = (0, 0, 0)
    for x_i in xrange(len(seq_x) + 1):
        for y_j in xrange(len(seq_y) + 1):
            if alignment_matrix[x_i][y_j] > maximum[0]:
                maximum = (alignment_matrix[x_i][y_j], x_i, y_j)
    x_i = maximum[1]
    y_j = maximum[2]
    align_x = ""
    align_y = ""
    while alignment_matrix[x_i][y_j] > 0:
        if (alignment_matrix[x_i][y_j] == alignment_matrix[x_i - 1][y_j - 1] 
            + scoring_matrix[seq_x[x_i - 1]][seq_y[y_j - 1]]):
            align_x = seq_x[x_i - 1] + align_x
            align_y = seq_y[y_j - 1] + align_y
            x_i -= 1
            y_j -= 1
        elif (alignment_matrix[x_i][y_j] == alignment_matrix[x_i - 1][y_j] 
              + scoring_matrix[seq_x[x_i - 1]]['-']):
            align_x = seq_x[x_i - 1] + align_x
            align_y = '-' + align_y
            x_i -= 1
        else:
            align_x = '-' + align_x
            align_y = seq_y[y_j - 1] + align_y
            y_j -= 1
    return (maximum[0], align_x, align_y)
        
        
                                                                                           
                                                                                           
                         
                         
                     
    



            
                
                
            
