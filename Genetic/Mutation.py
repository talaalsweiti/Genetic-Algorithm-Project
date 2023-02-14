import random
from Data.TimeSlots import slots
from Genetic.GenerateSoulation import check_if_consecutive


def child_mutation(child):
    child_course_slots = child[3]
    cnt = 0  # to check if we have 5 successful sections changes (%15 from the total courses number)

    while cnt < 6:
        random_course_index = random.randint(0, 1)
        randomCourse = list(child_course_slots)[random_course_index]
        visited = {}
        flg = True
        if randomCourse.is_lab:
            for j in range(0, len(child_course_slots[randomCourse]) - 1, 2):
                first_time_slot = child_course_slots[randomCourse][j][0]
                sec_time_slot = child_course_slots[randomCourse][j + 1][0]
                teacher = child_course_slots[randomCourse][j][1]
                time_slot_index = random.randint(0, 28)
                visited[time_slot_index] = 1
                while (slots[time_slot_index] in teacher.time_slots) or (slots[time_slot_index + 1] in teacher.time_slots) \
                        or (slots[time_slot_index][1] == '3') or (slots[time_slot_index + 1][1] == '8'):
                    time_slot_index = random.randint(0, 28)
                    visited[time_slot_index] = 1
                    if len(visited) == 29:
                        flg = False
                        break
                if not flg:
                    break
                if first_time_slot in teacher.time_slots:
                    teacher.time_slots.pop(first_time_slot)
                if sec_time_slot in teacher.time_slots:
                    teacher.time_slots.pop(sec_time_slot)
                child_course_slots[randomCourse][j][0] = slots[time_slot_index]
                child_course_slots[randomCourse][j + 1][0] = slots[time_slot_index + 1]
                teacher.time_slots[slots[time_slot_index]] = randomCourse.course_id
                teacher.time_slots[slots[time_slot_index + 1]] = randomCourse.course_id
        else:
            for j in range(0, len(child_course_slots[randomCourse]) - 1, 2):
                first_time_slot = child_course_slots[randomCourse][j][0]
                sec_time_slot = child_course_slots[randomCourse][j + 1][0]
                teacher = child_course_slots[randomCourse][j][1]
                index = random.randint(0, 29)
                index2 = random.randint(0, 29)
                while (slots[index2] in teacher.time_slots) or (
                        check_if_consecutive(slots[index][0], slots[index2][0])) or (
                        check_if_consecutive(slots[index2][0], slots[index][0])) or (slots[index] in teacher.time_slots):
                    index2 = random.randint(0, 29)
                    index = random.randint(0, 29)
                    if len(visited) == 29:
                        flg = False
                        break
                if not flg:
                    break

                if first_time_slot in teacher.time_slots:
                    teacher.time_slots.pop(first_time_slot)
                if sec_time_slot in teacher.time_slots:
                    teacher.time_slots.pop(sec_time_slot)
                child_course_slots[randomCourse][j][0] = slots[index]
                child_course_slots[randomCourse][j + 1][0] = slots[index2]
                teacher.time_slots[slots[index]] = randomCourse.course_id
                teacher.time_slots[slots[index2]] = randomCourse.course_id
        if flg:
            cnt += 1
