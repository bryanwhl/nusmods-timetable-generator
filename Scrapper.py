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

#=========================================================================
#Fetch timetable data
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

#=========================================================================
# remove modules past cutoff time
filtered = copy.deepcopy(timetable)
cutoff = 1700

for module_code in timetable:
    for slot_type in timetable[module_code]:
        for slot_number in timetable[module_code][slot_type]:
            for date_time in timetable[module_code][slot_type][slot_number]:
                time_list = date_time['times']
                remove = False
                for hour in time_list:
                    if hour > cutoff:
                        remove = True
            if remove:
                filtered[module_code][slot_type].pop(slot_number)

timetable = filtered
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

def getAvgFreeTime(finalTimetable):
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
                    schedule[day][int(time/100 - 8)]= 1

    gapNo = 0;
    gapTotal = 0;
    for day in schedule:
        counting = False
        for hour in day:
            if not counting and hour == 0:
                counting = True
                gapNo += 1
                gapTotal += 1
            elif counting and hour == 1:
                counting = False
            elif counting and hour == 0:
                gapTotal += 1
    return gapTotal / gapNo if gapNo > 0 else 0



'''
#initialize empty schedule
schedule = []
for i in range(5):
    schedule.append([])
    for j in range(14):
        schedule[i].append(0)

#print(schedule)
'''

validTimetables = []
for i in range(10000):
    #randomly assign timetable
    dictLen = len(timetable)
    randomTimetable = {}
    for module in timetable:
        classTypes = timetable[module]
        for classType in classTypes:
            classes = classTypes[classType]
            chosenClass = choice([*classes])
            if module not in randomTimetable:
                randomTimetable[module] = {}

            randomTimetable[module][classTypeConverter(classType)] = chosenClass

    #print(checkConflict(randomTimetable))
    if not checkConflict(randomTimetable):
        #print(OutputParser.create_url(randomTimetable))
        validTimetables.append(randomTimetable)
        #print(randomTimetable)
        #break
print("generated")
maxFreeTime = 0
bestTimetable = None
for validTimetable in validTimetables:
    #print(getAvgFreeTime(validTimetable))
    avgFreeTime = getAvgFreeTime(validTimetable)
    if avgFreeTime > maxFreeTime:
        maxFreeTime = avgFreeTime
        bestTimetable = validTimetable

print(OutputParser.create_url(bestTimetable))
print(maxFreeTime)
print("done")
