# ExaminationsPy

A python library for interacting with examinations.ie

## Usage

Import the library

```python
import ExaminationsPy as ex
```

Check which subjects are available

```python
Examinations = ex.Examinations("lc")
subjects = Examinations.subjects()
```

Check which years are available

```python
years = Examinations.years()
```

Get the url for the 2019 Higher Level Accounting Paper

```python
papers = Examinations.papers("Accounting", year = 2019, level = "Higher Level")
print(papers[0].url)
```

Get the url for the 2019 Higher Level Accounting Marking Scheme

```python
schemes = Examinations.schemes("Accounting", year = 2019, level = "Higher Level")
print(schemes[0].url)
```

Get all the Accounting Higher Level Papers

```python
papers = Examinations.papers(subject = "Accounting", level = "Higher Level")
```
