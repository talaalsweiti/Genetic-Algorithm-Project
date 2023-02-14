from Models.Course import Course
from Models.Teacher import Teacher
import os


def read_courses_name():
    # Get the directory path of the current script
    current_dir = os.path.dirname(__file__)

    # Specify the file name
    file_name = "CoursesFile.txt"
    # Get the full path of the file
    file_path = os.path.join(current_dir, file_name)
    f = open(file_path, "r")
    ############
    id_name = {}
    for line in f:
        if line == '\n':
            continue
        else:
            current_line = line.split(";")
            course_id = current_line[0]
            id_name[course_id] = current_line[1]
    return id_name


def read_courses(courses_file, courses, all_teachers):
    for line in courses_file:
        if line == '\n':
            continue
        else:
            current_teachers = []
            current_line = line.split(";")
            course_id = current_line[0]
            teachers_list = current_line[1].split(",")

            for t in teachers_list:
                flag = False
                t = t.strip()  # to remove \n in the end of the line
                for teacher in all_teachers:
                    # if the teacher already exists, just add the course to it
                    if t == teacher.name:
                        flag = True
                        current_teachers.append(teacher)

                # if it's a new teacher
                if not flag:
                    teacherObject = Teacher(t)
                    current_teachers.append(teacherObject)
                    all_teachers.append(teacherObject)

            course = Course(course_id, current_teachers, int(course_id[4]), course_id[5] == '1')
            courses.append(course)