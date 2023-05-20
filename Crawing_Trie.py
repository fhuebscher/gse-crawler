import pandas as pd
from bs4_text_crawling import Crawler 
from Trie import Trie

def get_url_node(path, crawler, trie, elements = ['h1', 'h2', 'title']):

  column_names = ["type", "id", "link"]
  graph = pd.read_csv(path, sep=" ", header=0, names=column_names)

  for index, row in graph.iterrows():
    
    url = row["link"]
    id = row["id"]


    headers = crawler.get_elements_from_url(url, elements)
    print(headers)
    
    trie.insert(headers, id)


if __name__ == "__main__":

    path = 'CaliforniaGraph_small'

    crawler = Crawler()

    trie = Trie()

    get_url_node(path, crawler, trie)


    # text = get_text_from_url(url)
    # print(text)

    # links = get_links_from_url(url)
    # print(links)

    # # more elements can be added
    
    # headers = get_elements_from_url(url, elements)
    # print(headers)
