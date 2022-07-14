

entries = ["CSS", "Django", "Git", "HTML", "Python"]
entries = [entry.lower() for entry in entries]

query = input("query:" )
searchResult = []

for entry in entries:
    if query in entry:
        searchResult.append(entry)
        

print(searchResult)