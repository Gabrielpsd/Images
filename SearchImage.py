import urllib
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import random, uuid
import sys, time, os
from SearchEnginesParameters import *

#https://yandex.com
header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
}

BARSIZE = 10

FILELOCATION = os.path.abspath(os.path.dirname(__name__)) + '\\Download'

def createsURL(Json:dict[str:any])-> dict[str:any]:
    print(Json)
    ignoredParameters = {}
    
    if(Json["searchEngine"] == "google"):
        SearchEngine = SEARCH_ENGINES[Json["searchEngine"]]
        searcLink = SearchEngine + "&"+"q="+ Json["query"] +"&"+"epq="+Json["epq"]+"&"+"oq="+Json["oq"]+"&"+"eq="+Json["eq"]
        
        # image size
        if Json["imgsz"] not in GOOGLE_IMAGES_SIZES and Json["imgsz"] != "": 
            ignoredParameters.update({"ImageSizeNotFound":Json["imgsz"]})
        else:
            if Json["imgsz"] != "":
                searcLink = searcLink + "&" + "imgsz=" + Json["imgsz"]
        
        #image porportion
        if Json["imgar"] not in GOOGLE_IMAGES_PROPRORTIONS and Json["imgar"] != "": 
            ignoredParameters.update({"ImageProportionNotFound":Json["imgar"]})
        else:
            if Json["imgar"] != "":
                searcLink = searcLink + "&" + "imgar=" + Json["imgar"]
                
        #image color
        if Json["imgcolor"] not in GOOGLE_IMAGES_COLORS and Json["imgcolor"] != "": 
            ignoredParameters.update({"ImageColorNotFound":Json["imgcolor"]})
        else:
            if Json["imgcolor"] != "":
                searcLink = searcLink + "&" + "imgcolor=" + Json["imgcolor"]
        
        #image type
        if Json["imgtype"] not in GOOGLE_IMAGES_TYPES and Json["imgtype"] != "": 
            ignoredParameters.update({"ImageTypeNotfound":Json["imgtype"]})
        else:
            if Json["imgtype"] != "":
                searcLink = searcLink + "&" + "imgtype=" + Json["imgtype"]
                
        #image color
        if Json["filetype"] not in GOOGLE_FILE_TYPES and Json["filetype"] != "": 
            ignoredParameters.update({"ImageFileTypeNotFound":Json["filetype"]})
        else:
            if Json["filetype"] != "":
                searcLink = searcLink + "&" + "filetype=" + Json["filetype"]
                
        if Json["sitesearch"]:
            searcLink = searcLink + "&" + "site=" + Json["sitesearch"]   
            
        return {"url":searcLink,
                "ignoredParameters": ignoredParameters}

def downloadImage(listImages: list[str])-> str:
    """ download a src image usin the request function

    Args:
        listImages (list[str]): a list of validates links
    """
    choice = random.choice(listImages)
    filename = str(uuid.uuid4()) + ".png"
    with urllib.request.urlopen(choice) as response:
        data = response.read()
        with open(file=os.path.join(FILELOCATION,filename),mode='wb') as photo:
            photo.write(data)
            
    return os.path.join(FILELOCATION,filename)
    
def gettinDataFromBrowser(url: str):  
    option = Options()
    option.add_argument("--headless")
    driver = webdriver.Chrome(options=option)
    
    #Navigate to Google Images
    driver.get(url)
    
    driver.implicitly_wait(10)
    
    """  for link in links:
        print(link.get_attribute('href')) """
        
    html = driver.page_source
    
    driver.quit()
    
    return html
    
def inputData()-> str:
    """ this function gets the terms to be searched and formates to the "q" google url parameter

    Returns:
        str: search term to be used in "q" parameter
    """
    terms = input("Digite o(s) termo(s) a ser buscado:").split(' ')
    
    terms = [term for term in terms if term != '']
    
    SearchString = '+'.join(str(term) for term in terms)
    
    return SearchString


def treatingContent(HTMLContent: bytes) -> list:
    """
        Receives a HTML collected by the selenium request
        
        return:
        list: a list with links to acess directly a image
        
    """
    content = BeautifulSoup(HTMLContent,"html.parser")

    saida = content.find(id="rcnt")
        
    saida = saida.find_all('img')
    
    
    links = []
    
    for image in saida:
        
        if(image["alt"] != ""):
            if not 'gif' in image["src"]:
                links.append(image["src"])
    
    return links
    
def progressBar(downloaded: int, totalFile: int, phase: str):
    """ this is a funtion that print a progress bar in 

    Args:
        downloaded (int): bytes donloaded 
        totalFile (int): total of bytes to be downloaded
    """
    progress = int(downloaded*BARSIZE/totalFile)
    completed = str(int(downloaded*100/totalFile)) + '%'
    # exit =  str(f''[',chr(9608)*progress,' ',completed, '.'*(BARSIZE),']',str(downloaded)+'/'+str(totalFile)')
    exit = f"[{'.'*progress}{completed}{'.'*((BARSIZE)-progress)}]{str(downloaded)}/{str(totalFile)} - {phase}"
    sys.stdout.write(exit + '\r')
    sys.stdout.flush()   
    

def DownloadFile(Json: dict[str:any]): 
    #print("dentro da função: ",Json)
    if ValidJson(Json):
        response = createsURL(Json)
        HTML = gettinDataFromBrowser(url=response["url"])
        result = treatingContent(HTMLContent=HTML)
        filename = downloadImage(result)
        response.update({"Image":filename})
        return response
    else:
        #print("Nenhum parametro de busca foi passado")
        return {}

def ValidJson(Json: dict[str:any]) -> bool:
    if not (Json["epq"]) and not (Json["oq"]) and not (Json["query"]):
        print("nenhum parametro passado")
        return False
    if Json["searchEngine"] not in SEARCH_ENGINES:
        return False
    
    return True

def main() -> None:
    """main function
    """
    
    term:str 
    
    term = inputData()
    time.sleep(2)
    progressBar(0,5,"Criando URL")
    time.sleep(2)
    url = createsURL(terms=term)
    progressBar(1,5,"URL Criada")
    time.sleep(2)
    progressBar(2,5,"Realizando busca no Browser")
    HTML = gettinDataFromBrowser(url=url)
    progressBar(3,5,"Tratando conteudo")
    result = treatingContent(HTMLContent=HTML)
    progressBar(4,5,"Baixando imagem             ")
    filename =downloadImage(result)
    progressBar(5,5,"Imagem Baixada: ")
    print()
    print("Nome do arquivo: ",filename)
    
if __name__ == "__main__":
    main()