import re

phone_number_string = 'phone number: '


def process_text(string):
    phone_numbers = []
    possible_indices = [substring.end() for substring in re.finditer(phone_number_string, string.lower())]
    for index in possible_indices:
        if index == len(string):
            continue
        next_word = string[index:].split()[0]
        if next_word.isnumeric():
            phone_numbers.append(next_word)
    return phone_numbers


if __name__ == '__main__':
    input_string = input()
    while input_string:
        numbers = process_text(input_string)
        print("Extracted phone numbers:", ', '.join(numbers))
        input_string = input()
