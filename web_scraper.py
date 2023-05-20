import requests
from bs4 import BeautifulSoup

url = "https://en.wikipedia.org/wiki/My_Neighbor_Totoro"


def Get_info(url):
  #Initialise Various Arrays to hold data for dictionary
    links = []
    text = []
    titles = []
    subtitles = []
    section_titles = []
    
    #This can be changed for a basic html input file rather than a request
    page = requests.get(url, timeout=10)

    #Convert html doc content into a soup object
    content = BeautifulSoup(page.content, "html.parser")

    #grab title and subtitle information
    title_content = content.find_all("h1")
    subtitle_content = content.find_all("h2")
    section_title_content = content.find_all("h3")

    for each in title_content:
      titles.append(each.text.strip())

    for each in subtitle_content:
      subtitles.append(each.text.strip())

    for each in section_title_content:
      section_titles.append(each.text.strip())


    #Grab text info
    text_content = content.find_all("p")
    for each in text_content:
      text.append(each.text.strip())

    #Grab link info
    link_content = content.find_all("a")
    for each in link_content:
      links.append(each.text.strip())

      #Append all info to dictionary
    dictionary  = {
        "links": links,
        "text" : text,
        "titles" : titles,
        "subtitles" : subtitles,
        "section_titles" : section_titles
        }



    #Dictionary structure is a dictionary of array of arrays
    return dictionary
