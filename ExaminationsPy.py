import requests, pdb
import examinations_environment

class ExamMaterial():

    def __init__(self, type, year, exam, subject, level):
        self.type = type
        self.year = year
        self.exam = exam
        self.subject = self.__subjectId(subject)
        self.level = level

    def __subjectId(self, subjectName):
        subjects = examinations_environment.EXAMINATION_SUBJECTS[self.exam]
        return subjects[subjectName]

    def __parsePage(self, content):
        next = False
        for line in iter(content.splitlines()):
            if self.level in str(line):
                if "IV" not in str(line):
                    next = True
            if next and "href=?fp" in str(line):
                url = str(line).split("href=")[1]
                url = url.split(" ")[0]
                return url

    def url(self):
        post_data = {"MaterialArchive__noTable__sbv__ViewType": "exampapers", "MaterialArchive__noTable__sbv__YearSelect": 2019, "MaterialArchive__noTable__sbv__ExaminationSelect": "lc", "MaterialArchive__noTable__sbv__SubjectSelect": 32}
        post_data.update(examinations_environment.POST_DATA)
        r = requests.post("https://www.examinations.ie/exammaterialarchive/index.php", data=post_data)
        url = "https://examinations.ie/exammaterialarchive/" + self.__parsePage(r.content)
        return url

class Examinations():

    def __init__(self, exam = "", level = ""):
        self.exam = exam
        self.level = level

    def query(self, type = "", year = "", exam = "", subject = ""):
        post_data = {"MaterialArchive__noTable__sbv__ViewType": type, "MaterialArchive__noTable__sbv__YearSelect": year, "MaterialArchive__noTable__sbv__ExaminationSelect": exam}
        post_data.update(examinations_environment.POST_DATA)
        r = requests.post("https://www.examinations.ie/exammaterialarchive/index.php", data=post_data)
        return r

    def __parseOptions(self, content, delimeter):
        nextLines = False
        options = []
        for line in iter(content.splitlines()):
            if delimeter in str(line):
                elements = str(line).split(">")
                for element in elements:
                    if "</" in element and element.split("</")[0] != "":
                        options.append(element.split("</")[0])
                break
        return options

    def years(self, exam = ""):
        exam = self.exam if exam == "" else exam
        if(exam == ""):
            return False
        r = self.query("exampapers")
        years = self.__parseOptions(r.content, "[Select Year]")
        return years[2:]

    def subjects(self, exam = ""):
        exam = self.exam if exam == "" else exam
        if(exam == ""):
            return False
        r = self.query("exampapers", 2019, exam)
        subjects = self.__parseOptions(r.content, "[Select Subject]")
        return subjects[2:]

ex = Examinations()
print(ex.subjects("lc"))
