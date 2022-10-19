import psycopg2
from flask import Flask, request
import requests

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def form_example():
    if request.method == 'POST':
        film_title = request.form.get('film_title')
        url = "https://imdb8.p.rapidapi.com/auto-complete"

        querystring = {"q":film_title}

        headers = {
            "X-RapidAPI-Key": "62008096b2mshfb208128fa454d7p14c074jsne7881457ef9a",
            "X-RapidAPI-Host": "imdb8.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        title = response.json()["d"][0]["l"]
        year = response.json()["d"][0]["y"]
        cast = response.json()["d"][0]["s"]
        title1 = response.json()["d"][1]["l"]
        year1 = response.json()["d"][1]["y"]
        cast1 = response.json()["d"][1]["s"]
        title2 = response.json()["d"][2]["l"]
        year2 = response.json()["d"][2]["y"]
        cast2 = response.json()["d"][2]["s"]
        title = title.replace('\'', '')
        cast = cast.replace('\'', '')
        year = str(year)
        title1 = title1.replace('\'', '')
        cast1 = cast1.replace('\'', '')
        year1 = str(year1)
        title2 = title2.replace('\'', '')
        cast2 = cast2.replace('\'', '')
        year2 = str(year2)

        con = psycopg2.connect(
            database="flask",
            user="postgres",
            password="ad1"
        )
        con.autocommit = True

        cur = con.cursor()

        cur.execute(f"INSERT INTO rooms (film_name, year, actors) VALUES (\'{title}\', \'{year}\', \'{cast}\');")
        cur.execute(f"INSERT INTO rooms (film_name, year, actors) VALUES (\'{title1}\', \'{year1}\', \'{cast1}\');")
        cur.execute(f"INSERT INTO rooms (film_name, year, actors) VALUES (\'{title2}\', \'{year2}\', \'{cast2}\');")

        cur.close()
        con.close()
        return '''
                  <h1 style="text-align:center">Movie searcher. Know your film!</h1>
                  <h2>Film is: {}, {}</h2>
                  <h3>Cast: {}</h3>
                  <h2>Film is: {}, {}</h2>
                  <h3>Cast: {}</h3>
                  <h2>Film is: {}, {}</h2>
                  <h3>Cast: {}</h3>'''.format(title, year, cast, title1, year1, cast1, title2, year2, cast2)

    return '''
              <form method="POST">
                  <h1 style="text-align:center">Movie searcher. Know your film!</h1>
                  <div><label>Film title: <input type="text" name="film_title"></label></div>
                  <input type="submit" value="Submit">
              </form>'''

if __name__ == '__main__':
    app.run(debug=True, port=3000, host="127.0.0.1") #
