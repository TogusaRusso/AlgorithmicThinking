import math
ALIGNMENT_DISTRIBUTION = {37: 1, 38: 1, 39: 3, 40: 10, 41: 20, 42: 23, 43: 37, 44: 40, 45: 46, 46: 56, 47: 64, 48: 63, 49: 66, 50: 60, 51: 56, 52: 56, 53: 63, 54: 51, 55: 35, 56: 28, 57: 25, 58: 23, 59: 24, 60: 22, 61: 20, 62: 14, 63: 17, 64: 13, 65: 5, 66: 11, 67: 2, 68: 5, 69: 3, 70: 6, 71: 3, 72: 2, 73: 2, 74: 2, 75: 3, 76: 5, 77: 2, 78: 2, 79: 2, 80: 1, 81: 1, 83: 1, 84: 2, 86: 1, 89: 1, 93: 1}
scores = []
for key, value in ALIGNMENT_DISTRIBUTION.items():
    for _ in xrange(value):
        scores.append(key)

N = len(scores)
mean = sum(scores)
mean = float(mean) / N
s_d = 0
for score in scores:
    s_d += (score - mean) ** 2
s_d = math.sqrt(float(s_d) / N)
real_score = 875
z_s = (real_score - mean) / s_d

print "Mean              :", mean
print "Standart deviation:", s_d
print "z-score           :", z_s
