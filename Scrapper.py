import requests
import copy
from random import choice

import UserInput
import OutputParser

def dayConverter(dayString):
    if dayString == "Monday":
        return 0
    elif dayString == "Tuesday":
        return 1
    elif dayString == "Wednesday":
        return 2
    elif dayString == "Thursday":
        return 3
    elif dayString == "Friday":
        return 4

def classTypeConverter(classType):
    if classType == "Lecture":
        return "LEC"
    elif classType == "Laboratory":
        return "LAB"
    elif classType == "Recitation":
        return "REC"
    elif classType == "Sectional":
        return "SECT"
    elif classType == "Tutorial":
        return "TUT"
    elif classType == "LEC":
        return "Lecture"
    elif classType == "LAB":
        return "Laboratory"
    elif classType == "REC":
        return "Recitation"
    elif classType == "SECT":
        return "Sectional"
    elif classType == "TUT":
        return "Tutorial"

'''
userInput = UserInput.ask_for_inputs()
academicYear = userInput["acadYear"]
semester = userInput["semNumber"]
modules = userInput["modArray"]
data = {"constraintList" : userInput["constraintList"],
        "constraintData" : userInput["constraintData"]}
'''

academicYear = "2019-2020"
semester = 1
modules = ["CS2030", "CS2040S", "MA2216", "MA2104", "GER1000", "GET1029", "GES1023"]

timetable = {}

for module in modules:
    response = requests.get("https://api.nusmods.com/v2/" + academicYear + "/modules/" + module + ".json")
    moduleData = response.json()
    #print("====================================================")
    #print("Timetable for " + module)
    #print(moduleData)
    timetableData = {}
    if len(moduleData["semesterData"]) > 1:
        timetableData = moduleData["semesterData"][semester]["timetable"]
    else:
        timetableData = moduleData["semesterData"][0]["timetable"]


    slots = {}
    for classSlot in timetableData:
        lessonType = classSlot["lessonType"]
        classNo = classSlot["classNo"]
        classDay = classSlot["day"]

        times = []
        for i in range(int(classSlot["startTime"]), int(classSlot["endTime"]), 100):
            times.append(i)

        '''
        print("Class: " + classNo)
        print("Day: " + classDay)
        print("Start Time: " + classSlot["startTime"])
        print("End Time: " + classSlot["endTime"])
        print(times)
        print("Type: " + lessonType)
        '''

        if lessonType not in slots:
            slots[lessonType] = {}

        if classNo not in slots[lessonType]:
            slots[lessonType][classNo] = []

        slots[lessonType][classNo].append({ "day" : classDay, "times" : times })

    timetable[module] = slots

print(timetable)

def checkConflict(finalTimetable):
    #initialize empty schedule
    schedule = []
    for i in range(5):
        schedule.append([])
        for j in range(14):
            schedule[i].append(0)

    for module in finalTimetable:
        classTypes = finalTimetable[module]
        for classType in classTypes:
            chosenClass = classTypes[classType]
            slots = timetable[module][classTypeConverter(classType)][chosenClass]
            for slot in slots:
                day = dayConverter(slot["day"])
                times = slot["times"]
                for time in times:
                    if schedule[day][int(time/100 - 8)] == 1:
                        return True
                    else:
                        schedule[day][int(time/100 - 8)]= 1

    return False


'''
#initialize empty schedule
schedule = []
for i in range(5):
    schedule.append([])
    for j in range(14):
        schedule[i].append(0)

#print(schedule)
'''
for i in range(1000):
    #randomly assign timetable
    available = copy.deepcopy(timetable)
    dictLen = len(available)
    randomTimetable = {}
    while dictLen > 0:
        module = choice([*available])
        moduleData = available[module]
        chosenClass = ""
        typeLen = len(moduleData)

        while typeLen > 0:
            chosenClassType = choice([*moduleData])
            classes = moduleData[chosenClassType]
            chosenClass = choice([*classes])

            for timeslot in classes[chosenClass]:
                day = dayConverter(timeslot["day"])
                times = timeslot["times"]
                for time in times:
                    #schedule[day][int((time/100) - 8)] = { "ModuleCode" : module, "ClassType" : chosenClassType, "ClassNo" : chosenClass}
                    if module not in randomTimetable:
                        randomTimetable[module] = {}

                    randomTimetable[module][classTypeConverter(chosenClassType)] = chosenClass

            typeLen -= 1
            del available[module][chosenClassType]
        del available[module]
        dictLen -= 1

    #print(checkConflict(randomTimetable))
    if not checkConflict(randomTimetable):
        print(OutputParser.create_url(randomTimetable))
        #print(randomTimetable)
        #break

print("done")
