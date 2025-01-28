
with open("games.csv", "r") as file:
    lines = file.readlines()

with open("games.csv", "w") as file:
    file.writelines(line for line in lines if line.strip())