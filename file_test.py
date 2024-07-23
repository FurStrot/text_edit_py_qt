with open("text.txt", "r") as file:
    data = file.readlines()

total = 0

for line in data:
    numbers = line.split(" ")
    for number in numbers:
        if number == "1":
            total += 1

with open("text_number.txt", "w") as file:
    file.write(str(total))

# сумма всех 1 вывести в отд. файл