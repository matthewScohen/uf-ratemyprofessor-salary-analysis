from tableauscraper import TableauScraper as TS
import pandas as pd
import pickle

url = "https://public.tableau.com/views/GatorEvalsFall2019toSpring2022PublicData/GatorEvalsPublic"

ts = TS()
df = pd.DataFrame()

terms = ["Fall 2019", "Spring 2020"]

for term in terms:
    # We have to reload the workbook each time in order to reset the filters, there is probably a better way to do this but
    # the tableauscraper library doesn't provide a way to clear filters as far as I can tell
    ts.loads(url)
    workbook = ts.getWorkbook()
    ws = workbook.worksheets[0]
    
    term_workbook = ws.setFilter("Term", term)
    filters = ws.getFilters()

    # some semesters have a professor at the top of the list with name -, - that just lists all professors
    if filters[3]["values"][0] == "-, -":
        # we remove -, - if its at the top of the list of professors
        professor_names = filters[3]["values"][1:None] 
    else:
        professor_names = filters[3]["values"]
    professors_done = 0
    for professor in professor_names:
        # reset worksheet (see comment above)
        ts.loads(url)
        workbook = ts.getWorkbook()
        ws = workbook.worksheets[0]
        wb = ws.setFilter("INSTRUCTOR_NAME", professor)
        # get courses
        filters = ws.getFilters()
        courses = filters[1]["values"]
        # print(courses)
        for course in courses:    
            wb = ws.setFilter("COMBINED_COURSE", course)
            wb.worksheets[0].data["professor"] = professor
            wb.worksheets[0].data["term"] = term
            wb.worksheets[0].data["course"] = course
            df = pd.concat([df, wb.worksheets[0].data])

            professors_done += 1
            print(f"Collecting data for {term}... {professors_done/len(professor_names):.2f}")

with open("new_gator_eval_data.pickle", "wb") as handle:
        pickle.dump(df, handle, protocol=pickle.HIGHEST_PROTOCOL)