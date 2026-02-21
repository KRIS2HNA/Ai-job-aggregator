import requests

def scrape_jobs():
    """Mock Scraper (sim;uated scraped data)
    Later we replace with real scraping
    """
    url = "https://remotive.com/api/remote-jobs"
    
    response = requests.get(url)
    
    if response.status_code != 200:
        return []
    data = response.json()
    
    jobs = []
    
    for item in data.get("jobs", [])[:5]: # Limit to first 5 jobs for demo
            
        jobs.append({
            "title": item.get("title"),
            "company": item.get("company_name"),
            "location": item.get("candidate_required_location"),
            "description": item.get("description"),
            "apply_link": item.get("url"),
            "skills": []  # Placeholder for skills, can be extracted from description later
        })
    return jobs

    
    jobs = [
        {
            "title": "Software Engineer",
            "company": "Tech Company A",
            "location": "New York, NY",
            "description": "Develop and maintain software applications.",
            "apply_link": "https://www.example.com/jobs/software-engineer"
        },
        {
            "title": "Data Scientist",
            "company": "Tech Company B",
            "location": "San Francisco, CA",
            "description": "Analyze and interpret complex data to help make informed decisions.",
            "apply_link": "https://www.example.com/jobs/data-scientist"
        }
    ]
    return jobs