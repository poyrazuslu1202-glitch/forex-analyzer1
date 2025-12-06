// ============================================
// FOREX ANALYZER - ICT Concepts + Trade Signals
// TradingView Dark Theme (Grafiksiz versiyon)
// ============================================

import 'package:flutter/material.dart';
import 'dart:convert';
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
  String? error;
  final String apiUrl = 'http://localhost:8000';

  @override
  void initState() {
    super.initState();
    _fetchData();
  }
  
  Future<void> _fetchData() async {
    setState(() { isLoading = true; error = null; });
    
    try {
      final response = await http.get(Uri.parse('$apiUrl/full-report'));
      if (response.statusCode == 200) {
        setState(() { fullReport = json.decode(response.body); isLoading = false; });
      } else {
        setState(() { error = 'API Hatası: ${response.statusCode}'; isLoading = false; });
      }
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
    final signal = fullReport?['trade_signal'];
    final ict = fullReport?['ict_analysis'];
    
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
                  child: const Text('₿', style: TextStyle(fontSize: 24, color: TV.orange)),
                ),
                const SizedBox(width: 12),
                const Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text('FOREX ANALYZER', style: TextStyle(fontSize: 14, fontWeight: FontWeight.bold, color: TV.text, letterSpacing: 1)),
                    Text('ICT Strategy Edition', style: TextStyle(fontSize: 11, color: TV.textDim)),
                  ],
                ),
              ],
            ),
          ),
          
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
          }).toList(),
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
    
    final btc = fullReport!['btc_report'];
    final signal = fullReport!['trade_signal'];
    final ict = fullReport!['ict_analysis'];
    
    return SingleChildScrollView(
      padding: const EdgeInsets.all(24),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _buildHeader(btc, signal),
          const SizedBox(height: 24),
          _buildPriceChart(btc),
          const SizedBox(height: 24),
          Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Expanded(child: _buildSignalsCard(signal)),
              const SizedBox(width: 16),
              Expanded(child: _buildLevelsCard(signal)),
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
          _buildBacktestCard(fullReport!['backtest']),
          const SizedBox(height: 24),
          _buildCandleTable(btc),
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
  
  Widget _buildHeader(Map<String, dynamic>? btc, Map<String, dynamic>? signal) {
    final summary = btc?['summary'] ?? {};
    final price = summary['current_price'] ?? 0;
    final change = summary['total_change_percent'] ?? 0;
    final direction = signal?['direction'] ?? 'WAIT';
    Color changeColor = change >= 0 ? TV.green : TV.red;
    
    return Container(
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(color: TV.card, borderRadius: BorderRadius.circular(12), border: Border.all(color: TV.border)),
      child: Row(
        children: [
          Row(
            children: [
              Container(
                padding: const EdgeInsets.all(14),
                decoration: BoxDecoration(color: TV.orange.withOpacity(0.1), borderRadius: BorderRadius.circular(12)),
                child: const Text('₿', style: TextStyle(fontSize: 32, color: TV.orange)),
              ),
              const SizedBox(width: 16),
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text('BTC/USD', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: TV.text)),
                  Text('Son 24 saat raporu', style: TextStyle(fontSize: 12, color: TV.textDim)),
                ],
              ),
            ],
          ),
          const Spacer(),
          Column(
            crossAxisAlignment: CrossAxisAlignment.end,
            children: [
              Text('\$${_fmt(price)}', style: const TextStyle(fontSize: 28, fontWeight: FontWeight.bold, color: TV.text)),
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
  
  Widget _buildPriceChart(Map<String, dynamic>? btc) {
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
    
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(color: TV.card, borderRadius: BorderRadius.circular(12), border: Border.all(color: TV.border)),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('FİYAT GRAFİĞİ (Son 24 Saat)', style: TextStyle(fontSize: 12, color: TV.textDim, fontWeight: FontWeight.w600)),
          const SizedBox(height: 16),
          SizedBox(
            height: 200,
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.end,
              children: candles.map((c) {
                final open = (c['open'] ?? 0).toDouble();
                final close = (c['close'] ?? 0).toDouble();
                final isBull = close >= open;
                final height = ((close - minPrice) / range * 180).clamp(10.0, 180.0);
                
                return Expanded(
                  child: Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 1),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.end,
                      children: [
                        Container(
                          height: height,
                          decoration: BoxDecoration(
                            color: isBull ? TV.green : TV.red,
                            borderRadius: BorderRadius.circular(2),
                          ),
                        ),
                      ],
                    ),
                  ),
                );
              }).toList(),
            ),
          ),
          const SizedBox(height: 8),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text('\$${_fmt(minPrice)}', style: const TextStyle(fontSize: 10, color: TV.textMuted)),
              Text('\$${_fmt(maxPrice)}', style: const TextStyle(fontSize: 10, color: TV.textMuted)),
            ],
          ),
        ],
      ),
    );
  }
  
  Widget _buildSignalsCard(Map<String, dynamic>? signal) {
    final trendSignals = signal?['trend_signals'] as List? ?? [];
    final ictSignals = signal?['ict_signals'] as List? ?? [];
    
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(color: TV.card, borderRadius: BorderRadius.circular(12), border: Border.all(color: TV.border)),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('SİNYALLER', style: TextStyle(fontSize: 12, color: TV.textDim, fontWeight: FontWeight.w600)),
          const SizedBox(height: 16),
          ...trendSignals.take(5).map((s) {
            final isLong = s['type'] == 'LONG';
            return Padding(
              padding: const EdgeInsets.only(bottom: 8),
              child: Row(
                children: [
                  Icon(isLong ? Icons.arrow_upward : Icons.arrow_downward, size: 14, color: isLong ? TV.green : TV.red),
                  const SizedBox(width: 8),
                  Expanded(child: Text(s['name'] ?? '', style: const TextStyle(fontSize: 11, color: TV.text))),
                  Text('+${s['weight']}', style: TextStyle(fontSize: 10, color: isLong ? TV.green : TV.red)),
                ],
              ),
            );
          }).toList(),
          if (ictSignals.isNotEmpty) ...[
            const SizedBox(height: 8),
            const Divider(color: TV.border),
            const SizedBox(height: 8),
            ...ictSignals.map((s) => Padding(
              padding: const EdgeInsets.only(bottom: 6),
              child: Text(s, style: const TextStyle(fontSize: 11, color: TV.blue)),
            )).toList(),
          ],
        ],
      ),
    );
  }
  
  Widget _buildLevelsCard(Map<String, dynamic>? signal) {
    final levels = signal?['levels'] ?? {};
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(color: TV.card, borderRadius: BorderRadius.circular(12), border: Border.all(color: TV.border)),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('DESTEK / DİRENÇ', style: TextStyle(fontSize: 12, color: TV.textDim, fontWeight: FontWeight.w600)),
          const SizedBox(height: 16),
          _levelRow('R3', levels['resistance_3'], TV.red),
          _levelRow('R2', levels['resistance_2'], TV.red),
          _levelRow('R1', levels['resistance_1'], TV.red),
          const Divider(color: TV.border, height: 24),
          _levelRow('Pivot', levels['pivot'], TV.blue),
          const Divider(color: TV.border, height: 24),
          _levelRow('S1', levels['support_1'], TV.green),
          _levelRow('S2', levels['support_2'], TV.green),
          _levelRow('S3', levels['support_3'], TV.green),
        ],
      ),
    );
  }
  
  Widget _levelRow(String label, dynamic value, Color color) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(label, style: TextStyle(fontSize: 11, color: color, fontWeight: FontWeight.w600)),
          Text('\$${_fmt(value)}', style: const TextStyle(fontSize: 11, color: TV.text, fontFamily: 'monospace')),
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
  
  Widget _buildCandleTable(Map<String, dynamic>? btc) {
    final candles = btc?['candles'] as List? ?? [];
    
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(color: TV.card, borderRadius: BorderRadius.circular(12), border: Border.all(color: TV.border)),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('SON 24 SAAT MUM DETAYLARI', style: TextStyle(fontSize: 12, color: TV.textDim, fontWeight: FontWeight.w600)),
          const SizedBox(height: 16),
          Container(
            padding: const EdgeInsets.symmetric(vertical: 8),
            decoration: const BoxDecoration(border: Border(bottom: BorderSide(color: TV.border))),
            child: const Row(
              children: [
                SizedBox(width: 30),
                SizedBox(width: 60, child: Text('SAAT', style: TextStyle(fontSize: 10, color: TV.textMuted))),
                Expanded(child: Text('AÇILIŞ', textAlign: TextAlign.right, style: TextStyle(fontSize: 10, color: TV.textMuted))),
                Expanded(child: Text('KAPANIŞ', textAlign: TextAlign.right, style: TextStyle(fontSize: 10, color: TV.textMuted))),
                SizedBox(width: 70, child: Text('DEĞİŞİM', textAlign: TextAlign.right, style: TextStyle(fontSize: 10, color: TV.textMuted))),
              ],
            ),
          ),
          ...candles.map((c) {
            final isBull = c['type'] == 'YESIL';
            final color = isBull ? TV.green : TV.red;
            final ts = (c['timestamp'] ?? '').toString();
            final timeStr = ts.length >= 16 ? ts.substring(11, 16) : ts;
            
            return Container(
              padding: const EdgeInsets.symmetric(vertical: 8),
              decoration: const BoxDecoration(border: Border(bottom: BorderSide(color: TV.border, width: 0.3))),
              child: Row(
                children: [
                  SizedBox(width: 30, child: Text(c['emoji'] ?? '', style: const TextStyle(fontSize: 12))),
                  SizedBox(width: 60, child: Text(timeStr, style: const TextStyle(fontSize: 11, color: TV.text, fontFamily: 'monospace'))),
                  Expanded(child: Text('\$${_fmt(c['open'])}', textAlign: TextAlign.right, style: const TextStyle(fontSize: 11, color: TV.textDim, fontFamily: 'monospace'))),
                  Expanded(child: Text('\$${_fmt(c['close'])}', textAlign: TextAlign.right, style: TextStyle(fontSize: 11, color: color, fontFamily: 'monospace', fontWeight: FontWeight.w600))),
                  SizedBox(width: 70, child: Text('${c['change_percent']?.toStringAsFixed(2)}%', textAlign: TextAlign.right, style: TextStyle(fontSize: 11, color: color, fontFamily: 'monospace'))),
                ],
              ),
            );
          }).toList(),
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



