import time
import requests
import json
from itertools import product
from string import ascii_lowercase
import csv
import pickle
import lxml.html as lh

# These headers need to be part of get and post requests made to the gator eval pages. I'm not sure why or if you need all of them.
REQUEST_HEADERS = { "Accept" : "application/json, text/javascript, */*; q=0.01",
                "Accept-Encoding" : "gzip, deflate, br",
                "Accept-Language" : "en-US,en;q=0.9",
                "Connection" : "keep-alive",
                "Content-Type" : "application/json; charset=utf-8",
                "Cookie" : "ASP.NET_SessionId=1salc5haqgw5x3mm0skuyobq; _shibsession_75726e3a6564753a75666c3a70726f643a303031393975726e3a6564753a75666c3a70726f643a3030313939=_97fc8233af5584b81881fce082a8b19c",
                "DNT" : "1",
                "Host" : "evaluations.ufl.edu",
                "Referer" : "https://evaluations.ufl.edu/results/",
                "sec-ch-ua" : '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
                "sec-ch-ua-mobile" : "?0",
                "sec-ch-ua-platform" : "Windows",
                "Sec-Fetch-Dest" : "empty",
                "Sec-Fetch-Mode" : "cors",
                "Sec-Fetch-Site" : "same-origin",
                "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
                "X-Requested-With" : "XMLHttpRequest"
                }

def generate_professor_id_set():
    ### This function makes requests to the gator evals website and records the key used to query each professor.
    ### The keys are stored in a set and then saved to a pickle file.
    professor_id_set = set()
    # The website only lets you search for professors using 2+ characters in the search so we search all
    # combinations of 2 letters to get all professor ids.
    two_letter_combos = (''.join(i) for i in product(ascii_lowercase, ascii_lowercase))
    keys_done = 0
    total_keys = 26*26
    print(f"Generating professor key set...")
    for key in two_letter_combos:
        response = requests.get(f"https://evaluations.ufl.edu/results/default.aspx/GetInstructorsByName?query={key}", headers=REQUEST_HEADERS)
        json_response = json.loads(response.content)
        professor_list = json_response['d']['aaData']
        for professor_data in professor_list:
            professor_id_set.add(professor_data['Key'])
        keys_done += 1
        print(f"{keys_done/total_keys:.2%}")
    
    # Save data
    with open("professor_eval_ids.pickle", "wb") as handle:
        pickle.dump(professor_id_set, handle, protocol=pickle.HIGHEST_PROTOCOL)

def main():
    ### Uncomment line below the first time this script is run ###
    # generate_professor_id_set()  

    # Load professor ids
    professor_id_set = set()
    with open("professor_eval_ids.pickle", 'rb') as handle:
        professor_id_set = pickle.load(handle)

    CSV_COLUMNS = [
        "Professor",
        "College Code",
        "College Name",
        "Department Code",
        "Department Name",
        "Section",
        "Instructor Title",
        "Term",
        "Course",
        "Enrolled",
        "Responded",
        "Response Rate",
        "Question",
        "1",
        "2",
        "3",
        "4",
        "5",
    ]
    professors_recorded = 0
    professors_to_record = len(professor_id_set)

    with open("professor_evals.csv", "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        print(f"Getting eval data...")
        # Navigate to each professor's page, each professor has a page with a different id and a table of evals.
        # Each section the professor has ever taught is a different row in the eval table.
        for professor_id in professor_id_set:
            section_cells = list()
            try:
                page = requests.get(f"https://evaluations.ufl.edu/results/instructor.aspx?ik={professor_id}")
                doc = lh.fromstring(page.content)
                # Get all data cells from the table of sections the professor has taught
                section_cells = doc.xpath('//td')
            except Exception as e:
                print(f"Error getting data for professor {professor_id}: {e}")

            # Get urls of eval data for each section in the table. Each professor's page has a table with "view" buttons and each "view" button makes a request to
            # retreive a table that has the eval information for that class section. The url to get the eval data consists of the section number, professor id, and term.
            table_urls = list()
            for i, value in enumerate(section_cells):
                try:
                    # The term/section_number is the 1st/3rd item in each row and each row has 7 items in it
                    term = section_cells[(7*i+1)].text[0:5]
                    section_number = section_cells[(7*i+3)].text
                    # Sometimes the section number is actually a list of section numbers and the url is the section numbers separated by dashes (-)
                    section_number = section_number.replace(" ", "-")
                    section_number = section_number.replace(",", "")
                    table_urls.append(f"https://evaluations.ufl.edu/results/Instructor.aspx/GetEvaluation?e={term}_{professor_id}_{section_number}")
                except IndexError:
                    break
            # Make a request to the url of each section and write the evaluation data to a spread sheet.
            for url in table_urls:
                try:
                    eval_response = requests.post(url, headers=REQUEST_HEADERS)
                    json_response = json.loads(eval_response.content)
                    eval_data = json_response['d']
                    for i, question in enumerate(eval_data["Questions"]):
                        csv_row = {
                            "Professor" : eval_data["InstructorName"],
                            "College Code" : eval_data["CollegeCode"],
                            "College Name" : eval_data["CollegeName"],
                            "Department Code" : eval_data["DepartmentCode"],
                            "Department Name" : eval_data["DepartmentName"],
                            "Section" : eval_data["Section"],
                            "Instructor Title" : eval_data["InstructorTitle"],
                            "Term" : eval_data["TermLit"],
                            "Course" : eval_data["Course"],
                            "Enrolled" : eval_data["Enrolled"],
                            "Responded" : eval_data["Responded"],
                            "Response Rate" : eval_data["ResponseRate"],
                            "Question" : eval_data["Questions"][i]["Text"],
                            "1" : eval_data['Questions'][i]["Ones"],
                            "2" : eval_data['Questions'][i]["Twos"],
                            "3" : eval_data['Questions'][i]["Threes"],
                            "4": eval_data['Questions'][i]["Fours"],
                            "5" : eval_data['Questions'][i]["Fives"],
                        }
                        writer.writerow(csv_row)
                except Exception as e:
                    print(f"Error getting url {url}: {e}")
            # Output progress
            professors_recorded += 1
            print(f"{professors_recorded/professors_to_record:.3%}")

if __name__ == "__main__":
    main()