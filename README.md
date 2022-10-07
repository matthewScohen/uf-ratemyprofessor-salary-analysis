# UF Ratemyprofessor-Salary Analysis

## Project Purpose
The purpose of this project was to determine if there was any relationship between the salaries of lecturing professors and student's approval of their teaching. See the [github pages](PUT GITHUB PAGES LINK HERE) for results and more information.

## Data Collection
### Rating Data
The professor rating data was collected from ratemyprofessor.com with the help of code modified from [this repository](https://github.com/tisuela/ratemyprof-api). The src/collect_data.py script is used to generate a .pickle file that stores a dictionary of the professor data and a .csv file with their rating information. To use this script to collect data for a different school edit the SID at the top of collect_data.py. 

`SID = 1100`

The SID can be obtained from the URL of the school's ratemyprofessor page (eg. [https://www.ratemyprofessors.com/campusRatings.jsp?**sid=1100**](https://www.ratemyprofessors.com/campusRatings.jsp?sid=1100)).

### Salary Data
The salary data was collected from **PUT SALARY DATA LINK HERE**.
