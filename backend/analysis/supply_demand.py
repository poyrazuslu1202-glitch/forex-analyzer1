# ============================================
# SUPPLY & DEMAND ZONES - Arz ve Talep Bölgeleri
# ============================================
# ICT/SMC konseptlerine uygun Supply/Demand zone tespiti

from typing import Dict, List
from datetime import datetime

def find_supply_zones(candles: List[Dict], min_move_percent: float = 0.5) -> List[Dict]:
    """
    Supply Zone (Arz Bölgesi) bulur.
    
    Supply Zone: Fiyatın güçlü bir şekilde düştüğü bölge.
    Genellikle büyük bir bearish mum sonrası oluşur.
    
    Kriterler:
    - Güçlü bearish mum (en az %0.5 düşüş)
    - Sonraki mumlarda fiyat bu bölgeye geri dönmemiş
    - Bölge: O mumun high'ı ile open'ı arası
    """
    supply_zones = []
    
    if len(candles) < 5:
        return supply_zones
    
    for i in range(1, len(candles) - 2):
        candle = candles[i]
        prev_candle = candles[i - 1]
        
        open_price = candle['open']
        close_price = candle['close']
        high_price = candle['high']
        low_price = candle['low']
        
        # Bearish mum mu?
        if close_price >= open_price:
            continue
        
        # Yeterince güçlü mü?
        move_percent = ((open_price - close_price) / open_price) * 100
        if move_percent < min_move_percent:
            continue
        
        # Önceki mum bullish veya nötr mü? (demand'den supply'a geçiş)
        prev_bullish = prev_candle['close'] >= prev_candle['open']
        
        # Supply zone tanımla
        zone_top = high_price
        zone_bottom = max(open_price, close_price)  # Mumun gövdesinin üstü
        zone_mid = (zone_top + zone_bottom) / 2
        
        # Zone hala geçerli mi? (fiyat geri dönmemiş mi?)
        still_valid = True
        times_tested = 0
        
        for j in range(i + 1, len(candles)):
            future_high = candles[j]['high']
            if future_high >= zone_bottom:
                times_tested += 1
                if future_high >= zone_top:
                    still_valid = False
                    break
        
        # Fresh zone (hiç test edilmemiş) daha değerli
        freshness = "FRESH" if times_tested == 0 else f"TESTED ({times_tested}x)"
        
        if still_valid or times_tested <= 2:
            supply_zones.append({
                "type": "SUPPLY",
                "emoji": "🔴",
                "zone_top": round(zone_top, 2),
                "zone_bottom": round(zone_bottom, 2),
                "zone_mid": round(zone_mid, 2),
                "strength": round(move_percent, 2),
                "timestamp": candle['timestamp'],
                "freshness": freshness,
                "still_valid": still_valid,
                "times_tested": times_tested,
                "description": f"Supply Zone - {freshness}"
            })
    
    # En güçlü ve en yakın zone'ları döndür
    supply_zones.sort(key=lambda x: (-x['strength'], x['times_tested']))
    return supply_zones[:5]


def find_demand_zones(candles: List[Dict], min_move_percent: float = 0.5) -> List[Dict]:
    """
    Demand Zone (Talep Bölgesi) bulur.
    
    Demand Zone: Fiyatın güçlü bir şekilde yükseldiği bölge.
    Genellikle büyük bir bullish mum sonrası oluşur.
    
    Kriterler:
    - Güçlü bullish mum (en az %0.5 yükseliş)
    - Sonraki mumlarda fiyat bu bölgeye geri dönmemiş
    - Bölge: O mumun low'u ile open'ı arası
    """
    demand_zones = []
    
    if len(candles) < 5:
        return demand_zones
    
    for i in range(1, len(candles) - 2):
        candle = candles[i]
        prev_candle = candles[i - 1]
        
        open_price = candle['open']
        close_price = candle['close']
        high_price = candle['high']
        low_price = candle['low']
        
        # Bullish mum mu?
        if close_price <= open_price:
            continue
        
        # Yeterince güçlü mü?
        move_percent = ((close_price - open_price) / open_price) * 100
        if move_percent < min_move_percent:
            continue
        
        # Önceki mum bearish veya nötr mü? (supply'dan demand'e geçiş)
        prev_bearish = prev_candle['close'] <= prev_candle['open']
        
        # Demand zone tanımla
        zone_bottom = low_price
        zone_top = min(open_price, close_price)  # Mumun gövdesinin altı
        zone_mid = (zone_top + zone_bottom) / 2
        
        # Zone hala geçerli mi? (fiyat geri dönmemiş mi?)
        still_valid = True
        times_tested = 0
        
        for j in range(i + 1, len(candles)):
            future_low = candles[j]['low']
            if future_low <= zone_top:
                times_tested += 1
                if future_low <= zone_bottom:
                    still_valid = False
                    break
        
        # Fresh zone (hiç test edilmemiş) daha değerli
        freshness = "FRESH" if times_tested == 0 else f"TESTED ({times_tested}x)"
        
        if still_valid or times_tested <= 2:
            demand_zones.append({
                "type": "DEMAND",
                "emoji": "🟢",
                "zone_top": round(zone_top, 2),
                "zone_bottom": round(zone_bottom, 2),
                "zone_mid": round(zone_mid, 2),
                "strength": round(move_percent, 2),
                "timestamp": candle['timestamp'],
                "freshness": freshness,
                "still_valid": still_valid,
                "times_tested": times_tested,
                "description": f"Demand Zone - {freshness}"
            })
    
    # En güçlü ve en yakın zone'ları döndür
    demand_zones.sort(key=lambda x: (-x['strength'], x['times_tested']))
    return demand_zones[:5]


