# ============================================
# STRATEGY ANALYZER - Strateji Analizi & Yön Tahmini
# ============================================
# Net Long/Short sinyali ve güven skoru hesaplar

from typing import Dict, List
from datetime import datetime

def analyze_trend_direction(candles: List[Dict]) -> Dict:
    """
    Mum verilerinden trend yönünü analiz eder.
    """
    if len(candles) < 5:
        return {"error": "Yetersiz veri"}
    
    closes = [c['close'] for c in candles]
    opens = [c['open'] for c in candles]
    highs = [c['high'] for c in candles]
    lows = [c['low'] for c in candles]
    
    # Son 5 mum analizi
    recent_closes = closes[-5:]
    
    # EMA hesapla (basit)
    ema_5 = sum(closes[-5:]) / 5
    ema_10 = sum(closes[-10:]) / 10 if len(closes) >= 10 else ema_5
    ema_20 = sum(closes[-20:]) / 20 if len(closes) >= 20 else ema_10
    
    current_price = closes[-1]
    
    # Trend skorları
    trend_score = 0
    signals = []
    
    # 1. Fiyat EMA'ların üstünde/altında mı?
    if current_price > ema_5:
        trend_score += 15
        signals.append({"name": "Fiyat > EMA5", "type": "LONG", "weight": 15})
    else:
        trend_score -= 15
        signals.append({"name": "Fiyat < EMA5", "type": "SHORT", "weight": 15})
    
    if current_price > ema_10:
        trend_score += 15
        signals.append({"name": "Fiyat > EMA10", "type": "LONG", "weight": 15})
    else:
        trend_score -= 15
        signals.append({"name": "Fiyat < EMA10", "type": "SHORT", "weight": 15})
    
    if current_price > ema_20:
        trend_score += 10
        signals.append({"name": "Fiyat > EMA20", "type": "LONG", "weight": 10})
    else:
        trend_score -= 10
        signals.append({"name": "Fiyat < EMA20", "type": "SHORT", "weight": 10})
    
    # 2. EMA sıralaması
    if ema_5 > ema_10 > ema_20:
        trend_score += 20
        signals.append({"name": "EMA Bullish Order", "type": "LONG", "weight": 20})
    elif ema_5 < ema_10 < ema_20:
        trend_score -= 20
        signals.append({"name": "EMA Bearish Order", "type": "SHORT", "weight": 20})
    
    # 3. Son 5 mumun yönü
    bullish_candles = sum(1 for i in range(-5, 0) if closes[i] > opens[i])
    bearish_candles = 5 - bullish_candles
    
    if bullish_candles >= 4:
        trend_score += 15
        signals.append({"name": f"Son 5 mum: {bullish_candles} yeşil", "type": "LONG", "weight": 15})
    elif bearish_candles >= 4:
        trend_score -= 15
        signals.append({"name": f"Son 5 mum: {bearish_candles} kırmızı", "type": "SHORT", "weight": 15})
    
    # 4. Higher High / Lower Low analizi
    if highs[-1] > highs[-2] and lows[-1] > lows[-2]:
        trend_score += 10
        signals.append({"name": "Higher High + Higher Low", "type": "LONG", "weight": 10})
    elif highs[-1] < highs[-2] and lows[-1] < lows[-2]:
        trend_score -= 10
        signals.append({"name": "Lower High + Lower Low", "type": "SHORT", "weight": 10})
    
    # 5. Momentum (son 3 mum toplam değişim)
    momentum = ((closes[-1] - closes[-4]) / closes[-4]) * 100 if len(closes) >= 4 else 0
    if momentum > 1:
        trend_score += 15
        signals.append({"name": f"Güçlü momentum: +{momentum:.2f}%", "type": "LONG", "weight": 15})
    elif momentum < -1:
        trend_score -= 15
        signals.append({"name": f"Zayıf momentum: {momentum:.2f}%", "type": "SHORT", "weight": 15})
    
    return {
        "trend_score": trend_score,
        "ema_5": round(ema_5, 2),
        "ema_10": round(ema_10, 2),
        "ema_20": round(ema_20, 2),
        "current_price": round(current_price, 2),
        "momentum_percent": round(momentum, 2),
        "bullish_candles": bullish_candles,
        "bearish_candles": bearish_candles,
        "signals": signals
    }


