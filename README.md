# LeverX_HomeTask_Lesson_1

Scrypt for sorting students by rooms

It take 3 parameters as console inputs - path to rooom file, path to students file and desirable output format (JSON or XML. If not valid format was given, scrypt ends its work and prints error message.

Result data is represented as modified original room file, where new key is added - list of students with their names and id.

For example,

  {
    "id": 0,
    "name": "Room #0",
    "students": [
      {
        "id": 345,
        "name": "William Perez"
      },
      {
        "id": 976,
        "name": "Daniel Smith"
      },
    ]
  },
