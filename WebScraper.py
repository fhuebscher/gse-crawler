import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

url = "https://en.wikipedia.org/wiki/My_Neighbor_Totoro"


# TODO initialise class in other classes for 
#   get_Info 
class WebScraper:
  def get_web_content(self, url):
    #Initialise Various Arrays to hold data for dictionary
      # links = []
      text = []
      titles = []
      subtitles = []
      section_titles = []
        
      #This can be changed for a basic html input file rather than a request
      page = requests.get(url, timeout=5)

      if page.status_code != 200:
        raise Exception(f"Status code: {page.status_code} for {url}")

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

      # # Grab link info
      # link_content = content.find_all("a")
      # for each in link_content:
      #   links.append(each.text.strip())

        #Append all info to dictionary
      website_data_dict  = {
          # "links": links,
          "text" : text,
          "titles" : titles,
          "subtitles" : subtitles,
          "section_titles" : section_titles
          }

      #Dictionary structure is a dictionary of array of arrays
      return website_data_dict


if __name__ == "__main__":
    
  json_data_store = {}

  path = 'CaliforniaGraph_small'
  output_path = 'datasets/CaliforniaGraph/CaliforniaGraph_crawling_json'

  column_names = ["type", "id", "link"]
  crawler = WebScraper()

  path = "datasets/CaliforniaGraph/CaliforniaGraph_small"
  graph = pd.read_csv(path, sep=" ", header=0, names=column_names)

  for index, row in graph.iterrows():
    
    url = row["link"]
    id = row["id"]

    try:
      website_data_dict = crawler.get_web_content(url)
    except Exception as e:
      print(e)
      website_data_dict = {}

    json_data_store[id] = website_data_dict

  with open(output_path, 'w') as outfile:
    json.dump(json_data_store, outfile)
  
  
  