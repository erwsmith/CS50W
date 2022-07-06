people = [
    {"name": "Harry", "house": "Gryffindor"},
    {"name": "Cho", "house": "Ravenclaw"},
    {"name": "Draco", "house": "Slytherin"},
]

# def f(person):
#     # return person["house"]
#     return person["name"]
# people.sort(key=f)

# alternative to above using lambda:
people.sort(key=lambda person: person["name"])

print(people)