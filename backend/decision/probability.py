# ============================================
# PROBABILITY CALCULATOR - Olasılık Hesaplama
# ============================================
# Bu dosya tüm indikatörleri analiz edip Long/Short olasılığı hesaplar.

from typing import Dict

def calculate_rsi_signal(rsi: float) -> Dict:
    """
    RSI değerine göre sinyal üretir.
    
    RSI Yorumlama:
    - 0-30: Oversold (Aşırı satım) → LONG sinyali
    - 30-50: Zayıf → Hafif LONG
    - 50-70: Zayıf → Hafif SHORT  
    - 70-100: Overbought (Aşırı alım) → SHORT sinyali
    
    Parametreler:
    -------------
    rsi : float
        RSI değeri (0-100 arası)
    
    Döndürür:
    ---------
    Dict : Sinyal bilgisi (signal, score, reason)
    """
    if rsi is None:
        return {"signal": "NEUTRAL", "score": 0, "reason": "RSI verisi yok"}
    
    if rsi < 30:
        return {
            "signal": "LONG",
            "score": 25,  # Maksimum puan
            "reason": f"RSI {rsi:.1f} - Oversold (Aşırı satım)"
        }
    elif rsi < 40:
        return {
            "signal": "LONG",
            "score": 15,
            "reason": f"RSI {rsi:.1f} - Düşük bölge"
        }
    elif rsi < 50:
        return {
            "signal": "LONG",
            "score": 5,
            "reason": f"RSI {rsi:.1f} - Hafif düşük"
        }
    elif rsi < 60:
        return {
            "signal": "SHORT",
            "score": -5,
            "reason": f"RSI {rsi:.1f} - Hafif yüksek"
        }
    elif rsi < 70:
        return {
            "signal": "SHORT",
            "score": -15,
            "reason": f"RSI {rsi:.1f} - Yüksek bölge"
        }
    else:
        return {
            "signal": "SHORT",
            "score": -25,
            "reason": f"RSI {rsi:.1f} - Overbought (Aşırı alım)"
        }


def calculate_macd_signal(macd: float, signal: float) -> Dict:
    """
    MACD değerlerine göre sinyal üretir.
    
    MACD Yorumlama:
    - MACD > Signal: Bullish (Yükseliş) → LONG
    - MACD < Signal: Bearish (Düşüş) → SHORT
    - Fark büyükse sinyal güçlü
    
    Parametreler:
    -------------
    macd : float
        MACD değeri
    signal : float
        Signal line değeri
    """
    if macd is None or signal is None:
        return {"signal": "NEUTRAL", "score": 0, "reason": "MACD verisi yok"}
    
    diff = macd - signal
    
    if diff > 0:
        score = min(20, diff * 1000)  # Farka göre puan
        return {
            "signal": "LONG",
            "score": score,
            "reason": f"MACD Bullish Crossover (Fark: {diff:.5f})"
        }
    else:
        score = max(-20, diff * 1000)
        return {
            "signal": "SHORT",
            "score": score,
            "reason": f"MACD Bearish Crossover (Fark: {diff:.5f})"
        }


def calculate_ema_signal(price: float, ema_20: float, ema_50: float, ema_200: float) -> Dict:
    """
    EMA değerlerine göre sinyal üretir.
    
    EMA Yorumlama:
    - Fiyat > EMA: Yükseliş trendi
    - EMA20 > EMA50 > EMA200: Golden order (güçlü yükseliş)
    - EMA20 < EMA50 < EMA200: Death order (güçlü düşüş)
    """
    if None in [price, ema_20, ema_50, ema_200]:
        return {"signal": "NEUTRAL", "score": 0, "reason": "EMA verisi eksik"}
    
    score = 0
    reasons = []
    
    # Fiyat pozisyonu
    if price > ema_20:
        score += 5
        reasons.append("Fiyat EMA20 üstünde")
    else:
        score -= 5
        reasons.append("Fiyat EMA20 altında")
    
    if price > ema_50:
        score += 5
        reasons.append("Fiyat EMA50 üstünde")
    else:
        score -= 5
        reasons.append("Fiyat EMA50 altında")
    
    if price > ema_200:
        score += 5
        reasons.append("Fiyat EMA200 üstünde")
    else:
        score -= 5
        reasons.append("Fiyat EMA200 altında")
    
    # EMA sıralaması
    if ema_20 > ema_50 > ema_200:
        score += 10
        reasons.append("Golden Order (güçlü yükseliş)")
    elif ema_20 < ema_50 < ema_200:
        score -= 10
        reasons.append("Death Order (güçlü düşüş)")
    
    signal = "LONG" if score > 0 else "SHORT" if score < 0 else "NEUTRAL"
    
    return {
        "signal": signal,
        "score": score,
        "reason": " | ".join(reasons[:2])  # İlk 2 sebep
    }


