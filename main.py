from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import getpass

import os 
import sys
from time import sleep

FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(FOLDER_PATH, "lib"))
CHROME_DRIVER = FOLDER_PATH + r'\chromedriver.exe'

OPTIONS = ChromeOptions()
OPTIONS.headless = False
OPTIONS.add_argument("user-data-dir=C:\\Users\\"+getpass.getuser()+"\\AppData\\Local\\Google\\Chrome\\User Data")
OPTIONS.add_experimental_option('excludeSwitches', ['enable-logging'])

class Instagram:

    def __init__(self):
        while True:
            try:
                self.browser = self.instagram_login()
                break
            except:
                try:
                    self.browser.quit()
                    sleep(3)
                    self.browser = self.instagram_login()
                    break
                except:
                    self.browser.quit()
                    print("Não foi possível localizar os elementos")
            
    def instagram_login(self):

        url = "https://www.instagram.com/"
        self.browser = Chrome(executable_path=CHROME_DRIVER, options=OPTIONS)
        self.browser.get(url)
        return self.browser

    def posts_url(self, username, quantity):

        """With the input of an account page, scrape the 25 most recent posts urls"""
        instagram_url = "https://www.instagram.com/" + username + "/"
        self.browser.get(instagram_url)
        post = 'https://www.instagram.com/p/'

        post_links = []
        total_quantity = 0
        while len(post_links) < quantity:
            links = [a.get_attribute('href') for a in self.browser.find_elements_by_tag_name('a')]
            for link in links:
                if post in link and link not in post_links:
                    post_links.append(link)
            scroll_down = "window.scrollTo(0, document.body.scrollHeight);"
            self.browser.execute_script(scroll_down)
            sleep(10)
            total_quantity += 1
            if total_quantity != len(post_links):
                break

        return post_links[:quantity]

    def post_number_likes(self, url):
        instagram_url = 'https://www.instagram.com'

        likes = []
        comments = []
        for links in url:
            self.browser.get(links)

            post_ref = links[len(instagram_url):]

            LIKES_HREF = f'//a[@href="{post_ref}liked_by/"]/span'
            LIKES_CLASS = f'//span[@class="vcOH2"]/span'

            sleep(3)
            try:
                number_of_likes = self.browser.find_element_by_xpath(LIKES_HREF).text
            except:
                number_of_likes = self.browser.find_element_by_xpath(LIKES_CLASS).text
            if "." in number_of_likes:
                number_of_likes = number_of_likes.replace(".", "")

            number_of_likes = int(number_of_likes)
            likes.append(number_of_likes)

            COMMENTS_HREF = f"//*[local-name()='svg' and @aria-label='Carregar mais comentários']"

            for comment_button in range(20):
                try:
                    self.browser.find_element_by_xpath(COMMENTS_HREF).click()
                    sleep(1)
                except:
                    continue

            html = self.browser.page_source
            soup = BeautifulSoup(html, 'html.parser')
            number_of_comments = soup.find_all(class_="Mr508")
            number_of_answers = soup.find_all(class_="EizgU")

            for answer in range(len(number_of_answers)):
                number_of_answers[answer] = str(number_of_answers[answer])
                answer_text = '<span class="EizgU">Ver respostas ('

                number_of_answers[answer] = number_of_answers[answer][len(answer_text):len(answer_text) + 1]
                if "." in number_of_answers[answer]:
                    number_of_answers[answer] = number_of_answers[answer].replace(".", "")

                try:    
                    number_of_answers[answer] = int(number_of_answers[answer])
                except:
                    number_of_answers[answer] = 0

                
            number_of_answers = sum(number_of_answers)             
            number_of_comments = len(number_of_comments)
            total_comments = number_of_comments + number_of_answers
            comments.append(total_comments)

        engagement = {"likes": likes, "comments": comments}

        return engagement

        

if __name__ == "__main__":

    instagram = Instagram()
    posts = instagram.posts_url("google", 2)
    engagement = instagram.post_number_likes(posts)
    likes = engagement["likes"]
    comments = engagement["comments"]
    print(f'posts: {posts}')
    print(f'likes: {likes}')
    print(f'comments: {comments}')


    


