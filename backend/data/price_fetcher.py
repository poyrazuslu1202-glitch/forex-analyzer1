# ============================================
# PRICE FETCHER - TradingView'dan Veri Çekme
# ============================================
# Bu dosya TradingView'dan fiyat ve indikatör verisi çeker.

from tradingview_ta import TA_Handler, Interval

def get_analysis(symbol: str, exchange: str = "FX_IDC", interval: str = "1h"):
    """
    TradingView'dan analiz verisi çeker.
    
    Parametreler:
    -------------
    symbol : str
        Parite adı. Örnek: "EURUSD", "GBPUSD", "XAUUSD"
    
    exchange : str
        Borsa adı. Forex için "FX_IDC" kullanıyoruz.
        
    interval : str
        Zaman dilimi. Seçenekler:
        - "1m"  = 1 dakika
        - "5m"  = 5 dakika
        - "15m" = 15 dakika
        - "1h"  = 1 saat
        - "4h"  = 4 saat
        - "1d"  = 1 gün
    
    Döndürür:
    ---------
    dict : Analiz sonuçları (fiyat, indikatörler, özet)
    """
    
    # Interval mapping - string'i TradingView formatına çevir
    interval_map = {
        "1m": Interval.INTERVAL_1_MINUTE,
        "5m": Interval.INTERVAL_5_MINUTES,
        "15m": Interval.INTERVAL_15_MINUTES,
        "30m": Interval.INTERVAL_30_MINUTES,
        "1h": Interval.INTERVAL_1_HOUR,
        "2h": Interval.INTERVAL_2_HOURS,
        "4h": Interval.INTERVAL_4_HOURS,
        "1d": Interval.INTERVAL_1_DAY,
        "1w": Interval.INTERVAL_1_WEEK,
        "1M": Interval.INTERVAL_1_MONTH,
    }
    
    try:
        # TradingView Handler oluştur
        handler = TA_Handler(
            symbol=symbol,
            exchange=exchange,
            screener="forex",
            interval=interval_map.get(interval, Interval.INTERVAL_1_HOUR)
        )
        
        # Analiz al
        analysis = handler.get_analysis()
        
        # Sonuçları düzenle
        result = {
            "success": True,
            "symbol": symbol,
            "interval": interval,
            
            # Fiyat bilgileri (get() ile güvenli erişim)
            "price": {
                "close": analysis.indicators.get("close"),
                "open": analysis.indicators.get("open"),
                "high": analysis.indicators.get("high"),
                "low": analysis.indicators.get("low"),
                "change": analysis.indicators.get("change"),
                "change_percent": (analysis.indicators.get("change", 0) / analysis.indicators.get("open", 1)) * 100 if analysis.indicators.get("open") else 0
            },
            
            # TradingView'ın kendi özeti
            "summary": {
                "recommendation": analysis.summary.get("RECOMMENDATION", "NEUTRAL"),
                "buy": analysis.summary.get("BUY", 0),
                "sell": analysis.summary.get("SELL", 0),
                "neutral": analysis.summary.get("NEUTRAL", 0)
            },
            
            # İndikatörler (get() ile güvenli erişim)
            "indicators": {
                "RSI": analysis.indicators.get("RSI"),
                "MACD": {
                    "macd": analysis.indicators.get("MACD.macd"),
                    "signal": analysis.indicators.get("MACD.signal")
                },
                "EMA_20": analysis.indicators.get("EMA20"),
                "EMA_50": analysis.indicators.get("EMA50"),
                "EMA_200": analysis.indicators.get("EMA200"),
                "SMA_20": analysis.indicators.get("SMA20"),
                "SMA_50": analysis.indicators.get("SMA50"),
                "SMA_200": analysis.indicators.get("SMA200"),
                "Bollinger": {
                    "upper": analysis.indicators.get("BB.upper"),
                    "lower": analysis.indicators.get("BB.lower")
                },
                "Stochastic": {
                    "k": analysis.indicators.get("Stoch.K"),
                    "d": analysis.indicators.get("Stoch.D")
                },
                "ATR": analysis.indicators.get("ATR"),
                "ADX": analysis.indicators.get("ADX")
            },
            
            # Ham veri (tüm indikatörler)
            "raw_indicators": analysis.indicators
        }
        
        return result
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "symbol": symbol
        }


# Test kodu - Bu dosya direkt çalıştırılırsa test eder
if __name__ == "__main__":
    print("EURUSD test ediliyor...")
    result = get_analysis("EURUSD")
    
    if result["success"]:
        print(f"\n✅ Başarılı!")
        print(f"Parite: {result['symbol']}")
        print(f"Fiyat: {result['price']['close']}")
        print(f"RSI: {result['indicators']['RSI']:.2f}")
        print(f"Öneri: {result['summary']['recommendation']}")
    else:
        print(f"\n❌ Hata: {result['error']}")

