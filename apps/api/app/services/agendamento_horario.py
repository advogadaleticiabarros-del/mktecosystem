"""Compara data+horário de um agendamento (fuso do tenant) contra o agora."""
from datetime import date, datetime, timezone
from zoneinfo import ZoneInfo

FUSO_PADRAO = ZoneInfo("America/Sao_Paulo")


def horario_ja_chegou(data_agendada: date, horario: str, agora_utc: datetime | None = None) -> bool:
    """True quando data_agendada+horario (interpretado no fuso do tenant) já
    passou em relação a agora_utc (default: agora de verdade)."""
    agora_utc = agora_utc or datetime.now(timezone.utc)
    hora, minuto = (int(parte) for parte in horario.split(":"))
    alvo_local = datetime(
        data_agendada.year, data_agendada.month, data_agendada.day,
        hora, minuto, tzinfo=FUSO_PADRAO,
    )
    return alvo_local.astimezone(timezone.utc) <= agora_utc


def hoje_brasilia(agora_utc: datetime | None = None) -> date:
    """A data de hoje no fuso do escritório (o servidor roda em UTC: depois das
    21h de Brasília, `date.today()` já seria o dia seguinte)."""
    return (agora_utc or datetime.now(timezone.utc)).astimezone(FUSO_PADRAO).date()
