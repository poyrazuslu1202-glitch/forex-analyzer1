# ============================================
# FOREX ANALYZER - Ana API Server
# ============================================
# Bu dosya tüm modülleri birleştirip API endpoint'leri sunar.
# Flutter uygulaması bu API'ye bağlanacak.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Kendi modüllerimiz
from data.price_fetcher import get_analysis
from data.session_tracker import get_session_status
from data.btc_reporter import get_btc_candles
from decision.probability import calculate_probability
from analysis.ict_concepts import get_all_kill_zones_status, get_ict_analysis
from analysis.strategy_analyzer import generate_trade_signal
from analysis.backtester import backtest_strategy, get_real_confidence
from analysis.supply_demand import find_all_zones
from analysis.killzone_strategy import get_full_killzone_analysis, get_active_killzone_strategy, KILLZONE_BEHAVIORS
from analysis.trade_journal import record_signal, verify_past_signals, get_journal_stats, get_signal_history, clear_journal
from data.crypto_fetcher import get_crypto_candles, get_multi_crypto_summary, SUPPORTED_CRYPTOS
from data.news_fetcher import get_full_news_report, get_crypto_news, get_fear_greed_index, get_market_sentiment
from data.market_data import get_top_coins, get_trending_coins, get_global_market_data, get_economic_calendar, get_full_market_data

# ============================================
# FastAPI Uygulaması Oluştur
# ============================================
app = FastAPI(
    title="Forex Analyzer API",
    description="TradingView verisi ile Forex analizi yapan API",
    version="1.0.0"
)

# CORS ayarları (Flutter'ın bağlanabilmesi için)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tüm origin'lere izin ver
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================
# API Modelleri (Request/Response şablonları)
# ============================================
class AnalyzeRequest(BaseModel):
    """Analiz isteği için model"""
    symbol: str = "EURUSD"
    interval: str = "1h"


class PairInfo(BaseModel):
    """Parite bilgisi"""
    symbol: str
    name: str
    category: str


# ============================================
# Desteklenen Pariteler
# ============================================
SUPPORTED_PAIRS = [
    {"symbol": "EURUSD", "name": "Euro / US Dollar", "category": "Major"},
    {"symbol": "GBPUSD", "name": "British Pound / US Dollar", "category": "Major"},
    {"symbol": "USDJPY", "name": "US Dollar / Japanese Yen", "category": "Major"},
    {"symbol": "USDCHF", "name": "US Dollar / Swiss Franc", "category": "Major"},
    {"symbol": "AUDUSD", "name": "Australian Dollar / US Dollar", "category": "Major"},
    {"symbol": "USDCAD", "name": "US Dollar / Canadian Dollar", "category": "Major"},
    {"symbol": "NZDUSD", "name": "New Zealand Dollar / US Dollar", "category": "Major"},
    {"symbol": "XAUUSD", "name": "Gold / US Dollar", "category": "Commodity"},
    {"symbol": "XAGUSD", "name": "Silver / US Dollar", "category": "Commodity"},
]


# ============================================
# API Endpoint'leri
# ============================================

@app.get("/")
def root():
    """
    Ana sayfa - API'nin çalıştığını kontrol eder.
    
    Kullanım: GET http://localhost:8000/
    """
    return {
        "status": "running",
        "message": "Forex Analyzer API çalışıyor! 🚀",
        "endpoints": {
            "/analyze": "Parite analizi yap",
            "/sessions": "Session durumlarını gör",
            "/pairs": "Desteklenen pariteleri listele"
        }
    }


@app.get("/pairs")
def get_pairs():
    """
    Desteklenen pariteleri listeler.
    
    Kullanım: GET http://localhost:8000/pairs
    """
    return {
        "success": True,
        "pairs": SUPPORTED_PAIRS
    }


@app.get("/sessions")
def get_sessions():
    """
    Forex session durumlarını döndürür.
    
    Kullanım: GET http://localhost:8000/sessions
    
    Döndürür:
    - Aktif session'lar
    - Kill zone durumu
    - Kalan süreler
    """
    return get_session_status()


