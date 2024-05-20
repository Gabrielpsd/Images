from serpapi import GoogleSearch
import requests
import configparser

def loadKey() -> str:
    """ load the api key

    Returns:
        str: ApiKey
    """
    confiParser = configparser.ConfigParser()
    confiParser.read("CONFIG.INI")
    
    return confiParser["API"]["APIKEY"]
    
def main():
    
    text: str = input("Digite um termo a ser buscado: ")
    ApiKey:str = loadKey()
    
    params = {
    "engine": "google_images",
    "q": text,
    "location": "Austin, TX, Texas, United States",
    "api_key": ApiKey
    }

    results: dict[any:any] = searcImage(params)
    
    firstImage:dict[any:any] = results["images_results"][0]
    linkToImage:str = firstImage.get('original')
    
    downloadImage(link=linkToImage)
    
    print("Imagem baixada")

def downloadImage(link: str) -> None:
    """
        Save the image in the Download path, the folder must exists where th program is called
    """
    request = requests.get(link)
    with open('Download\\image.jpg','wb') as f:
        f.write(request.content)
    
def searcImage(search: dict[any:any]) -> dict:
    """ searches the image in the Serapi Google search

    Args:
        search (_type_): A dict that contain the content to be searched

    Returns:
        dict: returns a dict with all the data that the api returns 
    """
    
    search = GoogleSearch(search)
    return search.get_dict()
    

if __name__== "__main__":
    main()