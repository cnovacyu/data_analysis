#Many organizations have user ids which are constrained in some way. 
# #Imagine you work at an internet service provider and the user ids 
# are all two letters followed by two numbers (e.g. aa49). Your task 
# at such an organization might be to hold a record on the billing 
# activity for each possible user.

#Write an initialization line as a single list comprehension which 
# creates a list of all possible user ids. Assume the letters are all lower case.

lowercase = 'abcdefghijklmnopqrstuvwxyz'
digits = '0123456789'

userid = []
for i in lowercase:
    for j in lowercase:
        for x in digits:
            for y in digits:
                userid.append(i+j+x+y)

print(len(userid))

list_comp = [i+j+x+y for i in lowercase for j in lowercase for x in digits for y in digits]

print(len(list_comp))
print(userid == list_comp)