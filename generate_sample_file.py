import lorem

with open('sample.txt', "w") as file:
    file.write(
        ("".join([lorem.text() for _ in range(3)])).replace("\n", "")
    )
    file.close()
