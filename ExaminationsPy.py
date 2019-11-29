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
        # pdb.set_trace()
        url = "https://examinations.ie/exammaterialarchive/" + self.__parsePage(r.content)
        return url

##USAGE:
## paper = ExamMaterial('exampapers', 2019, 'lc', 'Accounting', 'Higher Level')
## paper.url -> https://examinations.ie/exammaterialarchive/?fp=41.112.91.108.41.113.113.113.41.91.108.93.98.99.112.95.39.104.95.113.41.95.114.91.103.106.91.106.95.108.109.41.44.42.43.51.41.70.61.42.45.44.59.70.74.42.42.42.63.80.40.106.94.96.104
