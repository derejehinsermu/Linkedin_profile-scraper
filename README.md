
## Installation


pip install linkedin_scraper


## Setup
First, you must set up your chromedriver location

follow the link to install chromedriver for ubuntu

### ubuntu:

https://skolo.online/documents/webscrapping/

### Macos:

https://www.swtestacademy.com/install-chrome-driver-on-mac/

verify for macos since it not verified by macos

    $ xattr -d com.apple.quarantine chromedrive

or
follow this link

https://stackoverflow.com/questions/60362018/macos-catalinav-10-15-3-error-chromedriver-cannot-be-opened-because-the-de

## open main.py and login.py

replace this line with you email

    email = 'your email'
    password = 'your password'


Finally:

run the python code:

    $ python main.py

it will prompt for to ask for url 

Enter the profile URL of the person:"Enter any Linkedin url"

example enter this url: https://www.linkedin.com/in/hamid-shafigh-4703b0133/

it may be the Linkedin asked you for verification.

Exception:

    if User has restricted their connection visibility.
    
    it will ask again for url
    

 OUTPUT

 the url of user connection is saved to profile_urls.csv

 the details of url is saved profile_data.csv
