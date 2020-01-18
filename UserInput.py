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
            constraint4Data = input("Please input the module code, type and class number of the slot that you want to fix in your timetable in the following example format: CS2040 LAB [18]")
            constraintDict[4] = constraint4Data
        elif i == 5:
            constraint5Data = input("Please state the day and time block that you want to leave empty in the following format: Friday 1300 to 2100")
            constraintDict[5] = constraint5Data
    return constraintDict
            
        

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
    for i in modArray[0:len(modArray)-1]:
        modString = modString + i + ", "
    modString = modString + "and " + modArray[-1] + "."
    print(modString)

    #Constraint settings
    constraintDict = {}
    constraintPrompt = input("There are 5 possible constraints to the timetable that we can try to implement for you: \n 1: Limit to the consecutive number of hours of lessons \n 2: Free days with no lessons \n 3: A limit to the ending time of your lessons, or limit to the earliest starting time of your lessons in a day \n 4: Lecture/Tutorial slots that you want to fix permanently in your schedule \n 5: Fixed emply slots that contains no lessons that you want to have in your timetable. \n Please give us the two numbers of constraints that you want us to prioritize while creating your timetable, with the first number you name being the most prioritized constraint. (e.g. 4 and 2, in this case 4 will be the highest priority constraint)")
    constraintListTemp = constraintPrompt.split()
    constraintList = [int(constraintListTemp[0]), int(constraintListTemp[2])]
    constraintDict = constraint_check(constraintList)
        
    
    '''
    #Constraint settings
    constraint1Prompt = input("For your upcoming semester, do you want to set a limit to the number of consecutive lessons in your timetable? Please input Y/N")
    if constraint1Prompt == "Y":
        constraintOne = int(input("Please input the maximum number of consecutive hours of lessons you want your timetable to have."))
    elif constraint1Prompt == "N":
        constraintOne = 0
    constraint2Prompt = input("Do you want us to maximise the number of free days in your timetable? Please input Y/N")
    if constraint2Prompt == "Y":
        constraintTwo = 1
    elif constraint2Prompt == "N":
        constraintTwo = 0
    constraint3Prompt = input("Do you want to set a limit to the latest time that you want to end your lesson on? Please input Y/N")
    if constraint3Prompt == "Y":
        constraint3Data = input("Please input the latest time that you want your school to end in the format Xpm (e.g. 7pm)")
        constraintThree = int(constraint3Data[0])
    elif constraint3Prompt == "N":
        constraint3Data = 0
        constraintThree = 0
    constraint4Prompt = input("Do you want to fix a particular lesson slot? Please input Y/N")
    if constraint4Prompt == "Y":
        constraintFour = 1
        constraint4Data = input("Please input the module code, type and class number of the slot that you want to fix in your timetable in the following example format: CS2040 LAB [18]")
    elif constraint4Prompt == "N":
        constraintFour = 0
        constraint4Data = 0
    constraint5Prompt = input("Do you want to fix an empty time block in your timetable? Please input Y/N")
    if constraint5Prompt == "Y":
        constraint5Data = input("Please state the day and time block that you want to leave empty in the following format: Friday 1300 to 2100")
        constraintFive = 1
    elif constraint5Prompt == "N":
        constraintFive = 0
        constraint5Data = 0

    constraintList = [constraintOne, constraintTwo, constraintThree, constraintFour, constraintFive]
    constraintData = {"constraint3Data":constraint3Data, "constraint4Data":constraint4Data, "constraint5Data":constraint5Data}
    '''

    masterDictionary = {"acadYear": acadYear, "semNumber":semNumber, "modArray":modArray, "constraintDict":constraintDict}
    return masterDictionary

print(ask_for_inputs())
