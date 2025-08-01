# sinais/views.py
from django.db import connection
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    with connection.cursor() as cursor:
        # Trades bem sucedidos
        cursor.execute("""
            SELECT hs.symbol, hs.price, hs.signal, hs.timestamp, t.type, hs.sinal, t.percentage 
            FROM sinais.historical_signals hs
            INNER JOIN sinais.trades t ON t.signal_id = hs.id
            WHERE t.percentage > 0
            UNION ALL
            SELECT hss.symbol, hss.price, hss.signal, hss.timestamp, ts.type, hss.sinal, ts.percentage 
            FROM sinais.historical_signals_short hss
            INNER JOIN sinais.trades_short ts ON ts.signal_id = hss.id
            WHERE ts.percentage > 0
            LIMIT 10
        """)
        winning_trades = cursor.fetchall()

        # Trades mal sucedidos
        cursor.execute("""
            SELECT hs.symbol, hs.price, hs.signal, hs.timestamp, t.type, hs.sinal, t.percentage 
            FROM sinais.historical_signals hs
            INNER JOIN sinais.trades t ON t.signal_id = hs.id
            WHERE t.percentage < 0
            UNION ALL
            SELECT hss.symbol, hss.price, hss.signal, hss.timestamp, ts.type, hss.sinal, ts.percentage 
            FROM sinais.historical_signals_short hss
            INNER JOIN sinais.trades_short ts ON ts.signal_id = hss.id
            WHERE ts.percentage < 0
            LIMIT 10
        """)
        losing_trades = cursor.fetchall()

        # Estatísticas totais
        cursor.execute("""
            SELECT 
                'Ganhos' AS tipo,
                SUM(percentage) AS total,
                COUNT(*) AS quantidade
            FROM (
                SELECT percentage FROM sinais.trades_short WHERE profit > 0
                UNION ALL
                SELECT percentage FROM sinais.trades WHERE profit > 0
            ) AS ganhos
            UNION ALL
            SELECT 
                'Perdas' AS tipo,
                SUM(percentage) AS total,
                COUNT(*) AS quantidade
            FROM (
                SELECT percentage FROM sinais.trades_short WHERE profit < 0
                UNION ALL
                SELECT percentage FROM sinais.trades WHERE profit < 0
            ) AS perdas
        """)
        stats = cursor.fetchall()

    return render(request, 'home.html', {
        'winning_trades': winning_trades,
        'losing_trades': losing_trades,
        'stats': stats,
        'user': request.user
    })