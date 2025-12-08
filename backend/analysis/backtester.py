# ============================================
# BACKTESTER - Gerçek İstatistik Hesaplama
# ============================================
# Geçmiş verilerle strateji test edip GERÇEK win rate hesaplar

from typing import Dict, List
from datetime import datetime
import statistics

def backtest_strategy(candles: List[Dict], lookback: int = 5, min_trades: int = 50) -> Dict:
    """
    Geçmiş verilerle strateji backtest yapar.
    
    Her mum için sinyal üretir, sonraki mumlara bakarak
    sinyalin doğru çıkıp çıkmadığını kontrol eder.
    
    Parameters:
    -----------
    candles : List[Dict]
        Mum verileri (open, high, low, close, timestamp)
    lookback : int
        Sinyal üretmek için geriye bakılacak mum sayısı
    
    Returns:
    --------
    Dict : Backtest sonuçları ve istatistikler
    """
    if len(candles) < lookback + 5:
        return {"error": "Yetersiz veri", "min_required": lookback + 5}
    
    trades = []
    
    # Her mum için sinyal üret ve sonucu kontrol et
    for i in range(lookback, len(candles) - 3):
        # Son 'lookback' mumu al
        window = candles[i-lookback:i+1]
        current_candle = candles[i]
        
        # Basit sinyal üret
        signal = _generate_signal(window)
        
        if signal['direction'] == 'WAIT':
            continue
        
        # Sonraki 3 muma bak
        entry_price = current_candle['close']
        future_candles = candles[i+1:i+4]
        
        if len(future_candles) < 3:
            continue
        
        # En yüksek ve en düşük fiyatı bul
        future_high = max(c['high'] for c in future_candles)
        future_low = min(c['low'] for c in future_candles)
        exit_price = future_candles[-1]['close']
        
        # Trade sonucunu hesapla
        if signal['direction'] == 'LONG':
            # Stop loss %1, Take profit %1.5
            stop_loss = entry_price * 0.99
            take_profit = entry_price * 1.015
            
            if future_low <= stop_loss:
                result = 'LOSS'
                pnl_percent = -1.0
            elif future_high >= take_profit:
                result = 'WIN'
                pnl_percent = 1.5
            else:
                # TP veya SL'ye ulaşmadı, kapanış fiyatına göre
                pnl_percent = ((exit_price - entry_price) / entry_price) * 100
                result = 'WIN' if pnl_percent > 0 else 'LOSS'
        
        else:  # SHORT
            stop_loss = entry_price * 1.01
            take_profit = entry_price * 0.985
            
            if future_high >= stop_loss:
                result = 'LOSS'
                pnl_percent = -1.0
            elif future_low <= take_profit:
                result = 'WIN'
                pnl_percent = 1.5
            else:
                pnl_percent = ((entry_price - exit_price) / entry_price) * 100
                result = 'WIN' if pnl_percent > 0 else 'LOSS'
        
        trades.append({
            'timestamp': current_candle['timestamp'],
            'direction': signal['direction'],
            'entry_price': entry_price,
            'exit_price': exit_price,
            'result': result,
            'pnl_percent': round(pnl_percent, 2),
            'signal_strength': signal['strength']
        })
    
    # İstatistikleri hesapla
    return _calculate_statistics(trades)


def _generate_signal(candles: List[Dict]) -> Dict:
    """
    Mum verilerinden basit sinyal üretir.
    """
    if len(candles) < 3:
        return {'direction': 'WAIT', 'strength': 0}
    
    closes = [c['close'] for c in candles]
    opens = [c['open'] for c in candles]
    
    # Basit EMA
    ema_short = sum(closes[-3:]) / 3
    ema_long = sum(closes) / len(closes)
    
    # Son mumların yönü
    bullish_count = sum(1 for i in range(-3, 0) if closes[i] > opens[i])
    
    # Momentum
    momentum = (closes[-1] - closes[0]) / closes[0] * 100
    
    score = 0
    
    # EMA crossover
    if ema_short > ema_long:
        score += 30
    else:
        score -= 30
    
    # Mum yönü
    if bullish_count >= 2:
        score += 20
    elif bullish_count <= 1:
        score -= 20
    
    # Momentum
    if momentum > 0.5:
        score += 20
    elif momentum < -0.5:
        score -= 20
    
    if score >= 40:
        return {'direction': 'LONG', 'strength': score}
    elif score <= -40:
        return {'direction': 'SHORT', 'strength': abs(score)}
    else:
        return {'direction': 'WAIT', 'strength': abs(score)}


