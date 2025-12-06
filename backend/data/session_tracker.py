# ============================================
# SESSION TRACKER - Kill Zone Takibi
# ============================================
# Bu dosya Forex session'larını ve kill zone'ları takip eder.

from datetime import datetime, timezone, timedelta
from typing import Dict, List

# Türkiye saat dilimi (UTC+3)
TURKEY_OFFSET = timedelta(hours=3)

# Session tanımlamaları (UTC saatleri)
SESSIONS = {
    "ASIA": {
        "name": "Asya/Tokyo",
        "start_utc": 0,   # 00:00 UTC = 03:00 Türkiye
        "end_utc": 9,     # 09:00 UTC = 12:00 Türkiye
        "kill_zone_start": 0,
        "kill_zone_end": 2,
        "emoji": "🌏"
    },
    "LONDON": {
        "name": "Londra",
        "start_utc": 7,   # 07:00 UTC = 10:00 Türkiye
        "end_utc": 16,    # 16:00 UTC = 19:00 Türkiye
        "kill_zone_start": 7,
        "kill_zone_end": 9,
        "emoji": "🇬🇧"
    },
    "NEW_YORK": {
        "name": "New York",
        "start_utc": 12,  # 12:00 UTC = 15:00 Türkiye
        "end_utc": 21,    # 21:00 UTC = 00:00 Türkiye
        "kill_zone_start": 12,
        "kill_zone_end": 14,
        "emoji": "🇺🇸"
    }
}


def get_current_time_utc() -> datetime:
    """Şu anki UTC zamanını döndürür."""
    return datetime.now(timezone.utc)


def get_current_time_turkey() -> datetime:
    """Şu anki Türkiye zamanını döndürür."""
    utc_now = get_current_time_utc()
    return utc_now + TURKEY_OFFSET


def is_session_active(session_name: str) -> bool:
    """
    Belirtilen session'ın aktif olup olmadığını kontrol eder.
    
    Parametreler:
    -------------
    session_name : str
        Session adı: "ASIA", "LONDON", "NEW_YORK"
    
    Döndürür:
    ---------
    bool : Session aktif mi?
    """
    if session_name not in SESSIONS:
        return False
    
    session = SESSIONS[session_name]
    current_hour = get_current_time_utc().hour
    
    # Gece yarısını geçen session'lar için özel kontrol
    if session["end_utc"] < session["start_utc"]:
        return current_hour >= session["start_utc"] or current_hour < session["end_utc"]
    
    return session["start_utc"] <= current_hour < session["end_utc"]


def is_kill_zone_active(session_name: str) -> bool:
    """
    Belirtilen session'ın kill zone'unun aktif olup olmadığını kontrol eder.
    Kill zone = Session'ın en aktif saatleri (ilk 2 saat)
    
    Parametreler:
    -------------
    session_name : str
        Session adı: "ASIA", "LONDON", "NEW_YORK"
    
    Döndürür:
    ---------
    bool : Kill zone aktif mi?
    """
    if session_name not in SESSIONS:
        return False
    
    session = SESSIONS[session_name]
    current_hour = get_current_time_utc().hour
    
    return session["kill_zone_start"] <= current_hour < session["kill_zone_end"]


def get_active_sessions() -> List[Dict]:
    """
    Şu an aktif olan tüm session'ları döndürür.
    
    Döndürür:
    ---------
    List[Dict] : Aktif session bilgileri
    """
    active = []
    
    for session_name, session_info in SESSIONS.items():
        if is_session_active(session_name):
            active.append({
                "id": session_name,
                "name": session_info["name"],
                "emoji": session_info["emoji"],
                "is_kill_zone": is_kill_zone_active(session_name)
            })
    
    return active


def get_session_status() -> Dict:
    """
    Tüm session'ların durumunu döndürür.
    
    Döndürür:
    ---------
    Dict : Session durumları ve zaman bilgileri
    """
    utc_now = get_current_time_utc()
    turkey_now = get_current_time_turkey()
    
    sessions_status = {}
    
    for session_name, session_info in SESSIONS.items():
        is_active = is_session_active(session_name)
        is_kill_zone = is_kill_zone_active(session_name)
        
        # Kalan süre hesapla
        remaining_minutes = None
        if is_active:
            if is_kill_zone:
                # Kill zone bitimine kalan süre
                end_hour = session_info["kill_zone_end"]
                remaining = (end_hour - utc_now.hour - 1) * 60 + (60 - utc_now.minute)
                remaining_minutes = max(0, remaining)
            else:
                # Session bitimine kalan süre
                end_hour = session_info["end_utc"]
                if end_hour < session_info["start_utc"]:  # Gece yarısını geçiyorsa
                    end_hour += 24
                current = utc_now.hour if utc_now.hour >= session_info["start_utc"] else utc_now.hour + 24
                remaining = (end_hour - current - 1) * 60 + (60 - utc_now.minute)
                remaining_minutes = max(0, remaining)
        
        sessions_status[session_name] = {
            "name": session_info["name"],
            "emoji": session_info["emoji"],
            "is_active": is_active,
            "is_kill_zone": is_kill_zone,
            "remaining_minutes": remaining_minutes,
            "start_utc": f"{session_info['start_utc']:02d}:00",
            "end_utc": f"{session_info['end_utc']:02d}:00",
            "start_turkey": f"{(session_info['start_utc'] + 3) % 24:02d}:00",
            "end_turkey": f"{(session_info['end_utc'] + 3) % 24:02d}:00"
        }
    
    return {
        "current_time_utc": utc_now.strftime("%H:%M"),
        "current_time_turkey": turkey_now.strftime("%H:%M"),
        "sessions": sessions_status,
        "active_sessions": get_active_sessions()
    }


# Test kodu
if __name__ == "__main__":
    print("Session Durumu Test Ediliyor...\n")
    
    status = get_session_status()
    
    print(f"🕐 UTC Saati: {status['current_time_utc']}")
    print(f"🕐 Türkiye Saati: {status['current_time_turkey']}")
    print()
    
    print("📊 Session Durumları:")
    print("-" * 50)
    
    for session_id, session in status["sessions"].items():
        emoji = session["emoji"]
        name = session["name"]
        active = "✅ AKTİF" if session["is_active"] else "❌ Kapalı"
        kill_zone = " (🔥 KILL ZONE!)" if session["is_kill_zone"] else ""
        
        print(f"{emoji} {name}: {active}{kill_zone}")
        print(f"   Saat (TR): {session['start_turkey']} - {session['end_turkey']}")
        if session["remaining_minutes"]:
            print(f"   Kalan: {session['remaining_minutes']} dakika")
        print()

