
from typing import Any
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as firefoxOptions
from selenium.webdriver.chrome.options import Options as chromeOptions
from selenium.webdriver.common.by import By
from time import sleep
from csv import DictWriter
from selenium.common.exceptions import NoSuchElementException
 

class Linkeden:
    def __init__(self,keywords , baseLink:str ):
        options = firefoxOptions()
        self.jobsInfo = []
        options.add_argument('-headless')
        self.driverFirefox = webdriver.Firefox(options=options)
        self.driverFirefox.set_page_load_timeout(18000000)
        self.links = self.createLinks(keywords,baseLink)
    def createLinks(self,keywords,baseLink:str):
        links = []
        for key in keywords:
            key.replace(" ","%20")
            links.append (baseLink.replace("ENTERKEYWORD",key))
        return links
    def __call__(self):
        self.scrape()
        self.writeToCsv()
    def scrape(self):
        for link in self.links:
            self.driverFirefox.get(url = link)
            print("going to link" + link  )
            title = self.driverFirefox.title
            numberofres = ""
            for char in title:
                if char.isdigit():
                    numberofres = numberofres+char
                if not char.isdigit():
                    break
            numberofres = int(numberofres)
            print("number of reults found = ",numberofres)
            # implement auto scrolling now
            # two possibile solutions
            # 1 scroll all the way down you need then click on all the lis one by one 
            # 2 scroll one by one by scrolling all down first would be easier i think#
            scrollScript = """function scroll() {
    let totalHeight = 0;
    const distance = 1000;
    
    const timer = setInterval(() => {
      const button = document.querySelector("#main-content > section.two-pane-serp-page__results-list > button");
      
      if (button) {
        button.click();
      }          
      
      const scrollHeight = document.body.scrollHeight;
      window.scrollBy(0, distance);
      totalHeight += distance;
      
    //  if(document.querySelectorAll('.jobs-search__results-list li').length >= 200) {
    //  console.log("done")
    //     clearInterval(timer);
      // }
    }, 1000);
  }
  
  scroll();
            """

            while 1:
                jobLis = self.driverFirefox.find_elements(By.CSS_SELECTOR ,".jobs-search__results-list li")
                # print(dir(jobLis[0]))
                print("job lis found")
                x = (len(jobLis))
                print (str(x) + " jobs found")
                if not input("continue scrolling press y (lower case)") == 'y':
                    break
                self.driverFirefox.execute_script(script=scrollScript)
                sleep(5)
            print("auto Scrolling done")
            jobLis = self.driverFirefox.find_elements(By.CSS_SELECTOR ,".jobs-search__results-list li")
            # print(dir(jobLis[0]))
            print("job lis found")
            x = (len(jobLis))
            print (str(x) + " jobs found")
            for i  in  range(x):
                print("job number " +str(i))
                anchor = jobLis[i].find_element(By.TAG_NAME,"a")
                anchor.click()
                sleep(2)
                jobLink = anchor.get_property("href")
                try:
                    linkEl = self.driverFirefox.find_element(By.CSS_SELECTOR,".topcard__org-name-link")
                    companyLink = linkEl.get_attribute("href")
                    companyName = linkEl.text
                except NoSuchElementException:
                    companyLink = "NOT FOUND"
                applicants = self.driverFirefox.find_element(By.CSS_SELECTOR,".num-applicants__caption").get_property("textContent").strip()
                jobTitle = self.driverFirefox.find_element(By.CSS_SELECTOR,".top-card-layout__title").get_property("textContent")
                sleep(1)
                singleJob = {
                   "jobLink" : jobLink,
                   "companyLink" : companyLink,
                   "applicants" : applicants,
                   "jobTitle" : jobTitle,
                   "companyName" : companyName
                }
                self.jobsInfo.append(singleJob)
                print("added job info")
            print("all jobs done for this link")
        self.driverFirefox.quit()
        print("all scrapping done writing to csv now")
    def scrapeWithoutApplicants(self):
        for link in self.links:
            self.driverFirefox.get(url = link)
            print("going to link " + link  )
            title = self.driverFirefox.title

            print("\n",title)
            scrollScript = """function scroll() {
    let totalHeight = 0;
    const distance = 2000;
    
    const timer = setInterval(() => {
      const button = document.querySelector("#main-content > section.two-pane-serp-page__results-list > button");
      
      if (button) {
        button.click();
      }          
      
      const scrollHeight = document.body.scrollHeight;
      window.scrollBy(0, distance);
      totalHeight += distance;
      
     // if(document.querySelectorAll('.jobs-search__results-list li').length >= 500) {
     // console.log("done")
   //     clearInterval(timer);
      //}
    }, 1000);
  }
  
  scroll();
            """

            while 1:
                jobLis = self.driverFirefox.find_elements(By.CSS_SELECTOR ,".jobs-search__results-list li")
                # print(dir(jobLis[0]))
                print("job lis found")
                x = (len(jobLis))
                print (str(x) + " jobs found")
                if not input("continue scrolling press y (lower case)") == 'y':
                    break
                self.driverFirefox.execute_script(script=scrollScript)
                sleep(5)
            print("auto Scrolling done")
            jobLis = self.driverFirefox.find_elements(By.CSS_SELECTOR ,".jobs-search__results-list li")
            # print(dir(jobLis[0]))
            print("job lis found")
            x = (len(jobLis))
            print (str(x) + " jobs found")
            for i  in  range(x):
                print("job number " +str(i))
                try:
                    anchor = jobLis[i].find_element(By.CSS_SELECTOR,".base-card__full-link")
                except:
                    print("anchor not found for this link")
                    continue
                jobLink = anchor.get_property("href")
                jobTitle = jobLis[i].find_element(By.CSS_SELECTOR,".base-search-card__title").text
                companyEl = jobLis[i].find_element(By.CSS_SELECTOR,".base-search-card__subtitle")
                location = jobLis[i].find_element(By.CSS_SELECTOR,".job-search-card__location").text
                
                companyName = companyEl.text
                companyLink = companyEl.find_element(By.TAG_NAME,'a').get_property("href")
                # sleep(2)
                # try:
                #     linkEl = self.driverFirefox.find_element(By.CSS_SELECTOR,".topcard__org-name-link")
                #     companyLink = linkEl.get_attribute("href")
                #     companyName = linkEl.text
                # except NoSuchElementException:
                #     companyLink = "NOT FOUND"
                # applicants = self.driverFirefox.find_element(By.CSS_SELECTOR,".num-applicants__caption").get_property("textContent").strip()
                # jobTitle = self.driverFirefox.find_element(By.CSS_SELECTOR,".top-card-layout__title").get_property("textContent")
                # sleep(1)
                singleJob = {
                   "jobLink" : jobLink,
                   "companyLink" : companyLink,
                   'location':location,
                   
                   "jobTitle" : jobTitle,
                   "companyName" : companyName
                }
                self.jobsInfo.append(singleJob)
                print("added job info")
            print("all jobs done for this link")
        self.driverFirefox.quit()
        print("all scrapping done writing to csv now")
        self.writeToCsv()

    def writeToCsv(self):
        with open("output.csv", "w", newline="",encoding="utf-8") as csvfile:
            fieldnames = self.jobsInfo[0].keys()
            writer = DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in self.jobsInfo:
                writer.writerow(row)

                


if __name__ == "__main__":

##
# Job Titles: MERN Stack Developer | ReactJS Developer | NodeJS Developer | Frontend Developer | Full Stack Developer
# Javascript developer
# Junior, entry level aur internship

    keywords = [
                # "product owner",  #2000+ taking 900
               "Product Manager", #5000+ taking 1000
               "network engineering", #78
               "informatics", #25
               "automation" , #287
               'IT support',#208
               "Java Developer"

]
    link = 'https://www.linkedin.com/jobs/search?keywords=ENTERKEYWORD&location=United%20States&locationId=&geoId=103644278&f_TPR=&f_WT=2&f_SB2=5&position=1&pageNum=0'
    link2 = "https://uk.linkedin.com/jobs/search?keywords=ENTERKEYWORD&location=United%20Kingdom&locationId=&geoId=101165590&f_TPR=&f_WT=2&position=1&pageNum=0"
    linkeden = Linkeden(keywords= keywords ,baseLink=link2 )
    linkeden.scrapeWithoutApplicants()

    # 900  https://www.linkedin.com/jobs/search?keywords=product owner&location=United%20States&locationId=&geoId=103644278&f_TPR=&f_WT=2&f_SB2=5&position=1&pageNum=0