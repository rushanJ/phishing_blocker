from flask import Flask
from flask_restful import Api, Resource,reqparse
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
cors = CORS(app, resorces={r'/d/*': {"origins": '*'}})


main_post_args = reqparse.RequestParser()
main_post_args.add_argument('link', type=str, help='Rate cannot be converted')


def addToblocklist(url):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="phishing_protector"
    )

    mycursor = mydb.cursor()

    sql = "INSERT INTO blacklist (url) VALUES ('"+url+"')"

    mycursor.execute(sql)

    mydb.commit()




def scrapingTest(url):
    try:
        source = requests.get(url)
        soup = BeautifulSoup(source.text, 'lxml')
        # print (soup.prettify())
        pageUrl = urlparse(source.url).netloc
        print (pageUrl)
        form = soup.find('form').get('action')
        print (form)
        source1 = requests.post('https://' + pageUrl + '/' + form, data={'userName': ''})
        print (source1.url)
        responseUrl = urlparse(source1.url).netloc
        print (responseUrl)
        print (responseUrl == pageUrl)
        if (responseUrl == pageUrl):
            print("Success")
            return {"data": 'true',"message":"Secure. Happy Surfing "}
        else:
            addToblocklist(url)
            print("Seems Phishing website")
            return {"data": 'false',"message":"Seems Phishing website"}

    except Exception as e:
        addToblocklist(url)
        print(e)
        print("Not Secure")
        return {"data": 'false', "message": "Not Secure"}


def dbCheck(url):
    import mysql.connector

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="phishing_protector"
    )

    mycursor = mydb.cursor()
    print(url)
    mycursor.execute("SELECT * FROM blacklist WHERE `url` LIKE '%"+url+"%'")

    myresult = mycursor.fetchall()

    for x in myresult:
        return 'true'
    return 'false'



class Main(Resource):
    def get(self):
        return {"data" :"HelloWorld"}
    def post(self):
        args = main_post_args.parse_args()
        url=args.link
        print(url)
        if dbCheck(url)== 'true':
            print("Blacklisted")
            return {"data": 'false',"message":"Blacklisted"}
        else:
            return scrapingTest(url)

api.add_resource(Main, "/hello")


if __name__ == "__main__":
	app.run(debug=True)