def calculate_stochastic_signal(k: float, d: float) -> Dict:
    """
    Stochastic Oscillator sinyali.
    
    Yorumlama:
    - K < 20: Oversold → LONG
    - K > 80: Overbought → SHORT
    - K > D: Bullish
    - K < D: Bearish
    """
    if k is None or d is None:
        return {"signal": "NEUTRAL", "score": 0, "reason": "Stochastic verisi yok"}
    
    score = 0
    
    # Oversold/Overbought
    if k < 20:
        score += 15
        reason = f"Stoch K={k:.1f} - Oversold"
    elif k > 80:
        score -= 15
        reason = f"Stoch K={k:.1f} - Overbought"
    elif k > d:
        score += 5
        reason = f"Stoch K({k:.1f}) > D({d:.1f}) - Bullish"
    else:
        score -= 5
        reason = f"Stoch K({k:.1f}) < D({d:.1f}) - Bearish"
    
    signal = "LONG" if score > 0 else "SHORT" if score < 0 else "NEUTRAL"
    
    return {"signal": signal, "score": score, "reason": reason}


def calculate_bollinger_signal(price: float, upper: float, lower: float) -> Dict:
    """
    Bollinger Bands sinyali.
    
    Yorumlama:
    - Fiyat alt banda yakın: LONG (bounce beklentisi)
    - Fiyat üst banda yakın: SHORT (bounce beklentisi)
    """
    if None in [price, upper, lower]:
        return {"signal": "NEUTRAL", "score": 0, "reason": "Bollinger verisi yok"}
    
    band_width = upper - lower
    position = (price - lower) / band_width if band_width > 0 else 0.5
    
    if position < 0.2:
        return {
            "signal": "LONG",
            "score": 15,
            "reason": f"Fiyat alt banda yakın ({position:.0%})"
        }
    elif position > 0.8:
        return {
            "signal": "SHORT",
            "score": -15,
            "reason": f"Fiyat üst banda yakın ({position:.0%})"
        }
    else:
        return {
            "signal": "NEUTRAL",
            "score": 0,
            "reason": f"Fiyat bant ortasında ({position:.0%})"
        }


