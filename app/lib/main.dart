// ============================================
// FOREX ANALYZER PRO - ICT Concepts + Candlestick
// TradingView Dark Theme
// ============================================

import 'package:flutter/material.dart';
import 'dart:convert';
import 'dart:math' as math;
import 'package:http/http.dart' as http;

void main() {
  runApp(const ForexAnalyzerApp());
}

// TradingView Dark Theme Colors
class TV {
  static const bg = Color(0xFF131722);
  static const card = Color(0xFF1E222D);
  static const border = Color(0xFF2A2E39);
  static const text = Color(0xFFD1D4DC);
  static const textDim = Color(0xFF787B86);
  static const textMuted = Color(0xFF5D606B);
  static const green = Color(0xFF089981);
  static const greenBg = Color(0xFF0E2D28);
  static const red = Color(0xFFF23645);
  static const redBg = Color(0xFF2D1F21);
  static const blue = Color(0xFF2962FF);
  static const orange = Color(0xFFF7931A);
  static const purple = Color(0xFF9C27B0);
  static const cyan = Color(0xFF00BCD4);
}

class ForexAnalyzerApp extends StatelessWidget {
  const ForexAnalyzerApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Forex Analyzer Pro',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(brightness: Brightness.dark, scaffoldBackgroundColor: TV.bg, fontFamily: 'Segoe UI'),
      home: const HomePage(),
    );
  }
}

class HomePage extends StatefulWidget {
  const HomePage({super.key});
  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  bool isLoading = false;
  Map<String, dynamic>? fullReport;
  Map<String, dynamic>? supplyDemand;
  Map<String, dynamic>? solanaData;
  String? error;
  final String apiUrl = 'https://forex-analyzer1-cyhv.onrender.com';
  String selectedCrypto = 'BTC'; // BTC veya SOL

  @override
  void initState() {
    super.initState();
    _fetchData();
  }
  
  Future<void> _fetchData() async {
    setState(() { isLoading = true; error = null; });
    
    try {
      // Paralel API çağrıları
      final responses = await Future.wait([
        http.get(Uri.parse('$apiUrl/full-report')),
        http.get(Uri.parse('$apiUrl/supply-demand/BTC')),
        http.get(Uri.parse('$apiUrl/full-analysis/SOL')),
      ]);
      
      if (responses[0].statusCode == 200) {
        fullReport = json.decode(responses[0].body);
      }
      if (responses[1].statusCode == 200) {
        supplyDemand = json.decode(responses[1].body);
      }
      if (responses[2].statusCode == 200) {
        solanaData = json.decode(responses[2].body);
      }
      
      setState(() { isLoading = false; });
    } catch (e) {
      setState(() { error = 'Backend çalışıyor mu?\n\n$e'; isLoading = false; });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: TV.bg,
      body: Row(
        children: [
          _buildLeftPanel(),
          Expanded(child: _buildMainContent()),
        ],
      ),
    );
  }
  
