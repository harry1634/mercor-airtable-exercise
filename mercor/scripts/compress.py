import json, os
from pyairtable import Table
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("AIRTABLE_API_KEY")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")
APPLICANTS_TABLE = "Applicants"
PERSONAL_TABLE = "Personal Details"
WORK_TABLE = "Work Experience"
SALARY_TABLE = "Salary Preferences"

def compress_applicant(applicant_id):
    applicants = Table(API_KEY, BASE_ID, APPLICANTS_TABLE)
    personal = Table(API_KEY, BASE_ID, PERSONAL_TABLE)
    work = Table(API_KEY, BASE_ID, WORK_TABLE)
    salary = Table(API_KEY, BASE_ID, SALARY_TABLE)

    personal_data = personal.all(formula=f"{{Applicant ID}}='{applicant_id}'")
    work_data = work.all(formula=f"{{Applicant ID}}='{applicant_id}'")
    salary_data = salary.all(formula=f"{{Applicant ID}}='{applicant_id}'")

    json_obj = {
        "personal": personal_data[0]["fields"] if personal_data else {},
        "experience": [w["fields"] for w in work_data],
        "salary": salary_data[0]["fields"] if salary_data else {}
    }

    applicants.update(applicant_id, {"Compressed JSON": json.dumps(json_obj)})
    return json_obj

if __name__ == "__main__":
    test_id = "recXXXXXXXX"  # Replace with real record ID
    print(compress_applicant(test_id))
