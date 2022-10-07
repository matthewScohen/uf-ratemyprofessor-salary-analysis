import pickle
import json
import math
import csv
import requests
from ratemyprof_api import RateMyProfApi

SID = 1100
CSV_COLUMNS = [
            "professor",
            "attendance",
            "clarityColor",
            "easyColor",
            "helpColor",
            "helpCount",
            "id",
            "notHelpCount",
            "onlineClass",
            "quality",
            "rClarity",
            "rClass",
            "rComments",
            "rDate",
            "rEasy",
            "rEasyString",
            "rErrorMsg",
            "rHelpful",
            "rInterest",
            "rOverall",
            "rOverallString",
            "rStatus",
            "rTextBookUse",
            "rTimestamp",
            "rWouldTakeAgain",
            "sId",
            "takenForCredit",
            "teacher",
            "teacherGrade",
            "teacherRatingTags",
            "unUsefulGrouping",
            "usefulGrouping",
        ]

def scrape_and_save_professor_data(fname="../professors.pickle"):
    uf = RateMyProfApi(school_id = SID)
    uf_professors = uf.professors

    with open(fname, "wb") as handle:
        pickle.dump(uf_professors, handle, protocol=pickle.HIGHEST_PROTOCOL)

def load_data(fname="../professors.pickle"):
    with open(fname, 'rb') as handle:
        return pickle.load(handle)

def get_num_of_reviews(id):
    num_of_reviews = 0
    try:
        page = requests.get(
            "https://www.ratemyprofessors.com/paginate/professors/ratings?tid="
            + str(id)
            + "&filter=&courseCode=&page=1"
        )
        try:
            temp_jsonpage = json.loads(page.content)
            num_of_reviews = temp_jsonpage["remaining"] + 20
        except json.JSONDecodeError as e:
            print(f"Error {e} decoding json of number of reviews page with id {id}. Most likely the server returned a 404 or related error.")
    except Exception as e:
        print(f"Unkown error {e} while trying to get number of reviews of id {id}")  
    
    return num_of_reviews

def create_reviews_list(tid):
    tempreviewslist = []
    num_of_reviews = get_num_of_reviews(tid)
    # RMP only loads 20 reviews per page,
    # so num_of_pages tells us how many pages we need to get all the reviews
    num_of_pages = math.ceil(num_of_reviews / 20)
    i = 1
    while i <= num_of_pages:
        try:
            page = requests.get(
                "https://www.ratemyprofessors.com/paginate/professors/ratings?tid="
                + str(tid)
                + "&filter=&courseCode=&page="
                + str(i)
            )
            try:
                temp_jsonpage = json.loads(page.content)
                temp_list = temp_jsonpage["ratings"]
                tempreviewslist.extend(temp_list)
            except json.JSONDecodeError as e:
                print(f"Error {e} decoding json of review page {i} of professor with tid {tid}. Most likely the server returned a 404 or related error.")
            i += 1
        except Exception as e:
            print(f"Unknown error {e} creating review list on tid {tid}")
    return tempreviewslist

def main():
    scrape_and_save_professor_data()
    uf_professors = load_data()

    # Write professor reviews to CSV file
    with open("../professor_reviews.csv", "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=CSV_COLUMNS)
        writer.writeheader()

        professors_written = 0
        for professor in uf_professors.values():
            review_list = create_reviews_list(tid=professor.ratemyprof_id)
            for review in review_list:
                appended_review = {"professor": professor.name}
                appended_review.update(review)
                writer.writerow(appended_review)

            professors_written += 1
            percent_done = professors_written / len(uf_professors.values())
            print(f"Collecting data: {percent_done:.2%}%")

if __name__ == "__main__":
    main()