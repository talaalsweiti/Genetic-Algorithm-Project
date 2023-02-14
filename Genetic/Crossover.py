import copy
import random

from Genetic.Fitness import fitness_calculator
from Genetic.Mutation import child_mutation


def crossover(solutions):
    solutions.sort(key=lambda x: int(x[0]))
    length = len(solutions)
    # take the highest two fitness
    first_parent = solutions[length - 1]
    sec_parent = solutions[length - 2]
    temp_first_parent = copy.deepcopy(first_parent)
    temp_sec_parent = copy.deepcopy(sec_parent)

    first_parent_course_slots = first_parent[3]

    sec_parent_course_slots = sec_parent[3]
    # print("First parent score ",first_parent[0], " second parent score : " , sec_parent[0])
    visited = {}

    for course in first_parent_course_slots:
        if len(visited) == 33:
            break
        for i in range(0, len(first_parent_course_slots[course]) - 1, 2):
            first_time_slot = first_parent_course_slots[course][i][0]
            sec_time_slot = first_parent_course_slots[course][i + 1][0]
            teacher = first_parent_course_slots[course][i][1]
            random_course_index = random.randint(0, 33)
            random_course = list(sec_parent_course_slots)[random_course_index]
            if course.is_lab:
                while not random_course.is_lab or course.course_id == random_course.course_id or random_course_index in visited:
                    random_course_index = random.randint(0, 33)
                    random_course = list(sec_parent_course_slots)[random_course_index]
            else:
                while random_course.is_lab or course.course_id == random_course.course_id or random_course_index in visited:
                    random_course_index = random.randint(0, 33)
                    random_course = list(sec_parent_course_slots)[random_course_index]

            for j in range(0, len(sec_parent_course_slots[random_course]) - 1, 2):
                # take section by section (each consecutive time slots are one section)
                third_time_slot = sec_parent_course_slots[random_course][j][0]
                fourth_time_slot = sec_parent_course_slots[random_course][j + 1][0]
                sec_teacher = sec_parent_course_slots[random_course][j][1]

                if (third_time_slot in teacher.time_slots) or (fourth_time_slot in teacher.time_slots) \
                        or (first_time_slot in sec_teacher.time_slots) \
                        or (sec_time_slot in sec_teacher.time_slots):
                    continue

                if first_time_slot in teacher.time_slots:
                    teacher.time_slots.pop(first_time_slot)
                if sec_time_slot in teacher.time_slots:
                    teacher.time_slots.pop(sec_time_slot)

                first_parent_course_slots[course][i][0], sec_parent_course_slots[random_course][j][0] = \
                    sec_parent_course_slots[random_course][j][0], first_parent_course_slots[course][i][0]
                first_parent_course_slots[course][i + 1][0], sec_parent_course_slots[random_course][j + 1][0] = \
                    sec_parent_course_slots[random_course][j + 1][0], first_parent_course_slots[course][i + 1][0]

                teacher.time_slots[third_time_slot] = course.course_id
                teacher.time_slots[fourth_time_slot] = course.course_id

                visited[random_course] = True

                break

    # mutation
    score = []
    fitness_calculator(first_parent[3], score)
    new_child = copy.deepcopy(first_parent)
    child_mutation(new_child)
    fitness_calculator(new_child[3], score)

    # print("after crossover", score[0], " after Mutation", score[1])

    solutions.append([score[1], new_child[1], new_child[2], new_child[3]])
    first_parent = copy.deepcopy(temp_first_parent)
    sec_parent = copy.deepcopy(temp_sec_parent)
