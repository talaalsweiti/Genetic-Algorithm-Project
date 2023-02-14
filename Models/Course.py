class Course:

    def __init__(self, course_id, teachers, year, is_lab):
        self.course_id = course_id
        self.teachers = teachers
        self.year = year
        self.is_lab = is_lab

    def __str__(self):
        teachers_list = []
        for i in self.teachers:
            teachers_list.append(str(i))
        return str(self.course_id) + " " + str(teachers_list)