def find_all_zones(candles: List[Dict]) -> Dict:
    """
    Tüm Supply ve Demand zone'ları bulur ve analiz eder.
    """
    if len(candles) < 5:
        return {"error": "Yetersiz veri"}
    
    supply_zones = find_supply_zones(candles)
    demand_zones = find_demand_zones(candles)
    
    current_price = candles[-1]['close']
    
    # En yakın zone'ları bul
    nearest_supply = None
    nearest_demand = None
    
    for zone in supply_zones:
        if zone['zone_bottom'] > current_price:
            if nearest_supply is None or zone['zone_bottom'] < nearest_supply['zone_bottom']:
                nearest_supply = zone
    
    for zone in demand_zones:
        if zone['zone_top'] < current_price:
            if nearest_demand is None or zone['zone_top'] > nearest_demand['zone_top']:
                nearest_demand = zone
    
    # Fiyat zone içinde mi?
    price_in_supply = False
    price_in_demand = False
    current_zone = None
    
    for zone in supply_zones:
        if zone['zone_bottom'] <= current_price <= zone['zone_top']:
            price_in_supply = True
            current_zone = zone
            break
    
    for zone in demand_zones:
        if zone['zone_bottom'] <= current_price <= zone['zone_top']:
            price_in_demand = True
            current_zone = zone
            break
    
    # Trading önerisi
    if price_in_demand:
        suggestion = "🟢 DEMAND ZONE İÇİNDE - LONG fırsatı"
        bias = "LONG"
    elif price_in_supply:
        suggestion = "🔴 SUPPLY ZONE İÇİNDE - SHORT fırsatı"
        bias = "SHORT"
    elif nearest_demand and nearest_supply:
        dist_to_demand = current_price - nearest_demand['zone_top']
        dist_to_supply = nearest_supply['zone_bottom'] - current_price
        
        if dist_to_demand < dist_to_supply:
            suggestion = f"🟢 Demand zone'a yakın (${dist_to_demand:.2f})"
            bias = "LONG"
        else:
            suggestion = f"🔴 Supply zone'a yakın (${dist_to_supply:.2f})"
            bias = "SHORT"
    else:
        suggestion = "⚪ Net zone yok"
        bias = "NEUTRAL"
    
    return {
        "current_price": round(current_price, 2),
        "supply_zones": supply_zones,
        "demand_zones": demand_zones,
        "nearest_supply": nearest_supply,
        "nearest_demand": nearest_demand,
        "price_in_supply": price_in_supply,
        "price_in_demand": price_in_demand,
        "current_zone": current_zone,
        "suggestion": suggestion,
        "bias": bias,
        "total_supply_zones": len(supply_zones),
        "total_demand_zones": len(demand_zones)
    }


# Test
if __name__ == "__main__":
    # Test verisi
    test_candles = [
        {"timestamp": "01:00", "open": 100, "high": 101, "low": 99, "close": 100.5},
        {"timestamp": "02:00", "open": 100.5, "high": 102, "low": 100, "close": 101.8},  # Bullish
        {"timestamp": "03:00", "open": 101.8, "high": 103, "low": 101, "close": 102.5},  # Bullish
        {"timestamp": "04:00", "open": 102.5, "high": 103, "low": 101, "close": 101.2},  # Bearish
        {"timestamp": "05:00", "open": 101.2, "high": 102, "low": 99, "close": 99.5},   # Strong Bearish - SUPPLY
        {"timestamp": "06:00", "open": 99.5, "high": 100, "low": 98, "close": 98.5},
        {"timestamp": "07:00", "open": 98.5, "high": 99, "low": 97, "close": 97.5},
        {"timestamp": "08:00", "open": 97.5, "high": 99, "low": 97, "close": 98.8},    # Bullish
        {"timestamp": "09:00", "open": 98.8, "high": 101, "low": 98.5, "close": 100.5}, # Strong Bullish - DEMAND
        {"timestamp": "10:00", "open": 100.5, "high": 101, "low": 100, "close": 100.8},
    ]
    
    result = find_all_zones(test_candles)
    
    print("=" * 50)
    print("  SUPPLY & DEMAND ZONES")
    print("=" * 50)
    print(f"\n💰 Current Price: ${result['current_price']}")
    print(f"📊 Suggestion: {result['suggestion']}")
    print(f"🎯 Bias: {result['bias']}")
    
    print(f"\n🔴 SUPPLY ZONES ({result['total_supply_zones']}):")
    for zone in result['supply_zones']:
        print(f"   ${zone['zone_bottom']} - ${zone['zone_top']} | {zone['freshness']} | Strength: {zone['strength']}%")
    
    print(f"\n🟢 DEMAND ZONES ({result['total_demand_zones']}):")
    for zone in result['demand_zones']:
        print(f"   ${zone['zone_bottom']} - ${zone['zone_top']} | {zone['freshness']} | Strength: {zone['strength']}%")
    
    print("=" * 50)

