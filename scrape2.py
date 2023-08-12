import csv
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, date
import os

# Links for each country to extract data analyst job listings
links = {
  "usa":{
      "onsite": "https://www.linkedin.com/jobs/search/?currentJobId=3351674810&f_WT=1&geoId=103644278&keywords=data%20analyst&location=United%20States&refresh=true&start=",
      "remote": "https://www.linkedin.com/jobs/search/?currentJobId=3205250146&f_WRA=true&f_WT=2&geoId=103644278&keywords=data%20analyst&location=United%20States&refresh=true&start=",
      "hybrid": "https://www.linkedin.com/jobs/search/?currentJobId=3343518868&f_WRA=true&f_WT=3&geoId=103644278&keywords=data%20analyst&location=United%20States&refresh=true&start="
      },
  "canada":{
      "onsite": "https://www.linkedin.com/jobs/search/?currentJobId=3223346796&f_WT=1&geoId=101174742&keywords=data%20analyst&location=Canada&refresh=true&start=",
      "remote": "https://www.linkedin.com/jobs/search/?currentJobId=3335580667&f_WT=2&geoId=101174742&keywords=data%20analyst&location=Canada&refresh=true&start=",
      "hybrid": "https://www.linkedin.com/jobs/search/?currentJobId=3335356174&f_WT=3&geoId=101174742&keywords=data%20analyst&location=Canada&refresh=true&start="
      },
  "nigeria": {
      "onsite": "https://www.linkedin.com/jobs/search?keywords=Data%20Analyst&location=Nigeria&locationId=&geoId=105365761&f_TPR=&f_WT=1&position=1&pageNum=0",
      "remote": "https://www.linkedin.com/jobs/search?keywords=Data%20Analyst&location=Nigeria&locationId=&geoId=105365761&f_TPR=&f_WT=2&position=1&pageNum=0",
      "hybrid": "https://www.linkedin.com/jobs/search?keywords=Data%20Analyst&location=Nigeria&locationId=&geoId=105365761&f_TPR=&f_WT=3&position=1&pageNum=0"
      },
  "south_africa": {
      "onsite": "https://www.linkedin.com/jobs/search?keywords=Data%20Analyst&location=South%20Africa&locationId=&geoId=104035573&f_TPR=&f_WT=1&position=1&pageNum=0",
      "remote": "https://www.linkedin.com/jobs/search?keywords=Data%20Analyst&location=South%20Africa&locationId=&geoId=104035573&f_TPR=&f_WT=2&position=1&pageNum=0",
      "hybrid": "https://www.linkedin.com/jobs/search?keywords=Data%20Analyst&location=South%20Africa&locationId=&geoId=104035573&f_TPR=&f_WT=3&position=1&pageNum=0"
      },
  "united_kingdom":{
      "onsite": "https://www.linkedin.com/jobs/search/?currentJobId=3643998233&f_WT=1&geoId=101165590&keywords=data%20analyst&location=United%20Kingdom&refresh=true",
      "remote": "https://www.linkedin.com/jobs/search/?currentJobId=3688656251&f_WT=2&geoId=101165590&keywords=data%20analyst&location=United%20Kingdom&refresh=true",
      "hybrid": "https://www.linkedin.com/jobs/search/?currentJobId=3664365216&f_WT=3&geoId=101165590&keywords=data%20analyst&location=United%20Kingdom&refresh=true"
      },
  "germany": {
      "onsite": "https://www.linkedin.com/jobs/search?keywords=Data%20Analyst&location=Germany&locationId=&geoId=101282230&f_TPR=&f_WT=1&position=1&pageNum=0",
      "remote": "https://www.linkedin.com/jobs/search?keywords=Data%20Analyst&location=Germany&locationId=&geoId=101282230&f_TPR=&f_WT=2&position=1&pageNum=0",
      "hybrid": "https://www.linkedin.com/jobs/search?keywords=Data%20Analyst&location=Germany&locationId=&geoId=101282230&f_TPR=&f_WT=3&position=1&pageNum=0",
      },
  "ireland": {
      "onsite": "https://www.linkedin.com/jobs/search?keywords=Data%20Analyst&location=Ireland&locationId=&geoId=104738515&f_TPR=&f_WT=1&position=1&pageNum=0",
      "remote": "https://www.linkedin.com/jobs/search?keywords=Data%20Analyst&location=Ireland&locationId=&geoId=104738515&f_TPR=&f_WT=2&position=1&pageNum=0",
      "hybrid": "https://www.linkedin.com/jobs/search?keywords=Data%20Analyst&location=Ireland&locationId=&geoId=104738515&f_TPR=&f_WT=3&position=1&pageNum=0",
      },
  "uae": {
      "onsite": "https://www.linkedin.com/jobs/search?keywords=Data%20Analyst&location=United%20Arab%20Emirates&locationId=&geoId=104305776&f_TPR=&f_WT=1&position=1&pageNum=0",
      "remote": "https://www.linkedin.com/jobs/search?keywords=Data%20Analyst&location=United%20Arab%20Emirates&locationId=&geoId=104305776&f_TPR=&f_WT=2&position=1&pageNum=0",
      "hybrid": "https://www.linkedin.com/jobs/search?keywords=Data%20Analyst&location=United%20Arab%20Emirates&locationId=&geoId=104305776&f_TPR=&f_WT=3&position=1&pageNum=0",
      },
  }