def calculate_probability(analysis_data: Dict, session_data: Dict = None) -> Dict:
    """
    Tüm indikatörleri birleştirip final olasılık hesaplar.
    
    Parametreler:
    -------------
    analysis_data : Dict
        price_fetcher'dan gelen analiz verisi
    session_data : Dict
        session_tracker'dan gelen session verisi
    
    Döndürür:
    ---------
    Dict : Long/Short olasılıkları ve detaylı analiz
    """
    if not analysis_data.get("success"):
        return {
            "success": False,
            "error": analysis_data.get("error", "Analiz verisi alınamadı")
        }
    
    indicators = analysis_data.get("indicators", {})
    price_data = analysis_data.get("price", {})
    
    # Her indikatörden sinyal al
    signals = {}
    
    # RSI
    signals["RSI"] = calculate_rsi_signal(indicators.get("RSI"))
    
    # MACD
    macd_data = indicators.get("MACD", {})
    signals["MACD"] = calculate_macd_signal(
        macd_data.get("macd"),
        macd_data.get("signal")
    )
    
    # EMA
    signals["EMA"] = calculate_ema_signal(
        price_data.get("close"),
        indicators.get("EMA_20"),
        indicators.get("EMA_50"),
        indicators.get("EMA_200")
    )
    
    # Stochastic
    stoch_data = indicators.get("Stochastic", {})
    signals["Stochastic"] = calculate_stochastic_signal(
        stoch_data.get("k"),
        stoch_data.get("d")
    )
    
    # Bollinger
    bb_data = indicators.get("Bollinger", {})
    signals["Bollinger"] = calculate_bollinger_signal(
        price_data.get("close"),
        bb_data.get("upper"),
        bb_data.get("lower")
    )
    
    # Toplam skor hesapla
    total_score = sum(s["score"] for s in signals.values())
    
    # Session bonusu (eğer kill zone aktifse)
    session_bonus = 0
    session_info = None
    if session_data:
        active_sessions = session_data.get("active_sessions", [])
        for session in active_sessions:
            if session.get("is_kill_zone"):
                session_bonus = 10 if total_score > 0 else -10
                session_info = f"{session['emoji']} {session['name']} Kill Zone aktif!"
                break
    
    final_score = total_score + session_bonus
    
    # Olasılık hesapla (-100 ile +100 arası skoru 0-100'e çevir)
    # Basit formül: (score + 100) / 2
    long_probability = min(100, max(0, (final_score + 100) / 2))
    short_probability = 100 - long_probability
    
    # Ana öneri
    if long_probability >= 65:
        recommendation = "STRONG_LONG"
        recommendation_text = "💪 GÜÇLÜ LONG"
    elif long_probability >= 55:
        recommendation = "LONG"
        recommendation_text = "📈 LONG"
    elif short_probability >= 65:
        recommendation = "STRONG_SHORT"
        recommendation_text = "💪 GÜÇLÜ SHORT"
    elif short_probability >= 55:
        recommendation = "SHORT"
        recommendation_text = "📉 SHORT"
    else:
        recommendation = "NEUTRAL"
        recommendation_text = "⚖️ NÖTR"
    
    return {
        "success": True,
        "symbol": analysis_data.get("symbol"),
        "interval": analysis_data.get("interval"),
        "price": price_data,
        
        "probability": {
            "long": round(long_probability, 1),
            "short": round(short_probability, 1)
        },
        
        "recommendation": recommendation,
        "recommendation_text": recommendation_text,
        
        "scores": {
            "technical": total_score,
            "session_bonus": session_bonus,
            "final": final_score
        },
        
        "signals": signals,
        "session_info": session_info,
        
        "tradingview_summary": analysis_data.get("summary")
    }


# Test kodu
if __name__ == "__main__":
    # Örnek veri ile test
    test_analysis = {
        "success": True,
        "symbol": "EURUSD",
        "interval": "1h",
        "price": {"close": 1.0850, "open": 1.0840, "high": 1.0860, "low": 1.0830},
        "indicators": {
            "RSI": 35,
            "MACD": {"macd": 0.0002, "signal": 0.0001},
            "EMA_20": 1.0845,
            "EMA_50": 1.0840,
            "EMA_200": 1.0820,
            "Stochastic": {"k": 25, "d": 30},
            "Bollinger": {"upper": 1.0900, "lower": 1.0800}
        },
        "summary": {"RECOMMENDATION": "BUY"}
    }
    
    result = calculate_probability(test_analysis)
    
    print("=" * 50)
    print(f"  {result['symbol']} ANALİZ SONUCU")
    print("=" * 50)
    print(f"\n📈 LONG:  %{result['probability']['long']}")
    print(f"📉 SHORT: %{result['probability']['short']}")
    print(f"\n🎯 ÖNERİ: {result['recommendation_text']}")
    print(f"\n📊 Teknik Skor: {result['scores']['technical']}")
    print("\n📋 İndikatör Detayları:")
    for name, signal in result['signals'].items():
        emoji = "✅" if signal['signal'] == "LONG" else "❌" if signal['signal'] == "SHORT" else "⚪"
        print(f"   {emoji} {name}: {signal['reason']}")