def calculate_support_resistance(candles: List[Dict]) -> Dict:
    """
    Destek ve direnç seviyelerini hesaplar.
    """
    if len(candles) < 10:
        return {"error": "Yetersiz veri"}
    
    highs = [c['high'] for c in candles]
    lows = [c['low'] for c in candles]
    closes = [c['close'] for c in candles]
    
    current_price = closes[-1]
    
    # Pivot Point hesaplama (klasik)
    high = max(highs[-24:]) if len(highs) >= 24 else max(highs)
    low = min(lows[-24:]) if len(lows) >= 24 else min(lows)
    close = closes[-1]
    
    pivot = (high + low + close) / 3
    
    r1 = 2 * pivot - low
    r2 = pivot + (high - low)
    r3 = high + 2 * (pivot - low)
    
    s1 = 2 * pivot - high
    s2 = pivot - (high - low)
    s3 = low - 2 * (high - pivot)
    
    # En yakın destek ve direnç
    resistances = [r for r in [r1, r2, r3] if r > current_price]
    supports = [s for s in [s1, s2, s3] if s < current_price]
    
    nearest_resistance = min(resistances) if resistances else r1
    nearest_support = max(supports) if supports else s1
    
    # Risk/Reward hesapla
    risk = current_price - nearest_support
    reward = nearest_resistance - current_price
    rr_ratio = reward / risk if risk > 0 else 0
    
    return {
        "pivot": round(pivot, 2),
        "resistance_1": round(r1, 2),
        "resistance_2": round(r2, 2),
        "resistance_3": round(r3, 2),
        "support_1": round(s1, 2),
        "support_2": round(s2, 2),
        "support_3": round(s3, 2),
        "nearest_resistance": round(nearest_resistance, 2),
        "nearest_support": round(nearest_support, 2),
        "current_price": round(current_price, 2),
        "risk_reward_ratio": round(rr_ratio, 2)
    }


def generate_trade_signal(candles: List[Dict], ict_analysis: Dict = None) -> Dict:
    """
    Tüm analizleri birleştirip net bir trade sinyali üretir.
    
    Returns:
        direction: "LONG" | "SHORT" | "WAIT"
        confidence: 0-100 arası güven skoru
        entry_price: Önerilen giriş fiyatı
        stop_loss: Stop loss seviyesi
        take_profit: Take profit seviyesi
    """
    if len(candles) < 10:
        return {"error": "Yetersiz veri"}
    
    # Trend analizi
    trend = analyze_trend_direction(candles)
    trend_score = trend.get('trend_score', 0)
    
    # Destek/Direnç
    sr = calculate_support_resistance(candles)
    
    current_price = candles[-1]['close']
    
    # ICT analizinden ekstra skorlar
    ict_score = 0
    ict_signals = []
    
    if ict_analysis:
        # Kill Zone bonusu
        active_zone = ict_analysis.get('kill_zones', {}).get('active_zone')
        if active_zone:
            ict_score += 10
            ict_signals.append(f"✅ {active_zone.get('name', 'Kill Zone')} aktif")
        
        # Premium/Discount
        pd = ict_analysis.get('premium_discount', {})
        zone = pd.get('current_zone')
        if zone == 'DISCOUNT':
            ict_score += 15  # Long için iyi
            ict_signals.append("✅ Discount zone - Alım bölgesi")
        elif zone == 'PREMIUM':
            ict_score -= 15  # Short için iyi
            ict_signals.append("✅ Premium zone - Satış bölgesi")
        
        # Market Structure
        ms = ict_analysis.get('market_structure', {})
        if ms.get('bos_detected'):
            if 'BULLISH' in (ms.get('bos_type') or ''):
                ict_score += 20
                ict_signals.append("✅ Bullish BOS tespit edildi")
            elif 'BEARISH' in (ms.get('bos_type') or ''):
                ict_score -= 20
                ict_signals.append("✅ Bearish BOS tespit edildi")
        
        # Order Blocks
        obs = ict_analysis.get('order_blocks', [])
        for ob in obs:
            if ob.get('type') == 'BULLISH_OB' and current_price <= ob.get('high', 0):
                ict_score += 10
                ict_signals.append("✅ Fiyat Bullish OB'de")
            elif ob.get('type') == 'BEARISH_OB' and current_price >= ob.get('low', 0):
                ict_score -= 10
                ict_signals.append("✅ Fiyat Bearish OB'de")
    
    # Toplam skor
    total_score = trend_score + ict_score
    
    # Yön belirleme - GERÇEKÇİ ORANLAR
    # Trading'de %60-70 bile çok iyi bir oran
    # %75 üstü = çok güçlü sinyal (nadir)
    # %55-65 = normal sinyal
    # %50-55 = zayıf sinyal
    
    if total_score >= 50:
        direction = "LONG"
        direction_emoji = "🟢"
        direction_text = "YUKARI - LONG AÇ"
        # Max %75, genelde %58-68 arası
        confidence = min(75, 52 + (total_score * 0.3))
        entry = current_price
        stop_loss = sr.get('nearest_support', current_price * 0.98)
        take_profit_1 = sr.get('resistance_1', current_price * 1.02)
        take_profit_2 = sr.get('resistance_2', current_price * 1.04)
    elif total_score <= -50:
        direction = "SHORT"
        direction_emoji = "🔴"
        direction_text = "AŞAĞI - SHORT AÇ"
        # Max %75, genelde %58-68 arası
        confidence = min(75, 52 + (abs(total_score) * 0.3))
        entry = current_price
        stop_loss = sr.get('nearest_resistance', current_price * 1.02)
        take_profit_1 = sr.get('support_1', current_price * 0.98)
        take_profit_2 = sr.get('support_2', current_price * 0.96)
    elif total_score >= 25:
        direction = "LONG"
        direction_emoji = "🟢"
        direction_text = "HAFİF YUKARI - DİKKATLİ OL"
        confidence = 50 + (total_score * 0.2)
        entry = current_price
        stop_loss = sr.get('nearest_support', current_price * 0.98)
        take_profit_1 = sr.get('resistance_1', current_price * 1.02)
        take_profit_2 = sr.get('resistance_2', current_price * 1.04)
    elif total_score <= -25:
        direction = "SHORT"
        direction_emoji = "🔴"
        direction_text = "HAFİF AŞAĞI - DİKKATLİ OL"
        confidence = 50 + (abs(total_score) * 0.2)
        entry = current_price
        stop_loss = sr.get('nearest_resistance', current_price * 1.02)
        take_profit_1 = sr.get('support_1', current_price * 0.98)
        take_profit_2 = sr.get('support_2', current_price * 0.96)
    else:
        direction = "WAIT"
        direction_emoji = "🟡"
        direction_text = "BEKLE - NET SİNYAL YOK"
        confidence = 45 + (abs(total_score) * 0.1)
        entry = current_price
        stop_loss = sr.get('nearest_support', current_price * 0.98)
        take_profit_1 = sr.get('resistance_1', current_price * 1.02)
        take_profit_2 = sr.get('resistance_2', current_price * 1.04)
    
    # Güven oranını sınırla (gerçekçi aralık)
    confidence = max(45, min(75, confidence))
    
    # Risk/Reward
    risk = abs(entry - stop_loss)
    reward = abs(take_profit_1 - entry)
    rr_ratio = reward / risk if risk > 0 else 0
    
    return {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        
        # Ana Sinyal
        "direction": direction,
        "direction_emoji": direction_emoji,
        "direction_text": direction_text,
        "confidence": round(confidence, 1),
        
        # Trade Planı
        "trade_plan": {
            "entry_price": round(entry, 2),
            "stop_loss": round(stop_loss, 2),
            "take_profit_1": round(take_profit_1, 2),
            "take_profit_2": round(take_profit_2, 2),
            "risk_reward": round(rr_ratio, 2),
            "risk_percent": round((risk / entry) * 100, 2),
        },
        
        # Skorlar
        "scores": {
            "trend_score": trend_score,
            "ict_score": ict_score,
            "total_score": total_score,
        },
        
        # Destek/Direnç
        "levels": sr,
        
        # Sinyaller
        "trend_signals": trend.get('signals', []),
        "ict_signals": ict_signals,
        
        # EMA değerleri
        "ema": {
            "ema_5": trend.get('ema_5'),
            "ema_10": trend.get('ema_10'),
            "ema_20": trend.get('ema_20'),
        }
    }


