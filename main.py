from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup as bs
import json
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def root ():
    return """
    <style>
        .center {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 50%;
        }
        body {
        font-family: 'IBM Plex Sans', sans-serif;
        color: white !important;
        background-color: black !important;
        }

        h1 {
        font-family: 'IBM Plex Mono', monospace;
        font-weight: 600 !important;
        text-align: center;
        font-size:5vw !important;
        }

        h2 {
        font-family: 'IBM Plex Mono', monospace;
        font-weight: 600 !important;
        text-align: center;
        font-size:3vw;
        }

        a {
        color: #46b966;
        text-decoration: none !important;
        }

        a:hover {
        color: #17B2B5 !important;
        }

        .logoPic {
        width: 70%;
        margin: auto;
        display: block;
        }

        .header {
        background-color: #0e2f44;
        }

        ul {
        display: table;
        margin: 0 auto;
        }
    </style>
    <h1>Smogon API</h1>
    <p>
    <image src="https://www.dropbox.com/s/u4ognce7sevfkgx/smogonBanner.png?dl=1" style="width:600px;height:150px;" class="center"></image><br />
    Welcome to the Smogon API Project! This project is aimed at allowing developers 
    to access all of the data on <a href="https://smogon.com">Smogon</a> using API-style endpoints, in order
    to perform analysis or present different views. 
    </p>
    <p> You can find a list of the different endpoints that we have <a href="/docs">here</a>. 
    """

@app.get("/charizard")
def getCharizard():
    url = "https://www.smogon.com/dex/sm/pokemon/charizard"
    urlPage = requests.get(url)
    soup = bs(urlPage.content, 'html.parser')

    script = soup.find_all("script")[1]
    script_insides = bs(script.text)
    smogon_html = script_insides.find("p").text
    first_overview = smogon_html.split("<\\/p>")[0].replace("<\\/a>", "")
    return {"overview": first_overview}

@app.get("/firstOverview")
def getFirstOverview(pokemonName):
    url = "https://www.smogon.com/dex/sm/pokemon/" + pokemonName.lower()
    urlPage = requests.get(url)
    soup = bs(urlPage.content, 'html.parser')

    script = soup.find_all("script")[1]
    script_insides = bs(script.text)
    smogon_html = script_insides.find("p").text
    first_overview = smogon_html.split("<\\/p>")[0].replace("<\\/a>", "")
    return {"overview": first_overview}

@app.get("/getJSONGen7")
def getJSON(pokemonName):
    url = "https://www.smogon.com/dex/sm/pokemon/" + pokemonName.lower()
    urlPage = requests.get(url)
    soup = bs(urlPage.content, 'html.parser')

    script = soup.find_all("script")[1]
    script_insides = script.text
    return json.loads(script_insides.replace("dexSettings = ", "").strip())['injectRpcs'][2][1]

@app.get("/getJSONGen8")
def getJSON(pokemonName):
    url = "https://www.smogon.com/dex/ss/pokemon/" + pokemonName.lower()
    urlPage = requests.get(url)
    soup = bs(urlPage.content, 'html.parser')

    script = soup.find_all("script")[1]
    script_insides = script.text
    return json.loads(script_insides.replace("dexSettings = ", "").strip())['injectRpcs'][2][1]

@app.get("/getGen7Data")
def getPokemonData():
    url = "https://www.smogon.com/dex/sm/pokemon/charizard"
    urlPage = requests.get(url)
    soup = bs(urlPage.content, 'html.parser')

    script = soup.find_all("script")[1]
    script_insides = script.text
    return json.loads(script_insides.replace("dexSettings = ", "").strip())['injectRpcs'][1][1]