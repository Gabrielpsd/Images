import requests
from bs4 import BeautifulSoup

#https://yandex.com
header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
}

def createsURL(terms:str)-> str:
    #return f"https://www.google.com/search?q={terms}&udm=2"
    return f"https://yandex.com/images/search?text={terms}&itype=jpeg"
    
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

def requestGoogleSearch(url:str, header: dict[str:str]) -> bytes:
    response = requests.get(url,headers=header)
    #print(response.content) Depuration mode
    return response.content

def treatingContent(HTMLContent: bytes):
    content = BeautifulSoup(HTMLContent,"html.parser")

    print(content)
    
    for result in content.find_all("div",attrs={"class":"ContentImage"}):
        link = result.descendants
        
        print(link)
        
        for a in link:
            print(a)
            
        print(result)
    
def main() -> None:
    """main function
    """
    
    term:str 
    
    term = inputData()
    url = createsURL(term)
    print(url)
    response = requestGoogleSearch(url, header=header)
    treatingContent(response)
    
if __name__ == "__main__":
    main()