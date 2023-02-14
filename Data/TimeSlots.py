slots = ["S8", "S9:30", "S11", "S12:30", "S2", "S3:30"
    , "M8", "M9:30", "M11", "M12:30", "M2", "M3:30"
    , "T8", "T9:30", "T11", "T12:30", "T2", "T3:30"
    , "W8", "W9:30", "W11", "W12:30", "W2", "W3:30"
    , "R8", "R9:30", "R11", "R12:30", "R2", "R3:30"]


#+ 1:15 hour for normal courses , or 2:45 for labs
def get_end_time(start_time, end_time, isL_lab):
    if start_time[1] == "8":  # if starts at 8
        if isL_lab:
            end_time = "10:45"
        else:
            end_time = "9:15"
    elif start_time[1] == "9":  # if starts at 9:30
        if isL_lab:
            end_time = "12:15"
        else:
            end_time = "10:45"
    elif start_time[1] == "2":  # if starts at 2
        if isL_lab:
            end_time = "4:45"
        else:
            end_time = "3:15"
    elif start_time[1] == "3":  # if starts at 3:30,no lab starts at this time
        end_time = "4:45"
    elif start_time[1] == "1" and start_time[2] == "1":  # if starts at 11
        if isL_lab:
            end_time = "1:45"
        else:
            end_time = "12:15"
    elif start_time[1] == "1" and start_time[2] == "2":  # if starts at 12:30
        if isL_lab:
            end_time = "3:15"
        else:
            end_time = "1:45"
    return end_time
