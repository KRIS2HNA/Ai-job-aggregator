def scrape_jobs():
    """Mock Scraper (sim;uated scraped data)
    Later we replace with real scraping
    """
    
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