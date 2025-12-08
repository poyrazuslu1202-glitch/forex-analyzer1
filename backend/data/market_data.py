# ============================================
# MARKET DATA - CoinMarketCap & Economic Calendar
# ============================================
# Yatırım haberleri, Market Cap, Ekonomik Takvim

import requests
from datetime import datetime, timedelta
from typing import Dict, List

# ============================================
# COINMARKETCAP - Market Cap & Top Coins
# ============================================

def get_top_cryptos() -> List[Dict]:
    """
    En büyük 20 kripto parayı döndürür.
    CoinGecko API (ücretsiz)
    """
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 20,
            "page": 1,
            "sparkline": False,
            "price_change_percentage": "24h,7d"
        }
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            cryptos = []
            for coin in data:
                change_24h = coin.get('price_change_percentage_24h', 0) or 0
                change_7d = coin.get('price_change_percentage_7d_in_currency', 0) or 0
                
                cryptos.append({
                    "rank": coin.get('market_cap_rank', 0),
                    "symbol": coin.get('symbol', '').upper(),
                    "name": coin.get('name', ''),
                    "price": coin.get('current_price', 0),
                    "market_cap": coin.get('market_cap', 0),
                    "volume_24h": coin.get('total_volume', 0),
                    "change_24h": round(change_24h, 2),
                    "change_7d": round(change_7d, 2),
                    "image": coin.get('image', ''),
                    "ath": coin.get('ath', 0),
                    "ath_change_percent": coin.get('ath_change_percentage', 0)
                })
            
            return cryptos
    except Exception as e:
        print(f"Top cryptos hatası: {e}")
    
    return []


def get_global_market_data() -> Dict:
    """
    Genel kripto piyasa verilerini döndürür.
    """
    try:
        url = "https://api.coingecko.com/api/v3/global"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json().get('data', {})
            
            return {
                "total_market_cap": data.get('total_market_cap', {}).get('usd', 0),
                "total_volume": data.get('total_volume', {}).get('usd', 0),
                "btc_dominance": round(data.get('market_cap_percentage', {}).get('btc', 0), 2),
                "eth_dominance": round(data.get('market_cap_percentage', {}).get('eth', 0), 2),
                "active_cryptos": data.get('active_cryptocurrencies', 0),
                "markets": data.get('markets', 0),
                "market_cap_change_24h": round(data.get('market_cap_change_percentage_24h_usd', 0), 2)
            }
    except Exception as e:
        print(f"Global market data hatası: {e}")
    
    return {}


def get_trending_coins() -> List[Dict]:
    """
    Trend olan coinleri döndürür.
    """
    try:
        url = "https://api.coingecko.com/api/v3/search/trending"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            coins = data.get('coins', [])
            
            trending = []
            for item in coins[:10]:
                coin = item.get('item', {})
                trending.append({
                    "rank": coin.get('market_cap_rank', 0),
                    "symbol": coin.get('symbol', '').upper(),
                    "name": coin.get('name', ''),
                    "score": coin.get('score', 0),
                    "price_btc": coin.get('price_btc', 0),
                    "image": coin.get('small', '')
                })
            
            return trending
    except Exception as e:
        print(f"Trending coins hatası: {e}")
    
    return []


# ============================================
# ECONOMIC CALENDAR - Ekonomik Takvim
# ============================================

ECONOMIC_EVENTS = [
    {
        "event": "FOMC Meeting",
        "country": "🇺🇸",
        "impact": "HIGH",
        "description": "Federal Reserve faiz kararı",
        "affects": ["USD", "BTC", "Hisse Senetleri", "Altın"]
    },
    {
        "event": "Non-Farm Payrolls",
        "country": "🇺🇸",
        "impact": "HIGH",
        "description": "ABD Tarım Dışı İstihdam (Her ayın ilk Cuması)",
        "affects": ["USD", "Altın"]
    },
    {
        "event": "CPI (Inflation)",
        "country": "🇺🇸",
        "impact": "HIGH",
        "description": "Tüketici Fiyat Endeksi - Enflasyon verisi",
        "affects": ["USD", "BTC", "Altın"]
    },
    {
        "event": "ECB Rate Decision",
        "country": "🇪🇺",
        "impact": "HIGH",
        "description": "Avrupa Merkez Bankası faiz kararı",
        "affects": ["EUR", "EUR/USD"]
    },
    {
        "event": "GDP Growth",
        "country": "🇺🇸",
        "impact": "MEDIUM",
        "description": "Gayri Safi Yurtiçi Hasıla büyüme oranı",
        "affects": ["USD", "Hisse Senetleri"]
    },
    {
        "event": "Unemployment Rate",
        "country": "🇺🇸",
        "impact": "MEDIUM",
        "description": "İşsizlik oranı",
        "affects": ["USD"]
    },
    {
        "event": "Retail Sales",
        "country": "🇺🇸",
        "impact": "MEDIUM",
        "description": "Perakende satış verileri",
        "affects": ["USD", "Hisse Senetleri"]
    },
    {
        "event": "PMI Manufacturing",
        "country": "🇺🇸",
        "impact": "MEDIUM",
        "description": "İmalat Sektörü PMI",
        "affects": ["USD"]
    },
    {
        "event": "BOJ Rate Decision",
        "country": "🇯🇵",
        "impact": "HIGH",
        "description": "Japonya Merkez Bankası faiz kararı",
        "affects": ["JPY", "USD/JPY"]
    },
    {
        "event": "BOE Rate Decision",
        "country": "🇬🇧",
        "impact": "HIGH",
        "description": "İngiltere Merkez Bankası faiz kararı",
        "affects": ["GBP", "GBP/USD"]
    }
]


