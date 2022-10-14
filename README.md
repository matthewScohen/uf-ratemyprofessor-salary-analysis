# Project Purpose
The purpose of this project was to determine if there was any relationship between the salaries of lecturing professors and student's approval of their teaching. Addtionally we've collected some interesting figures about gator evals and ratemyprofessor reviews that aren't necessarily related to professor salary.

# Data Collection
## Ratemyprofessor Data
The Ratemyprofessorg data was collected from ratemyprofessor.com with the help of code modified from [this repository](https://github.com/tisuela/ratemyprof-api). The data is stored in `data/professor_reviews.csv` and `data/uf_professors.pickle` (A pickle of a python dict that contains the professor data). The csv contains the same information as the pickle file.

The `src/collect_rmp_data.py` script is used to generate a .pickle file that stores a dictionary of the professor data and then creates a .csv file with the same data. To use this script to collect data for a different school edit the SID at the top of collect_data.py.

`SID = 1100`

The SID can be obtained from the URL of the school's ratemyprofessor page (eg. [https://www.ratemyprofessors.com/campusRatings.jsp?**sid=1100**](https://www.ratemyprofessors.com/campusRatings.jsp?sid=1100)).

## Gator Eval Data
The gator eval data is publically available from the [evaluations website](https://evaluations.ufl.edu/results/). We were unable to find anywhere with all of the data published in a single spreadsheet (as opposed to being able to query information from a database via a web app). The `collect_gator_eval.py` script was used to create `data/professor_evals.csv` which contains all of the data available from the evaluations website. It also creates `professor_eval_ids.pickle` which is a python set containing the unique ids of all professors in the evaluation database (eg https://evaluations.ufl.edu/results/instructor.aspx?ik=-1154288659 the id is -1154288659). 

Each row in the csv represents response data from 1 of 8 questions available from the evaluation results website (ie each professor has many rows in the csv and each class section is represented by 8 different rows). The csv is too big to publish to github but can be downloaded from [PUT LINK TO CSV DOWNLOAD HERE](link address).

## Salary Data
The salary and employment data was collected from [here](https://prod.flbog.net:4445/pls/apex/f?p=140:1) and [here](https://www.floridahasarighttoknow.myflorida.com/search_state_payroll).
