# impotring modules
import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest

# intializing lists to store needed info
job_title = []
company = []
location = []
job_skills = []
job_posted = []
links = []

# collecting jobs from all pages by looping over pages
page_number = 0
while True:

    # using requsts to fetch the url and save page content
    result = requests.get(f"https://wuzzuf.net/search/jobs/?a=hpb%7Cspbg&q=data%20analysis&start={page_number}")
    source = result.content

    # creating soup object to parse content
    soup = BeautifulSoup(source, "lxml")

    # checking the page number and break the loop if it exceeded the limit
    jop_numbers = int(soup.find("strong").text)
    page_limit = jop_numbers // 15
    if page_number > page_limit:
        break

    # finding the elemnts containing info we need
    job_titles = soup.find_all("h2", {"class": "css-m604qf"})
    companies = soup.find_all("a", {"class": "css-17s97q8"})
    locations = soup.find_all("span", {"class": "css-5wys0k"})
    skills = soup.find_all("div", {"class": "css-y4udm8"})
    posted_new = soup.find_all("div", {"class": "css-4c4ojb"})
    posted_old = soup.find_all("div", {"class": "css-do6t5g"})
    posted = [*posted_old, *posted_new]
    all_skills = [*skills]
    jobs = len(job_titles)

    # extracting needed info into other lists
    for job in range(jobs):
        job_title.append(job_titles[job].text)
        links.append(job_titles[job].find("a").attrs["href"])
        company.append(companies[job].text)
        location.append(locations[job].text)
        job_skills.append(all_skills[job].text)
        job_posted.append(posted[job].text)
        page_number += 1

# creating csv file and fill it with values
file_list = [job_title, company, location, job_posted, job_skills, links]
exported = zip_longest(*file_list)
with open(r"C:\Users\lapy\Project\DataAnalysisJobs.csv", "w") as file:
    wr = csv.writer(file)
    wr.writerow(["job title", "company", "location", "date", "job type and skills", "link to apply"])
    wr.writerows(exported)
print("Done,now you can check the Excel sheet")
