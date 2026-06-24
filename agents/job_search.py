import requests


def search_remotive(role):
    jobs = []

    try:
        url = f"https://remotive.com/api/remote-jobs?search={role}"

        response = requests.get(url, timeout=10)
        data = response.json()

        for job in data.get("jobs", [])[:10]:
            jobs.append({
                "source": "Remotive",
                "title": job.get("title"),
                "company": job.get("company_name"),
                "location": job.get("candidate_required_location"),
                "url": job.get("url")
            })

    except Exception as e:
        print("Remotive Error:", e)

    return jobs


def search_arbeitnow(role):
    jobs = []

    try:
        url = "https://www.arbeitnow.com/api/job-board-api"

        response = requests.get(url, timeout=10)
        data = response.json()

        for job in data.get("data", []):

            title = job.get("title", "")

            if role.lower() in title.lower():

                jobs.append({
                    "source": "Arbeitnow",
                    "title": title,
                    "company": job.get("company_name"),
                    "location": job.get("location"),
                    "url": job.get("url")
                })

            if len(jobs) >= 10:
                break

    except Exception as e:
        print("Arbeitnow Error:", e)

    return jobs


def search_jobs(role):

    jobs = []

    jobs.extend(search_remotive(role))
    jobs.extend(search_arbeitnow(role))

    return jobs[:20]