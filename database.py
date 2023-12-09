import yaml

with open('locker_database.yaml', 'r') as file:
    data = yaml.safe_load(file)

[print(f"Locker {i + 1}: {path}") for i, path  in enumerate(data)]
print()


def write_to_database(locker_number = 1, path = None) -> str:
    """
    >>> write_to_database(locker_number = 1, 'img_database/1.jpg')
    ['img_database/1.jpg', 'img_database/2.jpg']"""
    with open('locker_database.yaml', 'r') as file:
        data = yaml.safe_load(file)

    with open('locker_database.yaml', 'w') as file:
        data[locker_number - 1] = path
        yaml.dump(data, file)



def read_from_database(locker_number = 1, path = None) -> str:
    """
    >>> read_from_database(1)
    'img_database/1.jpg'"""
    with open('locker_database.yaml', 'r') as file:
        data = yaml.safe_load(file)
        [print(f"Locker {i + 1}: {path}") for i, path  in enumerate(data)]
        return data[locker_number - 1]


if __name__ == "__main__":
    write_to_database(1, 'img_database/1.jpg')
    read_from_database(1)
    write_to_database(1, None)
    read_from_database(1)
