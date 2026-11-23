import re

def words_to_number(s):
    # Map words to numbers
    num_words = {
        'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
        'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
        'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14,
        'fifteen': 15, 'sixteen': 16, 'seventeen': 17, 'eighteen': 18,
        'nineteen': 19, 'twenty': 20, 'thirty': 30, 'forty': 40,
        'fifty': 50, 'sixty': 60, 'seventy': 70, 'eighty': 80, 'ninety': 90
    }
    multipliers = {
        'hundred': 100,
        'thousand': 1000,
        'lakh': 100000,
        'lakhs': 100000,
        'crore': 10000000,
        'crores': 10000000
    }
    
    tokens = re.findall(r'\b[a-zA-Z]+\b', s.lower())
    total = 0
    current = 0
    for token in tokens:
        if token in num_words:
            current += num_words[token]
        elif token == 'hundred':
            current = (current if current > 0 else 1) * 100
        elif token in multipliers:
            mult = multipliers[token]
            current = (current if current > 0 else 1) * mult
            total += current
            current = 0
        elif token == 'and':
            continue
    total += current
    return total

print("one lakh seven thousand three hundred ->", words_to_number("one lakh seven thousand three hundred"))
print("thirty-two thousand three hundred ->", words_to_number("thirty-two thousand three hundred"))
print("twenty-four thousand ->", words_to_number("twenty-four thousand"))
