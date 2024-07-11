from typing import Union
from urllib.error import HTTPError

from fastapi import FastAPI
import requests
from supabase import create_client, Client
from fastapi.middleware.cors import CORSMiddleware

url: str = "https://npqayqwogunposokodnt.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5wcWF5cXdvZ3VucG9zb2tvZG50Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjA2MjUwNzIsImV4cCI6MjAzNjIwMTA3Mn0.-me0gZbLTnwWKJ-FYoacdsdSMg-qD1HzPCYW1SZiGLs"
supabase: Client = create_client(url, key)

app = FastAPI()


origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = "DA3YZV066VHJK8GG"

@app.get("/")
def read_root():


    # Step 1: 
    response = supabase.table("stocks").select("*").eq("symbol","IBM").execute()

    if not response.data:
        try:
            url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo"
            response = requests.get(url)
            print(response)
            response.raise_for_status()
            if response.status_code == 200:
                tickers = response.json()
                add_stock_to_db = (supabase.table("stocks").insert({"symbol": "IBM"}).execute())
                stock_id_db = add_stock_to_db.data[0]["stock_id"]         
                print(stock_id_db)       
                if tickers["Time Series (Daily)"]:
                    data = tickers["Time Series (Daily)"]
                    date_range_data = []
                    for key in data:
                        stock_values = data[key]
                        open = stock_values["1. open"]
                        high = stock_values["2. high"]
                        low = stock_values["3. low"]
                        close = stock_values["4. close"]
                        volume = stock_values["5. volume"]
                        object = {"open": open, "high": high, "low":low, "volume":volume, "close":close, "date": key, "stock_id": stock_id_db}
                        # print(key, object)
                        date_range_data.append(object.copy())
                print("Adding data", date_range_data)
                add_stocks =  (supabase.table("stock_prices").insert(date_range_data).execute())
                return "Success"

        except Exception as exception:
            raise SystemExit(exception)
        
        else:
            return "Stock already exists"
            
        # data = data["Time Series (Daily)"]


  
    return response


@app.get("/get-ticker")
def read_item(ticker = None, from_date = None, to_date = None):
    ticker_id = supabase.table("stocks").select("*").eq("symbol",ticker).execute()
    if ticker_id.data:

        stock_id = ticker_id.data[0]["stock_id"]
        print(from_date, to_date)
        stock_data = supabase.table("stock_prices").select("*").eq("stock_id",stock_id).gte("date",from_date).lte("date", to_date).execute()
        return stock_data

    
    else: 
        return "Unable to find stock"


