import difflib

str1 = 'testtest'
str2 = 'testtest'
rate = difflib.SequenceMatcher(None, str1, str2).ratio()
print(rate)
