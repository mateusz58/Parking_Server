



string = input("Enter a string: ")

if all(x.isalpha() or x.isspace() for x in string):
    print("Only alphabetical letters and spaces: yes")
else:
    print("Only alphabetical letters and spaces: no")