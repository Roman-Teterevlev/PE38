import requests
from bs4 import BeautifulSoup

def get_html(url: str):
    return requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        },
    )


def extract_vacancy_data(html):
    soup = BeautifulSoup(html, 'html.parser')

    # Ищем название вакансии
    title = soup.find('h1', {'data-qa': 'vacancy-title'})
    title_text = title.get_text(strip=True) if title else 'Не указано'

    # Ищем название компании
    company = soup.find('a', {'data-qa': 'vacancy-company-name'})
    company_text = company.get_text(strip=True) if company else 'Не указано'

    # Ищем зарплату
    salary = soup.find('span', {'data-qa': 'vacancy-salary'})
    salary_text = salary.get_text(strip=True) if salary else 'Не указано'

    # Ищем описание вакансии
    description = soup.find('div', {'data-qa': 'vacancy-description'})
    description_text = description.get_text(strip=True) if description else 'Не указано'

    # Ищем ключевые навыки
    skills = soup.find_all('span', {'data-qa': 'bloko-tag__text'})
    skills_text = ', '.join(skill.get_text(strip=True) for skill in skills) if skills else 'Не указано'

    # Формируем Markdown строку
    markdown = f"""
# {title_text}

**Компания:** {company_text}

**Зарплата:** {salary_text}

## Описание
{description_text}

## Ключевые навыки
{skills_text}
"""
    return markdown

def extract_candidate_data(html):
    soup = BeautifulSoup(html, 'html.parser')

    # Extracting candidate's name
    name_tag = soup.find('h2', class_='bloko-header-1')
    name = name_tag.text.strip() if name_tag else 'Не указано'

    # Extracting candidate's personal details
    personal_details_tag = soup.find('p')
    personal_details = personal_details_tag.text.strip() if personal_details_tag else 'Не указано'

    # Extracting job search status
    job_search_status_tag = soup.find('span', class_='label--rWRLMsbliNlu_OMkM_D3')
    job_search_status = job_search_status_tag.text.strip() if job_search_status_tag else 'Не указано'

    # Extracting location and relocation readiness
    location_info = soup.find('div', class_='bloko-translate-guard')
    if location_info:
        location_paragraphs = location_info.find_all('p')
        location = location_paragraphs[0].text.strip() if len(location_paragraphs) > 0 else 'Не указано'
        relocation = location_paragraphs[1].text.strip() if len(location_paragraphs) > 1 else 'Не указано'
    else:
        location = 'Не указано'
        relocation = 'Не указано'

    # Extracting desired position and salary
    position_tag = soup.find('span', class_='resume-block__title-text')
    position = position_tag.text.strip() if position_tag else 'Не указано'
    salary_tag = soup.find('span', class_='resume-block__salary')
    salary = salary_tag.text.strip() if salary_tag else 'Не указано'

    # Extracting employment and work schedule
    employment_info = soup.find('div', class_='resume-block-container')
    if employment_info:
        employment_paragraphs = employment_info.find_all('p')
        employment = employment_paragraphs[0].text.strip() if len(employment_paragraphs) > 0 else 'Не указано'
        work_schedule = employment_paragraphs[1].text.strip() if len(employment_paragraphs) > 1 else 'Не указано'
    else:
        employment = 'Не указано'
        work_schedule = 'Не указано'

    # Extracting key skills
    skills = [skill.text.strip() for skill in soup.find_all('div', class_='bloko-tag__section_text')]

    # Extracting about me section
    about_me_tag = soup.find('div', {'data-qa': 'resume-block-skills-content'})
    about_me = about_me_tag.text.strip() if about_me_tag else 'Не указано'

    # Extracting education
    education = []
    education_blocks = soup.find_all('div', {'data-sentry-component': 'ResumeEducationBody'})
    for block in education_blocks:
        year_tag = block.find('div', class_='bloko-column_xs-2')
        details_tag = block.find('div', class_='resume-block-container')
        if year_tag and details_tag:
            year = year_tag.text.strip()
            details = details_tag.text.strip()
            education.append(f"{year}: {details}")

    # Extracting languages
    languages = [lang.text.strip() for lang in soup.find_all('p', {'data-qa': 'resume-block-language-item'})]

    # Extracting citizenship and work permit
    citizenship_tag = soup.find('div', {'data-qa': 'resume-block-additional'})
    if citizenship_tag:
        citizenship_info = [info.text.strip() for info in citizenship_tag.find_all('p')]
    else:
        citizenship_info = ['Не указано']

    # Constructing the markdown string
    markdown = f"""
# {name}

## Personal Details
- {personal_details}

## Job Search Status
- {job_search_status}

## Location and Relocation
- {location}
- {relocation}

## Desired Position and Salary
- **Position:** {position}
- **Salary:** {salary}

## Employment and Work Schedule
- {employment}
- {work_schedule}

## Key Skills
- {'; '.join(skills)}

## About Me
- {about_me}

## Education
- {'; '.join(education)}

## Languages
- {'; '.join(languages)}

## Citizenship and Work Permit
- {'; '.join(citizenship_info)}
    """

    return markdown.strip()

def get_candidate_info(url: str):
    response = get_html(url)
    return extract_candidate_data(response.text)

def get_job_description(url: str):
    response = get_html(url)
    return extract_vacancy_data(response.text)