def _calculate_statistics(trades: List[Dict]) -> Dict:
    """
    Trade listesinden istatistikleri hesaplar.
    """
    if not trades:
        return {
            "error": "Trade bulunamadı",
            "total_trades": 0
        }
    
    total_trades = len(trades)
    winning_trades = [t for t in trades if t['result'] == 'WIN']
    losing_trades = [t for t in trades if t['result'] == 'LOSS']
    
    win_count = len(winning_trades)
    loss_count = len(losing_trades)
    
    # Win Rate - EN ÖNEMLİ METRİK
    win_rate = (win_count / total_trades) * 100 if total_trades > 0 else 0
    
    # PnL hesaplamaları
    total_profit = sum(t['pnl_percent'] for t in winning_trades)
    total_loss = abs(sum(t['pnl_percent'] for t in losing_trades))
    net_pnl = sum(t['pnl_percent'] for t in trades)
    
    # Profit Factor
    profit_factor = total_profit / total_loss if total_loss > 0 else 0
    
    # Average Win / Loss
    avg_win = total_profit / win_count if win_count > 0 else 0
    avg_loss = total_loss / loss_count if loss_count > 0 else 0
    
    # Risk/Reward Ratio
    risk_reward = avg_win / avg_loss if avg_loss > 0 else 0
    
    # Expectancy (Trade başına beklenen getiri)
    expectancy = (win_rate/100 * avg_win) - ((100-win_rate)/100 * avg_loss)
    
    # Maximum Drawdown
    cumulative_pnl = []
    running_total = 0
    for t in trades:
        running_total += t['pnl_percent']
        cumulative_pnl.append(running_total)
    
    peak = cumulative_pnl[0]
    max_drawdown = 0
    for pnl in cumulative_pnl:
        if pnl > peak:
            peak = pnl
        drawdown = peak - pnl
        if drawdown > max_drawdown:
            max_drawdown = drawdown
    
    # Consecutive wins/losses
    max_consecutive_wins = 0
    max_consecutive_losses = 0
    current_wins = 0
    current_losses = 0
    
    for t in trades:
        if t['result'] == 'WIN':
            current_wins += 1
            current_losses = 0
            max_consecutive_wins = max(max_consecutive_wins, current_wins)
        else:
            current_losses += 1
            current_wins = 0
            max_consecutive_losses = max(max_consecutive_losses, current_losses)
    
    # Long vs Short performansı
    long_trades = [t for t in trades if t['direction'] == 'LONG']
    short_trades = [t for t in trades if t['direction'] == 'SHORT']
    
    long_win_rate = (len([t for t in long_trades if t['result'] == 'WIN']) / len(long_trades) * 100) if long_trades else 0
    short_win_rate = (len([t for t in short_trades if t['result'] == 'WIN']) / len(short_trades) * 100) if short_trades else 0
    
    return {
        "success": True,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        
        # Ana Metrikler
        "total_trades": total_trades,
        "winning_trades": win_count,
        "losing_trades": loss_count,
        
        # EN ÖNEMLİ: GERÇEK WIN RATE
        "win_rate": round(win_rate, 1),
        
        # Karlılık
        "profit_factor": round(profit_factor, 2),
        "net_pnl_percent": round(net_pnl, 2),
        "expectancy": round(expectancy, 3),
        
        # Ortalamalar
        "avg_win_percent": round(avg_win, 2),
        "avg_loss_percent": round(avg_loss, 2),
        "risk_reward_ratio": round(risk_reward, 2),
        
        # Risk
        "max_drawdown_percent": round(max_drawdown, 2),
        "max_consecutive_wins": max_consecutive_wins,
        "max_consecutive_losses": max_consecutive_losses,
        
        # Long vs Short
        "long_trades": len(long_trades),
        "short_trades": len(short_trades),
        "long_win_rate": round(long_win_rate, 1),
        "short_win_rate": round(short_win_rate, 1),
        
        # Son 10 trade
        "recent_trades": trades[-10:] if len(trades) >= 10 else trades
    }


def get_real_confidence(backtest_result: Dict, current_signal: str) -> float:
    """
    Backtest sonuçlarına göre GERÇEK güven oranı döndürür.
    
    Bu güven oranı TAHMİN DEĞİL, geçmiş verilerden hesaplanmış
    GERÇEK win rate'e dayanır.
    """
    if not backtest_result.get('success'):
        return 50.0  # Veri yoksa nötr
    
    if current_signal == 'LONG':
        return backtest_result.get('long_win_rate', 50.0)
    elif current_signal == 'SHORT':
        return backtest_result.get('short_win_rate', 50.0)
    else:
        return backtest_result.get('win_rate', 50.0)


# Test
if __name__ == "__main__":
    # Örnek test verisi oluştur
    import random
    
    test_candles = []
    price = 100
    
    for i in range(100):
        change = random.uniform(-2, 2)
        open_p = price
        close_p = price + change
        high_p = max(open_p, close_p) + random.uniform(0, 1)
        low_p = min(open_p, close_p) - random.uniform(0, 1)
        
        test_candles.append({
            'timestamp': f'2025-01-01 {i:02d}:00',
            'open': round(open_p, 2),
            'high': round(high_p, 2),
            'low': round(low_p, 2),
            'close': round(close_p, 2)
        })
        price = close_p
    
    result = backtest_strategy(test_candles)
    
    print("=" * 50)
    print("  BACKTEST SONUÇLARI")
    print("=" * 50)
    
    if result.get('success'):
        print(f"\n📊 TOPLAM TRADE: {result['total_trades']}")
        print(f"   ✅ Kazanan: {result['winning_trades']}")
        print(f"   ❌ Kaybeden: {result['losing_trades']}")
        
        print(f"\n🎯 WIN RATE: %{result['win_rate']}")
        print(f"   (Bu GERÇEK oran, tahmin değil!)")
        
        print(f"\n💰 KARLILIK:")
        print(f"   Profit Factor: {result['profit_factor']}")
        print(f"   Net PnL: %{result['net_pnl_percent']}")
        print(f"   Expectancy: {result['expectancy']}")
        
        print(f"\n📈 LONG vs SHORT:")
        print(f"   Long Win Rate: %{result['long_win_rate']}")
        print(f"   Short Win Rate: %{result['short_win_rate']}")
        
        print(f"\n⚠️ RİSK:")
        print(f"   Max Drawdown: %{result['max_drawdown_percent']}")
        print(f"   Max Consecutive Losses: {result['max_consecutive_losses']}")
    else:
        print(f"Hata: {result.get('error')}")
    
    print("=" * 50)