  Widget _buildLeftPanel() {
    // SOL seçiliyse SOL verisini kullan
    final bool isSol = selectedCrypto == 'SOL' && solanaData != null;
    Map<String, dynamic>? signal;
    Map<String, dynamic>? ict;
    
    if (isSol) {
      signal = solanaData?['trade_signal'];
      ict = solanaData?['ict_analysis'];
    } else {
      signal = fullReport?['trade_signal'];
      ict = fullReport?['ict_analysis'];
    }
    
    return Container(
      width: 320,
      decoration: const BoxDecoration(
        color: TV.card,
        border: Border(right: BorderSide(color: TV.border)),
      ),
      child: Column(
        children: [
          // Header
          Container(
            padding: const EdgeInsets.all(20),
            decoration: const BoxDecoration(border: Border(bottom: BorderSide(color: TV.border))),
            child: Row(
              children: [
                Container(
                  padding: const EdgeInsets.all(10),
                  decoration: BoxDecoration(color: TV.orange.withOpacity(0.1), borderRadius: BorderRadius.circular(10)),
                  child: const Text('📊', style: TextStyle(fontSize: 24)),
                ),
                const SizedBox(width: 12),
                const Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text('FOREX ANALYZER', style: TextStyle(fontSize: 14, fontWeight: FontWeight.bold, color: TV.text, letterSpacing: 1)),
                    Text('ICT Strategy Pro', style: TextStyle(fontSize: 11, color: TV.textDim)),
                  ],
                ),
              ],
            ),
          ),
          
          // Crypto Selector
          _buildCryptoSelector(),
          
          if (signal != null) _buildMainSignalCard(signal),
          if (ict != null) _buildKillZonesPanel(ict['kill_zones']),
          
          const Spacer(),
          
          Padding(
            padding: const EdgeInsets.all(16),
            child: SizedBox(
              width: double.infinity,
              child: ElevatedButton.icon(
                onPressed: isLoading ? null : _fetchData,
                icon: isLoading 
                  ? const SizedBox(width: 18, height: 18, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                  : const Icon(Icons.refresh, size: 18),
                label: Text(isLoading ? 'Analiz ediliyor...' : 'YENİLE'),
                style: ElevatedButton.styleFrom(
                  backgroundColor: TV.blue,
                  foregroundColor: Colors.white,
                  padding: const EdgeInsets.symmetric(vertical: 14),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
  
  Widget _buildCryptoSelector() {
    return Container(
      margin: const EdgeInsets.all(16),
      padding: const EdgeInsets.all(4),
      decoration: BoxDecoration(
        color: TV.bg,
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: TV.border),
      ),
      child: Row(
        children: [
          Expanded(
            child: GestureDetector(
              onTap: () => setState(() => selectedCrypto = 'BTC'),
              child: Container(
                padding: const EdgeInsets.symmetric(vertical: 10),
                decoration: BoxDecoration(
                  color: selectedCrypto == 'BTC' ? TV.orange.withOpacity(0.2) : Colors.transparent,
                  borderRadius: BorderRadius.circular(6),
                  border: Border.all(color: selectedCrypto == 'BTC' ? TV.orange : Colors.transparent),
                ),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Text('₿', style: TextStyle(fontSize: 16, color: selectedCrypto == 'BTC' ? TV.orange : TV.textDim)),
                    const SizedBox(width: 6),
                    Text('BTC', style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: selectedCrypto == 'BTC' ? TV.orange : TV.textDim)),
                  ],
                ),
              ),
            ),
          ),
          Expanded(
            child: GestureDetector(
              onTap: () => setState(() => selectedCrypto = 'SOL'),
              child: Container(
                padding: const EdgeInsets.symmetric(vertical: 10),
                decoration: BoxDecoration(
                  color: selectedCrypto == 'SOL' ? TV.purple.withOpacity(0.2) : Colors.transparent,
                  borderRadius: BorderRadius.circular(6),
                  border: Border.all(color: selectedCrypto == 'SOL' ? TV.purple : Colors.transparent),
                ),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Text('◎', style: TextStyle(fontSize: 16, color: selectedCrypto == 'SOL' ? TV.purple : TV.textDim)),
                    const SizedBox(width: 6),
                    Text('SOL', style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: selectedCrypto == 'SOL' ? TV.purple : TV.textDim)),
                  ],
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
  
  Widget _buildMainSignalCard(Map<String, dynamic> signal) {
    final direction = signal['direction'] ?? 'WAIT';
    final emoji = signal['direction_emoji'] ?? '🟡';
    final text = signal['direction_text'] ?? 'BEKLE';
    final confidence = (signal['confidence'] ?? 50).toDouble();
    final plan = signal['trade_plan'] ?? {};
    final confidenceSource = signal['confidence_source'] ?? 'ESTIMATED';
    final backtestTrades = signal['backtest_trades'] ?? 0;
    
    Color signalColor = direction == 'LONG' ? TV.green : (direction == 'SHORT' ? TV.red : TV.orange);
    Color bgColor = direction == 'LONG' ? TV.greenBg : (direction == 'SHORT' ? TV.redBg : TV.orange.withOpacity(0.1));
    
    return Container(
      margin: const EdgeInsets.all(16),
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: bgColor,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: signalColor, width: 2),
      ),
      child: Column(
        children: [
          Text(emoji, style: const TextStyle(fontSize: 40)),
          const SizedBox(height: 8),
          Text(direction, style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold, color: signalColor)),
          Text(text, style: const TextStyle(fontSize: 12, color: TV.textDim)),
          const SizedBox(height: 16),
          
          // Güven barı
          Row(
            children: [
              const Text('GÜVEN', style: TextStyle(fontSize: 10, color: TV.textDim)),
              const SizedBox(width: 8),
              Expanded(
                child: ClipRRect(
                  borderRadius: BorderRadius.circular(4),
                  child: LinearProgressIndicator(
                    value: confidence / 100,
                    backgroundColor: TV.border,
                    valueColor: AlwaysStoppedAnimation<Color>(signalColor),
                    minHeight: 8,
                  ),
                ),
              ),
              const SizedBox(width: 8),
              Text('%${confidence.toStringAsFixed(0)}', style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: signalColor)),
            ],
          ),
          const SizedBox(height: 6),
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                decoration: BoxDecoration(
                  color: confidenceSource == 'BACKTEST' ? TV.blue.withOpacity(0.2) : TV.orange.withOpacity(0.2),
                  borderRadius: BorderRadius.circular(4),
                ),
                child: Text(
                  confidenceSource == 'BACKTEST' ? '📊 GERÇEK VERİ ($backtestTrades trade)' : '⚠️ TAHMİNİ',
                  style: TextStyle(fontSize: 9, color: confidenceSource == 'BACKTEST' ? TV.blue : TV.orange),
                ),
              ),
            ],
          ),
          
          const SizedBox(height: 16),
          const Divider(color: TV.border),
          const SizedBox(height: 12),
          
          _buildPlanRow('Giriş', '\$${_fmt(plan['entry_price'])}', TV.text),
          _buildPlanRow('Stop Loss', '\$${_fmt(plan['stop_loss'])}', TV.red),
          _buildPlanRow('TP1', '\$${_fmt(plan['take_profit_1'])}', TV.green),
          _buildPlanRow('TP2', '\$${_fmt(plan['take_profit_2'])}', TV.green),
          _buildPlanRow('R/R', '${plan['risk_reward'] ?? 0}', TV.blue),
        ],
      ),
    );
  }
  
  Widget _buildPlanRow(String label, String value, Color valueColor) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(label, style: const TextStyle(fontSize: 12, color: TV.textDim)),
          Text(value, style: TextStyle(fontSize: 12, fontWeight: FontWeight.w600, color: valueColor)),
        ],
      ),
    );
  }
  
  Widget _buildKillZonesPanel(Map<String, dynamic>? kz) {
    if (kz == null) return const SizedBox();
    
    final zones = kz['zones'] as List? ?? [];
    final time = kz['current_time_turkey'] ?? '--:--';
    
    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 16),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: TV.bg,
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: TV.border),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text('ICT KILL ZONES', style: TextStyle(fontSize: 11, color: TV.textDim, fontWeight: FontWeight.w600)),
              Text('🕐 $time TR', style: const TextStyle(fontSize: 11, color: TV.textMuted)),
            ],
          ),
          const SizedBox(height: 12),
          
          ...zones.map((z) {
            final active = z['is_active'] ?? false;
            final color = _hexToColor(z['color'] ?? '#787B86');
            
            return Container(
              margin: const EdgeInsets.only(bottom: 6),
              padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
              decoration: BoxDecoration(
                color: active ? color.withOpacity(0.15) : Colors.transparent,
                borderRadius: BorderRadius.circular(6),
                border: Border.all(color: active ? color : TV.border),
              ),
              child: Row(
                children: [
                  Container(
                    width: 8, height: 8,
                    decoration: BoxDecoration(color: active ? color : TV.textMuted, shape: BoxShape.circle),
                  ),
                  const SizedBox(width: 8),
                  Expanded(child: Text(z['alias'] ?? '', style: TextStyle(fontSize: 11, color: active ? TV.text : TV.textDim))),
                  if (active)
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                      decoration: BoxDecoration(color: color, borderRadius: BorderRadius.circular(4)),
                      child: Text('${z['minutes_remaining']}dk', style: const TextStyle(fontSize: 9, color: Colors.white, fontWeight: FontWeight.bold)),
                    ),
                ],
              ),
            );
          }),
        ],
      ),
    );
  }
  
  Widget _buildMainContent() {
    if (error != null) {
      return Center(
        child: Container(
          padding: const EdgeInsets.all(32),
          margin: const EdgeInsets.all(32),
          decoration: BoxDecoration(color: TV.redBg, borderRadius: BorderRadius.circular(12), border: Border.all(color: TV.red)),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Icon(Icons.error_outline, color: TV.red, size: 48),
              const SizedBox(height: 16),
              Text(error!, textAlign: TextAlign.center, style: const TextStyle(color: TV.red)),
              const SizedBox(height: 24),
              ElevatedButton(onPressed: _fetchData, child: const Text('Tekrar Dene')),
            ],
          ),
        ),
      );
    }
    
    if (isLoading || fullReport == null) {
      return const Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            CircularProgressIndicator(color: TV.blue),
            SizedBox(height: 16),
            Text('Analiz yapılıyor...', style: TextStyle(color: TV.textDim)),
          ],
        ),
      );
    }
    
    // Seçilen crypto'ya göre veri
    final btc = fullReport!['btc_report'];
    
    // SOL seçiliyse SOL verisini kullan, değilse BTC
    final bool isSol = selectedCrypto == 'SOL' && solanaData != null;
    
    final Map<String, dynamic>? chartData = isSol ? solanaData!['report'] : btc;
    final Map<String, dynamic>? signal = isSol ? solanaData!['trade_signal'] : fullReport!['trade_signal'];
    final Map<String, dynamic>? ict = isSol ? solanaData!['ict_analysis'] : fullReport!['ict_analysis'];
    final Map<String, dynamic>? backtest = isSol ? solanaData!['backtest'] : fullReport!['backtest'];
    
    return SingleChildScrollView(
      padding: const EdgeInsets.all(24),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _buildHeader(chartData, signal),
          const SizedBox(height: 24),
          
          // Candlestick Chart - Seçilen kripto için
          _buildCandlestickChart(chartData),
          const SizedBox(height: 24),
          
          // Supply/Demand ve FVG
          Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Expanded(child: _buildSupplyDemandCard()),
              const SizedBox(width: 16),
              Expanded(child: _buildFVGCard(ict)),
            ],
          ),
          const SizedBox(height: 24),
          
          Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Expanded(child: _buildMarketStructureCard(ict)),
              const SizedBox(width: 16),
              Expanded(child: _buildPremiumDiscountCard(ict)),
            ],
          ),
          const SizedBox(height: 24),
          
          _buildBacktestCard(backtest),
          const SizedBox(height: 24),
          _buildKillZoneStrategyCard(fullReport!['killzone_strategy']),
          const SizedBox(height: 24),
          _buildJournalCard(fullReport!['journal']),
          const SizedBox(height: 24),
          _buildNewsCard(fullReport!['news']),
        ],
      ),
    );
  }
  
  Widget _buildJournalCard(Map<String, dynamic>? journal) {
    if (journal == null) return const SizedBox();
    
    final stats = journal['statistics'] ?? {};
    final realWinRate = (journal['real_win_rate'] ?? 0).toDouble();
    final totalSignals = journal['total_signals'] ?? 0;
    final totalVerified = journal['total_verified'] ?? 0;
    final recentSignals = journal['recent_signals'] as List? ?? [];
    
    final verifiedWins = stats['verified_wins'] ?? 0;
    final verifiedLosses = stats['verified_losses'] ?? 0;
    final pending = stats['pending_verification'] ?? 0;
    
    Color winRateColor = realWinRate >= 55 ? TV.green : (realWinRate >= 45 ? TV.orange : TV.red);
    
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: TV.card,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: TV.green, width: 2),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              const Icon(Icons.auto_stories, color: TV.green, size: 20),
              const SizedBox(width: 8),
              const Text('TRADE JOURNAL', 
                style: TextStyle(fontSize: 12, color: TV.green, fontWeight: FontWeight.w600, letterSpacing: 1)),
              const Spacer(),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                decoration: BoxDecoration(
                  color: TV.blue.withOpacity(0.1),
                  borderRadius: BorderRadius.circular(4),
                ),
                child: Text('$totalSignals sinyal kaydedildi', style: const TextStyle(fontSize: 10, color: TV.blue)),
              ),
            ],
          ),
          const SizedBox(height: 8),
          const Text('Tüm sinyaller kaydedilir ve sonuçları takip edilir. Bu GERÇEK performans verisidir.',
            style: TextStyle(fontSize: 10, color: TV.textMuted, fontStyle: FontStyle.italic)),
          const SizedBox(height: 20),
          
          // Ana istatistikler
          Row(
            children: [
              Expanded(
                child: Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: winRateColor.withOpacity(0.1),
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: winRateColor),
                  ),
                  child: Column(
                    children: [
                      const Text('GERÇEK WIN RATE', style: TextStyle(fontSize: 9, color: TV.textMuted)),
                      const SizedBox(height: 8),
                      Text('%${realWinRate.toStringAsFixed(1)}', 
                        style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold, color: winRateColor)),
                      Text('$totalVerified doğrulanmış trade', style: const TextStyle(fontSize: 10, color: TV.textDim)),
                    ],
                  ),
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: Column(
                  children: [
                    _buildJournalStat('✅ Kazanan', '$verifiedWins', TV.green),
                    const SizedBox(height: 8),
                    _buildJournalStat('❌ Kaybeden', '$verifiedLosses', TV.red),
                    const SizedBox(height: 8),
                    _buildJournalStat('⏳ Bekleyen', '$pending', TV.orange),
                  ],
                ),
              ),
            ],
          ),
          const SizedBox(height: 20),
          
          // Son sinyaller - Dropdown ile genişletilebilir
          if (recentSignals.isNotEmpty) ...[
            Row(
              children: [
                const Text('📜 SİNYAL GEÇMİŞİ', style: TextStyle(fontSize: 10, color: TV.textDim, fontWeight: FontWeight.w600)),
                const Spacer(),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                  decoration: BoxDecoration(
                    color: TV.purple.withOpacity(0.1),
                    borderRadius: BorderRadius.circular(4),
                  ),
                  child: Text('${recentSignals.length} kayıt', style: const TextStyle(fontSize: 9, color: TV.purple)),
                ),
              ],
            ),
            const SizedBox(height: 12),
            ...recentSignals.take(10).map((s) {
              final direction = s['direction'] ?? 'WAIT';
              final status = s['status'] ?? 'PENDING';
              final confidence = s['confidence'] ?? 0;
              final crypto = s['crypto'] ?? 'BTC';
              
              Color dirColor = direction == 'LONG' ? TV.green : (direction == 'SHORT' ? TV.red : TV.orange);
              Color statusColor = status == 'WIN' ? TV.green : (status == 'LOSS' ? TV.red : TV.orange);
              String statusEmoji = status == 'WIN' ? '✅' : (status == 'LOSS' ? '❌' : '⏳');
              
              // Tarih bilgisi
              String timeStr = '';
              try {
                final ts = s['timestamp'] ?? '';
                if (ts.toString().isNotEmpty) {
                  timeStr = ts.toString().substring(5, 16).replaceAll('T', ' ');
                }
              } catch (_) {}
              
              final entryPrice = s['entry_price'] ?? 0;
              final pnl = s['pnl_percent'];
              
              return Container(
                margin: const EdgeInsets.only(bottom: 8),
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: status == 'WIN' ? TV.green.withOpacity(0.05) : (status == 'LOSS' ? TV.red.withOpacity(0.05) : TV.bg),
                  borderRadius: BorderRadius.circular(8),
                  border: Border.all(color: status == 'WIN' ? TV.green.withOpacity(0.3) : (status == 'LOSS' ? TV.red.withOpacity(0.3) : TV.border)),
                ),
                child: Column(
                  children: [
                    Row(
                      children: [
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                          decoration: BoxDecoration(color: dirColor.withOpacity(0.2), borderRadius: BorderRadius.circular(4)),
                          child: Text(direction, style: TextStyle(fontSize: 10, color: dirColor, fontWeight: FontWeight.bold)),
                        ),
                        const SizedBox(width: 8),
                        Text(crypto, style: const TextStyle(fontSize: 11, color: TV.text, fontWeight: FontWeight.w600)),
                        const Spacer(),
                        Text(statusEmoji, style: const TextStyle(fontSize: 16)),
                        const SizedBox(width: 4),
                        Text(status, style: TextStyle(fontSize: 11, color: statusColor, fontWeight: FontWeight.bold)),
                      ],
                    ),
                    const SizedBox(height: 8),
                    Row(
                      children: [
                        Text('📅 $timeStr', style: const TextStyle(fontSize: 9, color: TV.textMuted)),
                        const Spacer(),
                        Text('Giriş: \$${_fmt(entryPrice)}', style: const TextStyle(fontSize: 9, color: TV.textDim)),
                        const SizedBox(width: 12),
                        Text('Güven: %${confidence.toStringAsFixed(0)}', style: const TextStyle(fontSize: 9, color: TV.textDim)),
                        if (pnl != null) ...[
                          const SizedBox(width: 12),
                          Text(
                            'PnL: ${pnl >= 0 ? '+' : ''}${pnl.toStringAsFixed(2)}%',
                            style: TextStyle(fontSize: 9, color: pnl >= 0 ? TV.green : TV.red, fontWeight: FontWeight.w600),
                          ),
                        ],
                      ],
                    ),
                  ],
                ),
              );
            }),
          ],
        ],
      ),
    );
  }
  
  Widget _buildJournalStat(String label, String value, Color color) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
      decoration: BoxDecoration(
        color: TV.bg,
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: TV.border),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(label, style: const TextStyle(fontSize: 11, color: TV.textDim)),
          Text(value, style: TextStyle(fontSize: 14, fontWeight: FontWeight.bold, color: color)),
        ],
      ),
    );
  }
  
  Widget _buildPoliticalNews(List politicalNews) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            const Text('🇺🇸', style: TextStyle(fontSize: 16)),
            const SizedBox(width: 6),
            const Text('POLİTİK & TRUMP HABERLERİ', style: TextStyle(fontSize: 10, color: TV.orange, fontWeight: FontWeight.w600)),
            const Spacer(),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
              decoration: BoxDecoration(
                color: TV.red.withOpacity(0.1),
                borderRadius: BorderRadius.circular(4),
                border: Border.all(color: TV.red.withOpacity(0.3)),
              ),
              child: const Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Icon(Icons.info_outline, size: 10, color: TV.red),
                  SizedBox(width: 4),
                  Text('Twitter API \$100+/ay', style: TextStyle(fontSize: 8, color: TV.red)),
                ],
              ),
            ),
          ],
        ),
        const SizedBox(height: 8),
        if (politicalNews.isEmpty)
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: TV.orange.withOpacity(0.1),
              borderRadius: BorderRadius.circular(8),
              border: Border.all(color: TV.orange.withOpacity(0.3)),
            ),
            child: const Column(
              children: [
                Text('⚠️ Twitter/X API Ücretli', style: TextStyle(fontSize: 11, color: TV.orange, fontWeight: FontWeight.w600)),
                SizedBox(height: 4),
                Text(
                  'Gerçek zamanlı Trump tweet\'leri için Twitter API gerekli (\$100+/ay). Şimdilik politik haber API\'lerinden veri çekiliyor.',
                  style: TextStyle(fontSize: 10, color: TV.textDim),
                  textAlign: TextAlign.center,
                ),
              ],
            ),
          ),
        const SizedBox(height: 12),
        ...politicalNews.take(3).map((n) => Container(
          margin: const EdgeInsets.only(bottom: 8),
          padding: const EdgeInsets.all(12),
          decoration: BoxDecoration(
            color: n['is_political'] == true ? TV.orange.withOpacity(0.1) : TV.bg,
            borderRadius: BorderRadius.circular(8),
            border: Border.all(color: n['is_political'] == true ? TV.orange.withOpacity(0.5) : TV.border),
          ),
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(n['emoji'] ?? '📰', style: const TextStyle(fontSize: 20)),
              const SizedBox(width: 12),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      n['title'] ?? '', 
                      style: TextStyle(
                        fontSize: 12, 
                        color: n['is_political'] == true ? TV.orange : TV.text, 
                        fontWeight: n['is_political'] == true ? FontWeight.w600 : FontWeight.w500,
                      ), 
                      maxLines: 2, 
                      overflow: TextOverflow.ellipsis,
                    ),
                    const SizedBox(height: 4),
                    Row(
                      children: [
                        Text(n['source'] ?? '', style: const TextStyle(fontSize: 10, color: TV.blue)),
                        if (n['is_political'] == true) ...[
                          const SizedBox(width: 8),
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                            decoration: BoxDecoration(
                              color: TV.orange,
                              borderRadius: BorderRadius.circular(4),
                            ),
                            child: const Text('HOT', style: TextStyle(fontSize: 8, color: Colors.white, fontWeight: FontWeight.bold)),
                          ),
                        ],
                      ],
                    ),
                  ],
                ),
              ),
            ],
          ),
        )),
      ],
    );
  }
  
  Widget _buildKillZoneStrategyCard(Map<String, dynamic>? kzStrategy) {
    if (kzStrategy == null) return const SizedBox();
    
    final asianRange = kzStrategy['asian_range'] ?? {};
    final activeStrategy = kzStrategy['active_strategy'] ?? {};
    final isActive = activeStrategy['is_active'] ?? false;
    
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: TV.card,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: TV.cyan, width: 2),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              const Icon(Icons.access_time_filled, color: TV.cyan, size: 20),
              const SizedBox(width: 8),
              const Text('KILL ZONE STRATEJİLERİ', 
                style: TextStyle(fontSize: 12, color: TV.cyan, fontWeight: FontWeight.w600, letterSpacing: 1)),
              const Spacer(),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                decoration: BoxDecoration(
                  color: isActive ? TV.green.withOpacity(0.1) : TV.orange.withOpacity(0.1),
                  borderRadius: BorderRadius.circular(4),
                  border: Border.all(color: isActive ? TV.green : TV.orange),
                ),
                child: Text(
                  isActive ? '🟢 AKTİF' : '⏳ BEKLİYOR',
                  style: TextStyle(fontSize: 10, color: isActive ? TV.green : TV.orange),
                ),
              ),
            ],
          ),
          const SizedBox(height: 20),
          
          // Asian Range
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: TV.bg,
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: TV.orange.withOpacity(0.5)),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    const Text('🌏', style: TextStyle(fontSize: 20)),
                    const SizedBox(width: 8),
                    const Text('ASIAN RANGE', style: TextStyle(fontSize: 12, color: TV.orange, fontWeight: FontWeight.w600)),
                    const Spacer(),
                    Text(
                      asianRange['position_emoji'] ?? '',
                      style: const TextStyle(fontSize: 16),
                    ),
                    const SizedBox(width: 4),
                    Text(
                      asianRange['position'] ?? 'N/A',
                      style: TextStyle(
                        fontSize: 11,
                        fontWeight: FontWeight.bold,
                        color: asianRange['position'] == 'ABOVE' ? TV.green 
                             : (asianRange['position'] == 'BELOW' ? TV.red : TV.orange),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 12),
                Row(
                  children: [
                    Expanded(
                      child: _buildRangeLevel('HIGH', asianRange['asian_high'], TV.red, asianRange['high_swept'] == true),
                    ),
                    const SizedBox(width: 8),
                    Expanded(
                      child: _buildRangeLevel('MID', asianRange['asian_mid'], TV.orange, false),
                    ),
                    const SizedBox(width: 8),
                    Expanded(
                      child: _buildRangeLevel('LOW', asianRange['asian_low'], TV.green, asianRange['low_swept'] == true),
                    ),
                  ],
                ),
                const SizedBox(height: 12),
                Container(
                  width: double.infinity,
                  padding: const EdgeInsets.all(10),
                  decoration: BoxDecoration(
                    color: TV.card,
                    borderRadius: BorderRadius.circular(6),
                  ),
                  child: Row(
                    children: [
                      const Text('💡 ', style: TextStyle(fontSize: 14)),
                      Expanded(
                        child: Text(
                          asianRange['suggestion'] ?? 'Veri bekleniyor...',
                          style: const TextStyle(fontSize: 11, color: TV.text),
                        ),
                      ),
                    ],
                  ),
                ),
                if (asianRange['high_swept'] == true || asianRange['low_swept'] == true) ...[
                  const SizedBox(height: 8),
                  Container(
                    width: double.infinity,
                    padding: const EdgeInsets.all(10),
                    decoration: BoxDecoration(
                      color: TV.blue.withOpacity(0.1),
                      borderRadius: BorderRadius.circular(6),
                      border: Border.all(color: TV.blue),
                    ),
                    child: Text(
                      asianRange['sweep_status'] ?? '',
                      style: const TextStyle(fontSize: 11, color: TV.blue, fontWeight: FontWeight.w600),
                      textAlign: TextAlign.center,
                    ),
                  ),
                ],
              ],
            ),
          ),
          const SizedBox(height: 16),
          
          // Active Zone Strategy
          if (isActive) ...[
            _buildActiveZoneCard(activeStrategy),
          ] else ...[
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: TV.bg,
                borderRadius: BorderRadius.circular(12),
              ),
              child: Column(
                children: [
                  const Text('⏳', style: TextStyle(fontSize: 32)),
                  const SizedBox(height: 8),
                  Text(
                    'Sonraki: ${activeStrategy['next_zone_name'] ?? 'N/A'}',
                    style: const TextStyle(fontSize: 14, color: TV.text, fontWeight: FontWeight.w600),
                  ),
                  Text(
                    '${activeStrategy['hours_until_next'] ?? 0} saat sonra',
                    style: const TextStyle(fontSize: 12, color: TV.textDim),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    activeStrategy['suggestion'] ?? '',
                    style: const TextStyle(fontSize: 11, color: TV.textMuted),
                    textAlign: TextAlign.center,
                  ),
                ],
              ),
            ),
          ],
        ],
      ),
    );
  }
  
  Widget _buildRangeLevel(String label, dynamic value, Color color, bool swept) {
    return Container(
      padding: const EdgeInsets.all(10),
      decoration: BoxDecoration(
        color: swept ? color.withOpacity(0.15) : TV.card,
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: swept ? color : TV.border),
      ),
      child: Column(
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text(label, style: TextStyle(fontSize: 9, color: color, fontWeight: FontWeight.w600)),
              if (swept) ...[
                const SizedBox(width: 4),
                const Text('🎯', style: TextStyle(fontSize: 10)),
              ],
            ],
          ),
          const SizedBox(height: 4),
          Text(
            '\$${_fmt(value)}',
            style: const TextStyle(fontSize: 11, color: TV.text, fontFamily: 'monospace'),
          ),
        ],
      ),
    );
  }
  
  Widget _buildActiveZoneCard(Map<String, dynamic> strategy) {
    final zone = strategy['zone'] ?? {};
    final phase = strategy['phase'] ?? 'MID';
    final phaseSuggestion = strategy['phase_suggestion'] ?? '';
    
    Color zoneColor = _hexToColor(zone['color'] ?? '#2962FF');
    
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: zoneColor.withOpacity(0.1),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: zoneColor),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Text(zone['emoji'] ?? '📊', style: const TextStyle(fontSize: 24)),
              const SizedBox(width: 12),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      zone['name'] ?? 'Unknown',
                      style: TextStyle(fontSize: 14, color: zoneColor, fontWeight: FontWeight.bold),
                    ),
                    Text(
                      zone['primary_behavior'] ?? '',
                      style: const TextStyle(fontSize: 10, color: TV.textDim),
                    ),
                  ],
                ),
              ),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                decoration: BoxDecoration(
                  color: phase == 'EARLY' ? TV.orange : (phase == 'LATE' ? TV.red : TV.green),
                  borderRadius: BorderRadius.circular(4),
                ),
                child: Text(
                  '$phase (${strategy['minutes_in_zone']}dk)',
                  style: const TextStyle(fontSize: 9, color: Colors.white, fontWeight: FontWeight.bold),
                ),
              ),
            ],
          ),
          const SizedBox(height: 12),
          
          // Phase Suggestion
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: TV.bg,
              borderRadius: BorderRadius.circular(8),
            ),
            child: Row(
              children: [
                const Text('💡 ', style: TextStyle(fontSize: 16)),
                Expanded(
                  child: Text(
                    phaseSuggestion,
                    style: const TextStyle(fontSize: 12, color: TV.text, fontWeight: FontWeight.w500),
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 12),
          
          // Warning
          if (zone['warning'] != null)
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(10),
              decoration: BoxDecoration(
                color: TV.red.withOpacity(0.1),
                borderRadius: BorderRadius.circular(6),
                border: Border.all(color: TV.red.withOpacity(0.3)),
              ),
              child: Text(
                zone['warning'],
                style: const TextStyle(fontSize: 10, color: TV.red),
                textAlign: TextAlign.center,
              ),
            ),
          
          const SizedBox(height: 12),
          
          // Key Concepts
          const Text('📚 KEY CONCEPTS', style: TextStyle(fontSize: 10, color: TV.textDim, fontWeight: FontWeight.w600)),
          const SizedBox(height: 8),
          ...(zone['key_concepts'] as List? ?? []).take(3).map((concept) => Container(
            margin: const EdgeInsets.only(bottom: 6),
            padding: const EdgeInsets.all(10),
            decoration: BoxDecoration(
              color: TV.bg,
              borderRadius: BorderRadius.circular(6),
            ),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(concept['emoji'] ?? '📌', style: const TextStyle(fontSize: 14)),
                const SizedBox(width: 8),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(concept['name'] ?? '', style: const TextStyle(fontSize: 11, color: TV.text, fontWeight: FontWeight.w600)),
                      Text(concept['how_to_use'] ?? '', style: const TextStyle(fontSize: 10, color: TV.textDim)),
                    ],
                  ),
                ),
              ],
            ),
          )),
        ],
      ),
    );
  }
  
  Widget _buildNewsCard(Map<String, dynamic>? news) {
    if (news == null) return const SizedBox();
    
    final fearGreed = news['fear_greed'] ?? {};
    final cryptoNews = news['crypto_news'] as List? ?? [];
    final events = news['important_events'] as List? ?? [];
    final sentiment = news['market_sentiment'] ?? {};
    
    final fgValue = fearGreed['value'] ?? 50;
    final fgEmoji = fearGreed['emoji'] ?? '😐';
    final fgClass = fearGreed['classification'] ?? 'Neutral';
    final fgColor = _hexToColor(fearGreed['color'] ?? '#F7931A');
    final fgSuggestion = fearGreed['suggestion'] ?? '';
    
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: TV.card,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: TV.purple, width: 2),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              const Icon(Icons.newspaper, color: TV.purple, size: 20),
              const SizedBox(width: 8),
              const Text('PIYASA HABERLERİ & SENTIMENT', 
                style: TextStyle(fontSize: 12, color: TV.purple, fontWeight: FontWeight.w600, letterSpacing: 1)),
            ],
          ),
          const SizedBox(height: 20),
          
          // Fear & Greed Index
          Row(
            children: [
              // Fear & Greed Gauge
              Expanded(
                child: Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: TV.bg,
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: fgColor.withOpacity(0.5)),
                  ),
                  child: Column(
                    children: [
                      Text(fgEmoji, style: const TextStyle(fontSize: 40)),
                      const SizedBox(height: 8),
                      Text('$fgValue', style: TextStyle(fontSize: 32, fontWeight: FontWeight.bold, color: fgColor)),
                      Text(fgClass, style: TextStyle(fontSize: 12, color: fgColor)),
                      const SizedBox(height: 8),
                      Container(
                        height: 8,
                        decoration: BoxDecoration(
                          borderRadius: BorderRadius.circular(4),
                          gradient: const LinearGradient(colors: [TV.red, Color(0xFFFF6B00), TV.orange, TV.green, Color(0xFF00C853)]),
                        ),
                        child: Stack(
                          children: [
                            Positioned(
                              left: (fgValue / 100) * 180,
                              child: Container(
                                width: 4, height: 8,
                                decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(2)),
                              ),
                            ),
                          ],
                        ),
                      ),
                      const SizedBox(height: 8),
                      Text(fgSuggestion, style: const TextStyle(fontSize: 10, color: TV.textDim), textAlign: TextAlign.center),
                    ],
                  ),
                ),
              ),
              const SizedBox(width: 16),
              
              // Önemli Eventler
              Expanded(
                child: Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: TV.bg,
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: TV.border),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Row(
                        children: [
                          Icon(Icons.event, color: TV.orange, size: 16),
                          SizedBox(width: 6),
                          Text('ÖNEMLİ EVENTLER', style: TextStyle(fontSize: 10, color: TV.orange, fontWeight: FontWeight.w600)),
                        ],
                      ),
                      const SizedBox(height: 12),
                      if (events.isEmpty)
                        const Text('Yakın zamanda önemli event yok', style: TextStyle(fontSize: 11, color: TV.textMuted))
                      else
                        ...events.take(3).map((e) => Container(
                          margin: const EdgeInsets.only(bottom: 8),
                          padding: const EdgeInsets.all(8),
                          decoration: BoxDecoration(
                            color: e['impact'] == 'HIGH' ? TV.red.withOpacity(0.1) : TV.orange.withOpacity(0.1),
                            borderRadius: BorderRadius.circular(6),
                          ),
                          child: Row(
                            children: [
                              Text(e['emoji'] ?? '📅', style: const TextStyle(fontSize: 16)),
                              const SizedBox(width: 8),
                              Expanded(
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Text(e['name'] ?? '', style: const TextStyle(fontSize: 11, color: TV.text, fontWeight: FontWeight.w600)),
                                    Text(e['time'] ?? '', style: const TextStyle(fontSize: 9, color: TV.textDim)),
                                  ],
                                ),
                              ),
                              Container(
                                padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                                decoration: BoxDecoration(
                                  color: e['impact'] == 'HIGH' ? TV.red : TV.orange,
                                  borderRadius: BorderRadius.circular(4),
                                ),
                                child: Text(e['impact'] ?? '', style: const TextStyle(fontSize: 8, color: Colors.white, fontWeight: FontWeight.bold)),
                              ),
                            ],
                          ),
                        )),
                    ],
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 16),
          
          // Son Haberler
          const Row(
            children: [
              Icon(Icons.article, color: TV.cyan, size: 16),
              SizedBox(width: 6),
              Text('SON KRİPTO HABERLERİ', style: TextStyle(fontSize: 10, color: TV.cyan, fontWeight: FontWeight.w600)),
            ],
          ),
          const SizedBox(height: 12),
          
          // Politik/Trump Haberler
          _buildPoliticalNews(news['political_news'] as List? ?? []),
          const SizedBox(height: 16),
          
          if (cryptoNews.isEmpty)
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(color: TV.bg, borderRadius: BorderRadius.circular(8)),
              child: const Text('Haberler yükleniyor...', style: TextStyle(color: TV.textMuted), textAlign: TextAlign.center),
            )
          else
            ...cryptoNews.take(5).map((n) => Container(
              margin: const EdgeInsets.only(bottom: 8),
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: TV.bg,
                borderRadius: BorderRadius.circular(8),
                border: Border.all(color: TV.border),
              ),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(n['emoji'] ?? '📰', style: const TextStyle(fontSize: 20)),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(n['title'] ?? '', style: const TextStyle(fontSize: 12, color: TV.text, fontWeight: FontWeight.w500), maxLines: 2, overflow: TextOverflow.ellipsis),
                        const SizedBox(height: 4),
                        Row(
                          children: [
                            Text(n['source'] ?? '', style: const TextStyle(fontSize: 10, color: TV.blue)),
                            const SizedBox(width: 8),
                            Text('• ${n['time_ago'] ?? ''}', style: const TextStyle(fontSize: 10, color: TV.textMuted)),
                          ],
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            )),
        ],
      ),
    );
  }
  
  Widget _buildHeader(Map<String, dynamic>? reportData, Map<String, dynamic>? signal) {
    final summary = reportData?['summary'] ?? {};
    final price = (summary['current_price'] ?? 0).toDouble();
    final change = (summary['total_change_percent'] ?? 0).toDouble();
    final direction = signal?['direction'] ?? 'WAIT';
    Color changeColor = change >= 0 ? TV.green : TV.red;
    
    final cryptoSymbol = selectedCrypto == 'BTC' ? '₿' : '◎';
    final cryptoColor = selectedCrypto == 'BTC' ? TV.orange : TV.purple;
    
    final double displayPrice = price;
    
    return Container(
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(color: TV.card, borderRadius: BorderRadius.circular(12), border: Border.all(color: TV.border)),
      child: Row(
        children: [
          Row(
            children: [
              Container(
                padding: const EdgeInsets.all(14),
                decoration: BoxDecoration(color: cryptoColor.withOpacity(0.1), borderRadius: BorderRadius.circular(12)),
                child: Text(cryptoSymbol, style: TextStyle(fontSize: 32, color: cryptoColor)),
              ),
              const SizedBox(width: 16),
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('$selectedCrypto/USD', style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: TV.text)),
                  const Text('Son 24 saat raporu', style: TextStyle(fontSize: 12, color: TV.textDim)),
                ],
              ),
            ],
          ),
          const Spacer(),
          Column(
            crossAxisAlignment: CrossAxisAlignment.end,
            children: [
              Text('\$${_fmt(displayPrice)}', style: const TextStyle(fontSize: 28, fontWeight: FontWeight.bold, color: TV.text)),
              Row(
                children: [
                  Icon(change >= 0 ? Icons.arrow_upward : Icons.arrow_downward, color: changeColor, size: 16),
                  Text(' ${change >= 0 ? '+' : ''}${change.toStringAsFixed(2)}%', style: TextStyle(fontSize: 14, fontWeight: FontWeight.w600, color: changeColor)),
                ],
              ),
            ],
          ),
          const SizedBox(width: 32),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
            decoration: BoxDecoration(
              color: direction == 'LONG' ? TV.greenBg : (direction == 'SHORT' ? TV.redBg : TV.orange.withOpacity(0.1)),
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: direction == 'LONG' ? TV.green : (direction == 'SHORT' ? TV.red : TV.orange), width: 2),
            ),
            child: Column(
              children: [
                Text(direction == 'LONG' ? '🟢' : (direction == 'SHORT' ? '🔴' : '🟡'), style: const TextStyle(fontSize: 24)),
                Text(direction, style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: direction == 'LONG' ? TV.green : (direction == 'SHORT' ? TV.red : TV.orange))),
              ],
            ),
          ),
        ],
      ),
    );
  }
  
  Widget _buildCandlestickChart(Map<String, dynamic>? btc) {
    final candles = btc?['candles'] as List? ?? [];
    if (candles.isEmpty) return const SizedBox();
    
    // Min/Max bul
    double minPrice = double.infinity;
    double maxPrice = 0;
    for (var c in candles) {
      final low = (c['low'] ?? 0).toDouble();
      final high = (c['high'] ?? 0).toDouble();
      if (low < minPrice) minPrice = low;
      if (high > maxPrice) maxPrice = high;
    }
    final range = maxPrice - minPrice;
    final padding = range * 0.1;
    minPrice -= padding;
    maxPrice += padding;
    final totalRange = maxPrice - minPrice;
    
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(color: TV.card, borderRadius: BorderRadius.circular(12), border: Border.all(color: TV.border)),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Row(
                children: [
                  Text(
                    selectedCrypto == 'SOL' ? '◎' : '₿',
                    style: TextStyle(fontSize: 16, color: selectedCrypto == 'SOL' ? TV.purple : TV.orange),
                  ),
                  const SizedBox(width: 8),
                  Text('$selectedCrypto CANDLESTICK CHART', style: const TextStyle(fontSize: 12, color: TV.textDim, fontWeight: FontWeight.w600)),
                ],
              ),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                decoration: BoxDecoration(color: TV.blue.withOpacity(0.1), borderRadius: BorderRadius.circular(4)),
                child: const Text('1H • 24 Candles', style: TextStyle(fontSize: 10, color: TV.blue)),
              ),
            ],
          ),
          const SizedBox(height: 16),
          SizedBox(
            height: 250,
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                // Y-axis labels
                SizedBox(
                  width: 60,
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    crossAxisAlignment: CrossAxisAlignment.end,
                    children: [
                      Text('\$${_fmt(maxPrice)}', style: const TextStyle(fontSize: 9, color: TV.textMuted)),
                      Text('\$${_fmt((maxPrice + minPrice) / 2)}', style: const TextStyle(fontSize: 9, color: TV.textMuted)),
                      Text('\$${_fmt(minPrice)}', style: const TextStyle(fontSize: 9, color: TV.textMuted)),
                    ],
                  ),
                ),
                const SizedBox(width: 8),
                // Chart
                Expanded(
                  child: CustomPaint(
                    painter: CandlestickPainter(candles, minPrice, totalRange),
                    child: Container(),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
  
  Widget _buildSupplyDemandCard() {
    // Seçilen kripto için supply/demand
    Map<String, dynamic>? sdData;
    if (selectedCrypto == 'SOL' && solanaData != null) {
      sdData = solanaData!['supply_demand'];
    } else {
      sdData = supplyDemand;
    }
    
    if (sdData == null) {
      return Container(
        padding: const EdgeInsets.all(20),
        decoration: BoxDecoration(color: TV.card, borderRadius: BorderRadius.circular(12), border: Border.all(color: TV.border)),
        child: const Column(
          children: [
            Icon(Icons.hourglass_empty, color: TV.textDim, size: 32),
            SizedBox(height: 8),
            Text('Supply/Demand yükleniyor...', style: TextStyle(color: TV.textDim, fontSize: 12)),
          ],
        ),
      );
    }
    
    final supplyZones = sdData['supply_zones'] as List? ?? [];
    final demandZones = sdData['demand_zones'] as List? ?? [];
    final suggestion = sdData['suggestion'] ?? '';
    final bias = sdData['bias'] ?? 'NEUTRAL';
    
    Color biasColor = bias == 'LONG' ? TV.green : (bias == 'SHORT' ? TV.red : TV.orange);
    
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(color: TV.card, borderRadius: BorderRadius.circular(12), border: Border.all(color: TV.border)),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text('SUPPLY / DEMAND', style: TextStyle(fontSize: 12, color: TV.textDim, fontWeight: FontWeight.w600)),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                decoration: BoxDecoration(color: biasColor.withOpacity(0.1), borderRadius: BorderRadius.circular(4), border: Border.all(color: biasColor)),
                child: Text(bias, style: TextStyle(fontSize: 10, fontWeight: FontWeight.bold, color: biasColor)),
              ),
            ],
          ),
          const SizedBox(height: 12),
          
          // Suggestion
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(10),
            decoration: BoxDecoration(color: biasColor.withOpacity(0.1), borderRadius: BorderRadius.circular(6)),
            child: Text(suggestion, style: TextStyle(fontSize: 11, color: biasColor)),
          ),
          const SizedBox(height: 16),
          
          // Supply Zones
          const Text('🔴 SUPPLY ZONES', style: TextStyle(fontSize: 10, color: TV.red, fontWeight: FontWeight.w600)),
          const SizedBox(height: 8),
          ...supplyZones.take(3).map((zone) => _buildZoneRow(zone, TV.red)),
          
          const SizedBox(height: 12),
          
          // Demand Zones
          const Text('🟢 DEMAND ZONES', style: TextStyle(fontSize: 10, color: TV.green, fontWeight: FontWeight.w600)),
          const SizedBox(height: 8),
          ...demandZones.take(3).map((zone) => _buildZoneRow(zone, TV.green)),
        ],
      ),
    );
  }
  
  Widget _buildZoneRow(Map<String, dynamic> zone, Color color) {
    final top = zone['zone_top'] ?? zone['top'] ?? 0;
    final bottom = zone['zone_bottom'] ?? zone['bottom'] ?? 0;
    final freshness = zone['freshness'] ?? 'TESTED';
    final isFresh = freshness == 'FRESH';
    
    return Container(
      margin: const EdgeInsets.only(bottom: 6),
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
      decoration: BoxDecoration(
        color: color.withOpacity(0.05),
        borderRadius: BorderRadius.circular(6),
        border: Border.all(color: color.withOpacity(0.3)),
      ),
      child: Row(
        children: [
          Expanded(
            child: Text('\$${_fmt(bottom)} - \$${_fmt(top)}', style: const TextStyle(fontSize: 11, color: TV.text, fontFamily: 'monospace')),
          ),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
            decoration: BoxDecoration(
              color: isFresh ? TV.green.withOpacity(0.2) : TV.textMuted.withOpacity(0.2),
              borderRadius: BorderRadius.circular(4),
            ),
            child: Text(freshness, style: TextStyle(fontSize: 9, color: isFresh ? TV.green : TV.textMuted)),
          ),
        ],
      ),
    );
  }
  
  Widget _buildFVGCard(Map<String, dynamic>? ict) {
    final fvgs = ict?['fair_value_gaps'] as List? ?? [];
    final orderBlocks = ict?['order_blocks'] as List? ?? [];
    
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(color: TV.card, borderRadius: BorderRadius.circular(12), border: Border.all(color: TV.border)),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('FVG & ORDER BLOCKS', style: TextStyle(fontSize: 12, color: TV.textDim, fontWeight: FontWeight.w600)),
          const SizedBox(height: 16),
          
          // FVGs
          const Text('📊 FAIR VALUE GAPS', style: TextStyle(fontSize: 10, color: TV.cyan, fontWeight: FontWeight.w600)),
          const SizedBox(height: 8),
          
          if (fvgs.isEmpty)
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(color: TV.bg, borderRadius: BorderRadius.circular(6)),
              child: const Text('Aktif FVG bulunamadı', style: TextStyle(fontSize: 11, color: TV.textMuted), textAlign: TextAlign.center),
            )
          else
            ...fvgs.map((fvg) {
              final isBullish = fvg['type'] == 'BULLISH_FVG';
              final color = isBullish ? TV.green : TV.red;
              return Container(
                margin: const EdgeInsets.only(bottom: 6),
                padding: const EdgeInsets.all(10),
                decoration: BoxDecoration(
                  color: color.withOpacity(0.05),
                  borderRadius: BorderRadius.circular(6),
                  border: Border.all(color: color.withOpacity(0.3)),
                ),
                child: Row(
                  children: [
                    Text(fvg['emoji'] ?? '', style: const TextStyle(fontSize: 14)),
                    const SizedBox(width: 8),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(isBullish ? 'Bullish FVG' : 'Bearish FVG', style: TextStyle(fontSize: 11, color: color, fontWeight: FontWeight.w600)),
                          Text('\$${_fmt(fvg['bottom'])} - \$${_fmt(fvg['top'])}', style: const TextStyle(fontSize: 10, color: TV.textDim)),
                        ],
                      ),
                    ),
                  ],
                ),
              );
            }),
          
          const SizedBox(height: 16),
          
          // Order Blocks
          const Text('🧱 ORDER BLOCKS', style: TextStyle(fontSize: 10, color: TV.purple, fontWeight: FontWeight.w600)),
          const SizedBox(height: 8),
          
          if (orderBlocks.isEmpty)
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(color: TV.bg, borderRadius: BorderRadius.circular(6)),
              child: const Text('Aktif OB bulunamadı', style: TextStyle(fontSize: 11, color: TV.textMuted), textAlign: TextAlign.center),
            )
          else
            ...orderBlocks.map((ob) {
              final isBullish = ob['type'] == 'BULLISH_OB';
              final color = isBullish ? TV.green : TV.red;
              return Container(
                margin: const EdgeInsets.only(bottom: 6),
                padding: const EdgeInsets.all(10),
                decoration: BoxDecoration(
                  color: color.withOpacity(0.05),
                  borderRadius: BorderRadius.circular(6),
                  border: Border.all(color: color.withOpacity(0.3)),
                ),
                child: Row(
                  children: [
                    Text(ob['emoji'] ?? '', style: const TextStyle(fontSize: 14)),
                    const SizedBox(width: 8),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(isBullish ? 'Bullish OB' : 'Bearish OB', style: TextStyle(fontSize: 11, color: color, fontWeight: FontWeight.w600)),
                          Text('\$${_fmt(ob['low'])} - \$${_fmt(ob['high'])}', style: const TextStyle(fontSize: 10, color: TV.textDim)),
                        ],
                      ),
                    ),
                  ],
                ),
              );
            }),
        ],
      ),
    );
  }
  
  Widget _buildSolanaCard() {
    if (solanaData == null) return const SizedBox();
    
    final analysis = solanaData!['analysis'] ?? {};
    final price = analysis['current_price'] ?? 0;
    final trend = analysis['trend'] ?? 'NEUTRAL';
    final supplyZones = solanaData!['supply_demand']?['supply_zones'] as List? ?? [];
    final demandZones = solanaData!['supply_demand']?['demand_zones'] as List? ?? [];
    
    Color trendColor = trend == 'BULLISH' ? TV.green : (trend == 'BEARISH' ? TV.red : TV.orange);
    
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: TV.card, 
        borderRadius: BorderRadius.circular(12), 
        border: Border.all(color: TV.purple, width: 2),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Container(
                padding: const EdgeInsets.all(10),
                decoration: BoxDecoration(color: TV.purple.withOpacity(0.1), borderRadius: BorderRadius.circular(8)),
                child: const Text('◎', style: TextStyle(fontSize: 24, color: TV.purple)),
              ),
              const SizedBox(width: 12),
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text('SOLANA (SOL)', style: TextStyle(fontSize: 14, fontWeight: FontWeight.bold, color: TV.text)),
                  Text('Fiyat: \$${_fmt(price)}', style: const TextStyle(fontSize: 12, color: TV.textDim)),
                ],
              ),
              const Spacer(),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                decoration: BoxDecoration(color: trendColor.withOpacity(0.1), borderRadius: BorderRadius.circular(6), border: Border.all(color: trendColor)),
                child: Text(trend, style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: trendColor)),
              ),
            ],
          ),
          const SizedBox(height: 16),
          
          Row(
            children: [
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text('🔴 Supply Zones', style: TextStyle(fontSize: 10, color: TV.red)),
                    const SizedBox(height: 4),
                    ...supplyZones.take(2).map((z) => Padding(
                      padding: const EdgeInsets.only(bottom: 4),
                      child: Text('\$${_fmt(z['zone_bottom'])} - \$${_fmt(z['zone_top'])}', style: const TextStyle(fontSize: 10, color: TV.textDim)),
                    )),
                  ],
                ),
              ),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text('🟢 Demand Zones', style: TextStyle(fontSize: 10, color: TV.green)),
                    const SizedBox(height: 4),
                    ...demandZones.take(2).map((z) => Padding(
                      padding: const EdgeInsets.only(bottom: 4),
                      child: Text('\$${_fmt(z['zone_bottom'])} - \$${_fmt(z['zone_top'])}', style: const TextStyle(fontSize: 10, color: TV.textDim)),
                    )),
                  ],
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
  
  Widget _buildBacktestCard(Map<String, dynamic>? backtest) {
    if (backtest == null || backtest['error'] != null) {
      return const SizedBox();
    }
    
    final winRate = (backtest['win_rate'] ?? 0).toDouble();
    final totalTrades = backtest['total_trades'] ?? 0;
    final profitFactor = backtest['profit_factor'] ?? 0;
    final longWinRate = (backtest['long_win_rate'] ?? 0).toDouble();
    final shortWinRate = (backtest['short_win_rate'] ?? 0).toDouble();
    final maxDrawdown = backtest['max_drawdown_percent'] ?? 0;
    final expectancy = backtest['expectancy'] ?? 0;
    
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: TV.card,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: TV.blue, width: 2),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              const Icon(Icons.science, color: TV.blue, size: 20),
              const SizedBox(width: 8),
              const Text('BACKTEST SONUÇLARI', 
                style: TextStyle(fontSize: 12, color: TV.blue, fontWeight: FontWeight.w600, letterSpacing: 1)),
              const Spacer(),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                decoration: BoxDecoration(
                  color: TV.blue.withOpacity(0.1),
                  borderRadius: BorderRadius.circular(4),
                ),
                child: Text('$totalTrades trade analiz edildi',
                  style: const TextStyle(fontSize: 10, color: TV.blue)),
              ),
            ],
          ),
          const SizedBox(height: 8),
          const Text('Bu oranlar TAHMİN DEĞİL, geçmiş verilerden hesaplanmış GERÇEK istatistiklerdir.',
            style: TextStyle(fontSize: 10, color: TV.textMuted, fontStyle: FontStyle.italic)),
          const SizedBox(height: 16),
          
          Row(
            children: [
              Expanded(child: _buildBacktestStat('WIN RATE', '%${winRate.toStringAsFixed(1)}', 
                winRate >= 55 ? TV.green : (winRate >= 45 ? TV.orange : TV.red))),
              const SizedBox(width: 12),
              Expanded(child: _buildBacktestStat('PROFIT FACTOR', profitFactor.toStringAsFixed(2), 
                profitFactor >= 1.5 ? TV.green : (profitFactor >= 1 ? TV.orange : TV.red))),
              const SizedBox(width: 12),
              Expanded(child: _buildBacktestStat('EXPECTANCY', expectancy.toStringAsFixed(3), 
                expectancy > 0 ? TV.green : TV.red)),
            ],
          ),
          const SizedBox(height: 12),
          Row(
            children: [
              Expanded(child: _buildBacktestStat('LONG WIN', '%${longWinRate.toStringAsFixed(1)}', 
                longWinRate >= 55 ? TV.green : TV.textDim)),
              const SizedBox(width: 12),
              Expanded(child: _buildBacktestStat('SHORT WIN', '%${shortWinRate.toStringAsFixed(1)}', 
                shortWinRate >= 55 ? TV.green : TV.textDim)),
              const SizedBox(width: 12),
              Expanded(child: _buildBacktestStat('MAX DRAWDOWN', '%${maxDrawdown.toStringAsFixed(1)}', TV.red)),
            ],
          ),
        ],
      ),
    );
  }
  
  Widget _buildBacktestStat(String label, String value, Color valueColor) {
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: TV.bg,
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: TV.border),
      ),
      child: Column(
        children: [
          Text(label, style: const TextStyle(fontSize: 9, color: TV.textMuted, fontWeight: FontWeight.w600)),
          const SizedBox(height: 6),
          Text(value, style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: valueColor)),
        ],
      ),
    );
  }
  
  Widget _buildMarketStructureCard(Map<String, dynamic>? ict) {
    final ms = ict?['market_structure'] ?? {};
    final trend = ms['trend'] ?? 'RANGING';
    final emoji = ms['trend_emoji'] ?? '➡️';
    final structure = ms['structure'] ?? '';
    final bos = ms['bos_detected'] ?? false;
    Color trendColor = trend == 'BULLISH' ? TV.green : (trend == 'BEARISH' ? TV.red : TV.orange);
    
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(color: TV.card, borderRadius: BorderRadius.circular(12), border: Border.all(color: TV.border)),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('MARKET STRUCTURE', style: TextStyle(fontSize: 12, color: TV.textDim, fontWeight: FontWeight.w600)),
          const SizedBox(height: 16),
          Row(
            children: [
              Text(emoji, style: const TextStyle(fontSize: 32)),
              const SizedBox(width: 12),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(trend, style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: trendColor)),
                    Text(structure, style: const TextStyle(fontSize: 11, color: TV.textDim)),
                  ],
                ),
              ),
              if (bos)
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                  decoration: BoxDecoration(color: TV.blue.withOpacity(0.1), borderRadius: BorderRadius.circular(4), border: Border.all(color: TV.blue)),
                  child: const Text('BOS', style: TextStyle(fontSize: 10, color: TV.blue, fontWeight: FontWeight.bold)),
                ),
            ],
          ),
        ],
      ),
    );
  }
  
  Widget _buildPremiumDiscountCard(Map<String, dynamic>? ict) {
    final pd = ict?['premium_discount'] ?? {};
    final zone = pd['current_zone'] ?? 'EQUILIBRIUM';
    final position = (pd['position_percent'] ?? 50).toDouble();
    Color zoneColor = zone == 'PREMIUM' ? TV.red : (zone == 'DISCOUNT' ? TV.green : TV.orange);
    
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(color: TV.card, borderRadius: BorderRadius.circular(12), border: Border.all(color: TV.border)),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('PREMIUM / DISCOUNT', style: TextStyle(fontSize: 12, color: TV.textDim, fontWeight: FontWeight.w600)),
          const SizedBox(height: 16),
          Container(
            height: 24,
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(4),
              gradient: const LinearGradient(colors: [TV.green, TV.orange, TV.red]),
            ),
            child: Stack(
              children: [
                Positioned(
                  left: (position / 100) * 230,
                  top: 2, bottom: 2,
                  child: Container(
                    width: 4,
                    decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(2), boxShadow: const [BoxShadow(color: Colors.black54, blurRadius: 4)]),
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 12),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text('Discount', style: TextStyle(fontSize: 10, color: TV.green)),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                decoration: BoxDecoration(color: zoneColor.withOpacity(0.1), borderRadius: BorderRadius.circular(6), border: Border.all(color: zoneColor)),
                child: Text(zone, style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: zoneColor)),
              ),
              const Text('Premium', style: TextStyle(fontSize: 10, color: TV.red)),
            ],
          ),
        ],
      ),
    );
  }
  
  String _fmt(dynamic v) {
    if (v == null) return '0';
    final n = v is int ? v.toDouble() : (v as double);
    return n.toStringAsFixed(2).replaceAllMapped(RegExp(r'(\d{1,3})(?=(\d{3})+(?!\d))'), (m) => '${m[1]},');
  }
  
  Color _hexToColor(String hex) {
    hex = hex.replaceAll('#', '');
    return Color(int.parse('FF$hex', radix: 16));
  }
}

