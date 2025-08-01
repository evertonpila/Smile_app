from django.db import models

class HistoricalSignals(models.Model):
    id = models.AutoField(primary_key=True)
    symbol = models.CharField(max_length=100)
    signal = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=20, decimal_places=10)
    timestamp = models.DateTimeField()
    sinal = models.IntegerField()

    class Meta:
        managed = False  # Importante para tabelas existentes
        db_table = 'sinais"."historical_signals'  # Notação esquema.tabela
        verbose_name = 'Historical Signal'
        verbose_name_plural = 'Historical Signals'

    def __str__(self):
        return f"{self.symbol} - {self.signal} at {self.timestamp}"


class Trades(models.Model):
    id = models.AutoField(primary_key=True)
    symbol = models.CharField(max_length=100)
    entry_price = models.DecimalField(max_digits=20, decimal_places=10)
    exit_price = models.DecimalField(max_digits=20, decimal_places=10)
    quantity = models.FloatField()
    profit = models.FloatField()
    type = models.CharField(max_length=100)
    entry_time = models.DateTimeField()
    exit_time = models.DateTimeField()
    sinal = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'sinais"."trades'
        verbose_name = 'Trade'
        verbose_name_plural = 'Trades'

    def __str__(self):
        return f"{self.symbol} {self.type} trade"


class HistoricalSignalsShort(models.Model):
    id = models.AutoField(primary_key=True)
    symbol = models.CharField(max_length=100)
    signal = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=20, decimal_places=10)
    timestamp = models.DateTimeField()
    sinal = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'sinais"."historical_signals_short'
        verbose_name = 'Historical Signal Short'
        verbose_name_plural = 'Historical Signals Short'

    def __str__(self):
        return f"{self.symbol} - {self.signal} (short) at {self.timestamp}"


class TradesShort(models.Model):
    id = models.AutoField(primary_key=True)
    symbol = models.CharField(max_length=100)
    entry_price = models.FloatField()
    exit_price = models.FloatField()
    quantity = models.FloatField()
    profit = models.FloatField()
    type = models.CharField(max_length=100)
    entry_time = models.DateTimeField()
    exit_time = models.DateTimeField()
    sinal = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'sinais"."trades_short'
        verbose_name = 'Trade Short'
        verbose_name_plural = 'Trades Short'

    def __str__(self):
        return f"{self.symbol} {self.type} short trade"