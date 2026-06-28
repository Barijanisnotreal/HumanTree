def id_creator(name, birth, print_result=False):
    '''
    Function that receives a string with the name and a string with the birth,
    and creates an ID by joining the name and birth. The name is converted to lowercase
    and transformed into a list of ASCII values separated by semicolons. The birth is
    appended in plain text in the format DD/MM/YYYY.

    Parameters:
        name (str): The name to convert.
        birth (str): The birth date in format DD/MM/YYYY.
        print_result (bool): If True, the result is printed.

    Returns:
        str: The final ID string.
    '''
    name = name.lower()
    ascii_name = ';'.join(str(ord(char)) for char in name) + ';'
    result = ascii_name + birth

    if print_result:
        print(result)

    return result


print(id_creator("Barijan","06112005"))

