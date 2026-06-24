import requests

def find_jobs(role):

    url = f"https://remotive.com/api/remote-jobs?search={role}"

    try:
        response = requests.get(url)
        data = response.json()

        jobs = []

        for job in data["jobs"][:10]:
            jobs.append({
                "title": job["title"],
                "company": job["company_name"],
                "url": job["url"]
            })

        return jobs

    except:
        return []