# ============================================
# CRYPTO FETCHER - Kripto Veri Çekme
# ============================================
# BTC, SOL, ETH ve diğer kripto verilerini çeker

import yfinance as yf
from typing import Dict, List
from datetime import datetime

# Desteklenen kripto paralar
SUPPORTED_CRYPTOS = {
    "BTC": {"symbol": "BTC-USD", "name": "Bitcoin", "emoji": "₿"},
    "SOL": {"symbol": "SOL-USD", "name": "Solana", "emoji": "◎"},
    "ETH": {"symbol": "ETH-USD", "name": "Ethereum", "emoji": "Ξ"},
    "XRP": {"symbol": "XRP-USD", "name": "Ripple", "emoji": "✕"},
    "BNB": {"symbol": "BNB-USD", "name": "Binance Coin", "emoji": "🔶"},
    "ADA": {"symbol": "ADA-USD", "name": "Cardano", "emoji": "🔵"},
    "DOGE": {"symbol": "DOGE-USD", "name": "Dogecoin", "emoji": "🐕"},
    "AVAX": {"symbol": "AVAX-USD", "name": "Avalanche", "emoji": "🔺"},
}


def get_crypto_candles(crypto: str = "BTC", hours: int = 24, interval: str = "1h") -> Dict:
    """
    Kripto para için mum verisi çeker.
    
    Parameters:
    -----------
    crypto : str
        Kripto kodu: BTC, SOL, ETH, XRP, BNB, ADA, DOGE, AVAX
    hours : int
        Kaç saatlik veri
    interval : str
        Mum zaman dilimi: 1h, 4h, 1d
    
    Returns:
    --------
    Dict : Mum verileri ve analiz
    """
    crypto = crypto.upper()
    
    if crypto not in SUPPORTED_CRYPTOS:
        return {
            "success": False,
            "error": f"Desteklenmeyen kripto: {crypto}",
            "supported": list(SUPPORTED_CRYPTOS.keys())
        }
    
    crypto_info = SUPPORTED_CRYPTOS[crypto]
    symbol = crypto_info["symbol"]
    
    try:
        ticker = yf.Ticker(symbol)
        
        # Yeterli veri için daha fazla gün çek
        period = "5d" if hours <= 48 else "10d"
        df = ticker.history(period=period, interval=interval)
        
        if df.empty:
            return {"success": False, "error": "Veri alınamadı"}
        
        # Son X saatlik veriyi al
        df = df.tail(hours)
        
        # Mum listesi oluştur
        candles = []
        for idx, row in df.iterrows():
            timestamp = idx.strftime("%Y-%m-%d %H:%M") if hasattr(idx, 'strftime') else str(idx)
            
            open_price = row['Open']
            close_price = row['Close']
            high_price = row['High']
            low_price = row['Low']
            volume = row['Volume']
            
            # Mum tipi
            if close_price > open_price:
                candle_type = "YESIL"
                emoji = "🟢"
            elif close_price < open_price:
                candle_type = "KIRMIZI"
                emoji = "🔴"
            else:
                candle_type = "DOJI"
                emoji = "⚪"
            
            change_percent = ((close_price - open_price) / open_price) * 100
            
            candles.append({
                "timestamp": timestamp,
                "open": round(open_price, 4),
                "high": round(high_price, 4),
                "low": round(low_price, 4),
                "close": round(close_price, 4),
                "volume": round(volume, 2),
                "type": candle_type,
                "emoji": emoji,
                "change_percent": round(change_percent, 2)
            })
        
        # İstatistikler
        if candles:
            total_green = sum(1 for c in candles if c['type'] == "YESIL")
            total_red = sum(1 for c in candles if c['type'] == "KIRMIZI")
            
            first_open = candles[0]['open']
            last_close = candles[-1]['close']
            total_change = ((last_close - first_open) / first_open) * 100
            
            highest = max(c['high'] for c in candles)
            lowest = min(c['low'] for c in candles)
            
            if total_green > total_red:
                trend = "YUKARI"
                trend_emoji = "📈"
            elif total_red > total_green:
                trend = "ASAGI"
                trend_emoji = "📉"
            else:
                trend = "YATAY"
                trend_emoji = "➡️"
            
            summary = {
                "trend": trend,
                "trend_emoji": trend_emoji,
                "total_change_percent": round(total_change, 2),
                "green_candles": total_green,
                "red_candles": total_red,
                "highest_price": highest,
                "lowest_price": lowest,
                "current_price": last_close
            }
        else:
            summary = {}
        
        return {
            "success": True,
            "crypto": crypto,
            "name": crypto_info["name"],
            "emoji": crypto_info["emoji"],
            "symbol": symbol,
            "interval": interval,
            "period_hours": hours,
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "summary": summary,
            "candles": candles
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "crypto": crypto
        }


def get_multi_crypto_summary() -> Dict:
    """
    Birden fazla kripto için özet bilgi döndürür.
    """
    results = {}
    
    for crypto in ["BTC", "SOL", "ETH"]:
        data = get_crypto_candles(crypto, hours=24)
        if data.get('success'):
            results[crypto] = {
                "name": data['name'],
                "emoji": data['emoji'],
                "price": data['summary'].get('current_price', 0),
                "change_24h": data['summary'].get('total_change_percent', 0),
                "trend": data['summary'].get('trend', 'N/A')
            }
    
    return {
        "success": True,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "cryptos": results
    }


# Test
if __name__ == "__main__":
    print("Testing Solana...")
    sol = get_crypto_candles("SOL", hours=10)
    
    if sol['success']:
        print(f"\n{sol['emoji']} {sol['name']}")
        print(f"Fiyat: ${sol['summary']['current_price']:.2f}")
        print(f"24h Değişim: {sol['summary']['total_change_percent']:.2f}%")
        print(f"Trend: {sol['summary']['trend_emoji']} {sol['summary']['trend']}")
    else:
        print(f"Hata: {sol['error']}")

