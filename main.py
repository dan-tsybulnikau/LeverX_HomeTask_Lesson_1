import json

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


class DataDriver:
    """Base class for data manipulations"""
    def __init__(self):
        self.data = None

    def __convert_data(self):
        return json.loads(self.data)

    def read_data(self, path: str):
        with open(path, mode='r') as data:
            self.data = data.read()
        return self.__convert_data()

    def write_data(self, data):
        raise NotImplementedError


class JSONWriter(DataDriver):
    def write_data(self, data):
        with open('result.json', mode='w') as result_file:
            result_file.write(data)


class XMLWriter(DataDriver):
    def write_data(self, data):
        with open('result.xml', mode='w') as result_file:
            result_file.write(data)


class DataFormatter:

    @staticmethod
    def format_student_data(data: dict):
        del data['room']
        return data

    @staticmethod
    def format_to_json(data: list):
        return json.dumps(data)

    @staticmethod
    def format_to_xml(data: list):
        xml_text = ''
        for row in data:
            student_info = ''
            room_id = row.get("id")
            room_name = row.get("name")
            for record in row['students']:
                student_info += STUDENTS_SKELETON % (record.get('id'), record.get('name'))
            xml_text += ROOM_SKELETON % (room_id, room_name, student_info)
        return XML_SKELETON % xml_text


if __name__ == '__main__':
    path_to_rooms_file = input('Enter path to rooms file (absolute): ')
    path_to_students_file = input('Enter path to students file (absolute): ')
    output_format = input('Enter path to rooms file (JSON or XML): ')
    if output_format not in ['JSON', 'XML']:
        print('Not valid output format.')
        exit()
    data_driver = DataDriver()
    rooms = data_driver.read_data(path_to_rooms_file)
    students = data_driver.read_data(path_to_students_file)
    for room in rooms:
        room['students'] = [DataFormatter.format_student_data(student) for student in students
                            if student.get('room', None) == room['id']]

    if output_format == 'JSON':
        writer = JSONWriter()
        output_data = DataFormatter.format_to_json(rooms)
    elif output_format == 'XML':
        writer = XMLWriter()
        output_data = DataFormatter.format_to_xml(rooms)

    writer.write_data(output_data)

