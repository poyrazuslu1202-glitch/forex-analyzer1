# ============================================
# ICT CONCEPTS - Inner Circle Trader Stratejileri
# ============================================
# Kill Zones, Fair Value Gaps, Order Blocks, Market Structure

from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional
import pandas as pd

# ============================================
# KILL ZONES (ICT)
# ============================================
# ICT'nin tanımladığı en aktif trading saatleri

ICT_KILL_ZONES = {
    "ASIAN": {
        "name": "Asian Kill Zone",
        "alias": "Asya Seansı",
        "start_utc": 0,   # 00:00 UTC
        "end_utc": 4,     # 04:00 UTC
        "start_turkey": 3,
        "end_turkey": 7,
        "color": "#F7931A",  # Turuncu
        "description": "Tokyo açılışı, düşük volatilite, konsolidasyon",
        "emoji": "🌏",
        "characteristics": [
            "Düşük hacim",
            "Range oluşumu",
            "Likidite birikimi",
            "Stop hunt için hazırlık"
        ]
    },
    "LONDON": {
        "name": "London Kill Zone", 
        "alias": "Londra Seansı",
        "start_utc": 7,   # 07:00 UTC
        "end_utc": 10,    # 10:00 UTC
        "start_turkey": 10,
        "end_turkey": 13,
        "color": "#2962FF",  # Mavi
        "description": "En yüksek volatilite, trend başlangıcı",
        "emoji": "🇬🇧",
        "characteristics": [
            "Yüksek hacim",
            "Asian range kırılımı",
            "Güçlü trend hareketleri",
            "Stop hunt"
        ]
    },
    "NEW_YORK": {
        "name": "New York Kill Zone",
        "alias": "New York Seansı", 
        "start_utc": 12,  # 12:00 UTC
        "end_utc": 15,    # 15:00 UTC
        "start_turkey": 15,
        "end_turkey": 18,
        "color": "#089981",  # Yeşil
        "description": "Yüksek volatilite, London ile overlap",
        "emoji": "🇺🇸",
        "characteristics": [
            "Çok yüksek hacim",
            "News event'ler",
            "Reversal potansiyeli",
            "Günün en iyi fırsatları"
        ]
    },
    "LONDON_CLOSE": {
        "name": "London Close",
        "alias": "Londra Kapanışı",
        "start_utc": 15,  # 15:00 UTC
        "end_utc": 17,    # 17:00 UTC
        "start_turkey": 18,
        "end_turkey": 20,
        "color": "#787B86",  # Gri
        "description": "Pozisyon kapatma, reversal",
        "emoji": "🌆",
        "characteristics": [
            "Pozisyon kapatma",
            "Reversal hareketleri",
            "Azalan hacim",
            "Range'e dönüş"
        ]
    }
}


def get_current_kill_zone() -> Optional[Dict]:
    """
    Şu an hangi kill zone aktif olduğunu döndürür.
    """
    utc_now = datetime.now(timezone.utc)
    current_hour = utc_now.hour
    
    for zone_id, zone in ICT_KILL_ZONES.items():
        if zone["start_utc"] <= current_hour < zone["end_utc"]:
            return {
                "id": zone_id,
                "active": True,
                "minutes_remaining": (zone["end_utc"] - current_hour - 1) * 60 + (60 - utc_now.minute),
                **zone
            }
    
    return None


def get_all_kill_zones_status() -> Dict:
    """
    Tüm kill zone'ların durumunu döndürür.
    """
    utc_now = datetime.now(timezone.utc)
    turkey_now = utc_now + timedelta(hours=3)
    current_hour = utc_now.hour
    
    zones_status = []
    active_zone = None
    
    for zone_id, zone in ICT_KILL_ZONES.items():
        is_active = zone["start_utc"] <= current_hour < zone["end_utc"]
        
        # Sonraki zone'a kalan süre
        if current_hour < zone["start_utc"]:
            hours_until = zone["start_utc"] - current_hour
            minutes_until = hours_until * 60 - utc_now.minute
        else:
            # Yarın
            hours_until = 24 - current_hour + zone["start_utc"]
            minutes_until = hours_until * 60 - utc_now.minute
        
        zone_data = {
            "id": zone_id,
            "is_active": is_active,
            "minutes_until_start": minutes_until if not is_active else 0,
            "minutes_remaining": (zone["end_utc"] - current_hour - 1) * 60 + (60 - utc_now.minute) if is_active else 0,
            **zone
        }
        
        zones_status.append(zone_data)
        
        if is_active:
            active_zone = zone_data
    
    return {
        "current_time_utc": utc_now.strftime("%H:%M"),
        "current_time_turkey": turkey_now.strftime("%H:%M"),
        "active_zone": active_zone,
        "zones": zones_status
    }


