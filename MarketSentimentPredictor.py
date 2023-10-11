import datetime
import requests
import tkinter as tk
from tkinter import Listbox, ttk
from textblob import TextBlob


# API key for NewsAPI 
api_key = '<Your API Key>' 

# Store sources 
sources = []

# Tkinter GUI setup
root = tk.Tk()
root.title('Market Sentiment Analyzer')

frame = ttk.Frame(root)
frame.pack(pady=20, padx=20)

title_label = ttk.Label(frame, text="Market Sentiment Analyzer", font=("TkDefaultFont", 16))
title_label.grid(row=0, column=0, columnspan=2)

sentiment_label = ttk.Label(frame, text="Sentiment:")  
sentiment_label.grid(row=1, column=0)

sentiment_display = ttk.Label(frame, text="-", font=("TkDefaultFont", 14))
sentiment_display.grid(row=1, column=1)
 
analysis_button = ttk.Button(frame, text="Analyze Sentiment", command=lambda: analyze())
analysis_button.grid(row=2, column=0, columnspan=2, pady=10)

sources_button = ttk.Button(frame, text="View Sources", command=lambda: show_sources())
sources_button.grid(row=3, column=0) 

# graph_button = ttk.Button(frame, text="Show Graph", command=lambda: show_graph())
# graph_button.grid(row=3, column=0)

refresh_button = ttk.Button(frame, text="Refresh", command=lambda: refresh())
refresh_button.grid(row=3, column=1)

# Function to fetch news articles from NewsAPI
def get_news():
    url = 'https://newsapi.org/v2/everything'
    parameters = {
        'q': 'stock market',
        'language': 'en',
        'apiKey': api_key
    }
    response = requests.get(url, params=parameters)
    return response.json()['articles']

# Function to analyze sentiment of news articles
def analyze_articles(articles):
    positive = 0
    negative = 0
   
    for article in articles:
        text = article['description']
        blob = TextBlob(text)
        sentiment = blob.sentiment.polarity
    
    # Save sources    
    for article in articles:
        sources.append(article['url'])
        
        if sentiment > 0:
            positive += 1
        else:
            negative += 1   
            
    if positive > negative:
        return 'Bullish'
    elif negative > positive:
        return 'Bearish'
    else:
        return 'Neutral'
    
        
def analyze():
    articles = get_news()
    sentiment = analyze_articles(articles)    
    sentiment_display.config(text=sentiment)
    
    # Set sentiment label color
    if sentiment == 'Bullish':
        sentiment_display.config(foreground='green')
    elif sentiment == 'Bearish':
        sentiment_display.config(foreground='red')
    else:   
        sentiment_display.config(foreground='black')
      
# Graphing functions  
# sentiments = []
# dates = []

# def show_graph():
#     plt.plot(dates, sentiments)
#     plt.xlabel('Date')
#     plt.ylabel('Sentiment')
#     plt.title('Market Sentiment')
#     plt.show()
    
# Refresh functions
def refresh():
    global sentiments, dates
    sentiments = []
    dates = []
    
    articles = get_news()
    sentiment = analyze_articles(articles)
    
    today = datetime.datetime.now()
    
    sentiments.append(sentiment)
    dates.append(today)
    
    analyze()

# Sources functions
def show_sources():
    sources_window = tk.Toplevel(root)

    sources_listbox = Listbox(sources_window)
    sources_listbox.place(x=10, y=10, relwidth=1, relheight=1)
    
    for source in sources:
        sources_listbox.insert(tk.END, source)
    sources_window.deiconify()
    
    scrollbar = Scrollbar(sources_window)
    scrollbar.pack(side=RIGHT, fill=Y)

    sources_listbox = Listbox(sources_window, yscrollcommand=scrollbar.set)

    scrollbar.config(command=sources_listbox.yview)

    sources_window.geometry("400x300")
    
    frame = ttk.Frame(sources_window)
    frame.pack(pady=10, padx=10)

    sources_listbox = Listbox(frame)
    sources_listbox.pack(fill=BOTH, expand=1)

root.mainloop()