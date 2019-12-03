# ExaminationsPy

A python library for interacting with examinations.ie

## Usage

Import the library

```
import ExaminationsPy as ex
```

Check which subjects are available

```
Examinations = ex.Examinations
subjects = Examinations("lc")
```

Get the url for the 2019 Higher Level Accounting Paper

```
paper = ex.ExamMaterial('exampapers', 'lc', 2019, 'Accounting', 'Higher Level')
print(paper.url)
```
