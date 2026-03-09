import sys
import math

def get_parameter_vectors():
    '''
    This function parses e.txt and s.txt to get the  26-dimensional multinomial
    parameter vector (characters probabilities of English and Spanish) as
    descibed in section 1.2 of the writeup

    Returns: tuple of vectors e and s
    '''
    #Implementing vectors e,s as lists (arrays) of length 26
    #with p[0] being the probability of 'A' and so on
    e=[0]*26
    s=[0]*26

    with open('e.txt',encoding='utf-8') as f:
        for line in f:
            #strip: removes the newline character
            #split: split the string on space character
            char,prob=line.strip().split(" ")
            #ord('E') gives the ASCII (integer) value of character 'E'
            #we then subtract it from 'A' to give array index
            #This way 'A' gets index 0 and 'Z' gets index 25.
            e[ord(char)-ord('A')]=float(prob)
    f.close()

    with open('s.txt',encoding='utf-8') as f:
        for line in f:
            char,prob=line.strip().split(" ")
            s[ord(char)-ord('A')]=float(prob)
    f.close()

    return (e,s)

def shred(filename):
    #Using a dictionary here. You may change this to any data structure of
    #your choice such as lists (X=[]) etc. for the assignment
    X=dict()
    with open (filename,encoding='utf-8') as f:
        for line in f:
            for char in line:
                upper_char = char.upper()
                if 'A' <= upper_char <= 'Z':
                    if upper_char not in X:
                        X[upper_char] = 0
                    X[upper_char] += 1

    for letter in range(ord('A'), ord('Z') + 1):
        if chr(letter) not in X:
            X[chr(letter)] = 0

    return X

def multinomial_log_prob(X, p, prior):
    log_prob = math.log(prior)
    for i in range(26):
        if X[i] > 0:
            log_prob += X[i] * math.log(p[i])
    
    return log_prob

def robust_cond_prob(X, e, s, prior_e, prior_s):
    F_e = multinomial_log_prob(X, e, prior_e)
    F_s = multinomial_log_prob(X, s, prior_s)
    diff_in_F = F_s - F_e
    if diff_in_F >= 100:
        return 0
    elif diff_in_F <= -100:
        return 1
    else:
        return 1 / (1 + math.exp(diff_in_F))

if __name__ == "__main__":
    e, s = get_parameter_vectors()
    filename = sys.argv[1]
    prior_e = float(sys.argv[2])
    prior_s = float(sys.argv[3])
    letter_count = shred(filename)
    X = [letter_count[chr(i)] for i in range(ord('A'), ord('Z') + 1)]

    X1 = X[0]
    log_e1 = X1 * math.log(e[0]) if X1 > 0 else 0.0
    log_s1 = X1 * math.log(s[0]) if X1 > 0 else 0.0

    F_e = multinomial_log_prob(X, e, prior_e)
    F_s = multinomial_log_prob(X, s, prior_s)

    prob_e = robust_cond_prob(X, e, s, prior_e, prior_s)

    print("Q1")
    for letter in range(ord('A'), ord('Z') + 1):
        print(f"{chr(letter)} {letter_count[chr(letter)]}")

    print("Q2")
    print(f"{log_e1:.4f}")
    print(f"{log_s1:.4f}")

    print("Q3")
    print(f"{F_e:.4f}")
    print(f"{F_s:.4f}")

    print("Q4")
    print(f"{prob_e:.4f}")
