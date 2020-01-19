import requests
import copy
import json
import math
from random import choice

import UserInput
import OutputParser
import screenshot
from venue_distance import get_coord, find_distance


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
    elif classType == "Sectional Teaching":
        return "SEC"
    elif classType == "Tutorial":
        return "TUT"
    elif classType == "Seminar-Style Module Class":
        return "SEM"
    elif classType == "LEC":
        return "Lecture"
    elif classType == "LAB":
        return "Laboratory"
    elif classType == "REC":
        return "Recitation"
    elif classType == "SEC":
        return "Sectional Teaching"
    elif classType == "TUT":
        return "Tutorial"
    elif classType == "SEM":
        return "Seminar-Style Module Class"


def checkConflict(finalTimetable, timetableData):
    # initialize empty schedule
    schedule = []
    for i in range(5):
        schedule.append([])
        for j in range(14):
            schedule[i].append(0)

    for module in finalTimetable:
        classTypes = finalTimetable[module]
        for classType in classTypes:
            chosenClass = classTypes[classType]
            slots = timetableData[module][classTypeConverter(classType)][chosenClass]
            for slot in slots:
                day = dayConverter(slot["day"])
                times = slot["times"]
                for time in times:
                    if schedule[day][int(time / 100 - 8)] == 1:
                        return True
                    else:
                        schedule[day][int(time / 100 - 8)] = 1

    return False


def simplifyTimetable(finalTimetable, timetableData):
    # Convert timetable into array format
    # initialize empty schedule
    schedule = []
    for i in range(5):
        schedule.append([])
        for j in range(14):
            schedule[i].append(0)

    for module in finalTimetable:
        classTypes = finalTimetable[module]
        for classType in classTypes:
            chosenClass = classTypes[classType]
            slots = timetableData[module][classTypeConverter(classType)][chosenClass]
            for slot in slots:
                day = dayConverter(slot["day"])
                times = slot["times"]
                for time in times:
                    schedule[day][int(time / 100 - 8)] = 1
    return schedule


def getAvgFreeTime(finalTimetable, timetableData):
    tbl = simplifyTimetable(finalTimetable, timetableData)
    gapNo = 0;
    gapTotal = 0;
    for day in tbl:
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


def top_free_time(timetableList, timetableData, return_size):
    sorted_timetables = sorted(timetableList, key=lambda timetable: getAvgFreeTime(timetable, timetableData), reverse=True)
    return sorted_timetables[:return_size]


def filter_block_size(timetableList, timetableData, max_size):
    filtered = []

    for timetable in timetableList:
        tbl = simplifyTimetable(timetable, timetableData)
        maxBlockSize = 0
        blockSize = 0
        for day in tbl:
            counting = False
            for hour in day:
                if not counting and hour == 1:
                    counting = True
                    blockSize += 1
                elif counting and hour == 0:
                    counting = False
                    maxBlockSize = blockSize if blockSize > maxBlockSize else maxBlockSize
                    blockSize = 0
                elif counting and hour == 1:
                    blockSize += 1
        if maxBlockSize < max_size:
            filtered.append(timetable)

    return filtered


def travel_distance(finalTimetable, timetableData, venue_list):
    # Construct special array for keeping track of venue changes
    schedule = []
    for i in range(5):
        schedule.append([])
        for j in range(14):
            schedule[i].append(0)

    for module in finalTimetable:
        classTypes = finalTimetable[module]
        for classType in classTypes:
            chosenClass = classTypes[classType]
            slots = timetableData[module][classTypeConverter(classType)][chosenClass]
            for slot in slots:
                day = dayConverter(slot["day"])
                times = slot["times"]
                venue = slot["venue"]
                for time in times:
                    schedule[day][int(time / 100 - 8)] = venue

    distance = 0
    for day in schedule:
        prev_venue = day[0]
        for venue in day:
            if venue != prev_venue:
                if venue == 0:
                    continue
                if prev_venue != 0:
                    distance += math.log(find_distance(venue, prev_venue, venue_list))
                prev_venue = venue
    # print(distance)
    return distance