@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    """
    Parite analizi yapar ve Long/Short olasılığı döndürür.
    
    Kullanım: POST http://localhost:8000/analyze
    Body: {"symbol": "EURUSD", "interval": "1h"}
    
    Parametreler:
    - symbol: Parite (EURUSD, GBPUSD vs.)
    - interval: Zaman dilimi (1m, 5m, 15m, 1h, 4h, 1d)
    
    Döndürür:
    - Long/Short olasılıkları
    - İndikatör sinyalleri
    - Session bilgisi
    """
    # 1. TradingView'dan veri çek
    analysis = get_analysis(request.symbol, interval=request.interval)
    
    # 2. Session bilgisini al
    session = get_session_status()
    
    # 3. Olasılık hesapla
    result = calculate_probability(analysis, session)
    
    return result


@app.get("/analyze/{symbol}")
def analyze_quick(symbol: str, interval: str = "1h"):
    """
    Hızlı analiz - GET methodu ile.
    
    Kullanım: GET http://localhost:8000/analyze/EURUSD?interval=1h
    """
    analysis = get_analysis(symbol.upper(), interval=interval)
    session = get_session_status()
    result = calculate_probability(analysis, session)
    return result


@app.get("/btc-report")
def btc_report(hours: int = 10):
    """
    BTC mum raporu döndürür.
    
    Kullanım: GET http://localhost:8000/btc-report?hours=10
    """
    return get_btc_candles(hours=hours)


@app.get("/ict-analysis")
def ict_analysis():
    """
    ICT Concepts analizi döndürür.
    """
    btc_data = get_btc_candles(hours=24)
    
    if btc_data.get('success'):
        candles = btc_data.get('candles', [])
        return get_ict_analysis(candles)
    else:
        return {
            "kill_zones": get_all_kill_zones_status(),
            "market_structure": {"error": "Veri alınamadı"},
            "fair_value_gaps": [],
            "order_blocks": [],
            "premium_discount": {"error": "Veri alınamadı"}
        }


@app.get("/trade-signal")
def trade_signal():
    """
    Net trade sinyali döndürür.
    - LONG / SHORT / WAIT
    - Güven skoru
    - Giriş, Stop Loss, Take Profit seviyeleri
    
    Kullanım: GET http://localhost:8000/trade-signal
    """
    # 24 saatlik BTC verisi
    btc_data = get_btc_candles(hours=24)
    
    if not btc_data.get('success'):
        return {"error": "Veri alınamadı"}
    
    candles = btc_data.get('candles', [])
    
    # ICT analizi
    ict = get_ict_analysis(candles)
    
    # Trade sinyali üret
    signal = generate_trade_signal(candles, ict)
    
    # BTC özet bilgisi ekle
    signal['btc_summary'] = btc_data.get('summary', {})
    signal['candles'] = candles
    
    return signal


@app.get("/full-report")
def full_report():
    """
    Tam rapor - Tüm analizler tek endpoint'te.
    Artık GERÇEK backtest istatistikleri içeriyor!
    """
    # 24 saatlik veri
    btc_data = get_btc_candles(hours=24)
    
    if not btc_data.get('success'):
        return {"error": "Veri alınamadı", "details": btc_data.get('error')}
    
    candles = btc_data.get('candles', [])
    
    # ICT analizi
    ict = get_ict_analysis(candles)
    
    # Trade sinyali
    signal = generate_trade_signal(candles, ict)
    
    # BACKTEST - Gerçek istatistikler
    backtest = backtest_strategy(candles)
    
    # Gerçek güven oranını al
    if backtest.get('success'):
        real_confidence = get_real_confidence(backtest, signal.get('direction', 'WAIT'))
        signal['confidence'] = real_confidence
        signal['confidence_source'] = 'BACKTEST'
        signal['backtest_trades'] = backtest.get('total_trades', 0)
    else:
        signal['confidence_source'] = 'ESTIMATED'
    
    # News ve Sentiment
    news_report = get_full_news_report()
    
    # Kill Zone Stratejileri
    killzone_data = get_full_killzone_analysis(candles)
    
    # Journal istatistiklerini al (kaydetme işlemi ayrı endpoint'te)
    journal_stats = get_journal_stats()
    
    return {
        "generated_at": signal.get('generated_at'),
        "btc_report": btc_data,
        "ict_analysis": ict,
        "trade_signal": signal,
        "backtest": backtest,
        "news": news_report,
        "killzone_strategy": killzone_data,
        "journal": journal_stats
    }


