import requests, pdb
import examinations_environment

class ExamMaterial():

    def __init__(self, type, exam, year, subject, level, title, url):
        self.type = type
        self.year = year
        self.exam = exam
        self.subject = self.__subjectId(subject)
        self.level = level
        self.url = url
        self.title = title

    def __subjectId(self, subjectName):
        subjects = examinations_environment.EXAMINATION_SUBJECTS[self.exam]
        try:
            return subjects[subjectName]
        except KeyError:
            return subjectName

class Examinations():

    def __init__(self, exam):
        self.exam = exam

    def query(self, type = "", exam = "", subject = "", year = ""):
        post_data = {"MaterialArchive__noTable__sbv__ViewType": type, "MaterialArchive__noTable__sbv__YearSelect": year, "MaterialArchive__noTable__sbv__ExaminationSelect": exam, "MaterialArchive__noTable__sbv__SubjectSelect": subject}
        post_data.update(examinations_environment.POST_DATA)
        r = requests.post("https://www.examinations.ie/exammaterialarchive/index.php", data=post_data)
        return r

    def __parseOptions(self, content, delimeter, value = False):
        nextLines = False
        options = []
        for line in iter(content.splitlines()):
            if delimeter in str(line):
                elements = str(line).split("<")
                for element in elements:
                    if "option" in element and element.split(">")[1] != "":
                        toAppend = element.split(">")[1]
                        toAppend = toAppend.replace("\\x96 ", "") #Special characters present in some subjects
                        if(value):
                            id = element.split('="')[1].split('"')[0]
                            options.append([toAppend, id])
                        else:
                            options.append(toAppend)
                break
        return options

    def __extractMaterials(self, content):
        titles = []
        urls = []
        next = False
        for line in iter(content.splitlines()):
            line = str(line)
            if "class='materialbody'" in line and "</TD>" in line:
                title = line.split(">")[1].split("<")[0]
                titles.append(title)
                next = True
            if next and "<!--" not in line and "<a href=" in line:
                url = line.split('href=')[1].split(' ')[0]
                urls.append(url)
                next = False
        return titles, urls

    def subjectId(self, subjectName):
        subjects = examinations_environment.EXAMINATION_SUBJECTS[self.exam]
        try:
            return subjects[subjectName]
        except KeyError:
            return False

    def years(self):
        r = self.query("exampapers")
        years = self.__parseOptions(r.content, "[Select Year]")
        return years[2:]

    def subjects(self):
        r = self.query("exampapers", self.exam, year = 2019)
        subjects = self.__parseOptions(r.content, "[Select Subject]", True)
        return subjects[2:]

    def __materials(self, type, subject, year = None, level = None):
        materials = []
        years = self.years() if year == None else [year]
        subject = self.subjectId(subject)
        for year in years:
            r = self.query(type, self.exam, subject, year)
            paperTitles, paperUrls = self.__extractMaterials(r.content)
            for i, title in enumerate(paperTitles):
                if level == None or level in title:
                    url = "https://www.examinations.ie/exammaterialarchive/" + paperUrls[i] if "https" not in paperUrls[i] else paperUrls[i]
                    material = ExamMaterial(type, self.exam, year, subject, level, title, url)
                    materials.append(material)
        return materials

    def papers(self, subject, year = None, level = None):
        return self.__materials("exampapers", subject, year, level)

    def schemes(self, subject, year = None, level = None):
        return self.__materials("markingschemes", subject, year, level)