# ============================================
# MARKET STRUCTURE (ICT)
# ============================================

def analyze_market_structure(candles: List[Dict]) -> Dict:
    """
    ICT Market Structure analizi yapar.
    
    - Higher Highs (HH) / Lower Lows (LL)
    - Break of Structure (BOS)
    - Change of Character (CHoCH)
    """
    if len(candles) < 5:
        return {"error": "Yetersiz veri"}
    
    highs = [c['high'] for c in candles]
    lows = [c['low'] for c in candles]
    
    # Son 5 mum için swing high/low bul
    recent_highs = highs[-5:]
    recent_lows = lows[-5:]
    
    # Trend belirleme
    if highs[-1] > highs[-3] and lows[-1] > lows[-3]:
        trend = "BULLISH"
        structure = "Higher High + Higher Low"
        emoji = "📈"
    elif highs[-1] < highs[-3] and lows[-1] < lows[-3]:
        trend = "BEARISH"
        structure = "Lower High + Lower Low"
        emoji = "📉"
    else:
        trend = "RANGING"
        structure = "Konsolidasyon"
        emoji = "↔️"
    
    # BOS (Break of Structure) kontrolü
    bos_detected = False
    bos_type = None
    
    if len(candles) >= 3:
        prev_high = max(highs[-4:-1])
        prev_low = min(lows[-4:-1])
        current_close = candles[-1]['close']
        
        if current_close > prev_high:
            bos_detected = True
            bos_type = "BULLISH BOS"
        elif current_close < prev_low:
            bos_detected = True
            bos_type = "BEARISH BOS"
    
    return {
        "trend": trend,
        "trend_emoji": emoji,
        "structure": structure,
        "bos_detected": bos_detected,
        "bos_type": bos_type,
        "swing_high": max(recent_highs),
        "swing_low": min(recent_lows)
    }


# ============================================
# FAIR VALUE GAP (FVG) - ICT
# ============================================

def find_fair_value_gaps(candles: List[Dict]) -> List[Dict]:
    """
    Fair Value Gap (FVG) / Imbalance bölgelerini bulur.
    
    FVG: 3 ardışık mumda, 1. mumun high'ı ile 3. mumun low'u arasında boşluk
    """
    fvgs = []
    
    if len(candles) < 3:
        return fvgs
    
    for i in range(len(candles) - 2):
        candle1 = candles[i]
        candle2 = candles[i + 1]
        candle3 = candles[i + 2]
        
        # Bullish FVG: 1. mum high < 3. mum low
        if candle1['high'] < candle3['low']:
            fvgs.append({
                "type": "BULLISH_FVG",
                "emoji": "🟢",
                "top": candle3['low'],
                "bottom": candle1['high'],
                "midpoint": (candle3['low'] + candle1['high']) / 2,
                "timestamp": candle2['timestamp'],
                "description": "Bullish Fair Value Gap - Potansiyel destek"
            })
        
        # Bearish FVG: 1. mum low > 3. mum high
        if candle1['low'] > candle3['high']:
            fvgs.append({
                "type": "BEARISH_FVG",
                "emoji": "🔴",
                "top": candle1['low'],
                "bottom": candle3['high'],
                "midpoint": (candle1['low'] + candle3['high']) / 2,
                "timestamp": candle2['timestamp'],
                "description": "Bearish Fair Value Gap - Potansiyel direnç"
            })
    
    return fvgs[-3:] if len(fvgs) > 3 else fvgs  # Son 3 FVG


# ============================================
# ORDER BLOCKS (ICT)
# ============================================

