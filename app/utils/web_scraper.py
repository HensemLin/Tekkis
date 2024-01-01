from bs4 import BeautifulSoup
from ratelimit import limits, sleep_and_retry
import time
import requests
import logging
import json

class WebScraper:
    def __init__(self, url):
        """
        Constructor for the WebScraper class.

        Args:
            url (str): The URL from which content URLs will be scraped.
        """
        self.url = url
        self.session = requests.Session()  

    @sleep_and_retry
    @limits(calls=5, period=5)
    def _get_html(self, url):
        """
        Sends a GET request to the class's URL and returns the response as text.

        Returns:
            str: The HTML content of the webpage as text.
            None: If the GET request fails or the response status code is not 200.

        Raises:
            requests.exceptions.RequestException: If an error occurs during the GET request or the response status code is not 200.
        """
        retries = 0
        MAX_RETRIES = 3
        delay = 1
        while retries < MAX_RETRIES:
            try:
                response = self.session.get(url)
                if response.status_code == 200:
                    # Retrieve HTML content and return it
                    html_text = response.content
                    return html_text
                elif response.status_code == 429:
                    logging.info(f'Rate Limit occured retrying for: {retries}/{MAX_RETRIES}')
                    time.sleep(delay)  
                    retries += 1
                    delay *= 2 
                else:
                    # Raise an exception if the response status code is not 200
                    raise requests.exceptions.RequestException(f"Invalid response status code {response.status_code} for {self.url}")
            
            except requests.exceptions.RequestException as e:
                logging.error(f"Error retrieving HTML from {url}: {e}")
                time.sleep(delay)  # Backoff for other request exceptions
                retries += 1
                delay *= 2
            except Exception as e:
                logging.error(f"Error retrieving HTML from {url}: {e}")

    def _parse_html(self, html_text: bytes):
        """
        Parses the HTML content of the webpage using BeautifulSoup and returns a soup object.

        Returns:
            bs4.BeautifulSoup: The soup object containing the parsed HTML content of the webpage.
            None: If the HTML content cannot be retrieved or parsed.

        Raises:
            Exception: If an error occurs during HTML retrieval or parsing.
        """
        try:
            if html_text:
                # Parse HTML content and return soup object
                soup = BeautifulSoup(html_text, 'html5lib')
                return soup
            else:
                # Return None if the HTML content cannot be retrieved or parsed
                return None
        except Exception as e:
            error_message = 'Error occurred during HTML parsing: {}'.format(str(e))
            logging.error(msg=error_message)
            raise e

    def _get_car_link(self, soup: BeautifulSoup):
        """
        Extracts car listing hyperlinks from the given HTML soup. This method specifically looks for 
        'a' tags within a certain div structure and retrieves those with both 'href' and 'title' attributes, 
        which are assumed to be links to individual car listings.

        Args:
            soup (bs4.BeautifulSoup): The soup object containing the parsed HTML content of a car listings webpage.
        
        Returns:
            list: A list of BeautifulSoup Tag objects, each representing a car listing hyperlink.
        """
        try:
            car_links = []
            # Find the main content div and then extract hyperlinks from a specific inner div
            main_content = soup.find('div', attrs={'id':'__next'})
            div_container = main_content.find('div', attrs={'class':'mw15 mw4'})
            car_listing_links = div_container.findAll('a')

            for link in car_listing_links:
                # Append only those hyperlinks that have both href and title attributes
                if link.get('href') and link.get('title'):
                    if link.get('href') not in car_links:
                        car_links.append(link.get('href'))

            return car_links

        except Exception as e:
            error_message = f"Error occurred when getting car links: {str(e)}"
            logging.error(msg=error_message)
            raise e
     
    def _get_car_details(self, soup: BeautifulSoup):
        """
        Extracts car details from a JSON embedded within the HTML soup. This method looks for a 'script' 
        tag with a specific id and then parses the JSON content to retrieve car specifications.

        Args:
            soup (bs4.BeautifulSoup): The soup object containing the parsed HTML content of a car details page.
        
        Returns:
            dict: A dictionary with car specifications, extracted from the JSON content.
        """
        try:
            car_specifications = {}
            result = {}
            # Extracting JSON data from a script tag
            json_script_tag = soup.find('script', attrs={'id': '__NEXT_DATA__'})
            json_data = json.loads(json_script_tag.string)

            for item in json_data.get('props', {}).get('initialState', {}).get('adDetails', {}).get('byID').values():
                # Parsing each car specification from the JSON data
                car_specifications['PRICE'] = [{'label':'Price', 'value':item.get('attributes', {}).get('price')}]
                for car_spec in (item.get('attributes', {}).get('mcdParams', [])):
                    car_specifications[car_spec.get('header', '')] = car_spec.get('params', [])
            
            for category in car_specifications:
                result[category] = {}
                for item in car_specifications[category]:
                    label = item['label']
                    value = item['value']
                    result[category][label] = value
            
            return result

        except Exception as e:
            error_message = f"Error occurred during car details extraction: {str(e)}"
            logging.error(msg=error_message)
            return None

    def _next_page(self, soup: BeautifulSoup):
        """
        Finds and returns the URL of the next page from the HTML soup. This method searches for a 'link' 
        tag with a 'rel' attribute containing 'next', which indicates the link to the next page of listings.

        Args:
            soup (bs4.BeautifulSoup): The soup object containing the parsed HTML content of a webpage.

        Returns:
            str: The URL of the next page if found.
            None: If there is no next page or in case of an error.
        """
        try:
            links = soup.findAll("link")
            for link in links:
                if "next" in link.get('rel'):
                    return link.get('href')
            
            return None
                
        except Exception as e:
            error_message = f"Error occurred during next page extraction: {str(e)}"
            logging.error(msg=error_message)
            return None

    def scrap_all_cars(self, limit: int = 50):
        """
        Scrapes all cars from the website.

        Returns:
            list: A list of dictionaries, where each dictionary contains the details of the cars.
        """
        try:
            current_url = self.url
            car_details = []
            while current_url is not None:
                print(f"Scrapping from {current_url}")
                html_text = self._get_html(current_url)
                print(f"Parsing data from {current_url}")
                soup = self._parse_html(html_text)
                car_links = self._get_car_link(soup)
                print(f"Car links: ", car_links)
                for link in car_links:
                    print(f"Scrapping from {link}")
                    html_text = self._get_html(link)
                    print(f"Parsing data from {link}")
                    car_soup = self._parse_html(html_text)
                    car_detail = self._get_car_details(car_soup)
                    if car_detail is not None:
                        car_details.append(car_detail)
                    if len(car_details) >= limit:
                        return car_details
                current_url = self._next_page(soup)

        except Exception as e:
            error_message = f"Error occurred during scraping: {str(e)}"
            logging.error(msg=error_message)
            raise e

if __name__ == "__main__":
    # x = WebScraper(url="https://www.mudah.my/malaysia/cars-for-sale").scrap_all_cars()
    x= WebScraper("https://www.mudah.my/2009+Toyota+VIOS+1+5+S+A+TRD+VERY+GOOD+CONDITION-104588287.htm").scrap_all_cars()
    print(x)