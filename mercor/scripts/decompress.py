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

def decompress_applicant(applicant_id):
    applicants = Table(API_KEY, BASE_ID, APPLICANTS_TABLE)
    personal = Table(API_KEY, BASE_ID, PERSONAL_TABLE)
    work = Table(API_KEY, BASE_ID, WORK_TABLE)
    salary = Table(API_KEY, BASE_ID, SALARY_TABLE)

    record = applicants.get(applicant_id)
    data = json.loads(record["fields"].get("Compressed JSON", "{}"))

    personal.update_or_create({"Applicant ID": applicant_id}, data.get("personal", {}))

    for w in work.all(formula=f"{{Applicant ID}}='{applicant_id}'"):
        work.delete(w["id"])
    for w in data.get("experience", []):
        w["Applicant ID"] = [applicant_id]
        work.create(w)

    salary.update_or_create({"Applicant ID": applicant_id}, data.get("salary", {}))

if __name__ == "__main__":
    test_id = "recXXXXXXXX"
    decompress_applicant(test_id)
