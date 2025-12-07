# ============================================
# NEWS FETCHER - Finansal Haberler
# ============================================
# Kripto ve Forex için önemli haberleri çeker

import requests
from datetime import datetime, timedelta
from typing import Dict, List

# ============================================
# ECONOMIC CALENDAR - Ekonomik Takvim
# ============================================

IMPORTANT_EVENTS = {
    "FED": {
        "name": "Federal Reserve Faiz Kararı",
        "emoji": "🏦",
        "impact": "HIGH",
        "description": "ABD Merkez Bankası faiz kararı - Piyasaları en çok etkileyen olay",
        "affects": ["USD", "BTC", "Tüm piyasalar"]
    },
    "NFP": {
        "name": "Non-Farm Payrolls",
        "emoji": "👷",
        "impact": "HIGH",
        "description": "ABD Tarım Dışı İstihdam - Her ayın ilk Cuması",
        "affects": ["USD", "Altın", "Hisse senetleri"]
    },
    "CPI": {
        "name": "Consumer Price Index",
        "emoji": "📊",
        "impact": "HIGH",
        "description": "ABD Tüketici Fiyat Endeksi (Enflasyon)",
        "affects": ["USD", "BTC", "Altın"]
    },
    "ECB": {
        "name": "ECB Faiz Kararı",
        "emoji": "🇪🇺",
        "impact": "HIGH",
        "description": "Avrupa Merkez Bankası faiz kararı",
        "affects": ["EUR", "EUR/USD"]
    },
    "GDP": {
        "name": "Gross Domestic Product",
        "emoji": "📈",
        "impact": "MEDIUM",
        "description": "ABD Gayri Safi Yurtiçi Hasıla",
        "affects": ["USD", "Hisse senetleri"]
    },
    "FOMC": {
        "name": "FOMC Toplantı Tutanakları",
        "emoji": "📝",
        "impact": "MEDIUM",
        "description": "FED toplantı tutanakları açıklaması",
        "affects": ["USD", "BTC"]
    },
    "UNEMPLOYMENT": {
        "name": "Unemployment Claims",
        "emoji": "📉",
        "impact": "MEDIUM",
        "description": "Haftalık işsizlik başvuruları",
        "affects": ["USD"]
    },
    "RETAIL_SALES": {
        "name": "Retail Sales",
        "emoji": "🛒",
        "impact": "MEDIUM",
        "description": "ABD Perakende Satışlar",
        "affects": ["USD", "Hisse senetleri"]
    },
    "PMI": {
        "name": "PMI (Purchasing Managers Index)",
        "emoji": "🏭",
        "impact": "MEDIUM",
        "description": "İmalat/Hizmet Sektörü PMI",
        "affects": ["USD", "EUR"]
    },
    "BTC_HALVING": {
        "name": "Bitcoin Halving",
        "emoji": "⚡",
        "impact": "EXTREME",
        "description": "Bitcoin ödül yarılanması - 4 yılda bir",
        "affects": ["BTC", "Tüm kripto"]
    },
    "ETF": {
        "name": "Bitcoin/Crypto ETF Haberleri",
        "emoji": "📦",
        "impact": "HIGH",
        "description": "ETF onay/ret kararları",
        "affects": ["BTC", "ETH", "Tüm kripto"]
    }
}


def get_crypto_news() -> List[Dict]:
    """
    CryptoCompare'den kripto haberlerini çeker.
    """
    try:
        url = "https://min-api.cryptocompare.com/data/v2/news/?lang=EN&categories=BTC,ETH,SOL"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            news_list = data.get('Data', [])[:10]  # Son 10 haber
            
            formatted_news = []
            for news in news_list:
                # Kategori bazlı emoji
                categories = news.get('categories', '').lower()
                if 'btc' in categories or 'bitcoin' in categories:
                    emoji = '₿'
                elif 'eth' in categories or 'ethereum' in categories:
                    emoji = 'Ξ'
                elif 'sol' in categories or 'solana' in categories:
                    emoji = '◎'
                else:
                    emoji = '📰'
                
                # Zaman hesapla
                published = news.get('published_on', 0)
                hours_ago = int((datetime.now().timestamp() - published) / 3600)
                
                if hours_ago < 1:
                    time_str = "Az önce"
                elif hours_ago < 24:
                    time_str = f"{hours_ago} saat önce"
                else:
                    days = hours_ago // 24
                    time_str = f"{days} gün önce"
                
                formatted_news.append({
                    "title": news.get('title', ''),
                    "source": news.get('source', 'Unknown'),
                    "url": news.get('url', ''),
                    "emoji": emoji,
                    "time_ago": time_str,
                    "categories": news.get('categories', ''),
                    "body": news.get('body', '')[:200] + '...' if len(news.get('body', '')) > 200 else news.get('body', '')
                })
            
            return formatted_news
    except Exception as e:
        print(f"Haber çekme hatası: {e}")
    
    return []


