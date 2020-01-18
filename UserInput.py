def constraint_check(constraintList):
    constraintDict = {}
    for i in constraintList:
        if i == 1:
            constraintOne = int(input("Please input the maximum number of consecutive hours of lessons you want your timetable to have. (e.g. 4)"))
            constraintDict[1] = constraintOne
        elif i == 2:
            constraintDict[2] = "1"
        elif i == 3:
            constraint3Data = input("Please input the latest time that you want your school to end in the format Xpm (e.g. 7pm)")
            constraintThree = int(constraint3Data[0])
            constraintDict[3] = constraintThree
        elif i == 4:
            constraint4Data = input("Please state the day and time block that you want to leave empty in the following format: Friday 1300 to 2100")
            constraintDict[4] = constraint4Data
    return constraintDict

def moduleFormatting(moduleString):
    moduleDict = {}
    if len(moduleString.split()) > 4:
        moduleString = moduleString.split(",")
        newList = []
        for subString in moduleString:
            newList.append(subString.split())
        for element in newList:
            tempDict = {}
            tempDict[element[1]] = element[2]
            moduleDict[element[0]] = tempDict
    else:
        newList = moduleString.split()
        tempDict = {}
        tempDict[newList[1]] = newList[2]
        moduleDict[newList[0]] = tempDict

        return moduleDict
             

def ask_for_inputs():
    #Semester and module details
    acadYear = input("Please input your Academic Year in the form YYYY-YYYY (e.g. 2019-2020)")
    print("Your Academic Year is AY" + acadYear)
    
    semData = input("Please input the semester you are creating a timetable for (1 or 2)")
    semNumber = int(semData) - 1
    print("Your semester is " + semData)
    
    modInput = input("Please input the modules that you intend to take this semester with a spacing in between each modules (e.g. MA1101R CS1010 MA1505)")
    modArray = modInput.split()
    modString = "Your desired modules are "
    
    startEndPrompt = input("Do you want to add a limit to the start and end time of your timetable? Please input Y/N")
    if startEndPrompt == "Y":
        startEndInput = "Please input the start and end time that you want to restrict your timetable to in the format XXXX to XXXX in hours. (e.g. 0800 to 1700)"
        startEndSplit = startEndInput.split()
        startEndData = [startEndSplit[0], startEndSplit[2]]
    elif startEndPrompt == "N":
        startEndData = ["0800", "2200"]
                           
    fixedSlotPrompt = input("Do you want to fix a specific class slot into your timetable? Please input Y/N")
    if fixedSlotPrompt == "Y":
        moduleString = input("Please input your module code, type and class number that you want fixed in your timetable in the following example format: CS2040 LAB 18 (For multiple fixed slots, use a comma to separate the modules e.g. CS2040 LAB 18, CS2103 TUT 04)")
        moduleDict = moduleFormatting(moduleString)
    elif fixedSlotPrompt == "N":
        moduleDict = {}

    for i in modArray[0:len(modArray)-1]:
        modString = modString + i + ", "
    modString = modString + "and " + modArray[-1] + "."
    print(modString)

    #Constraint settings
    constraintDict = {}
    constraintPrompt = input("There are 5 possible constraints to the timetable that we can try to implement for you: \n 1: Limit to the consecutive number of hours of lessons \n 2: Free days with no lessons \n 3: Lecture/Tutorial slots that you want to fix permanently in your schedule \n 4: Fixed emply slots that contains no lessons that you want to have in your timetable. \n Please give us the two numbers of constraints that you want us to prioritize while creating your timetable, with the first number you name being the most prioritized constraint. (e.g. 4 and 2, in this case 4 will be the highest priority constraint)")
    constraintListTemp = constraintPrompt.split()
    constraintList = [int(constraintListTemp[0]), int(constraintListTemp[2])]
    constraintDict = constraint_check(constraintList)
        

    masterDictionary = {"acadYear": acadYear, "semNumber":semNumber, "modArray":modArray, "constraintDict":constraintDict}
    masterDictionary.update(moduleDict)
    return masterDictionary

print(ask_for_inputs())
