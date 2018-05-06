from langdetect import detect_langs


string = "Bonjour"
res = detect_langs(string)
print(res)

string = "The quick brown fox"
res = detect_langs(string)
print(res)

string = "Hallo, mein Freund"
res = detect_langs(string)
print(res)
