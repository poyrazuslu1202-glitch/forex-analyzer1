# 🚀 Forex Analyzer - ICT Edition

ICT Concepts ile Kripto ve Forex Analizi yapan PWA uygulaması.

## ✨ Özellikler

- 📊 **Supply & Demand Zones** - Arz ve talep bölgeleri
- 🕐 **ICT Kill Zones** - Asya, Londra, New York session'ları
- 📈 **Fair Value Gaps** - Fiyat boşlukları
- 🎯 **Trade Sinyalleri** - Long/Short önerileri
- 📉 **Backtest** - Gerçek istatistikler
- 🪙 **Multi-Crypto** - BTC, SOL, ETH ve daha fazlası

## 🛠️ Teknolojiler

- **Backend:** Python, FastAPI, yfinance
- **Frontend:** Flutter Web (PWA)
- **Analiz:** ICT/SMC Concepts

## 📱 Kurulum

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd app
flutter pub get
flutter run -d chrome
```

## 🌐 API Endpoints

| Endpoint | Açıklama |
|----------|----------|
| `/crypto/{symbol}` | Kripto verisi (BTC, SOL, ETH...) |
| `/supply-demand/{symbol}` | Supply/Demand zones |
| `/full-analysis/{symbol}` | Tam analiz |
| `/ict-analysis` | ICT analizi |
| `/backtest` | Backtest sonuçları |

## 📄 Lisans

MIT License

