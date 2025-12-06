# Hızlı test dosyası
from data.price_fetcher import get_analysis
from data.session_tracker import get_session_status
from decision.probability import calculate_probability

print("=" * 50)
print("  FOREX ANALYZER TEST")
print("=" * 50)

# 1. Session testi
print("\n1. Session Durumu:")
session = get_session_status()
print(f"   UTC: {session['current_time_utc']}")
print(f"   TR:  {session['current_time_turkey']}")
for s in session['active_sessions']:
    kz = " (KILL ZONE!)" if s['is_kill_zone'] else ""
    print(f"   {s['emoji']} {s['name']} aktif{kz}")

# 2. TradingView testi
print("\n2. TradingView Verisi (EURUSD):")
analysis = get_analysis("EURUSD", interval="1h")
if analysis['success']:
    print(f"   Fiyat: {analysis['price']['close']}")
    print(f"   RSI: {analysis['indicators']['RSI']:.2f}")
    print(f"   TV Oneri: {analysis['summary']['recommendation']}")
else:
    print(f"   HATA: {analysis['error']}")

# 3. Olasılık testi
print("\n3. Olasılık Hesaplama:")
if analysis['success']:
    result = calculate_probability(analysis, session)
    print(f"   LONG:  %{result['probability']['long']}")
    print(f"   SHORT: %{result['probability']['short']}")
    print(f"   Oneri: {result['recommendation_text']}")

print("\n" + "=" * 50)
print("  TEST TAMAMLANDI!")
print("=" * 50)

