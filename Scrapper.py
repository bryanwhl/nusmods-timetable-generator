import requests
import UserInput

userInput = UserInput.ask_for_inputs()
academicYear = userInput["acadYear"]
semester = userInput["semNumber"]
modules = userInput["modArray"]
data = {"constraintList" : userInput["constraintList"],
        "constraintData" : userInput["constraintData"]}

timetable = {}

for module in modules:
    response = requests.get("https://api.nusmods.com/v2/" + academicYear + "/modules/" + module + ".json")
    moduleData = response.json()
    #print("====================================================")
    #print("Timetable for " + module)

    timetableData = moduleData["semesterData"][semester]["timetable"]

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

data["Timetable"] = timetable
print(data)
