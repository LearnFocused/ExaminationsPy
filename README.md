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
subjects = Examinations.subjects("lc")
```

Check which years are available

```
years = Examinations.years("lc")
```

Get the url for the 2019 Higher Level Accounting Paper

```
papers = Examinations.papers("Accounting", year = 2019, level = "Higher Level")
print(papers[0].url)
```

Get the url for the 2019 Higher Level Accounting Marking Scheme

```
schemes = Examinations.schemes("Accounting", year = 2019, level = "Higher Level")
print(schemes[0].url)
```

Get all the Accounting Higher Level Papers

```
papers = Examinations.papers(subject = "Accounting", level = "Higher Level")
```
