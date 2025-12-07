# ============================================
# KILL ZONE STRATEGIES - ICT/TJR Stratejileri
# ============================================
# Asian Range, London Manipulation, NY Reversal
# Her Kill Zone'un özel davranışları ve stratejileri

from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional

# ============================================
# KILL ZONE BEHAVIORS - Her Zone'un Davranışları
# ============================================

KILLZONE_BEHAVIORS = {
    "ASIAN": {
        "name": "Asian Session",
        "emoji": "🌏",
        "primary_behavior": "RANGE FORMATION",
        "description": "Asya seansı genellikle düşük volatilite ile range oluşturur. Bu range, London ve NY için referans noktası olur.",
        "key_concepts": [
            {
                "name": "Asian Range",
                "emoji": "📦",
                "description": "Asia High ve Low - Günün en önemli seviyeleri",
                "how_to_use": "London açılışında bu seviyelerin kırılmasını bekle"
            },
            {
                "name": "Liquidity Pool",
                "emoji": "💧",
                "description": "Asian High/Low üzerinde stop loss'lar birikir",
                "how_to_use": "Smart Money bu likiditeyi avlar"
            },
            {
                "name": "Consolidation",
                "emoji": "⏸️",
                "description": "Düşük hacim, dar range",
                "how_to_use": "Trade yapma, sadece izle ve range'i belirle"
            }
        ],
        "strategies": [
            {
                "name": "Asian Range Breakout",
                "type": "BREAKOUT",
                "description": "London açılışında Asian High/Low kırılımını trade et",
                "entry": "Asian High kırılırsa LONG, Asian Low kırılırsa SHORT",
                "stop_loss": "Kırılan seviyenin diğer tarafı",
                "take_profit": "Range'in 1.5-2 katı"
            }
        ],
        "warning": "⚠️ Asia session'da trade yapma! Sadece range'i belirle.",
        "color": "#F7931A"
    },
    "LONDON": {
        "name": "London Session",
        "emoji": "🇬🇧",
        "primary_behavior": "MANIPULATION & TREND",
        "description": "En yüksek volatilite. İlk 30dk manipulation (fake move), sonra gerçek trend başlar.",
        "key_concepts": [
            {
                "name": "Judas Swing",
                "emoji": "🎭",
                "description": "İlk hareket genellikle YANLIŞ yöne olur",
                "how_to_use": "İlk 30dk bekle, fake move'u gör, sonra ters yönde gir"
            },
            {
                "name": "Stop Hunt",
                "emoji": "🎯",
                "description": "Asian High/Low sweep edilir",
                "how_to_use": "Sweep sonrası reversal için bekle"
            },
            {
                "name": "True Trend",
                "emoji": "📈",
                "description": "Manipulation sonrası gerçek günlük trend başlar",
                "how_to_use": "Sweep + reversal = Entry sinyali"
            }
        ],
        "strategies": [
            {
                "name": "London Sweep & Reverse",
                "type": "REVERSAL",
                "description": "Asian level sweep sonrası ters yönde trade",
                "entry": "Asian High sweep + bearish rejection = SHORT\nAsian Low sweep + bullish rejection = LONG",
                "stop_loss": "Sweep high/low üzeri",
                "take_profit": "Asian range'in diğer tarafı"
            },
            {
                "name": "London Breakout",
                "type": "TREND",
                "description": "Manipulation sonrası trend takibi",
                "entry": "Sweep + BOS (Break of Structure) sonrası",
                "stop_loss": "Son swing high/low",
                "take_profit": "1:2 veya 1:3 RR"
            }
        ],
        "warning": "⚠️ İlk 30 dakika TRADE YAPMA! Manipulation tamamlanmasını bekle.",
        "color": "#2962FF"
    },
    "NEW_YORK": {
        "name": "New York Session",
        "emoji": "🇺🇸",
        "primary_behavior": "CONTINUATION or REVERSAL",
        "description": "London trendini devam ettirir VEYA tersine çevirir. News event'lere dikkat!",
        "key_concepts": [
            {
                "name": "London Continuation",
                "emoji": "➡️",
                "description": "London trendi güçlüyse NY devam ettirir",
                "how_to_use": "Pullback'lerde trend yönünde gir"
            },
            {
                "name": "NY Reversal",
                "emoji": "🔄",
                "description": "London trend zayıfsa NY tersine çevirir",
                "how_to_use": "London high/low'da rejection ara"
            },
            {
                "name": "News Volatility",
                "emoji": "📰",
                "description": "Önemli ABD haberleri büyük hareketler yaratır",
                "how_to_use": "News öncesi pozisyon alma, sonra yönü takip et"
            }
        ],
        "strategies": [
            {
                "name": "NY Continuation",
                "type": "TREND",
                "description": "London trendini takip et",
                "entry": "London yönünde FVG veya OB'ye pullback",
                "stop_loss": "Swing high/low",
                "take_profit": "London high/low'un ötesi"
            },
            {
                "name": "NY Reversal",
                "type": "REVERSAL",
                "description": "Günlük high/low'da reversal",
                "entry": "Daily high/low + rejection candle",
                "stop_loss": "High/Low üzeri",
                "take_profit": "Equilibrium veya Asian range"
            }
        ],
        "warning": "⚠️ Büyük news saatlerinde dikkatli ol! Spread genişler.",
        "color": "#089981"
    },
    "LONDON_CLOSE": {
        "name": "London Close",
        "emoji": "🌆",
        "primary_behavior": "REVERSAL & PROFIT TAKING",
        "description": "Kurumlar pozisyon kapatır. Küçük reversal'lar olur.",
        "key_concepts": [
            {
                "name": "Profit Taking",
                "emoji": "💰",
                "description": "Günlük kazançlar realize edilir",
                "how_to_use": "Trend zayıflar, scalp fırsatları"
            },
            {
                "name": "Range Return",
                "emoji": "↩️",
                "description": "Fiyat equilibrium'a döner",
                "how_to_use": "Extremes'den mean reversion"
            }
        ],
        "strategies": [
            {
                "name": "LC Mean Reversion",
                "type": "REVERSAL",
                "description": "Günlük extremes'den geri dönüş",
                "entry": "Daily high/low'dan rejection",
                "stop_loss": "Extreme üzeri",
                "take_profit": "Daily equilibrium"
            }
        ],
        "warning": "⚠️ Büyük trade'ler için ideal değil. Scalp veya bekle.",
        "color": "#787B86"
    }
}


