# ============================================
# MARKET DATA - CoinGecko & Economic Calendar
# ============================================
# CoinMarketCap alternatifi olarak CoinGecko API
# Investing.com alternatifi olarak Economic Calendar

import requests
from datetime import datetime, timedelta
from typing import Dict, List

# ============================================
# COINGECKO API - Ücretsiz Kripto Verileri
# ============================================

COINGECKO_BASE = "https://api.coingecko.com/api/v3"


def get_top_coins(limit: int = 20) -> List[Dict]:
    """
    En büyük kriptolar (market cap sıralı).
    CoinMarketCap alternatifi.
    """
    try:
        url = f"{COINGECKO_BASE}/coins/markets"
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": limit,
            "page": 1,
            "sparkline": False,
            "price_change_percentage": "1h,24h,7d"
        }
        
        response = requests.get(url, params=params, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            
            coins = []
            for coin in data:
                change_24h = coin.get('price_change_percentage_24h', 0) or 0
                
                coins.append({
                    "rank": coin.get('market_cap_rank', 0),
                    "id": coin.get('id', ''),
                    "symbol": coin.get('symbol', '').upper(),
                    "name": coin.get('name', ''),
                    "image": coin.get('image', ''),
                    "price": coin.get('current_price', 0),
                    "market_cap": coin.get('market_cap', 0),
                    "volume_24h": coin.get('total_volume', 0),
                    "change_1h": coin.get('price_change_percentage_1h_in_currency', 0) or 0,
                    "change_24h": change_24h,
                    "change_7d": coin.get('price_change_percentage_7d_in_currency', 0) or 0,
                    "ath": coin.get('ath', 0),
                    "ath_change_percent": coin.get('ath_change_percentage', 0),
                    "is_bullish": change_24h > 0,
                    "emoji": "🟢" if change_24h > 0 else "🔴"
                })
            
            return coins
        else:
            print(f"CoinGecko API hatası: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"Top coins hatası: {e}")
        return []


def get_trending_coins() -> List[Dict]:
    """
    Trend olan kriptolar (son 24 saat arama hacmi).
    """
    try:
        url = f"{COINGECKO_BASE}/search/trending"
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            coins = data.get('coins', [])
            
            trending = []
            for item in coins[:10]:
                coin = item.get('item', {})
                trending.append({
                    "rank": coin.get('market_cap_rank', 0),
                    "id": coin.get('id', ''),
                    "symbol": coin.get('symbol', '').upper(),
                    "name": coin.get('name', ''),
                    "image": coin.get('small', ''),
                    "score": coin.get('score', 0),
                    "price_btc": coin.get('price_btc', 0),
                    "emoji": "🔥"
                })
            
            return trending
        else:
            return []
            
    except Exception as e:
        print(f"Trending coins hatası: {e}")
        return []


def get_global_market_data() -> Dict:
    """
    Global kripto piyasa verileri.
    """
    try:
        url = f"{COINGECKO_BASE}/global"
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            data = response.json().get('data', {})
            
            market_cap_change = data.get('market_cap_change_percentage_24h_usd', 0)
            
            return {
                "total_market_cap": data.get('total_market_cap', {}).get('usd', 0),
                "total_volume_24h": data.get('total_volume', {}).get('usd', 0),
                "btc_dominance": round(data.get('market_cap_percentage', {}).get('btc', 0), 1),
                "eth_dominance": round(data.get('market_cap_percentage', {}).get('eth', 0), 1),
                "active_cryptocurrencies": data.get('active_cryptocurrencies', 0),
                "markets": data.get('markets', 0),
                "market_cap_change_24h": round(market_cap_change, 2),
                "is_bullish": market_cap_change > 0,
                "emoji": "📈" if market_cap_change > 0 else "📉",
                "updated_at": datetime.now().isoformat()
            }
        else:
            return {}
            
    except Exception as e:
        print(f"Global market hatası: {e}")
        return {}


# ============================================
# ECONOMIC CALENDAR - Ekonomik Takvim
# ============================================

# Önemli ekonomik olaylar ve tarihleri
ECONOMIC_EVENTS = {
    "FED_RATE": {
        "name": "FED Faiz Kararı",
        "emoji": "🏦",
        "impact": "EXTREME",
        "currency": "USD",
        "description": "ABD Merkez Bankası faiz kararı",
        "typical_days": ["Çarşamba"],
        "frequency": "6 haftada bir"
    },
    "NFP": {
        "name": "Non-Farm Payrolls",
        "emoji": "👷",
        "impact": "HIGH",
        "currency": "USD",
        "description": "Tarım dışı istihdam verisi",
        "typical_days": ["Her ayın ilk Cuması"],
        "frequency": "Aylık"
    },
    "CPI_US": {
        "name": "ABD Enflasyon (CPI)",
        "emoji": "📊",
        "impact": "HIGH",
        "currency": "USD",
        "description": "Tüketici fiyat endeksi",
        "typical_days": ["Ayın ortası"],
        "frequency": "Aylık"
    },
    "ECB_RATE": {
        "name": "ECB Faiz Kararı",
        "emoji": "🇪🇺",
        "impact": "HIGH",
        "currency": "EUR",
        "description": "Avrupa Merkez Bankası faiz kararı",
        "typical_days": ["Perşembe"],
        "frequency": "6 haftada bir"
    },
    "FOMC_MINUTES": {
        "name": "FOMC Tutanakları",
        "emoji": "📝",
        "impact": "MEDIUM",
        "currency": "USD",
        "description": "FED toplantı tutanakları",
        "typical_days": ["Çarşamba"],
        "frequency": "3 haftada bir"
    },
    "GDP_US": {
        "name": "ABD GDP",
        "emoji": "📈",
        "impact": "MEDIUM",
        "currency": "USD",
        "description": "Gayri safi yurtiçi hasıla",
        "typical_days": ["Ayın sonu"],
        "frequency": "Çeyreklik"
    },
    "UNEMPLOYMENT_CLAIMS": {
        "name": "İşsizlik Başvuruları",
        "emoji": "📉",
        "impact": "MEDIUM",
        "currency": "USD",
        "description": "Haftalık işsizlik başvuruları",
        "typical_days": ["Perşembe"],
        "frequency": "Haftalık"
    },
    "RETAIL_SALES": {
        "name": "Perakende Satışlar",
        "emoji": "🛒",
        "impact": "MEDIUM",
        "currency": "USD",
        "description": "ABD perakende satış verileri",
        "typical_days": ["Ayın ortası"],
        "frequency": "Aylık"
    },
    "PMI_MANUFACTURING": {
        "name": "İmalat PMI",
        "emoji": "🏭",
        "impact": "MEDIUM",
        "currency": "USD",
        "description": "İmalat sektörü PMI",
        "typical_days": ["Ayın ilk iş günü"],
        "frequency": "Aylık"
    },
    "PMI_SERVICES": {
        "name": "Hizmet PMI",
        "emoji": "🏢",
        "impact": "MEDIUM",
        "currency": "USD",
        "description": "Hizmet sektörü PMI",
        "typical_days": ["Ayın 3. iş günü"],
        "frequency": "Aylık"
    }
}


def get_economic_calendar() -> List[Dict]:
    """
    Yaklaşan ekonomik olayları döndürür.
    Not: Gerçek API olmadan simüle edilmiş veri.
    """
    today = datetime.now()
    day_of_week = today.weekday()  # 0=Pazartesi, 4=Cuma
    day_of_month = today.day
    
    events = []
    
    # Perşembe = İşsizlik başvuruları
    if day_of_week == 3:  # Perşembe
        events.append({
            **ECONOMIC_EVENTS["UNEMPLOYMENT_CLAIMS"],
            "date": today.strftime("%Y-%m-%d"),
            "time": "15:30",
            "time_turkey": "15:30 TR",
            "status": "TODAY",
            "actual": None,
            "forecast": "220K",
            "previous": "218K"
        })
    
    # Ayın ilk Cuması = NFP
    if day_of_week == 4 and day_of_month <= 7:
        events.append({
            **ECONOMIC_EVENTS["NFP"],
            "date": today.strftime("%Y-%m-%d"),
            "time": "15:30",
            "time_turkey": "15:30 TR",
            "status": "TODAY",
            "actual": None,
            "forecast": "175K",
            "previous": "227K"
        })
    
    # Ayın ortası = CPI
    if 10 <= day_of_month <= 15:
        events.append({
            **ECONOMIC_EVENTS["CPI_US"],
            "date": today.strftime("%Y-%m-%d"),
            "time": "15:30",
            "time_turkey": "15:30 TR",
            "status": "THIS_WEEK",
            "actual": None,
            "forecast": "2.7%",
            "previous": "2.6%"
        })
    
    # Yaklaşan olaylar (her zaman göster)
    upcoming_date = today + timedelta(days=7)
    
    if not events:
        events.append({
            **ECONOMIC_EVENTS["FOMC_MINUTES"],
            "date": upcoming_date.strftime("%Y-%m-%d"),
            "time": "21:00",
            "time_turkey": "21:00 TR",
            "status": "UPCOMING",
            "actual": None,
            "forecast": "-",
            "previous": "-"
        })
    
    # Her zaman FED'i göster
    fed_date = today + timedelta(days=14)
    events.append({
        **ECONOMIC_EVENTS["FED_RATE"],
        "date": fed_date.strftime("%Y-%m-%d"),
        "time": "21:00",
        "time_turkey": "21:00 TR",
        "status": "UPCOMING",
        "actual": None,
        "forecast": "4.25-4.50%",
        "previous": "4.50-4.75%"
    })
    
    return events


def get_full_market_data() -> Dict:
    """
    Tüm piyasa verilerini tek seferde döndürür.
    """
    return {
        "top_coins": get_top_coins(20),
        "trending": get_trending_coins(),
        "global": get_global_market_data(),
        "calendar": get_economic_calendar(),
        "event_types": ECONOMIC_EVENTS,
        "updated_at": datetime.now().isoformat()
    }


# Test
if __name__ == "__main__":
    print("=" * 60)
    print("  MARKET DATA TEST")
    print("=" * 60)
    
    # Global Data
    print("\n📊 GLOBAL MARKET:")
    global_data = get_global_market_data()
    if global_data:
        print(f"   Total Market Cap: ${global_data['total_market_cap']:,.0f}")
        print(f"   BTC Dominance: {global_data['btc_dominance']}%")
        print(f"   24h Change: {global_data['market_cap_change_24h']}%")
    
    # Top Coins
    print("\n🏆 TOP 10 COINS:")
    top_coins = get_top_coins(10)
    for coin in top_coins[:10]:
        print(f"   {coin['rank']}. {coin['symbol']}: ${coin['price']:,.2f} ({coin['emoji']} {coin['change_24h']:.1f}%)")
    
    # Trending
    print("\n🔥 TRENDING:")
    trending = get_trending_coins()
    for coin in trending[:5]:
        print(f"   {coin['emoji']} {coin['symbol']} - {coin['name']}")
    
    # Calendar
    print("\n📅 ECONOMIC CALENDAR:")
    calendar = get_economic_calendar()
    for event in calendar[:5]:
        print(f"   {event['emoji']} {event['name']} - {event['date']} ({event['status']})")
    
    print("=" * 60)

