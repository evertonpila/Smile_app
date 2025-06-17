from django.db import models

class HistoricalSignal(models.Model):
    symbol = models.CharField(max_length=50)
    signal = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=20, decimal_places=10)
    timestamp = models.DateTimeField()
    sinal = models.IntegerField()
    percentage = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = 'sinais.historical_signals'
        verbose_name = 'Historical Signal'
        verbose_name_plural = 'Historical Signals'

    def __str__(self):
        return f"{self.symbol} - {self.signal} at {self.timestamp}"


class Trade(models.Model):
    symbol = models.CharField(max_length=50)
    entry_price = models.DecimalField(max_digits=20, decimal_places=10)
    exit_price = models.DecimalField(max_digits=20, decimal_places=10)
    quantity = models.FloatField()
    profit = models.FloatField()
    type = models.CharField(max_length=50)
    entry_time = models.DateTimeField()
    exit_time = models.DateTimeField()
    sinal = models.IntegerField()
    percentage = models.FloatField(null=True, blank=True)
    signal = models.ForeignKey(
        HistoricalSignal,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='trades'
    )

    class Meta:
        db_table = 'sinais.trades'
        verbose_name = 'Trade'
        verbose_name_plural = 'Trades'

    def __str__(self):
        return f"{self.symbol} - {self.type} trade"


class HistoricalSignalShort(models.Model):
    symbol = models.CharField(max_length=50)
    signal = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=20, decimal_places=10)
    timestamp = models.DateTimeField()
    sinal = models.IntegerField()
    percentage = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = 'sinais.historical_signals_short'
        verbose_name = 'Historical Signal Short'
        verbose_name_plural = 'Historical Signals Short'

    def __str__(self):
        return f"{self.symbol} - {self.signal} at {self.timestamp} (Short)"


class TradeShort(models.Model):
    symbol = models.CharField(max_length=50)
    entry_price = models.FloatField()
    exit_price = models.FloatField()
    quantity = models.FloatField()
    profit = models.FloatField()
    type = models.CharField(max_length=50)
    entry_time = models.DateTimeField()
    exit_time = models.DateTimeField()
    sinal = models.IntegerField()
    percentage = models.FloatField(null=True, blank=True)
    signal = models.ForeignKey(
        HistoricalSignalShort,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='trades_short'
    )

    class Meta:
        db_table = 'sinais.trades_short'
        verbose_name = 'Trade Short'
        verbose_name_plural = 'Trades Short'

    def __str__(self):
        return f"{self.symbol} - {self.type} short trade"