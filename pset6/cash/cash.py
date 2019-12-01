from cs50 import get_float

# Prompt user for change, and if user didn't provide a valid change reprompts user
while True:
    change = get_float("Change owed: ")
    if change >= 0:
        break

# Convert change into cents
cents = round(change * 100)

coins = 0

coins += cents // 25
cents = cents % 25

coins += cents // 10
cents = cents % 10

coins += cents // 5
cents = cents % 5

coins += cents // 1
cents = cents % 1

print(coins)
