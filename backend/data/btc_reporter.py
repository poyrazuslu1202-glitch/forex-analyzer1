# ============================================
# BTC REPORTER - Bitcoin Mum Raporu
# ============================================
# Son X saatlik BTC mumlarını çeker ve rapor oluşturur.

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List

def get_btc_candles(hours: int = 24, interval: str = "1h") -> Dict:
    """
    Bitcoin'in son X saatlik mum verilerini çeker.
    
    Parametreler:
    -------------
    hours : int
        Kaç saatlik veri çekilecek (varsayılan: 10)
    
    interval : str
        Mum zaman dilimi: "1h", "15m", "4h", "1d" vs.
    
    Döndürür:
    ---------
    Dict : Mum verileri ve analiz
    """
    try:
        # BTC-USD verisini çek
        btc = yf.Ticker("BTC-USD")
        
        # Son 3 günlük veri çek (24 saat için yeterli olması için)
        df = btc.history(period="3d", interval=interval)
        
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
            
            # Mum tipi belirle
            if close_price > open_price:
                candle_type = "YESIL"  # Bullish
                emoji = "🟢"
            elif close_price < open_price:
                candle_type = "KIRMIZI"  # Bearish
                emoji = "🔴"
            else:
                candle_type = "DOJI"
                emoji = "⚪"
            
            # Değişim yüzdesi
            change_percent = ((close_price - open_price) / open_price) * 100
            
            candles.append({
                "timestamp": timestamp,
                "open": round(open_price, 2),
                "high": round(high_price, 2),
                "low": round(low_price, 2),
                "close": round(close_price, 2),
                "volume": round(volume, 2),
                "type": candle_type,
                "emoji": emoji,
                "change_percent": round(change_percent, 2)
            })
        
        # Genel istatistikler
        total_green = sum(1 for c in candles if c['type'] == "YESIL")
        total_red = sum(1 for c in candles if c['type'] == "KIRMIZI")
        
        first_open = candles[0]['open'] if candles else 0
        last_close = candles[-1]['close'] if candles else 0
        total_change = ((last_close - first_open) / first_open) * 100 if first_open else 0
        
        highest = max(c['high'] for c in candles) if candles else 0
        lowest = min(c['low'] for c in candles) if candles else 0
        
        # Trend belirleme
        if total_green > total_red:
            trend = "YUKARI"
            trend_emoji = "📈"
        elif total_red > total_green:
            trend = "ASAGI"
            trend_emoji = "📉"
        else:
            trend = "YATAY"
            trend_emoji = "➡️"
        
        return {
            "success": True,
            "symbol": "BTC/USD",
            "interval": interval,
            "period_hours": hours,
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            
            "summary": {
                "trend": trend,
                "trend_emoji": trend_emoji,
                "total_change_percent": round(total_change, 2),
                "green_candles": total_green,
                "red_candles": total_red,
                "highest_price": highest,
                "lowest_price": lowest,
                "current_price": last_close
            },
            
            "candles": candles
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def print_btc_report(hours: int = 10):
    """
    BTC raporunu konsola yazdırır.
    """
    result = get_btc_candles(hours=hours)
    
    if not result['success']:
        print(f"❌ HATA: {result['error']}")
        return
    
    print("\n" + "=" * 60)
    print("                 🪙 BTC RAPORU")
    print("=" * 60)
    print(f"📅 Oluşturulma: {result['generated_at']}")
    print(f"⏱️  Periyot: Son {result['period_hours']} saat ({result['interval']} mumlar)")
    print("=" * 60)
    
    # Özet
    summary = result['summary']
    print(f"\n{summary['trend_emoji']} TREND: {summary['trend']}")
    print(f"💰 Şu anki fiyat: ${summary['current_price']:,.2f}")
    print(f"📊 Toplam değişim: %{summary['total_change_percent']:.2f}")
    print(f"⬆️  En yüksek: ${summary['highest_price']:,.2f}")
    print(f"⬇️  En düşük: ${summary['lowest_price']:,.2f}")
    print(f"🟢 Yeşil mum: {summary['green_candles']}")
    print(f"🔴 Kırmızı mum: {summary['red_candles']}")
    
    # Mum detayları
    print("\n" + "-" * 60)
    print("                    MUM DETAYLARI")
    print("-" * 60)
    print(f"{'Saat':<18} {'Açılış':>12} {'Kapanış':>12} {'Değişim':>10} {'Tip':<8}")
    print("-" * 60)
    
    for candle in result['candles']:
        print(f"{candle['timestamp']:<18} ${candle['open']:>10,.2f} ${candle['close']:>10,.2f} {candle['change_percent']:>9.2f}% {candle['emoji']}")
    
    print("=" * 60)
    print("                 RAPOR SONU")
    print("=" * 60 + "\n")
    
    return result


# Test kodu
if __name__ == "__main__":
    print_btc_report(hours=24)

