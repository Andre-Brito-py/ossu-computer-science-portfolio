# Assume s is a string of lower case characters.
# Write a program that counts up the number of vowels contained in the string s.
# Valid vowels are: 'a', 'e', 'i', 'o', and 'u'.
# For example, if s = 'azcbobobegghakl', your program should print:
# Number of vowels: 5

s = 'azcbobobegghakl'

vowel_count = 0
for char in s:
    if char in 'aeiou':
        vowel_count += 1

print(f"Number of vowels: {vowel_count}")

# Write a program that prints the number of times the string 'bob' occurs in s.
# For example, if s = 'azcbobobegghakl', then your program should print:
# Number of times bob occurs is: 2

bob_count = 0
for i in range(len(s) - 2):
    if s[i:i+3] == 'bob':
        bob_count += 1

print(f"Number of times bob occurs is: {bob_count}")

# Write a program that prints the longest substring of s in which the letters occur in alphabetical order.
longest = ""
current = ""

for i in range(len(s)):
    if i == 0 or s[i] >= s[i-1]:
        current += s[i]
    else:
        current = s[i]
    
    if len(current) > len(longest):
        longest = current

print(f"Longest substring in alphabetical order is: {longest}")
