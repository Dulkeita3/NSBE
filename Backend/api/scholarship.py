import requests # Used for making HTTP requests to scrape data from websites
from bs4 import BeautifulSoup # for scrapping the info off of websites via their html
from datetime import datetime
import re # for regex for dates, as of rn only for JVL

class NSBEScholarshipsJVL:
    def __init__(self, urls):
        self.urls = urls
        self.soup = None
        self.scholarships = {}
    
    def filter_links_by_month(self, links):
        # Get the current month as an integer (1 for January, 2 for February, etc.)
        current_month = datetime.now().month

        # Initialize an empty list for the filtered links
        filtered_links = []

        # Use a for loop to filter the links
        for i, link in enumerate(links, start=1):
            if (current_month - 3) <= i <= 12:
                filtered_links.append(link)

        return filtered_links
        
        
    def fetch_content(self, url):
        """
        Fetch the webpage content for a given URL and initialize the BeautifulSoup object.
        """
        response = requests.get(url)
        if response.status_code == 200:
            self.soup = BeautifulSoup(response.text, 'html.parser')
            pages = [url]
            page_links = self.soup.find('p', class_= 'page-links')
            if page_links:
                links = page_links.find_all('a')
                for x in range(len(links)-1):
                    pages.append(links[x].get('href'))
            return pages
        else:
            raise Exception(f"Failed to fetch content from {url}. Status code: {response.status_code}")
        
    def pull_closing_dates(self):
        closing_date_tags = self.soup.find_all('strong', string="Closing Date")
        dates = []
        for tag in closing_date_tags:
            date = tag.next_sibling  # Get the immediate sibling text
            if date and date != ":": # if it's not NONE
                posDate = date.replace(": ", "").strip()  # Remove ": " and clean up
                if posDate:  # If a valid date is found
                    dates.append(posDate)
                else:  # Check for <em> tags if no direct date is found
                    em_tag = tag.find_next("em")
                    if em_tag:
                        if em_tag == ":":
                            continue
                        updatedDate = em_tag.text.strip().replace("extended to ", "")
                        dates.append(updatedDate)
            else:
                em_tag = tag.find_next("em")  # Fallback to <em> if next_sibling is None
                if em_tag:
                    if em_tag == ":":
                        continue
                    updatedDate = em_tag.text.strip().replace("extended to ", "")
                    dates.append(updatedDate)
        return dates
    
    def pull_links(self):
        #links_tags = self.soup.select('div p strong a')
        links_tags = []
        link_info = []
        target_div = self.soup.find('div', class_='entry-content')
        paragraphs = target_div.find_all('p')
        for p in paragraphs:
    # Check for <strong><a> (strong wrapping a)
            strong_a = p.find('strong')
            if strong_a and strong_a.find('a'):
                links_tags.append(strong_a.find('a'))

            # Check for <a><strong> (a wrapping strong)
            a_tag = p.find('a')
            if a_tag and a_tag.find('strong'):
                links_tags.append(a_tag)
        
        
        for link in links_tags:
            link_info.append([link.text, link.get('href')])
        return link_info
    
    def pull_amounts(self):
        amounts_tags = self.soup.find_all('strong', string=re.compile(r"Amou", re.IGNORECASE))
        amount_info = []
        for amount in amounts_tags:
            amount_info.append(amount.next_sibling.replace(": ", ""))
        return amount_info
    
    def pull_descriptions(self):
# Find all <strong> tags with a string that contains "Descrip"
        descriptions_tags = self.soup.find_all('strong', string=re.compile(r"Descri", re.IGNORECASE))
        #descriptions_tags = self.soup.find_all('strong', string = "Description")
        description_info = []
        for description in descriptions_tags:
            description_info.append(description.next_sibling.replace(": ", ""))
        return description_info
            
    def valid_scholarships(self, links, amounts, dates, descriptions):
        today = datetime.today()
        for element in range(len(dates)):
            match = re.search(r'\b(January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, \d{4}\b', dates[element])
            if match:
                updated_date = match.group(0)
                closing_date = datetime.strptime(updated_date, "%B %d, %Y")
                if closing_date >= today:
                    self.scholarships[links[element][0]] = [links[element][1], amounts[element],dates[element], descriptions[element]]
                else:
                    continue
    
    def process_page(self, url):
        """
        Process a single webpage and add valid scholarships to the dictionary.
        """
        #self.fetch_content(url)
        all_pages = self.fetch_content(url)
        for page in all_pages:
            response = requests.get(page)
            if response.status_code == 200:
                self.soup = BeautifulSoup(response.text, 'html.parser')
            links = self.pull_links()
            amounts = self.pull_amounts()
            dates = self.pull_closing_dates()
            descriptions = self.pull_descriptions()
            self.valid_scholarships(links, amounts, dates, descriptions)

    def run(self):
        """
        Process all webpages and return a dictionary of scholarships.
        """
        updatedUrls = self.filter_links_by_month(self.urls)
        for url in updatedUrls:
            print(f"Processing {url}...")
            self.process_page(url)
        return self.scholarships


if __name__ == "__main__":
    urls = [
        "https://jlvcollegecounseling.com/scholarships/january-scholarships/",
        "https://jlvcollegecounseling.com/scholarships/february-scholarships/",
        "https://jlvcollegecounseling.com/scholarships/march-scholarships/",
        "https://jlvcollegecounseling.com/scholarships/april-scholarships/",
        "https://jlvcollegecounseling.com/scholarships/may-scholarships/",
        "https://jlvcollegecounseling.com/scholarships/june-scholarships/",
        "https://jlvcollegecounseling.com/scholarships/july-scholarships/",
        "https://jlvcollegecounseling.com/scholarships/august-scholarships/",
        "https://jlvcollegecounseling.com/scholarships/september-scholarships/",
        "https://jlvcollegecounseling.com/scholarships/october-scholarships/",
        "https://jlvcollegecounseling.com/scholarships/november-scholarships/",
        "https://jlvcollegecounseling.com/scholarships/december-scholarships/"

    ]

    scraper = NSBEScholarshipsJVL(urls)
    all_scholarships = scraper.run()

    print("Scholarships:")
    if len(all_scholarships) > 0:
        for val, name in enumerate(all_scholarships.keys()):
            print(f"Name: {name}, Due Date: {scraper.scholarships[name][2]}, Number: {val+1}\n")
    else:
        print("nada")
    # for name, details in all_scholarships.items():
    #     print(f"Name: {name}, Details: {details}")