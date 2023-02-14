# check how many courses in the same slot for the same year
def fitness_calculator(courseSlots, score):
    courses_in_the_same_slot = [0, 0, 0, 0, 0]
    # check year by year
    total_sec = 202  # theres 2 slots for each section -> 101 section * 2
    for year in range(5):
        slots = {}
        for course in courseSlots:
            if course.year == year + 1:
                # check the slots
                for slot in courseSlots[course]:
                    if slot[0] in slots:
                        slots[slot[0]] += 1
                    else:
                        slots[slot[0]] = 0

        for slot in slots:
            courses_in_the_same_slot[year] += slots[slot]

        total_sec -= courses_in_the_same_slot[year]
    score.append(total_sec)