def find_order_blocks(candles: List[Dict]) -> List[Dict]:
    """
    Order Block'ları bulur.
    
    Order Block: Güçlü hareket öncesi son ters yönlü mum
    """
    order_blocks = []
    
    if len(candles) < 4:
        return order_blocks
    
    for i in range(1, len(candles) - 2):
        prev_candle = candles[i - 1]
        current_candle = candles[i]
        next_candles = candles[i + 1:i + 3]
        
        # Mum yönlerini belirle
        current_bullish = current_candle['close'] > current_candle['open']
        current_bearish = current_candle['close'] < current_candle['open']
        
        # Sonraki mumlarda güçlü hareket var mı?
        if len(next_candles) >= 2:
            next_move = next_candles[-1]['close'] - current_candle['close']
            move_percent = abs(next_move / current_candle['close']) * 100
            
            # Bullish Order Block (düşüş sonrası son bearish mum)
            if current_bearish and next_move > 0 and move_percent > 0.3:
                order_blocks.append({
                    "type": "BULLISH_OB",
                    "emoji": "🟩",
                    "high": current_candle['high'],
                    "low": current_candle['low'],
                    "timestamp": current_candle['timestamp'],
                    "description": "Bullish Order Block - Potansiyel alım bölgesi"
                })
            
            # Bearish Order Block (yükseliş sonrası son bullish mum)
            if current_bullish and next_move < 0 and move_percent > 0.3:
                order_blocks.append({
                    "type": "BEARISH_OB",
                    "emoji": "🟥",
                    "high": current_candle['high'],
                    "low": current_candle['low'],
                    "timestamp": current_candle['timestamp'],
                    "description": "Bearish Order Block - Potansiyel satış bölgesi"
                })
    
    return order_blocks[-2:] if len(order_blocks) > 2 else order_blocks


# ============================================
# PREMIUM / DISCOUNT ZONES
# ============================================

def calculate_premium_discount(candles: List[Dict]) -> Dict:
    """
    Premium ve Discount bölgelerini hesaplar.
    
    - Discount: Fiyatın altında, alım için ideal
    - Premium: Fiyatın üstünde, satış için ideal
    - Equilibrium: Orta nokta (%50)
    """
    if len(candles) < 10:
        return {"error": "Yetersiz veri"}
    
    highs = [c['high'] for c in candles]
    lows = [c['low'] for c in candles]
    
    range_high = max(highs)
    range_low = min(lows)
    current_price = candles[-1]['close']
    
    # Range hesapla
    total_range = range_high - range_low
    equilibrium = range_low + (total_range * 0.5)
    
    # Premium/Discount seviyeleri
    premium_zone = range_low + (total_range * 0.75)  # Üst %25
    discount_zone = range_low + (total_range * 0.25)  # Alt %25
    
    # Fiyat nerede?
    if current_price >= premium_zone:
        zone = "PREMIUM"
        zone_emoji = "🔴"
        suggestion = "Satış için ideal bölge"
    elif current_price <= discount_zone:
        zone = "DISCOUNT"
        zone_emoji = "🟢"
        suggestion = "Alım için ideal bölge"
    else:
        zone = "EQUILIBRIUM"
        zone_emoji = "🟡"
        suggestion = "Nötr bölge, yön bekle"
    
    # Yüzde pozisyon
    position_percent = ((current_price - range_low) / total_range) * 100 if total_range > 0 else 50
    
    return {
        "current_zone": zone,
        "zone_emoji": zone_emoji,
        "suggestion": suggestion,
        "position_percent": round(position_percent, 1),
        "levels": {
            "range_high": round(range_high, 2),
            "premium_zone": round(premium_zone, 2),
            "equilibrium": round(equilibrium, 2),
            "discount_zone": round(discount_zone, 2),
            "range_low": round(range_low, 2)
        },
        "current_price": round(current_price, 2)
    }


# ============================================
# ICT FULL ANALYSIS
# ============================================

def get_ict_analysis(candles: List[Dict]) -> Dict:
    """
    Tüm ICT analizlerini birleştirir.
    """
    kill_zones = get_all_kill_zones_status()
    market_structure = analyze_market_structure(candles)
    fvgs = find_fair_value_gaps(candles)
    order_blocks = find_order_blocks(candles)
    premium_discount = calculate_premium_discount(candles)
    
    return {
        "kill_zones": kill_zones,
        "market_structure": market_structure,
        "fair_value_gaps": fvgs,
        "order_blocks": order_blocks,
        "premium_discount": premium_discount
    }


# Test
if __name__ == "__main__":
    print("ICT Kill Zones Test:")
    print("=" * 50)
    
    status = get_all_kill_zones_status()
    print(f"🕐 UTC: {status['current_time_utc']}")
    print(f"🕐 TR:  {status['current_time_turkey']}")
    
    if status['active_zone']:
        az = status['active_zone']
        print(f"\n✅ AKTİF: {az['emoji']} {az['name']}")
        print(f"   Kalan: {az['minutes_remaining']} dakika")
    else:
        print("\n❌ Şu an aktif kill zone yok")
    
    print("\n📊 Tüm Kill Zones:")
    for zone in status['zones']:
        active = "✅" if zone['is_active'] else "⏳"
        print(f"   {active} {zone['emoji']} {zone['name']}: {zone['start_turkey']:02d}:00-{zone['end_turkey']:02d}:00 TR")

