import urllib
import urllib.request
from bs4 import BeautifulSoup
import random, uuid
import sys, time, os
from SearchEnginesParameters import *
import psycopg2
from dotenv import load_dotenv
import json

BARSIZE = 10

FILELOCATION = os.path.abspath(os.path.dirname(__name__)) + '\\Download'

def createsURL(Json:dict[str:any])-> dict[str:any]:
    ignoredParameters = {}
    random.seed()
    
    while(True):
        number = random.randint(0,300)
        if number % 20 == 0:
            break
    
    if(Json["searchEngine"] == "google"):
        SearchEngine = SEARCH_ENGINES[Json["searchEngine"]]
        query = Json.pop("query","")
        if query != "":
            query = inputData(query)
                    
        epq = Json.pop("epq","")
        if epq != "":
            epq = inputData(epq)
            
        oq = Json.pop("oq","")
        if oq != "":
            oq = inputData(oq)
            
        eq = Json.pop("eq","")
        if eq != "":
            eq = inputData(eq)
            
        searcLink = SearchEngine + "&"+"q="+ query +"&"+"epq="+epq+"&"+"oq="+oq+"&"+"eq="+eq + "&" + str(number)
        
        # image size
        imgz = Json.pop("imgsz","")
        if imgz not in GOOGLE_IMAGES_SIZES and  imgz != "": 
            ignoredParameters.update({"ImageSizeNotFound":imgz})
        else:
            searcLink = searcLink + "&" + "imgsz=" + imgz
        
        #image porportion
        imgar = Json.pop("imgar","")
        if imgar not in GOOGLE_IMAGES_PROPRORTIONS and imgar != "": 
            ignoredParameters.update({"ImageProportionNotFound":imgar})
        else:
            searcLink = searcLink + "&" + "imgar=" + imgar
                
        #image color
        imgcolor = Json.pop("imgcolor","")
        if imgcolor not in GOOGLE_IMAGES_COLORS and imgcolor != "": 
            ignoredParameters.update({"ImageColorNotFound":imgcolor})
        else:
            searcLink = searcLink + "&" + "imgcolor=" + imgcolor
        
        #image type
        imgtype = Json.pop("imgtype","")
        if imgtype not in GOOGLE_IMAGES_TYPES and imgtype != "": 
            ignoredParameters.update({"ImageTypeNotfound":imgtype})
        else:
            searcLink = searcLink + "&" + "imgtype=" + imgtype
                
        #image color
        filetype = Json.pop("filetype","")
        if filetype not in GOOGLE_FILE_TYPES and filetype != "": 
            ignoredParameters.update({"ImageFileTypeNotFound":filetype})
        else:
            searcLink = searcLink + "&" + "filetype=" + filetype
        
        sitesearch = Json.pop("sitesearch","")
        if sitesearch:
            searcLink = searcLink + "&" + "site=" + Json["sitesearch"]   
            
        return {"url":searcLink,
                "ignoredParameters": ignoredParameters}

def creatJsonFromList(listImages: list[str])-> dict[str:str]:
    # creates a unic id to the search
    idOfSearch = str(uuid.uuid4())
    response = {}
    response['id'] = idOfSearch
    response['imagesLinks'] = {}
    for index,link in enumerate(listImages):
        response["imagesLinks"].update({f"image-{index}":link})   
    
    return response   
    
def downloadImage(Json:dict[int:str],quantidade: int)-> dict[str:str]:
    """ download a src image usin the request function

    Args:
        listImages (list[str]): a list of validates links
    """
    listImages = list(Json.values())
    
    if quantidade < 0:
        quantidade = 1
    elif quantidade > 20:
        quantidade = 20
        
    downloaded = []
    contador = 0
    return_ = {}
    
    while contador < quantidade:
        choice = random.choice(listImages)
        if choice not in downloaded:
            downloaded.append(choice)
            filename = str(uuid.uuid4()) + ".png"
            with urllib.request.urlopen(choice) as response:
                data = response.read()
                with open(file=os.path.join(FILELOCATION,filename),mode='wb') as photo:
                    photo.write(data)
            
                return_.update({f"image{contador}" : os.path.join(FILELOCATION,filename)})
                contador = contador + 1 
            
    return return_ 

def getSearcFromDatabase(uuid: str) -> dict[str:str]:
    load_dotenv()
    conn = psycopg2.connect(f"dbname=Image user=postgres password={os.getenv("DATABASE_PASSWORD")}")
    
    cursor = conn.cursor()
    cursor.execute(f"select responseterm from searchedimages where id = \'{uuid}\' ")
    response = cursor.fetchall() 
    conn.close()
    
    return response[0][0]

def gettinDataFromBrowser(url: str):  
    with urllib.request.urlopen(url=url['url']) as response:
        return response.read()
     
def inputData(termos: str)-> str:
    terms = termos.split(' ')    
    terms = [term for term in terms if term != '']
    SearchString = '+'.join(str(term) for term in terms)
    return SearchString

def progressBar(downloaded: int, totalFile: int, phase: str):
    progress = int(downloaded*BARSIZE/totalFile)
    completed = str(int(downloaded*100/totalFile)) + '%'
    exit = f"[{'.'*progress}{completed}{'.'*((BARSIZE)-progress)}]{str(downloaded)}/{str(totalFile)} - {phase}"
    sys.stdout.write(exit + '\r')
    sys.stdout.flush()   

def treatingContent(HTMLContent: bytes) -> list:
    content = BeautifulSoup(HTMLContent,"html.parser")
    saida = content.find(class_="GpQGbf")
    saida = saida.find_all('img')
    links = []
    for image in saida:
        links.append(image["src"])
    
    return links
    
def saveSearchInDatabase(EntryJson: dict[str:str],response: dict[str:str])->None:
    load_dotenv()
    conn = psycopg2.connect(f"dbname=Image user=postgres password={os.getenv("DATABASE_PASSWORD")}")
    
    cursor = conn.cursor()
    cursor.execute("INSERT INTO searchedImages (id,searchedTerm, responseTerm,ignoredParameters) VALUES (%s, %s,%s,%s)",(response["id"],json.dumps(EntryJson),json.dumps(response["imagesLinks"]),json.dumps(response["ignored"])))
    conn.commit()
    conn.close()
    
def ValidJson(Json: dict[str:any]) -> bool:
    query = Json.pop("query",False)
    epq = Json.pop("epq",False)
    oq = Json.pop("oq",False)
    if not(query or epq or oq):
        print("nenhum parametro passado")
        return False
    
    if Json["searchEngine"] not in SEARCH_ENGINES:
        return False
    
    return True

def searchImage(json: dict[str:str]) -> dict[str:str]:
    
    if ValidJson(json.copy()):
        
        if json.copy().pop("id",False):
            return getSearcFromDatabase(json["id"])
        else:
            response = createsURL(Json=json.copy())
            HTML = gettinDataFromBrowser(url=response)
            result = treatingContent(HTMLContent=HTML)
            responseJson =creatJsonFromList(result)
            responseJson.update({"ignored":response["ignoredParameters"]})
            saveSearchInDatabase(json,responseJson)
            return responseJson
    else:
        return {}
    
def main() -> None:
    """main function
    """
    
    # a test of an search
    term = {
    "searchEngine":"google",
    "query":"pacote de arroz 5kg",
    "quantity": 1,
    }

    response = searchImage(term)
    print(response)
    downloadImage(response["imagesLinks"],5)
    
if __name__ == "__main__":
    main()