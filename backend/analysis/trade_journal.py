# ============================================
# TRADE JOURNAL - Analiz Kayıt Sistemi
# ============================================
# Her analizi kaydeder ve sonuçları takip eder

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# Kayıt dosyası
JOURNAL_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'trade_journal.json')


def load_journal() -> Dict:
    """
    Journal dosyasını yükler.
    """
    try:
        if os.path.exists(JOURNAL_FILE):
            with open(JOURNAL_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Journal yükleme hatası: {e}")
    
    return {
        "created_at": datetime.now().isoformat(),
        "total_signals": 0,
        "signals": [],
        "statistics": {
            "total_long": 0,
            "total_short": 0,
            "total_wait": 0,
            "verified_wins": 0,
            "verified_losses": 0,
            "pending_verification": 0
        }
    }


def save_journal(journal: Dict) -> bool:
    """
    Journal'ı dosyaya kaydeder.
    """
    try:
        # Data klasörünü oluştur
        os.makedirs(os.path.dirname(JOURNAL_FILE), exist_ok=True)
        
        with open(JOURNAL_FILE, 'w', encoding='utf-8') as f:
            json.dump(journal, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Journal kaydetme hatası: {e}")
        return False


def record_signal(
    crypto: str,
    direction: str,
    confidence: float,
    entry_price: float,
    stop_loss: float,
    take_profit_1: float,
    take_profit_2: float,
    ict_analysis: Dict,
    backtest_stats: Dict
) -> Dict:
    """
    Yeni bir sinyal kaydeder.
    """
    journal = load_journal()
    
    signal_id = f"{crypto}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    new_signal = {
        "id": signal_id,
        "timestamp": datetime.now().isoformat(),
        "crypto": crypto,
        "direction": direction,
        "confidence": confidence,
        "entry_price": entry_price,
        "stop_loss": stop_loss,
        "take_profit_1": take_profit_1,
        "take_profit_2": take_profit_2,
        "status": "PENDING",  # PENDING, WIN, LOSS, EXPIRED
        "result": None,
        "result_price": None,
        "result_timestamp": None,
        "pnl_percent": None,
        "ict_summary": {
            "market_structure": ict_analysis.get('market_structure', {}).get('trend', 'N/A'),
            "kill_zone": ict_analysis.get('kill_zones', {}).get('active_zone', {}).get('name', 'None'),
            "premium_discount": ict_analysis.get('premium_discount', {}).get('current_zone', 'N/A')
        },
        "backtest_at_signal": {
            "win_rate": backtest_stats.get('win_rate', 0),
            "profit_factor": backtest_stats.get('profit_factor', 0),
            "total_trades": backtest_stats.get('total_trades', 0)
        }
    }
    
    # Journal'a ekle
    journal['signals'].insert(0, new_signal)  # En yeni en üstte
    journal['total_signals'] += 1
    
    # İstatistikleri güncelle
    if direction == 'LONG':
        journal['statistics']['total_long'] += 1
    elif direction == 'SHORT':
        journal['statistics']['total_short'] += 1
    else:
        journal['statistics']['total_wait'] += 1
    
    journal['statistics']['pending_verification'] += 1
    
    # Son 100 sinyali tut (bellek yönetimi)
    journal['signals'] = journal['signals'][:100]
    
    save_journal(journal)
    
    return new_signal


def verify_past_signals(current_price: float, crypto: str = "BTC") -> Dict:
    """
    Geçmiş sinyalleri doğrular - TP veya SL'e ulaşmış mı?
    """
    journal = load_journal()
    verified_count = 0
    
    for signal in journal['signals']:
        # Sadece aynı kripto ve PENDING olanları kontrol et
        if signal['crypto'] != crypto or signal['status'] != 'PENDING':
            continue
        
        # 24 saatten eski sinyalleri EXPIRED yap
        signal_time = datetime.fromisoformat(signal['timestamp'])
        if datetime.now() - signal_time > timedelta(hours=24):
            signal['status'] = 'EXPIRED'
            signal['result_timestamp'] = datetime.now().isoformat()
            journal['statistics']['pending_verification'] -= 1
            continue
        
        entry = signal['entry_price']
        sl = signal['stop_loss']
        tp1 = signal['take_profit_1']
        direction = signal['direction']
        
        # LONG kontrolü
        if direction == 'LONG':
            if current_price >= tp1:
                signal['status'] = 'WIN'
                signal['result'] = 'TP1_HIT'
                signal['result_price'] = current_price
                signal['pnl_percent'] = round(((tp1 - entry) / entry) * 100, 2)
                journal['statistics']['verified_wins'] += 1
                journal['statistics']['pending_verification'] -= 1
                verified_count += 1
            elif current_price <= sl:
                signal['status'] = 'LOSS'
                signal['result'] = 'SL_HIT'
                signal['result_price'] = current_price
                signal['pnl_percent'] = round(((sl - entry) / entry) * 100, 2)
                journal['statistics']['verified_losses'] += 1
                journal['statistics']['pending_verification'] -= 1
                verified_count += 1
        
        # SHORT kontrolü
        elif direction == 'SHORT':
            if current_price <= tp1:
                signal['status'] = 'WIN'
                signal['result'] = 'TP1_HIT'
                signal['result_price'] = current_price
                signal['pnl_percent'] = round(((entry - tp1) / entry) * 100, 2)
                journal['statistics']['verified_wins'] += 1
                journal['statistics']['pending_verification'] -= 1
                verified_count += 1
            elif current_price >= sl:
                signal['status'] = 'LOSS'
                signal['result'] = 'SL_HIT'
                signal['result_price'] = current_price
                signal['pnl_percent'] = round(((entry - sl) / entry) * 100, 2)
                journal['statistics']['verified_losses'] += 1
                journal['statistics']['pending_verification'] -= 1
                verified_count += 1
        
        if signal['status'] != 'PENDING':
            signal['result_timestamp'] = datetime.now().isoformat()
    
    save_journal(journal)
    
    return {
        "verified_count": verified_count,
        "message": f"{verified_count} sinyal doğrulandı"
    }


def get_journal_stats() -> Dict:
    """
    Journal istatistiklerini döndürür.
    """
    journal = load_journal()
    stats = journal['statistics']
    
    total_verified = stats['verified_wins'] + stats['verified_losses']
    real_win_rate = (stats['verified_wins'] / total_verified * 100) if total_verified > 0 else 0
    
    # Son 10 sinyal
    recent_signals = journal['signals'][:10]
    
    return {
        "total_signals": journal['total_signals'],
        "statistics": stats,
        "real_win_rate": round(real_win_rate, 1),
        "total_verified": total_verified,
        "recent_signals": recent_signals,
        "last_updated": datetime.now().isoformat()
    }


def get_signal_history(limit: int = 50) -> List[Dict]:
    """
    Sinyal geçmişini döndürür.
    """
    journal = load_journal()
    return journal['signals'][:limit]


def clear_journal() -> Dict:
    """
    Journal'ı temizler (dikkatli kullan!).
    """
    empty_journal = {
        "created_at": datetime.now().isoformat(),
        "total_signals": 0,
        "signals": [],
        "statistics": {
            "total_long": 0,
            "total_short": 0,
            "total_wait": 0,
            "verified_wins": 0,
            "verified_losses": 0,
            "pending_verification": 0
        }
    }
    save_journal(empty_journal)
    return {"message": "Journal temizlendi", "timestamp": datetime.now().isoformat()}


# Test
if __name__ == "__main__":
    print("=" * 50)
    print("  TRADE JOURNAL TEST")
    print("=" * 50)
    
    # Test kaydı
    test_signal = record_signal(
        crypto="BTC",
        direction="LONG",
        confidence=65.5,
        entry_price=89000,
        stop_loss=88000,
        take_profit_1=90000,
        take_profit_2=91000,
        ict_analysis={"market_structure": {"trend": "BULLISH"}},
        backtest_stats={"win_rate": 55, "profit_factor": 1.5}
    )
    
    print(f"\n✅ Sinyal kaydedildi: {test_signal['id']}")
    
    # İstatistikler
    stats = get_journal_stats()
    print(f"\n📊 Toplam Sinyal: {stats['total_signals']}")
    print(f"📈 Gerçek Win Rate: %{stats['real_win_rate']}")
    
    print("=" * 50)

