from os import listdir
import random
import re

def filenames():
    filenames = listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename) for filename in filenames if filename.endswith(".md")))

print(random.choice(filenames()))


# def lowerList(entries):
#     entries = [entry.lower() for entry in entries]

# entries = ["CSS", "Django", "Git", "HTML", "Python"]
# entries = [entry.lower() for entry in entries]