# Test
if __name__ == "__main__":
    # Test verisi
    test_candles = [
        {"open": 100, "high": 102, "low": 99, "close": 101, "timestamp": "2025-01-01 01:00"},
        {"open": 101, "high": 103, "low": 100, "close": 102, "timestamp": "2025-01-01 02:00"},
        {"open": 102, "high": 104, "low": 101, "close": 103, "timestamp": "2025-01-01 03:00"},
        {"open": 103, "high": 105, "low": 102, "close": 104, "timestamp": "2025-01-01 04:00"},
        {"open": 104, "high": 106, "low": 103, "close": 105, "timestamp": "2025-01-01 05:00"},
        {"open": 105, "high": 107, "low": 104, "close": 106, "timestamp": "2025-01-01 06:00"},
        {"open": 106, "high": 108, "low": 105, "close": 107, "timestamp": "2025-01-01 07:00"},
        {"open": 107, "high": 109, "low": 106, "close": 108, "timestamp": "2025-01-01 08:00"},
        {"open": 108, "high": 110, "low": 107, "close": 109, "timestamp": "2025-01-01 09:00"},
        {"open": 109, "high": 111, "low": 108, "close": 110, "timestamp": "2025-01-01 10:00"},
    ]
    
    signal = generate_trade_signal(test_candles)
    
    print("=" * 50)
    print(f"  {signal['direction_emoji']} {signal['direction_text']}")
    print("=" * 50)
    print(f"  Güven: %{signal['confidence']}")
    print(f"  Giriş: ${signal['trade_plan']['entry_price']}")
    print(f"  Stop Loss: ${signal['trade_plan']['stop_loss']}")
    print(f"  TP1: ${signal['trade_plan']['take_profit_1']}")
    print(f"  TP2: ${signal['trade_plan']['take_profit_2']}")
    print(f"  R/R: {signal['trade_plan']['risk_reward']}")
    print("=" * 50)