@app.get("/backtest")
def get_backtest(hours: int = 72):
    """
    Sadece backtest sonuçlarını döndürür.
    GERÇEK win rate ve istatistikler.
    En az 50 trade için 72 saat veri kullanır.
    
    Kullanım: GET http://localhost:8000/backtest?hours=72
    """
    btc_data = get_btc_candles(hours=hours)
    
    if not btc_data.get('success'):
        return {"error": "Veri alınamadı"}
    
    candles = btc_data.get('candles', [])
    return backtest_strategy(candles, min_trades=50)


@app.get("/crypto/{symbol}")
def get_crypto(symbol: str, hours: int = 24):
    """
    Kripto para verisi döndürür.
    
    Desteklenen: BTC, SOL, ETH, XRP, BNB, ADA, DOGE, AVAX
    
    Kullanım: GET http://localhost:8000/crypto/SOL?hours=24
    """
    return get_crypto_candles(symbol.upper(), hours=hours)


@app.get("/crypto-list")
def crypto_list():
    """
    Desteklenen kripto paraları listeler.
    """
    return {
        "supported": SUPPORTED_CRYPTOS,
        "count": len(SUPPORTED_CRYPTOS)
    }


@app.get("/multi-crypto")
def multi_crypto():
    """
    Birden fazla kripto için özet.
    """
    return get_multi_crypto_summary()


@app.get("/supply-demand/{symbol}")
def supply_demand(symbol: str, hours: int = 48):
    """
    Supply ve Demand zone'ları döndürür.
    
    Kullanım: GET http://localhost:8000/supply-demand/SOL?hours=48
    """
    data = get_crypto_candles(symbol.upper(), hours=hours)
    
    if not data.get('success'):
        return {"error": data.get('error', 'Veri alınamadı')}
    
    candles = data.get('candles', [])
    zones = find_all_zones(candles)
    
    return {
        "crypto": symbol.upper(),
        "current_price": data['summary'].get('current_price'),
        "zones": zones
    }


@app.get("/news")
def get_news():
    """
    Kripto ve piyasa haberleri döndürür.
    - Son haberler
    - Fear & Greed Index
    - Önemli ekonomik eventler
    - Piyasa sentiment'i
    
    Kullanım: GET http://localhost:8000/news
    """
    return get_full_news_report()


@app.get("/fear-greed")
def fear_greed():
    """
    Sadece Fear & Greed Index döndürür.
    
    Kullanım: GET http://localhost:8000/fear-greed
    """
    return get_fear_greed_index()


@app.get("/sentiment")
def sentiment():
    """
    Piyasa sentiment analizi döndürür.
    
    Kullanım: GET http://localhost:8000/sentiment
    """
    return get_market_sentiment()


# ============================================
# MARKET DATA - CoinGecko & Economic Calendar
# ============================================

@app.get("/market-data")
def market_data():
    """
    Tam piyasa verisi döndürür.
    - Top 20 Coins (CoinGecko)
    - Trending Coins
    - Global Market Data
    - Economic Calendar
    
    Kullanım: GET http://localhost:8000/market-data
    """
    return get_full_market_data()


@app.get("/top-coins")
def top_coins(limit: int = 20):
    """
    En büyük kripto paralar (market cap sıralı).
    
    Kullanım: GET http://localhost:8000/top-coins?limit=20
    """
    return {
        "coins": get_top_coins(limit),
        "count": limit,
        "updated_at": datetime.now().isoformat()
    }


@app.get("/trending-coins")
def trending_coins():
    """
    Trend olan kripto paralar.
    
    Kullanım: GET http://localhost:8000/trending-coins
    """
    return {
        "trending": get_trending_coins(),
        "updated_at": datetime.now().isoformat()
    }


@app.get("/global-market")
def global_market():
    """
    Global kripto piyasa verileri.
    - Total Market Cap
    - BTC/ETH Dominance
    - 24h Volume
    
    Kullanım: GET http://localhost:8000/global-market
    """
    return get_global_market_data()


