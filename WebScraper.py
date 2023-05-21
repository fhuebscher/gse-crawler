import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

url = "https://en.wikipedia.org/wiki/My_Neighbor_Totoro"

class WebScraper:
  # Fetch website content and return as dictionary
  def get_web_content(self, url, timeout=5, headers=None):
    # Initialise Various Arrays to hold data for dictionary
      # links = []
      text = []
      titles = []
      subtitles = []
      section_titles = []
        
      page = requests.get(url, timeout=timeout, headers=headers)

      if page.status_code != 200:
        raise Exception(f"Status code: {page.status_code} for {url}")

      # Convert html doc content into a soup object
      content = BeautifulSoup(page.content, "html.parser")

      # Grab title and subtitle information
      title_content = content.find_all("h1")
      subtitle_content = content.find_all("h2")
      section_title_content = content.find_all("h3")

      for each in title_content:
        titles.append(each.text.strip())

      for each in subtitle_content:
        subtitles.append(each.text.strip())

      for each in section_title_content:
        section_titles.append(each.text.strip())


      # Grab text info
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

      # Return website data dict
      return website_data_dict
  
  # Save output to file
  def save_to_file(self, output_path, json_data_store):
    with open(output_path, 'w') as outfile:
      json.dump(json_data_store, outfile)


if __name__ == "__main__":

  # Crawler configuration
  crawler = WebScraper()
  column_names = ["type", "id", "link"]
  headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/113.0', 
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', 
    'Accept-Language': 'en-US,en;q=0.5', 
    'Accept-Encoding': 'gzip, deflate, br', 
    'DNT': '1', 
    'Connection': 'keep-alive', 
    'Cookie': 'wp_devicetype=0; wp_ak_signinv2=1|20230125; wp_ak_pct=1|20230517; wp_ak_wab=1|0|3|1|0|1|1|1|1|20230418; wp_ak_v_mab=0|0|0|20230429; wp_pwapi_ar="H4sIAAAAAAAA/6uuBQBDv6ajAgAAAA=="; wp_usp=1---; wp_geo=AU|NSW|||; ak_bmsc=58A3B171450D4287415962140A5F5B52~000000000000000000000000000000~YAAQp1jWF6UvCDCIAQAAeg8CPBMndoUnsofvuMuxwQ88iWGc55tJ7qj3MOgsO26EGwVA49hRemlotiOHe1tncojNCSnbIPDSKR9Lek6sRhSxKTygoCbz9PXxo9RRtm9QiPJB6ShqHsepTizg1K3tU1XsY4W2lhIgaTvxrMpNYPd8vcHOvfk3jq8JO7Mjz8AZ8Gzg6Fp05/ZZGXXyBs9+0gU1DbYD97tnk8ioipH0Ud3HGsbyuDH0/ZAQ7U3qJUy9ZtMypX0pRcNSfTmGwTFlJSGQ1NiMNY7fOgvRCpyuH5HHB5S6FW+ACrjoMRimvDW+PqJTeWDf+clp+UrWbcl6Jr5KPHqVMaXdZjEqmofFXgYOOvhGYkKl415T/D57nZoKIUuCa8x0Qq+bU/eiAaxFjA==; wp_ak_bt=1|20200518; wp_ak_bfd=1|20201222; wp_ak_tos=1|20211110; wp_ak_sff=1|20220425; wp_ak_lr=0|20221020; wp_ak_co=2|20220505; wp_ak_pp=1|20210310; bm_sv=53E918F6AFB327449ED337160B79D1E7~YAAQp1jWF6eiCDCIAQAABKcNPBOhpwzrW7U8f1HZBI3QPuk65gkcf7JPmeD1zh/RPhznU7DO1xpPpbMv3D4OoUGl1faQTAZqFASIwlLYzH5uuK4qbxTSxjGJ030RFG4voNYGjbrT4He1bAs7WahBurXXrazhKa2g0Zct7Ae7IASLihwuIdA9NxtvNd5DC7Lt/Y1xic3TcBkdJtqT+GaEK9Frg10bshNQszpCcoN3iQfJjqZu7x7GYO4Ff/pqr/8uQ9W41KOlP2XQ~1', 
    'Upgrade-Insecure-Requests': '1', 
    'Sec-Fetch-Dest': 'document', 
    'Sec-Fetch-Mode': 'navigate', 
    'Sec-Fetch-Site': 'cross-site', 
    'Sec-Fetch-User': '?1', 
    'Sec-GPC': '1'
  }

  dataset_path = "datasets/CaliforniaGraph/CaliforniaGraph"
  checkpoint_path = "datasets/CaliforniaGraph/crawling_checkpoints/cp"
  output_path = 'datasets/CaliforniaGraph/CaliforniaGraph_crawling.json'

  graph = pd.read_csv(dataset_path, sep=" ", header=0, names=column_names)
  json_data_store = {}

  for index, row in graph.iterrows():
    
    type = row["type"]
    url = row["link"]
    id = row["id"]
    
    if type == 'n':
      try:
        website_data_dict = crawler.get_web_content(url, headers=headers)
      except Exception as e:
        print(e)
        website_data_dict = {}

      json_data_store[id] = website_data_dict

    # Save checkoint data
    if (index % 1000 == 0):
      crawler.save_to_file(f"{checkpoint_path}_{index}.json", json_data_store)

  # Save final crawling results data
  crawler.save_to_file(output_path, json_data_store)