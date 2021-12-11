import json
import pprint
import argparse
import sys

XML_SKELETON = """<?xml version="1.0" encoding="utf-8" ?>
<root>
%s
</root>"""

ROOM_SKELETON = """
    <room_id> %d </room_id>
    <room_name> %s </room_name>   
    <room_students> %s </room_students> 
"""

STUDENTS_SKELETON = """
    <student> 
    <student_id> %d </student_id>
    <student_name> %s </student_name>   
    </student> 
"""


class CLIParser:

    def __init__(self):
        self.parser = argparse.ArgumentParser()

    def parse_args(self):
        self.parser.add_argument('source_to_rooms_file', type=str, action='store', nargs='?')
        self.parser.add_argument('source_to_students_file', type=str, action='store', nargs='?')
        self.parser.add_argument('output_format', type=str, action='store', nargs='?')
        args = self.parser.parse_args()
        if None in vars(args).values():
            raise SystemExit("Error: all arguments must be given")
        return args


class DataReader:
    def __init__(self):
        self.data = None

    def read_data(self, path: str):
        raise NotImplementedError


class JsonReader(DataReader):

    def __convert_data(self):
        return json.loads(self.data)

    def read_data(self, path: str):
        with open(path, mode='r') as data:
            self.data = data.read()
        return self.__convert_data()


class DataSorter:
    def __init__(self, rooms_data, students_data):
        self.sorted_students = {}
        self.rooms = rooms_data
        self.students = students_data

    def sort_data(self):
        raise NotImplementedError


class StudentInRoomSorter(DataSorter):
    def sort_data(self):
        for person in self.students:
            student_room_number = person.get('room')
            self.sorted_students[student_room_number] = self.sorted_students.get(student_room_number, []) + [person]
        for room in self.rooms:
            room['students'] = self.sorted_students.get(room['id'], [])
        return self.rooms


class DataFormatter:
    def __init__(self, data):
        self.data = data

    def format_data(self):
        raise NotImplementedError


class DataToJsonFormatter(DataFormatter):
    def format_data(self):
        return json.dumps(self.data)


class DataToXmlFormatter(DataFormatter):
    def format_data(self):
        xml_text = ''
        for row in self.data:
            student_info = ''
            room_id = row.get("id")
            room_name = row.get("name")
            for record in row['students']:
                student_info += STUDENTS_SKELETON % (record.get('id'), record.get('name'))
            xml_text += ROOM_SKELETON % (room_id, room_name, student_info)
        return XML_SKELETON % xml_text


class DataWriter:
    def __init__(self):
        self.formats = {'json': DataToJsonFormatter,
                        'xml': DataToXmlFormatter,
                        }

    def write_data(self, data: list, output_format: str):
        try:
            driver = self._select_driver(output_format)
        except ValueError:
            print("Not supported output format")
            exit()
        else:
            output_data = driver(data).format_data()
            with open(f'result.{output_format}', mode='w') as result_data:
                result_data.write(output_data)

    def _select_driver(self, output_format: str):
        if output_format not in self.formats:
            raise ValueError('Not')
        else:
            return self.formats.get(output_format)


def main():
    cli_parser = CLIParser()
    options = cli_parser.parse_args()

    data_reader = JsonReader()
    rooms = data_reader.read_data(options.source_to_rooms_file)
    students = data_reader.read_data(options.source_to_students_file)
    result_file_format = options.output_format.lower()

    rooms_with_students_sorter = StudentInRoomSorter(rooms_data=rooms, students_data=students)
    rooms_with_students = rooms_with_students_sorter.sort_data()

    output_data_writer = DataWriter()
    output_data_writer.write_data(data=rooms_with_students, output_format=result_file_format)


if __name__ == '__main__':
    main()
