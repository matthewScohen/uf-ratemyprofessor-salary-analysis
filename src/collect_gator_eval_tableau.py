from tableauscraper import TableauScraper as TS
import pandas as pd
import pickle

url = "https://public.tableau.com/views/GatorEvalsFall2019toSpring2022PublicData/GatorEvalsPublic"

ts = TS()
df = pd.DataFrame()

terms = ["Fall 2019", "Spring 2020", "Summer 2020", "Fall 2020", "Spring 2021", "Summer 2021", "Fall 2021", "Spring 2022", "Summer 2022"]

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
    uncollected_professors = [] # a list of professor's the script failed to collect data on
    for professor in professor_names:
        # reset worksheet (see comment above)
        attempts = 0
        data_loaded = False
        while attempts < 5:
            try:
                ts.loads(url)
                attempts += 1
            except Exception as e:
                print(f"error collecting {url}: {e}")
            else:
                break
        if data_loaded:
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
            print(f"Collecting data for {term}... {professors_done/len(professor_names):.2f}%")
        else:
            uncollected_professors.append(professor)

print(f"Failed to collect data for these professors: {uncollected_professors}")
with open("new_gator_eval_data.pickle", "wb") as handle:
        pickle.dump(df, handle, protocol=pickle.HIGHEST_PROTOCOL)