import json
import ast


def read_files():
    """
    Reading the config file and the updates file
    :return:
    data :  dictionary of the curt configuration
    updates : List of demanded updates
    """
    f = open("config.json")
    data = json.load(f)
    f = open('updates.txt', 'r')
    updates = f.read().splitlines()
    return data, updates


def format_key(key):
    """
    Formatting the list slicing into a .idx  (page.data[0] => page.data.0)
    :param key: String, The update Key
    :return:
    new_key : String of the format
    """
    new_key = ''
    for i in key:
        if i == '[':
            new_key = new_key + '.'
        elif i == ']':
            continue
        else:
            new_key = new_key + i
    return new_key


def update_values(data, key, new_value):
    """
    Looping the configuration file the key and finally modify the value

    param data: Dictionary, the current configuration
    :param key: String, the path to the value to update
    :param new_value: The new value to the specified path
    """
    key = key.split('.')
    n = len(key)
    try:
        for idx, item in enumerate(key):
            if isinstance(data, list):
                item = int(item)
            if idx == n - 1:
                data[item] = new_value
            else:
                data = data[item]
        key = '.'.join(key)
        print(f'Update {key} is Successfully Done')
    except KeyError as error:
        key = '.'.join(key)
        print(f'Update {key} Failed. Reason: {error} key does not exist')


def RepresentsInt(new_value):
    """
    Checks if a String is an Int
    :param new_value, String. The new value
    :return: Boolean
    """
    try:
        int(new_value)
        return True
    except ValueError:
        return False


def transform_new_value(new_value):
    """
    Transforms a String to its possible data type
    :param new_value, String. The new value
    :return:
    Int or Dictionary : Depends on the String format
    """
    if RepresentsInt(new_value):
        new_value = int(new_value)
    elif isinstance(ast.literal_eval(new_value), dict):
        new_value = ast.literal_eval(new_value)
    return new_value


if __name__ == '__main__':
    data, updates = read_files()
    print("Original Configuration")
    print(json.dumps(data, indent=1))

    for update in updates:
        update = format_key(update)  # Formatting the update key
        key, new_value = update.split(':', 1)
        new_value = transform_new_value(new_value)  # Transforming the new value type
        update_values(data, key, new_value)  # Updating the configuration
    with open('new_config.json', 'w') as fp:
        print("New Configuration")
        print(json.dumps(data, indent=1))
        json.dump(data, fp, indent=4)