def calculate_asian_range(candles: List[Dict], asia_start_hour: int = 0, asia_end_hour: int = 4) -> Dict:
    """
    Asian Session Range'i hesaplar.
    
    Returns:
        - asian_high: Asia session'ın en yüksek fiyatı
        - asian_low: Asia session'ın en düşük fiyatı
        - asian_range: High - Low
        - current_position: Fiyat şu an nerede (above/below/inside)
    """
    if not candles:
        return {"error": "Veri yok"}
    
    # Asia session mumlarını bul (UTC 00:00 - 04:00)
    asia_candles = []
    
    for candle in candles:
        ts = candle.get('timestamp', '')
        try:
            # Timestamp'ten saat bilgisini çıkar
            if 'T' in str(ts):
                hour = int(str(ts).split('T')[1].split(':')[0])
            else:
                hour = int(str(ts).split(':')[0]) if ':' in str(ts) else -1
            
            if asia_start_hour <= hour < asia_end_hour:
                asia_candles.append(candle)
        except:
            continue
    
    if not asia_candles:
        # Tüm mumların ilk %20'sini Asia olarak kabul et
        asia_count = max(1, len(candles) // 5)
        asia_candles = candles[:asia_count]
    
    if not asia_candles:
        return {"error": "Asia verileri bulunamadı"}
    
    # High ve Low hesapla
    asian_high = max(c['high'] for c in asia_candles)
    asian_low = min(c['low'] for c in asia_candles)
    asian_range = asian_high - asian_low
    asian_mid = (asian_high + asian_low) / 2
    
    # Şu anki fiyat
    current_price = candles[-1]['close']
    
    # Pozisyon belirle
    if current_price > asian_high:
        position = "ABOVE"
        position_emoji = "⬆️"
        suggestion = "Asian High kırıldı - Bullish bias"
    elif current_price < asian_low:
        position = "BELOW"
        position_emoji = "⬇️"
        suggestion = "Asian Low kırıldı - Bearish bias"
    else:
        position = "INSIDE"
        position_emoji = "↔️"
        suggestion = "Hala Asian Range içinde - Breakout bekle"
    
    # Sweep kontrolü
    high_swept = any(c['high'] > asian_high for c in candles[len(asia_candles):])
    low_swept = any(c['low'] < asian_low for c in candles[len(asia_candles):])
    
    return {
        "asian_high": round(asian_high, 2),
        "asian_low": round(asian_low, 2),
        "asian_range": round(asian_range, 2),
        "asian_mid": round(asian_mid, 2),
        "current_price": round(current_price, 2),
        "position": position,
        "position_emoji": position_emoji,
        "suggestion": suggestion,
        "high_swept": high_swept,
        "low_swept": low_swept,
        "sweep_status": "🎯 High Swept!" if high_swept else ("🎯 Low Swept!" if low_swept else "No sweep yet")
    }


def get_active_killzone_strategy() -> Dict:
    """
    Şu anki aktif Kill Zone'a göre strateji önerileri döndürür.
    """
    utc_now = datetime.now(timezone.utc)
    turkey_now = utc_now + timedelta(hours=3)
    current_hour = utc_now.hour
    
    # Aktif zone'u bul
    active_zone = None
    active_zone_id = None
    
    zones_hours = {
        "ASIAN": (0, 4),
        "LONDON": (7, 10),
        "NEW_YORK": (12, 15),
        "LONDON_CLOSE": (15, 17)
    }
    
    for zone_id, (start, end) in zones_hours.items():
        if start <= current_hour < end:
            active_zone = KILLZONE_BEHAVIORS[zone_id]
            active_zone_id = zone_id
            break
    
    # Zone dışındaysa
    if not active_zone:
        # En yakın zone'u bul
        next_zone = None
        min_hours = 24
        
        for zone_id, (start, end) in zones_hours.items():
            hours_until = start - current_hour if start > current_hour else (24 - current_hour + start)
            if hours_until < min_hours:
                min_hours = hours_until
                next_zone = zone_id
        
        return {
            "is_active": False,
            "current_time_utc": utc_now.strftime("%H:%M"),
            "current_time_turkey": turkey_now.strftime("%H:%M"),
            "message": "Şu an aktif Kill Zone yok",
            "next_zone": next_zone,
            "next_zone_name": KILLZONE_BEHAVIORS[next_zone]["name"] if next_zone else None,
            "hours_until_next": min_hours,
            "suggestion": f"⏳ {KILLZONE_BEHAVIORS[next_zone]['name']}'a {min_hours} saat var. Bekle ve hazırlan." if next_zone else "Bekle"
        }
    
    # Aktif zone bilgileri
    minutes_in_zone = (current_hour - zones_hours[active_zone_id][0]) * 60 + utc_now.minute
    
    return {
        "is_active": True,
        "current_time_utc": utc_now.strftime("%H:%M"),
        "current_time_turkey": turkey_now.strftime("%H:%M"),
        "zone_id": active_zone_id,
        "zone": active_zone,
        "minutes_in_zone": minutes_in_zone,
        "phase": "EARLY" if minutes_in_zone < 30 else ("MID" if minutes_in_zone < 90 else "LATE"),
        "phase_suggestion": get_phase_suggestion(active_zone_id, minutes_in_zone)
    }


def get_phase_suggestion(zone_id: str, minutes: int) -> str:
    """
    Zone ve süreye göre ne yapılması gerektiğini söyler.
    """
    if zone_id == "ASIAN":
        return "📦 Range oluşuyor. High ve Low'u işaretle. Trade yapma!"
    
    elif zone_id == "LONDON":
        if minutes < 30:
            return "🎭 MANIPULATION FAZ! İlk hareket fake olabilir. BEKLE!"
        elif minutes < 60:
            return "🔍 Sweep kontrolü yap. Asian High/Low kırıldı mı?"
        else:
            return "📈 Gerçek trend başlamış olmalı. Entry ara!"
    
    elif zone_id == "NEW_YORK":
        if minutes < 30:
            return "🔄 London trendi devam mı reversal mı? Analiz et."
        else:
            return "📊 Trend belirgin. Continuation veya reversal trade'i al."
    
    elif zone_id == "LONDON_CLOSE":
        return "💰 Pozisyon kapat veya scalp yap. Büyük trade için uygun değil."
    
    return "Analiz et ve bekle."


def get_full_killzone_analysis(candles: List[Dict]) -> Dict:
    """
    Tam Kill Zone analizi döndürür.
    """
    asian_range = calculate_asian_range(candles)
    active_strategy = get_active_killzone_strategy()
    
    return {
        "asian_range": asian_range,
        "active_strategy": active_strategy,
        "all_behaviors": KILLZONE_BEHAVIORS
    }


# Test
if __name__ == "__main__":
    print("=" * 60)
    print("  KILL ZONE STRATEGY TEST")
    print("=" * 60)
    
    strategy = get_active_killzone_strategy()
    
    if strategy['is_active']:
        zone = strategy['zone']
        print(f"\n{zone['emoji']} AKTİF: {zone['name']}")
        print(f"📊 Davranış: {zone['primary_behavior']}")
        print(f"⏱️ Zone'da geçen süre: {strategy['minutes_in_zone']} dk")
        print(f"📍 Faz: {strategy['phase']}")
        print(f"\n💡 Öneri: {strategy['phase_suggestion']}")
        print(f"\n⚠️ {zone['warning']}")
    else:
        print(f"\n❌ Aktif Kill Zone yok")
        print(f"⏳ Sonraki: {strategy['next_zone_name']} ({strategy['hours_until_next']} saat)")
    
    print("=" * 60)

