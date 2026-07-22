from datetime import date, datetime, timezone

from app.services.agendamento_horario import horario_ja_chegou


def test_horario_no_passado_ja_chegou():
    agora = datetime(2026, 7, 22, 22, 0, tzinfo=timezone.utc)  # 19:00 em Brasília
    assert horario_ja_chegou(date(2026, 7, 22), "19:00", agora_utc=agora) is True


def test_horario_no_futuro_ainda_nao_chegou():
    agora = datetime(2026, 7, 22, 21, 0, tzinfo=timezone.utc)  # 18:00 em Brasília
    assert horario_ja_chegou(date(2026, 7, 22), "19:00", agora_utc=agora) is False


def test_horario_exato_ja_chegou():
    agora = datetime(2026, 7, 22, 22, 0, tzinfo=timezone.utc)  # exatamente 19:00 em Brasília
    assert horario_ja_chegou(date(2026, 7, 22), "19:00", agora_utc=agora) is True


def test_data_futura_nao_chegou_mesmo_com_horario_cedo():
    agora = datetime(2026, 7, 22, 23, 0, tzinfo=timezone.utc)  # 20:00 em Brasília, dia 22
    assert horario_ja_chegou(date(2026, 7, 23), "08:00", agora_utc=agora) is False
