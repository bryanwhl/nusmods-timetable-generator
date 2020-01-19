# NUSMods Timetable Scheduler (NUS Hack&Roll Hackathon Project)

Have you ever felt like your timetable could be improved? NUS Timetable Scheduler allows you to 
input your preferences for your timetable and our algorithms will customise the best suited timetable for you based on your
preferences. All you need to do is to key in the module codes of the modules that you are going to take for the upcoming 
semester, your academic year/semester and your preferences and an nusmods.com link will be generated for you to view your 
recommended timetable.

## Built With

The data of each modules in our project is obtained from NUSMODS API. The backend algorithms of the project is built with Python, whereas the frontend interface of the web app is built with HTML and Bootstrap. The routes between the web interface and the backend script is built with Flask.

## How-to-use

1. Go to the following URL: https://nus-mods-scheduler.herokuapp.com/

2. Follow the instructions and key in the preferences you want to set for your timetable. *Note that if you key in a module code of a module that is not offered on that particular semester, an error will occur. Similar errors will occur if you do not follow the input format strictly as stated on the input box.

3. Generate the timetables. *It might take awhile for the timetable to load.

4. Five possible timetables will be generated that is optimised to your preferences so that you can reference them and build your timetable according to which of the five you like the most.