// Custom Candlestick Painter
class CandlestickPainter extends CustomPainter {
  final List candles;
  final double minPrice;
  final double range;
  
  CandlestickPainter(this.candles, this.minPrice, this.range);
  
  @override
  void paint(Canvas canvas, Size size) {
    if (candles.isEmpty || range == 0) return;
    
    final candleWidth = size.width / candles.length;
    final bodyWidth = candleWidth * 0.6;
    final wickWidth = 1.5;
    
    for (var i = 0; i < candles.length; i++) {
      final c = candles[i];
      final open = (c['open'] ?? 0).toDouble();
      final close = (c['close'] ?? 0).toDouble();
      final high = (c['high'] ?? 0).toDouble();
      final low = (c['low'] ?? 0).toDouble();
      
      final isBullish = close >= open;
      final color = isBullish ? TV.green : TV.red;
      
      final x = i * candleWidth + candleWidth / 2;
      
      // Convert price to Y coordinate (inverted because canvas Y starts from top)
      double priceToY(double price) => size.height - ((price - minPrice) / range * size.height);
      
      final openY = priceToY(open);
      final closeY = priceToY(close);
      final highY = priceToY(high);
      final lowY = priceToY(low);
      
      // Draw wick
      final wickPaint = Paint()
        ..color = color
        ..strokeWidth = wickWidth;
      canvas.drawLine(Offset(x, highY), Offset(x, lowY), wickPaint);
      
      // Draw body
      final bodyPaint = Paint()
        ..color = color
        ..style = isBullish ? PaintingStyle.fill : PaintingStyle.fill;
      
      final bodyTop = math.min(openY, closeY);
      final bodyBottom = math.max(openY, closeY);
      final bodyHeight = math.max(bodyBottom - bodyTop, 2.0);
      
      canvas.drawRRect(
        RRect.fromRectAndRadius(
          Rect.fromLTWH(x - bodyWidth / 2, bodyTop, bodyWidth, bodyHeight),
          const Radius.circular(1),
        ),
        bodyPaint,
      );
    }
  }
  
  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => true;
}
