import argparse
import csv
import json
import os

parent_fieldnames = ['item_name', 'rel_answer', 'rel_objection']
sub_item_fieldnames = ['text', 'count', 'rel_count', 'type']


def process_answers(writer, parent_fields, answer_type, answer_list):
    for answer in answer_list:
        row_dict = parent_fields
        row_dict['text'] = answer['text']
        row_dict['count'] = answer['count']
        row_dict['rel_count'] = answer['rel_count']
        row_dict['type'] = answer_type
        writer.writerow(row_dict)


def process_item(item, writer):
    parent_item_fields = dict()
    parent_item_fields['item_name'] = item['name']
    parent_item_fields['rel_answer'] = item['rel_answer']
    parent_item_fields['rel_objection'] = item['rel_objection']

    process_answers(writer, parent_item_fields, 'Answer', item['answers'])
    process_answers(writer, parent_item_fields, 'Objection', item['objections'])


def parse_json(input_string, output_csv):
    if os.path.exists(output_csv):
        raise FileExistsError('\'' + output_csv + '\'')

    with open(output_csv, 'w+') as output_file:
        output_writer = csv.DictWriter(output_file, fieldnames=parent_fieldnames + sub_item_fieldnames)
        output_writer.writeheader()
        content = json.loads(input_string)
        for item in content['items']:
            process_item(item, output_writer)


def get_file_content(filename):
    return open(filename).read()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file', type=str, help='filename of the input json')
    parser.add_argument('-o', '--output_file', type=str,
                        default='result.csv', help='filename of the input json')
    try:
        arguments = parser.parse_args()
        parse_json(get_file_content(arguments.input_file), arguments.output_file)
        print("Json was parsed successfully")
    except FileNotFoundError as not_file_error:
        print("Couldn't find file", not_file_error.filename)
    except FileExistsError as file_exists_error:
        print("Failed to create the output file", file_exists_error, "as it already exists")
    except KeyError as key_error:
        print("Failed to parse json. No such field:", key_error)
    except Exception as exception:
        print("An error occurred")
        print(exception)