def get_fear_greed_index() -> Dict:
    """
    Crypto Fear & Greed Index'i çeker.
    """
    try:
        url = "https://api.alternative.me/fng/"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            fng = data.get('data', [{}])[0]
            
            value = int(fng.get('value', 50))
            classification = fng.get('value_classification', 'Neutral')
            
            # Emoji ve renk
            if value <= 20:
                emoji = "😱"
                color = "#F23645"
                suggestion = "Aşırı korku - Potansiyel alım fırsatı"
            elif value <= 40:
                emoji = "😟"
                color = "#FF6B00"
                suggestion = "Korku - Dikkatli ol"
            elif value <= 60:
                emoji = "😐"
                color = "#F7931A"
                suggestion = "Nötr - Bekle ve gör"
            elif value <= 80:
                emoji = "😊"
                color = "#089981"
                suggestion = "Açgözlülük - Dikkatli ol"
            else:
                emoji = "🤑"
                color = "#00C853"
                suggestion = "Aşırı açgözlülük - Potansiyel satış"
            
            return {
                "value": value,
                "classification": classification,
                "emoji": emoji,
                "color": color,
                "suggestion": suggestion,
                "last_updated": fng.get('timestamp', '')
            }
    except Exception as e:
        print(f"Fear & Greed hatası: {e}")
    
    return {
        "value": 50,
        "classification": "Neutral",
        "emoji": "😐",
        "color": "#F7931A",
        "suggestion": "Veri alınamadı"
    }


def get_important_events_today() -> List[Dict]:
    """
    Bugünkü önemli ekonomik olayları döndürür.
    Not: Gerçek API olmadan statik/örnek veri döndürür.
    """
    # Günün hangi günü olduğuna göre örnek eventler
    today = datetime.now()
    day_of_week = today.weekday()  # 0 = Pazartesi
    day_of_month = today.day
    
    events = []
    
    # Her ayın ilk Cuması NFP
    if day_of_week == 4 and day_of_month <= 7:
        events.append({
            **IMPORTANT_EVENTS["NFP"],
            "time": "15:30 TR",
            "status": "TODAY"
        })
    
    # Örnek upcoming eventler
    if not events:
        # Yaklaşan önemli eventler
        upcoming = [
            {
                **IMPORTANT_EVENTS["CPI"],
                "time": "Yakında",
                "status": "UPCOMING"
            },
            {
                **IMPORTANT_EVENTS["FED"],
                "time": "Yakında",
                "status": "UPCOMING"
            }
        ]
        events = upcoming[:2]
    
    return events


def get_market_sentiment() -> Dict:
    """
    Genel piyasa sentiment analizi.
    """
    fear_greed = get_fear_greed_index()
    
    # BTC dominance (örnek - gerçek API gerekir)
    btc_dominance = 52.5  # Örnek değer
    
    # Market durumu
    if fear_greed['value'] <= 30:
        market_mood = "FEARFUL"
        mood_emoji = "🐻"
        mood_color = "#F23645"
    elif fear_greed['value'] >= 70:
        market_mood = "GREEDY"
        mood_emoji = "🐂"
        mood_color = "#089981"
    else:
        market_mood = "NEUTRAL"
        mood_emoji = "⚖️"
        mood_color = "#F7931A"
    
    return {
        "fear_greed": fear_greed,
        "btc_dominance": btc_dominance,
        "market_mood": market_mood,
        "mood_emoji": mood_emoji,
        "mood_color": mood_color
    }


def get_full_news_report() -> Dict:
    """
    Tam haber raporu.
    """
    return {
        "crypto_news": get_crypto_news(),
        "fear_greed": get_fear_greed_index(),
        "important_events": get_important_events_today(),
        "market_sentiment": get_market_sentiment(),
        "event_definitions": IMPORTANT_EVENTS
    }


# Test
if __name__ == "__main__":
    print("=" * 60)
    print("  NEWS FETCHER TEST")
    print("=" * 60)
    
    # Fear & Greed
    fng = get_fear_greed_index()
    print(f"\n{fng['emoji']} Fear & Greed Index: {fng['value']} ({fng['classification']})")
    print(f"   {fng['suggestion']}")
    
    # Haberler
    news = get_crypto_news()
    print(f"\n📰 Son Haberler ({len(news)} haber):")
    for n in news[:5]:
        print(f"   {n['emoji']} {n['title'][:60]}...")
        print(f"      {n['source']} • {n['time_ago']}")
    
    # Önemli eventler
    events = get_important_events_today()
    print(f"\n📅 Önemli Eventler:")
    for e in events:
        print(f"   {e['emoji']} {e['name']} - {e['time']}")
    
    print("=" * 60)

