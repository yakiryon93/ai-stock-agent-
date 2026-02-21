import yfinance as yf
import google.generativeai as genai
import json
from datetime import datetime
import os

API_KEY = os.environ.get("GEMINI_API_KEY") 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')
TICKERS_TO_SCAN = ['AAPL', 'MSFT', 'TSLA', 'NVDA', 'AMD']

def run_agent():
    final_results = []
    for ticker in TICKERS_TO_SCAN:
        try:
            data = yf.download(ticker, period="6mo", progress=False)
            if data.empty: continue
            
            data['SMA_20'] = data['Close'].rolling(window=20).mean()
            data['STD_20'] = data['Close'].rolling(window=20).std()
            data['Band_Width'] = (data['SMA_20'] + (data['STD_20'] * 2) - (data['SMA_20'] - (data['STD_20'] * 2))) / data['SMA_20']
            data['Volume_SMA_20'] = data['Volume'].rolling(window=20).mean()
            
            latest = data.iloc[-1]
            if latest['Band_Width'] < 0.05 and latest['Volume'] > (latest['Volume_SMA_20'] * 1.5):
                news = "\n- ".join([item['title'] for item in yf.Ticker(ticker).news[:5]])
                resp = model.generate_content(f"מנתח פיננסי. כותרות {ticker}:\n{news}\nהחזר בדיוק 2 שורות:\nסנטימנט: [חיובי/שלילי/מעורב]\nהסבר: [משפט קצר בעברית]")
                text = resp.text.strip().split('\n')
                
                final_results.append({
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "ticker": ticker,
                    "price": round(float(latest['Close']), 2),
                    "ai_sentiment": text[0].replace("סנטימנט:", "").strip() if len(text)>0 else "לא ידוע",
                    "ai_reasoning": text[1].replace("הסבר:", "").strip() if len(text)>1 else "אין הסבר"
                })
        except:
            pass
            
    with open('agent_memory.json', 'w', encoding='utf-8') as f:
        json.dump(final_results, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    run_agent()
