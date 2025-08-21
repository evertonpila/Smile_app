# sinais/views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db import connection
from .forms import UserForm, CredenciaisForm
from .models import CredenciaisAPI

from django.contrib import messages

@login_required
def dashboard(request):
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

    return render(request, 'dashboard.html', {
        'winning_trades': winning_trades,
        'losing_trades': losing_trades,
        'stats': stats,
        'user': request.user
    })

@login_required
def home(request):
    return render(request, 'home.html')



@login_required
def chave(request):
    credenciais, created = CredenciaisAPI.objects.get_or_create(user=request.user)

    if request.method == "POST":
        credenciais.chave_api = request.POST.get("chave_api")
        credenciais.chave_secreta = request.POST.get("chave_secreta")
        credenciais.save()
        messages.success(request, "Credenciais salvas com sucesso! 🔑")
        return redirect("chave")

    return render(request, "chave.html", {
        "user": request.user,
        "credenciais": credenciais
    })







@login_required
def editar_conta(request):
    # Puxa o usuário logado
    user = request.user
    credenciais, created = CredenciaisAPI.objects.get_or_create(user=user)

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=user)
        cred_form = CredenciaisForm(request.POST, instance=credenciais)

        if user_form.is_valid() and cred_form.is_valid():
            user_form.save()
            cred_form.save()
            return redirect("home")  # redireciona para dashboard/home
    else:
        user_form = UserForm(instance=user)
        cred_form = CredenciaisForm(instance=credenciais)

    return render(request, "editar_conta.html", {
        "user_form": user_form,
        "cred_form": cred_form
    })
