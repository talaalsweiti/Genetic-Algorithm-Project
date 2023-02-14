import copy
import os
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Style

from tabulate import tabulate

from Data import ReadFile
from Data.ReadFile import read_courses_name
from Data.TimeSlots import get_end_time
from Genetic.Crossover import crossover
from Genetic.Fitness import fitness_calculator
from Genetic.GenerateSoulation import generate

courses = []
teachers = []
score = []
solutions = []


class RequestHandler(BaseHTTPRequestHandler):
    def _send_response(self, content):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(content)

    def do_GET(self):
        if self.path == '/':
            file_path = os.path.join(os.getcwd(), 'Course_Bowser.html')
            with open(file_path, 'r') as f:
                content = f.read()
                self._send_response(content.encode())


def printOutput():
    length = len(solutions)
    id_name = read_courses_name()
    # set the file path
    file_path = os.path.join(os.getcwd(), 'Course_Bowser.html')
    with open(file_path, 'w') as n:
        n.write('<html><body>')
        n.write('<div style="text-align: center; font-size: 24px; color: green;">Birzeit '
                'University</div>')
        n.write('<div style="text-align: center; font-size: 24px; color: black;">First Semester 2022/2023 </div>')
        n.write('<div style="text-align: center; font-size: 24px; color: green;">Bachelor Program of Computer '
                'Systems Engineering </div>')
        n.write('<div style="text-align: center; font-size: 24px; color: green;">Bachelor Level Courses of Computer'
                ' Systems Engineering</div>')

        # get the solution with the highest fitness
        for c in solutions[length - 1][3]:
            dataList = []
            header = ['Class Number', 'Instructor Name', 'Class Time']
            dataList.append(header)
            slots = solutions[length - 1][3][c]

            data = []
            sections = 1

            for j in range(0, len(slots) - 1, 2):
                if not c.is_lab:
                    end1 = get_end_time(slots[j][0], "", c.is_lab)
                    end2 = get_end_time(slots[j + 1][0], "", c.is_lab)
                    # data = [section#, Teacher name1, day, start time of c1, endTime of c2, //
                    #           section#, Teacher name2, day, start time of c2, endTime of c2]

                    data = [sections, slots[j][1].name, slots[j][0][0] + "  " + slots[j][0][1:] + " - "
                            + str(end1) + "// " + slots[j + 1][0][0] + "  " + slots[j + 1][0][1:] + " - " + str(
                        end2)]
                else:
                    end1 = get_end_time(slots[j][0], "", c.is_lab)
                    data = [sections, slots[j][1].name, slots[j][0][0] + "  " + slots[j][0][1:] + " - "
                            + str(end1)]
                dataList.append(data)
                sections += 1
            # To draw the course browser on console
            pdataList = tabulate(dataList, tablefmt="fancy_grid")
            print(pdataList)

            # To draw the course browser on html File
            hdataList = tabulate(dataList, tablefmt="html", headers="firstrow")

            # To draw table borders
            hdataList = hdataList.replace('<td', '<td style="border: 1px solid black;"', hdataList.count('<td'))
            hdataList = hdataList.replace('<th', '<th style="border: 1px solid black;"', hdataList.count('<th'))

            hdataList = hdataList.replace('<th', '<th style="background-color: SteelBlue;"')
            # align the cells of the table
            hdataList = hdataList.replace('<td', '<td align="center"', hdataList.count('<td'))
            hdataList = hdataList.replace('<th', '<th align="center"', hdataList.count('<th'))
            hdataList = hdataList.replace('<td>', '<td style="white-space: pre;">')

            # set the width of the table
            hdataList = hdataList.replace('<table', '<table style="width: 1250px;"')

            # print the course ID
            n.write('<br><span style="color: black; font-size: 18px; background-color: yellow;">{}</span><br>'.format(
                c.course_id + " : " + id_name[c.course_id]))
            n.write(hdataList)
        n.write('</body></html>')
    print("File Path: ", file_path)
    # Start a simple server
    httpd = HTTPServer(('localhost', 8000), RequestHandler)
    print("Serving the file at http://localhost:8000")
    webbrowser.open('http://localhost:8000/')
    httpd.serve_forever()


if __name__ == '__main__':

    root = Tk()
    root.title("Course Browser")
    root.minsize(300, 300)
    style = Style()


    def openfile():
        filepath = filedialog.askopenfilename()
        filelabel = Label(text=filepath)
        inputFile = open(filepath, 'r')
        ReadFile.read_courses(inputFile, courses, teachers)
        filelabel.pack()


    poplabel = Label(text="Please enter the input.txt file: ")
    poplabel.pack(pady=3)

    but = Button(
        text="Open file",
        command=openfile)

    but.pack(
        pady=10
    )

    poplabel = Label(text="Please enter the population: ")
    poplabel.pack()


    def solution():
        if popentry.get() == '':
            population = 1
        else:
            population = int(popentry.get())
        global teachers
        global courses
        copyTeachers = copy.deepcopy(teachers)
        copyCourses = copy.deepcopy(courses)

        for i in range(population):
            course_slots = {}
            courses = copy.deepcopy(copyCourses)
            teachers = copy.deepcopy(copyTeachers)
            generate(courses, course_slots)
            fitness_calculator(course_slots, score)
            solution = [score[i], courses, teachers, course_slots]
            solutions.append(solution)

            # reset time slots
            for teacher in teachers:
                teacher.time_slots = {}

        solutions.sort(key=lambda x: int(x[0]))

        # crossover loop
        for i in range(100):
            crossover(solutions)

        solutions.sort(key=lambda x: int(x[0]))
        printOutput()

        poplabel.pack()


    popentry = Entry()
    popentry.pack()

    but2 = Button(text="Generate a Solution", command=solution, bg="purple")
    but2.pack(pady=5)

    root.mainloop()