def min_travel_distance(timeTableList, timetableData, venue_list, return_size):
    sorted_timetables = sorted(timeTableList, key=lambda timetable: travel_distance(timetable, timetableData, venue_list))
    return sorted_timetables[:return_size]

def generate(parameters):
    #Set up ssl certificates


    # Load venue data
    with open('venues.json', 'r') as f:
        venue_list = json.load(f)

    academicYear = "2019-2020"
    semester = parameters["semester"]
    #modules = ["CS2030", "CS2040S", "CS2100", "IS1103", "GER1000", "ES1103"]
    modules = parameters["moduleArray"]
    # =========================================================================
    # Fetch timetable data
    timetable = {}
    for module in modules:
        response = requests.get("https://api.nusmods.com/v2/" + academicYear + "/modules/" + module + ".json")
        moduleData = response.json()
        # print("====================================================")
        # print("Timetable for " + module)
        # print(moduleData)
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
            classVenue = classSlot["venue"]

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

            slots[lessonType][classNo].append({"day": classDay, "times": times, "venue": classVenue})

        timetable[module] = slots

    # =========================================================================
    # remove modules past cutoff times and in fixed slots
    filtered = copy.deepcopy(timetable)
    startCutoff = parameters["startTime"]
    endCutoff = parameters["endTime"]
    #blocked = [("Monday", 1200), ("Wednesday", 1600)]
    #fixed = [("CS2100", "Tutorial", "15"), ("CS2030", "Laboratory", "06")]
    blocked = []
    fixed = []

    for module_code in timetable:
        for slot_type in timetable[module_code]:
            for slot_number in timetable[module_code][slot_type]:
                for date_time in timetable[module_code][slot_type][slot_number]:
                    day = date_time['day']
                    time_list = date_time['times']
                    remove = False
                    for slot in fixed:
                        if module_code == slot[0] and slot_type == slot[1] and slot_number != slot[2]:
                            remove = True
                    for hour in time_list:
                        if hour > endCutoff or hour < startCutoff or (day, hour) in blocked:
                            remove = True
                if remove:
                    filtered[module_code][slot_type].pop(slot_number)

    timetable = filtered
    # print(timetable)

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
    for i in range(20000):
        # randomly assign timetable
        dictLen = len(timetable)
        randomTimetable = {}
        for module in timetable:
            classTypes = timetable[module]
            if module not in randomTimetable:
                randomTimetable[module] = {}

            for classType in classTypes:
                classes = classTypes[classType]
                if (len(classes) > 0):
                    chosenClass = choice([*classes])
                else:
                    print("Timetable is impossible")
                    exit()

                randomTimetable[module][classTypeConverter(classType)] = chosenClass
        # print(checkConflict(randomTimetable))
        if not checkConflict(randomTimetable, timetable):
            # print(OutputParser.create_url(randomTimetable))
            validTimetables.append(randomTimetable)
            # print(randomTimetable)
            # break

    noOfTimetables = len(validTimetables)
    priorityFunctions = {"0" : lambda validTimetables: min_travel_distance(validTimetables, timetable, venue_list, noOfTimetables),
                         "1" : lambda validTimetables: top_free_time(validTimetables, timetable, noOfTimetables),
                         "2" : lambda validTimetables: filter_block_size(validTimetables, timetable, parameters["blockSize"])}

    if parameters["prioritizeDistance"]:
        validTimetables = priorityFunctions["0"](validTimetables)
    if parameters["prioritizeFreeTime"]:
        validTimetables = priorityFunctions["1"](validTimetables)

    validTimetables = priorityFunctions["2"](validTimetables)

    #print(OutputParser.create_url(validTimetables[:5]))
    print("done")
    urls = list(map(lambda timetable: OutputParser.create_url(timetable), validTimetables[:5]))

    print(urls)
    return urls
