
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import re
import csv
import json
import hashlib
# Setup the ChromeDriver and open the website
driver_service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=driver_service)
def getHrefs():
    driver.get("https://www.seattle.gov/neighborhoods/p-patch-gardening/garden-list")  # replace with your url

    # Initialize empty list to hold hrefs
    hrefs = []

    # Find all divs with the class "titleDateContainer"
    divs = driver.find_elements(By.CLASS_NAME, 'titleDateContainer')

    # For each div, find the <a> element and get its href
    for div in divs:
        a_element = div.find_element(By.TAG_NAME, 'a')
        href = a_element.get_attribute('href')
        hrefs.append(href)

    # Print the hrefs
    for href in hrefs:
        print(href)
    
    return hrefs
def createDict(url_list):

    # Initialize empty dictionary to hold data
    p_patches = {}

    # List of urls
    url_list = url_list  # Replace with your list of URLs

    # Class names to search for
    class_names = ["pageTitle", "Address", "features", "Numberofplots", "Established", "size", "waitTime", "span"]

    # Iterate over each URL
    for url in url_list:
        driver.get(url)

        # Initialize the nested dictionary for this page
        page_title = driver.find_element(By.CLASS_NAME, class_names[0]).text
        p_patches[page_title] = {}
        # Search for elements with each class name and add their inner text to the dictionary
        for class_name in class_names[1::]:
            try:
                element = driver.find_element(By.CLASS_NAME, class_name)
            except:
                print(f"Can't find the {class_name} element on {url}")
                p_patches[page_title][class_name] = f"We ain't got no {class_name} for {page_title}"
                continue
            if class_name == "features":
                p_patches[page_title][class_name] = []
                li_elements = element.find_elements(By.CLASS_NAME, 'ppatchFeature')
                for li_elem in li_elements:
                    # Concatenate the text from all elements with the same class name
                    text = li_elem.text
                    # Add the text to the page data dictionary, using the class name as the key
                    p_patches[page_title][class_name].append(text)
            elif class_name == "span":
                # Concatenate the text from all elements with the same class name
                text = re.split(': ', element.text)
                # Add the text to the page data dictionary, using the class name as the key
                p_patches[page_title]["description"] = text[-1]
            else:
                # Concatenate the text from all elements with the same class name
                text = re.split(': ', element.text)
                # Add the text to the page data dictionary, using the class name as the key
                p_patches[page_title][class_name] = text[-1]
            

    # Close the driver
    driver.quit()

    # Print the p_patches
    for title, data in p_patches.items():
        print(f"{title}: {data}\n\n\n")
    return p_patches

def toCsv(dictionary):
    # Specify the file name
    file_name = 'ppatchData.csv'
    fieldnames = list(next(iter(dictionary.values())).keys())
    # Write the dictionary to a CSV file
    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in dictionary.values():
            writer.writerow(item)
def toJSON(data):
    # Specify the file name
    file_name = 'output.txt'
    # Add an _id field to each JSON object
    # for obj in data:
    #     obj['_id'] = hashlib.sha256(json.dumps(obj, sort_keys=True).encode()).hexdigest()
    # force the dictionary into a list of the nested dictionaries
    data_list = list(data.values())
    # Write the dictionary to a text file
    with open(file_name, 'w') as file:
        json.dump(data_list, file, indent=4)
hrefs = getHrefs()
ppDict = createDict(hrefs)
toJSON(ppDict)
# toCsv(ppDict)