@app.get("/economic-calendar")
def economic_calendar():
    """
    Ekonomik takvim - Önemli finansal olaylar.
    - FED Kararları
    - NFP
    - CPI
    - GDP
    
    Kullanım: GET http://localhost:8000/economic-calendar
    """
    return {
        "events": get_economic_calendar(),
        "updated_at": datetime.now().isoformat()
    }


@app.get("/killzone-strategy")
def killzone_strategy():
    """
    Kill Zone stratejileri döndürür.
    - Asian Range
    - London Manipulation
    - NY Reversal
    - Aktif Zone bilgisi
    
    Kullanım: GET http://localhost:8000/killzone-strategy
    """
    btc_data = get_btc_candles(hours=24)
    
    if not btc_data.get('success'):
        return {"error": "Veri alınamadı"}
    
    candles = btc_data.get('candles', [])
    return get_full_killzone_analysis(candles)


@app.get("/killzone-behaviors")
def killzone_behaviors():
    """
    Tüm Kill Zone davranışlarını döndürür.
    
    Kullanım: GET http://localhost:8000/killzone-behaviors
    """
    return {
        "behaviors": KILLZONE_BEHAVIORS,
        "active_strategy": get_active_killzone_strategy()
    }


@app.get("/journal")
def journal():
    """
    Trade Journal istatistiklerini döndürür.
    
    Kullanım: GET http://localhost:8000/journal
    """
    return get_journal_stats()


@app.get("/journal/history")
def journal_history(limit: int = 50):
    """
    Sinyal geçmişini döndürür.
    
    Kullanım: GET http://localhost:8000/journal/history?limit=50
    """
    return {
        "signals": get_signal_history(limit),
        "count": len(get_signal_history(limit))
    }


@app.post("/journal/clear")
def journal_clear():
    """
    Journal'ı temizler (dikkatli kullan!).
    
    Kullanım: POST http://localhost:8000/journal/clear
    """
    return clear_journal()


@app.get("/full-analysis/{symbol}")
def full_analysis(symbol: str, hours: int = 24):
    """
    Tek bir kripto için TÜM analizler.
    - Mum verileri
    - ICT analizi
    - Supply/Demand zones
    - Trade sinyali
    - Backtest
    """
    # Kripto verisini çek
    crypto_data = get_crypto_candles(symbol.upper(), hours=hours)
    
    if not crypto_data.get('success'):
        return {"error": crypto_data.get('error', 'Veri alınamadı')}
    
    candles = crypto_data.get('candles', [])
    
    # Analizler
    ict = get_ict_analysis(candles)
    zones = find_all_zones(candles)
    signal = generate_trade_signal(candles, ict)
    backtest = backtest_strategy(candles)
    
    # Gerçek güven oranı
    if backtest.get('success'):
        signal['confidence'] = get_real_confidence(backtest, signal.get('direction', 'WAIT'))
        signal['confidence_source'] = 'BACKTEST'
    
    # Kill Zone Stratejileri
    killzone_data = get_full_killzone_analysis(candles)
    
    # Journal istatistiklerini al (hızlı)
    journal_stats = get_journal_stats()
    
    return {
        "crypto": symbol.upper(),
        "name": crypto_data.get('name'),
        "emoji": crypto_data.get('emoji'),
        "generated_at": crypto_data.get('generated_at'),
        "report": crypto_data,
        "ict_analysis": ict,
        "supply_demand": zones,
        "trade_signal": signal,
        "backtest": backtest,
        "killzone_strategy": killzone_data,
        "journal": journal_stats
    }


# ============================================
# Uygulama Başlatma
# ============================================
if __name__ == "__main__":
    import uvicorn
    
    print("=" * 50)
    print("  FOREX ANALYZER API")
    print("=" * 50)
    print("\n🚀 Server başlatılıyor...")
    print("📍 Adres: http://localhost:8000")
    print("📚 Docs: http://localhost:8000/docs")
    print("\n✅ Flutter uygulamasından bağlanabilirsin!")
    print("=" * 50)
    
    # Server'ı başlat
    uvicorn.run(app, host="0.0.0.0", port=8000)

