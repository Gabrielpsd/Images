import urllib
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import random, uuid
import base64

option = Options()
option.add_argument("--headless")
driver = webdriver.Chrome(options=option)

#https://yandex.com
header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
}

def createsURL(terms:str)-> str:
    return f"https://www.google.com/search?q={terms}&imgsz=vga&filetype=png&udm=2"
    #return f"https://yandex.com/images/search?text={terms}&itype=jpeg"

def downloadImage(listImages: list[str]):
    
    choice = random.choice(listImages)
    print(choice)
    filename = str(uuid.uuid4()) + ".png"
    print(filename)
    with urllib.request.urlopen(choice) as response:
        data = response.read()
        with open(file=filename,mode='wb') as photo:
            photo.write(data)
    
def gettinDataFromBrowser(url: str):  
    
    #Navigate to Google Images
    driver.get(url)
    
    
    # Going into search bar and input the search query
    """ search_box = driver.find_element(By.NAME,"q")
    search_box.send_keys(terms)
    search_box.submit()
     """
    #setting a waiting to the submit
    driver.implicitly_wait(10)
    
    # Find all <a> elements with href containing "/imgres" - images result links
    #links = driver.find_elements(By.XPATH, "//a[contains(@href,'imgres')]")
    
    #print(driver.page_source)
    
    #print the links
    """  for link in links:
        print(link.get_attribute('href')) """
        
    html = driver.page_source
        
    # print(html)
    
    driver.quit()
    
    return html
    
def inputData()-> str:
    """ this function gets the terms to be searched and formates to the "q" google url parameter

    Returns:
        str: search term to be used in "q" parameter
    """
    terms = input("Digite o(s) termo(s) a ser buscado:").split(' ')
    
    terms = [term for term in terms if term != '']

    #print(terms) depuration
    
    SearchString = '+'.join(str(term) for term in terms)
    
    #print(SearchString) depuration  
    return SearchString


def treatingContent(HTMLContent: bytes) -> list:
    """
        Receives a HTML collected by the selenium request
        
        return:
        list: a list with links to acess directly a image
        
    """
    content = BeautifulSoup(HTMLContent,"html.parser")

    #print(content.find(id="main").prettify())
    saida = content.find(id="rcnt")
        
    saida = saida.find_all('img')
    
    # print(saida)
    
    links = []
    
    for image in saida:
        #print(image["src"])
        #print(image["width"])
        #print(image["height"])
        #width = int(image["width"])
        #height = int(image["height"])
        
        if(image["alt"] != ""):
            if not 'gif' in image["src"]:
                links.append(image["src"])
            
    """ for result in saida.find_all("div",attrs={"data-attrid":"images universal"}):
        
        print(result.prettify()) """
    
    return links
    
def main() -> None:
    """main function
    """
    
    term:str 
    
    term = inputData()
    url = createsURL(terms=term)
    print("URL criada: ",url)
    print("Realizando busca no browser")
    HTML = gettinDataFromBrowser(url=url)
    print("Tratando do conteudo ")
    result = treatingContent(HTMLContent=HTML)
    print("Baixando imagem")
    downloadImage(result)
    
if __name__ == "__main__":
    main()