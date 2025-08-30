TIER1 = {"Google", "Meta", "OpenAI", "Microsoft", "Amazon"}

def evaluate_shortlist(applicant_json):
    exp_years = 0
    for exp in applicant_json.get("experience", []):
        start, end = exp.get("Start"), exp.get("End")
        if start and end and start[:4].isdigit() and end[:4].isdigit():
            exp_years += (int(end[:4]) - int(start[:4]))
        if exp.get("Company") in TIER1:
            exp_years = max(exp_years, 4)

    salary = applicant_json.get("salary", {})
    personal = applicant_json.get("personal", {})

    if (
        exp_years >= 4 and
        salary.get("Preferred Rate", 999) <= 100 and
        salary.get("Availability", 0) >= 20 and
        personal.get("Location", "").lower() in ["us", "canada", "uk", "germany", "india"]
    ):
        return True, "Meets all criteria: strong experience, affordable, available, good location"
    return False, "Did not meet criteria"

if __name__ == "__main__":
    sample = {
        "personal": {"Location": "India"},
        "experience": [{"Company": "Google", "Start": "2018-01-01", "End": "2022-01-01"}],
        "salary": {"Preferred Rate": 90, "Availability": 25}
    }
    print(evaluate_shortlist(sample))
