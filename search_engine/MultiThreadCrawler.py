import multiprocessing, time
from bs4 import BeautifulSoup
from queue import Queue, Empty
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, urlparse
import requests

from Database import isExistInDB,  InsertUrlObject

links = []



HEADERS = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0'
}
EXCLUDED_EXTENSIONS = ['.jpg', '.png', '.gif', '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.mp4', '@', '#' ]
EXClUDED_SITES = ['facebook', 'youtube', 'instagram', 'linkedin', 'twitter']
# link filter
def isValidLink(link):
    if "http" not in link:
        # print("this url", link, " is not valid ")
         return False
    for ex in EXCLUDED_EXTENSIONS:
        if ex in link: return False
    
    for exsite in EXClUDED_SITES:
        if exsite in link: return False
    return True



class MultiThreadedCrawler:
  
    def __init__(self, seed_url):
        self.seed_url = seed_url
        self.root_url = '{}://{}'.format(urlparse(self.seed_url).scheme,
                                         urlparse(self.seed_url).netloc)
        self.pool = ThreadPoolExecutor(max_workers=4)
        self.scraped_pages = set([]) # visited urls
        self.crawl_queue = Queue()
        self.crawl_queue.put(self.seed_url)
  

  
    def parse_and_retrieve(self, html): # to extract links and content 
        
        
        soup = BeautifulSoup(html, 'lxml')
        
        #1-  extreact Links
        extractedLinks = []
        Anchor_Tags = soup.find_all('a', href=True)

        
        for link in Anchor_Tags:
            url = link['href']
           # print("WHAT's THE FUCKIS THIS HISHISH ", url)
            if url not in self.scraped_pages and isValidLink(url) and not isExistInDB(url):
                    #print("yes indexing this url", url)
                    self.crawl_queue.put(url)
                    extractedLinks.append(url)
        
        page_title = soup.find('title').text
        web_page_paragraph_contents = soup('p')
        content = ''
        for para in web_page_paragraph_contents:
            if not ('https:' in str(para.text)):
                content = content + str(para.text).strip()
        print('Text Present in The WebPage is --->', content[0: 20])
        
        return page_title, content, extractedLinks

        
    def post_scrape_callback(self, res):
        result = res.result()
        url = result.url
        print("hooooooooooooo", url)
        if result and result.status_code == 200:
            page_title,  content, extractedLinks = self.parse_and_retrieve(result.text)
            Url = {'url': url, 'title': page_title, 'content': content, 'extractedLinks': extractedLinks}
            InsertUrlObject(Url)
            print(Url['url'], " this is indexed url")
            
            #self.parse_and_retrieve(result.text)
            #self.parse_links(result.text)
           # self.scrape_info(result.text)
  
    def requestPage(self, url): # get response
        try:
            res = requests.get(url, timeout=(3, 30), headers=HEADERS)
            return res
        except requests.RequestException:
            return
  
    def run_web_crawler(self, num_of_sites):
        while num_of_sites:
            num_of_sites-=1
            try:
              #  print("\n Name of the current executing process: ",
               #       multiprocessing.current_process().name, '\n')
                target_url = self.crawl_queue.get(timeout=60)
                if target_url not in self.scraped_pages:
                    print("Scraping URL: {}".format(target_url))
                    self.current_scraping_url = "{}".format(target_url)
                    self.scraped_pages.add(target_url)
                    job = self.pool.submit(self.requestPage, target_url)
                    job.add_done_callback(self.post_scrape_callback)
  
            except Empty:
                return
            except Exception as e:
                print(e)
                continue
  
    def info(self):
        print('\n Seed URL is: ', self.seed_url, '\n')
        print('Scraped pages are: ', self.scraped_pages, '\n')
  
  
def run():
    seed = "https://www.mayoclinic.org/diseases-conditions/hearing-loss/symptoms-causes/syc-20373072"
    NUM_OF_STIES = 10


    cc = MultiThreadedCrawler(seed)


    cc.run_web_crawler(NUM_OF_STIES)

    #cc.info()
run()