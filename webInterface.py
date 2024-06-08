from flask import Flask,request,send_file
import SearchImage as Search
app = Flask(__name__)
@app.get("/photos")
def helloworld():
    #print(request.get_json())
    #print(Search.DownloadFile(request.get_json()))
    if request.method == 'GET':
        json = request.get_json()
        print(json)
        response = Search.DownloadFile(json)
        
        if response:
            if response["image"] != "":
                return send_file(path_or_file=response["image"],as_attachment='png')
        #result = Search.DownloadFile(queryParameters=queryparameters)
        else:
            return {"nothing":"nothin to show"}


if __name__ == "__main__":
    app.run(debug=True)

     
