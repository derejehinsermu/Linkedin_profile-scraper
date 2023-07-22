from linkedin_scraper import Person, actions
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import csv


from scrape_profiles import scrape_profiles
from export_csv import export_to_csv

# Scrape profiles
profile_urls = scrape_profiles()

# Export profile URLs to CSV
csv_file = "profile_urls.csv"
export_to_csv(profile_urls, csv_file)

print(f"Profile URLs exported to {csv_file} successfully.")


email = 'Your email'
password = 'Your password'

# Define the CSV file path containing profile URLs
csv_file_path = "profile_urls.csv"

# Read the profile URLs from the CSV file
profile_urls = []
with open(csv_file_path, "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        profile_urls.append(row["Profile URLs"])

# Define the CSV file path to save the profile data
csv_file = "profile_data.csv"

# Define the fieldnames for the CSV file
fieldnames = [
    "Name",
    "Degree",
    "Institution Name",
    "Position Title",
    "From Date",
    "To Date",
    "Duration",
    "Location",
   
]

# Create a new instance of the WebDriver
driver = webdriver.Chrome()

# Write experiences and educations to the CSV file
with open(csv_file, "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

    for profile_url in profile_urls:
        person = None

        try:
            # Create a new instance of the WebDriver and log in
            driver = webdriver.Chrome()
            actions.login(driver, email=email, password=password, timeout=1000)

            # Create a new Person instance and scrape the profile
            person = Person(profile_url, driver=driver,scrape=False)
            person.scrape()

            # Scrape educations
            educations = person.educations

            for education in educations:
                education_dict = {
                    "Name": "",
                    "Degree": education.degree,
                    "Institution Name": education.institution_name,
                    "Position Title": "data is unavailable",
                    "From Date": education.from_date,
                    "To Date": education.to_date,
                    "Duration": "data is unavailable",
                    "Location": "data is unavailable",
                   
                }
                try:
                    if person.name is not None:
                        education_dict["Name"] = person.name.splitlines()[0]
                    else:
                        print("Person name is not available. Skipping...")
                except AttributeError:
                    pass

                writer.writerow(education_dict)

            if hasattr(person, "experiences"):
                # Scrape experiences
                experiences = person.experiences

                previous_experience = None

                for experience in experiences:
                    experience_dict = {
                        "Name": "data is unavailable",
                        "Degree": "data is unavailable",
                        "Institution Name": "data is unavailable",
                        "Position Title": "data is unavailable",
                        "From Date": "data is unavailable",
                        "To Date": "data is unavailable",
                        "Duration": "data is unavailable",
                        "Location": "data is unavailable",
                     
                    }
                    try:
                        if person.name is not None:
                            experience_dict["Name"] = person.name.splitlines()[0]
                        else:
                            print("Person name is not available. Skipping...")
                    except AttributeError:
                        pass
      
                    try:
                        if experience.institution_name:
                            experience_dict["Institution Name"] = experience.institution_name
                    except NoSuchElementException:
                        pass

                    try:
                        if experience.position_title:
                            experience_dict["Position Title"] = experience.position_title
                    except NoSuchElementException:
                        pass

                    try:
                        if experience.from_date:
                            experience_dict["From Date"] = experience.from_date
                    except NoSuchElementException:
                        pass

                    try:
                        if experience.to_date:
                            experience_dict["To Date"] = experience.to_date
                    except NoSuchElementException:
                        pass

                    try:
                        if experience.duration:
                            experience_dict["Duration"] = experience.duration
                    except NoSuchElementException:
                        pass

                    try:
                        if experience.location:
                            experience_dict["Location"] = experience.location
                    except NoSuchElementException:
                        pass
                        
                    if experience_dict != previous_experience:
                        writer.writerow(experience_dict)
                        previous_experience =experience_dict
            else:
                print(f"No experiences found for {person.name}")

            try:
                if person.name is not None:
                    print(f"Profile data for {person.name.splitlines()[0]} exported to {csv_file} successfully.")
                else:
                    print("Person name is not available. Skipping...")
            except AttributeError:
                print("Error accessing person's name. Skipping...")
                continue

        except NoSuchElementException:
            if person:
                print(f"Error accessing experience details for {person.name.splitlines()[0]}. Skipping.")
            else:
                print("Error accessing experience details for profile. Skipping.")

        finally:
            # Close the browser
            driver.quit()

print("All profile data exported to profile_data.csv successfully.")
