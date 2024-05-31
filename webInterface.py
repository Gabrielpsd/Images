from flask import Flask,request,send_file
import SearchImage as Search
app = Flask(__name__)
@app.get("/photos/<queryparameters>")
def helloworld(queryparameters):
    if request.method == 'GET':
        result = Search.DownloadFile(queryParameters=queryparameters)
        return send_file(path_or_file=result,as_attachment='png')


if __name__ == "__main__":
    app.run(debug=True)

     
