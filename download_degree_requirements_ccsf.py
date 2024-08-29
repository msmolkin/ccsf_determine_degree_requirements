import os
import requests
from bs4 import BeautifulSoup

# Define the URL to scrape
url = "https://www.ccsf.edu/academics/ccsf-catalog/courses-by-department/child-development-and-family-studies"

# Send a GET request to the URL
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Save the scraped HTML content to a file
with open('cdev_degrees.html', 'w', encoding='utf-8') as file:
    file.write(f"<!-- {url} -->\n")
    file.write(soup.prettify())


# Create directories for courses and degrees
os.makedirs('courses', exist_ok=True)
os.makedirs('degrees/major', exist_ok=True)
os.makedirs('degrees/certificate', exist_ok=True)

# Extract and save courses
courses_section = soup.find('div', {'class': 'view-content'})
if courses_section:
    courses = courses_section.find_all('div', {'class': 'views-row'})
    with open('courses/courses.md', 'w', encoding='utf-8') as file:
        with open('courses/courses_with_descriptions.md', 'w', encoding='utf-8') as desc_file:
            file.write("# Courses\n\n")
            for course in courses:
                course_title_div = course.find('div', {'class': 'catalog-title'})
                if course_title_div:
                    course_title = course_title_div.text.strip()
                    course_description_div = course.find('div', {'class': 'course-description'})
                    course_description = course_description_div.text.strip() if course_description_div else "No description available."
                    file.write(f"- {course_title}\n")
                    desc_file.write(f"- {course_title}\n")
                    desc_file.write(f"  {course_description}\n\n")

# Extract and save degrees
main_content = soup.find('main', {'class': 'row', 'role': 'main'})
if main_content:
    article = main_content.find('article', {'class': 'catalog_page'})
    if article:
        degrees_section = article.find('div', {'class': 'clearfix text-formatted field field--name-body field--type-text-with-summary field--label-hidden field__item'})
        if degrees_section:
            majors = degrees_section.find('h3', string='Majors')
            certificates = degrees_section.find('h3', string='Certificates')

            if majors:
                major_list = majors.find_next('ul').find_all('li')
                for item in major_list:
                    degree_url = item.find('a')['href']
                    degree_response = requests.get(degree_url)
                    degree_name = item.text.strip()
                    degree_name = degree_name.replace(':', '_').replace('/', '_')
                    with open(f'degrees/major/{degree_name}.html', 'w', encoding='utf-8') as file:
                        file.write(f"<!-- {degree_url} -->\n")
                        file.write(degree_response.text)

            if certificates:
                certificate_list = certificates.find_next('ul').find_all('li')
                for item in certificate_list:
                    certificate_url = item.find('a')['href']
                    certificate_response = requests.get(certificate_url)
                    certificate_name = item.text.strip()
                    certificate_name = certificate_name.replace(':', '_').replace('/', '_')
                    with open(f'degrees/certificate/{certificate_name}.html', 'w', encoding='utf-8') as file:
                        file.write(f"<!-- {certificate_url} -->\n")
                        file.write(certificate_response.text)
