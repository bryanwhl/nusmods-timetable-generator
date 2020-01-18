timetable = {"CS2030" : {"LEC" : 2, "LAB" : 18, "REC" : 2},
            "CS2040S" : {"TUT" : 19, "REC" : 7, "LEC" : 1}}

semester = 2

#Parser
def create_url(timetable):
    url = "https://nusmods.com/timetable/sem-" + str(semester) + "/share?"

    for module in timetable:
        url += module + "="

        for classType in timetable[module]:
            url += classType + ":" + str(timetable[module][classType]) + ","

        url += "&"

    return url


#print(create_url(timetable))
