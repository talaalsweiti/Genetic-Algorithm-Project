import random
from Data.TimeSlots import slots


# two slots for each course
# M X (T) , T x (M,W) , W X (T,R) , R X (W)
def check_if_consecutive(day1, day2):
    if day1 == 'S' and day2 == 'S':
        return True
    if day1 == 'M':
        if day2 == 'T' or day2 == 'M':
            return True
    if day1 == 'T':
        if day2 == 'M' or day2 == 'W' or day2 == 'T':
            return True
    if day1 == 'W':
        if day2 == 'T' or day2 == 'R' or day2 == 'W':
            return True
    if day1 == 'R':
        if day2 == 'W' or day2 == 'R':
            return True
    return False


def generate(courses, course_slots):
    for course in courses:
        used_slots = []
        course_teachers = course.teachers

        for teacher in course_teachers:
            if not course.is_lab:
                index = random.randint(0, 29)
                index2 = random.randint(0, 29)
                while (slots[index2] in teacher.time_slots) or (
                        check_if_consecutive(slots[index][0], slots[index2][0])) or (
                        check_if_consecutive(slots[index2][0], slots[index][0])) or (slots[index] in teacher.time_slots):
                    index2 = random.randint(0, 29)
                    index = random.randint(0, 29)
                teacher.time_slots[slots[index]] = course.course_id
                teacher.time_slots[slots[index2]] = course.course_id
                used_slots.append([slots[index],teacher])
                used_slots.append([slots[index2],teacher])
            else:
                index = random.randint(0, 28)
                while (slots[index] in teacher.time_slots) or (slots[index + 1] in teacher.time_slots) \
                        or (slots[index][1] == '3') or (slots[index + 1][1] == '8'):
                    index = random.randint(0, 28)
                teacher.time_slots[slots[index]] = course.course_id
                used_slots.append([slots[index],teacher])
                index += 1
                teacher.time_slots[slots[index]] = course.course_id
                used_slots.append([slots[index],teacher])
        course_slots[course] = used_slots