def get_economic_calendar() -> Dict:
    """
    Ekonomik takvim verilerini döndürür.
    Not: Gerçek API olmadan statik veri kullanılıyor.
    """
    today = datetime.now()
    
    # Örnek yaklaşan eventler
    upcoming = []
    
    for i, event in enumerate(ECONOMIC_EVENTS[:5]):
        # Rastgele tarih ata (demo için)
        event_date = today + timedelta(days=i*3+1)
        
        upcoming.append({
            **event,
            "date": event_date.strftime("%Y-%m-%d"),
            "time": "15:30" if event['country'] == "🇺🇸" else "14:00",
            "days_until": (event_date - today).days
        })
    
    return {
        "upcoming_events": upcoming,
        "high_impact_count": len([e for e in upcoming if e['impact'] == 'HIGH']),
        "all_events": ECONOMIC_EVENTS
    }


def get_forex_rates() -> Dict:
    """
    Ana forex paritelerini döndürür.
    """
    try:
        # Ücretsiz forex API
        url = "https://api.exchangerate-api.com/v4/latest/USD"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            rates = data.get('rates', {})
            
            pairs = {
                "EUR/USD": round(1 / rates.get('EUR', 1), 5),
                "GBP/USD": round(1 / rates.get('GBP', 1), 5),
                "USD/JPY": round(rates.get('JPY', 0), 3),
                "USD/CHF": round(rates.get('CHF', 0), 5),
                "AUD/USD": round(1 / rates.get('AUD', 1), 5),
                "USD/CAD": round(rates.get('CAD', 0), 5),
                "NZD/USD": round(1 / rates.get('NZD', 1), 5)
            }
            
            return {
                "pairs": pairs,
                "base": "USD",
                "last_updated": data.get('date', '')
            }
    except Exception as e:
        print(f"Forex rates hatası: {e}")
    
    return {}


def get_full_market_report() -> Dict:
    """
    Tam piyasa raporu.
    """
    return {
        "global_data": get_global_market_data(),
        "top_cryptos": get_top_cryptos(),
        "trending": get_trending_coins(),
        "economic_calendar": get_economic_calendar(),
        "forex_rates": get_forex_rates(),
        "generated_at": datetime.now().isoformat()
    }


# Test
if __name__ == "__main__":
    print("=" * 60)
    print("  MARKET DATA TEST")
    print("=" * 60)
    
    # Global
    global_data = get_global_market_data()
    print(f"\n📊 Global Market Cap: ${global_data.get('total_market_cap', 0):,.0f}")
    print(f"   BTC Dominance: {global_data.get('btc_dominance')}%")
    
    # Top Cryptos
    top = get_top_cryptos()
    print(f"\n🏆 Top 5 Crypto:")
    for coin in top[:5]:
        print(f"   {coin['rank']}. {coin['symbol']}: ${coin['price']:,.2f} ({coin['change_24h']:+.2f}%)")
    
    # Trending
    trending = get_trending_coins()
    print(f"\n🔥 Trending:")
    for coin in trending[:5]:
        print(f"   {coin['symbol']}: {coin['name']}")
    
    # Calendar
    calendar = get_economic_calendar()
    print(f"\n📅 Upcoming Events:")
    for event in calendar['upcoming_events'][:3]:
        print(f"   {event['country']} {event['event']} - {event['date']}")
    
    print("=" * 60)