print("Links defined successfully...")

# Function to scrap job listings
def create_job_csv(country_links: dict, country: str):
    try:
        # Calculate the date 14 days ago
        two_weeks_ago = datetime.now() - timedelta(days=14)

        # Set to keep track of processed job links
        processed_links = set()

        # Load processed links from existing CSV
        if os.path.exists('data/linkedin-jobs.csv'):
            with open('data/linkedin-jobs.csv', mode='r', encoding='UTF-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    processed_links.add(row[-1])  # last column is link

        # create file or open file in append mode
        with open('data/linkedin-jobs.csv', mode='a', newline='', encoding='UTF-8') as file:
            writer = csv.writer(file)

            # Only add headers if the file is empty
            if os.stat('data/linkedin-jobs.csv').st_size == 0:
                writer.writerow(['title', 'company', 'description', 'onsite_remote',
                                'salary', 'location', 'criteria', 'posted_date', 'link'])

            def linkedin_scraper(webpage, page_number, onsite_remote):
                count = 0
                next_page = webpage + str(page_number)
                response = requests.get(str(next_page))
                soup = BeautifulSoup(response.content, 'html.parser')

                # Extracting job details
                jobs = soup.find_all(
                    'div', class_='base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card')

                for job in jobs:
                    job_datetime = job.find(
                        'time', class_='job-search-card__listdate')
                    if job_datetime:
                        job_link = job.find('a', class_='base-card__full-link')['href']

                        if job_link not in processed_links:
                            job_date = datetime.strptime(
                                job_datetime['datetime'], '%Y-%m-%d').date()

                        if job_date >= two_weeks_ago.date():
                            job_criteria = []
                            job_title = job.find(
                                'h3', class_='base-search-card__title').text.strip()
                            job_company = job.find(
                                'h4', class_='base-search-card__subtitle').text.strip()
                            job_location = job.find(
                                'span', class_='job-search-card__location').text.strip()
                            job_datetime = job.find(
                                'time', class_='job-search-card__listdate')['datetime'] if job.find(
                                'time', class_='job-search-card__listdate') is not None else job.find(
                                'time', class_='job-search-card__listdate--new')['datetime']
                            job_salary = job.find('span', class_='job-search-card__salary-info').text.strip(
                            ) if job.find('span', class_='job-search-card__salary-info') is not None else "NaN"

                            job_link = job.find('a', class_='base-card__full-link')['href']
                            resp = requests.get(job_link)
                            sp = BeautifulSoup(resp.content, 'html.parser')

                            # Save requests as html pages to help view classes for scraping
                            # if count == 0 :
                            with open('templates/job_list.html', mode='w', encoding="utf-8") as job_list:
                                job_list.write(str(response.content))
                                job_list.close()
                            with open('templates/job.html', mode='w', encoding="utf-8") as job_detail:
                                job_detail.write(str(resp.content))
                                job_detail.close()
                            # count += 1

                            try:
                                job_desc = sp.find('div', class_='show-more-less-html__markup show-more-less-html__markup--clamp-after-5 relative overflow-hidden').text.strip(
                                )
                            except Exception as e:
                                job_desc = "Nan"
                                print(f"An error occurred while extracting job description: {e}")

                            criteria = sp.find_all(
                                'li', class_='description__job-criteria-item')
                            for criterion in criteria:
                                feature = criterion.find(
                                    'h3', class_='description__job-criteria-subheader').text.strip()
                                value = criterion.find(
                                    'span', class_='description__job-criteria-text description__job-criteria-text--criteria').text.strip()
                                job_criteria.append({feature: value})

                            writer.writerow([job_title, job_company, job_desc, onsite_remote, job_salary,
                                            job_location, job_criteria, job_datetime, job_link])
                            print('Job Data updated')

                            processed_links.add(job_link)

                if page_number < 5000:
                    # Move to the next page
                    page_number = page_number + 25
                    linkedin_scraper(webpage, page_number, onsite_remote)

            for work_type in country_links:
                linkedin_scraper(country_links[work_type], 0, work_type)

        output_file_path = "data/linkedin-jobs.csv"
        print("LinkedIn data scrapping competed successfully and saved at:", output_file_path)

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    for country in links:
        create_job_csv(links[country], country)

if __name__ == '__main__':
    for country in links:
        create_job_csv(links[country], country)
