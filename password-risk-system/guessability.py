import re
import math 
def load_sequences(path):
    sequence = []
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            seq = line.strip().lower()
            if seq:
                sequence.append(seq)
    return sequence

file_path = "/Users/saheed/Desktop/main project/data/10k-most-common.txt"
common_patterns = set(load_sequences(file_path))

def estimate_guesses_and_reason(pw):
    reasons = []
    if pw is None or pw == "":
        return 0, ["Empty Password"]

    pw_length = len(pw)

    low_char_pw = any("a" <= c <= "z" for c in pw)
    upper_pw = any("A" <= c <= "Z" for c in pw)
    digit_pw = any(c.isdigit() for c in pw)
    symbol_pw = any(not c.isalnum() for c in pw)

    charcter_size = 0
    if low_char_pw:
        charcter_size += 26
    if upper_pw:
        charcter_size += 26
    if digit_pw:
        charcter_size += 10
    if symbol_pw:
        charcter_size += 32
    if charcter_size == 0:
        charcter_size = 1

    guesses = charcter_size ** pw_length

    #entropy formula = E = L × log2(R) 

    entropy = pw_length * math.log2(charcter_size)  

    if pw_length < 12:
        reasons.append("password is less than twelve characters")

    lower_pw = pw.lower()

    if lower_pw in common_patterns:
        reasons.append("dictionary password")

    m = re.fullmatch(r"([a-z]{3,})(\d{1,6})", lower_pw)
    if m and m.group(1) in common_patterns:
        reasons.append("dictionary word + digits")

    if any(w in lower_pw for w in common_patterns):
        reasons.append("contains dictionary word")
    
    if re.search(r"(.)\1{3,}", pw):
        reasons.append("repeated character sequence")


    leet = str.maketrans({
        "@": "a", "4": "a", "8": "b", "3": "e", "6": "g", "#": "h",
        "1": "i", "!": "i", "|": "i", "0": "o", "$": "s", "5": "s",
        "7": "t", "+": "t", "2": "z"
    })
    normalized = lower_pw.translate(leet)
    if normalized in common_patterns:
        reasons.append("leetspeak dictionary password")
    
    if any(w in normalized for w in common_patterns):
        reasons.append("contains leetspeak dictionary word")

    return guesses, reasons, entropy


def decision(pw):
    guesses, reasons, entropy = estimate_guesses_and_reason(pw)

    if pw is None or len(pw.strip()) < 12:
        return "NON ACCEPTABLE", None, reasons

    #Structural Rejcetions
    if any(r in reasons for r in [
        "dictionary password",
        "dictionary word + digits",
        "leetspeak dictionary password","contains dictionary word", "contains leetspeak dictionary word", "repeated character sequence", "entropy below 75 bits"
    ]):
        return "NON ACCEPTABLE", None, reasons
    
    #Entropy Rejection if below threshold 

    if entropy < 75 :
        reasons.append("entropy below 75 bits")
        return "NON ACCEPTABLE", None, reasons

    
    return "ACCEPTABLE", guesses, reasons
