# ExaminationsPy

A python library for interacting with examinations.ie

## Usage

Getting a paper's URL

```
import ExaminationsPy as ex
paper = ex.ExamMaterial('exampapers', 'lc', 2019, 'Accounting', 'Higher Level')
print(paper.url)
```

