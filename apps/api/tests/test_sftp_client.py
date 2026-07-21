from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.integrations.publish.sftp_client import SFTPClient


@pytest.mark.anyio
async def test_upload_conecta_uma_vez_e_escreve_arquivo():
    with patch("app.integrations.publish.sftp_client.asyncssh.connect", new=AsyncMock()) as mock_connect:
        conn = mock_connect.return_value
        sftp = AsyncMock()
        conn.start_sftp_client = AsyncMock(return_value=sftp)
        arquivo_remoto = AsyncMock()
        arquivo_remoto.write = AsyncMock()
        sftp.open = MagicMock()
        sftp.open.return_value.__aenter__ = AsyncMock(return_value=arquivo_remoto)
        sftp.open.return_value.__aexit__ = AsyncMock(return_value=False)

        cliente = SFTPClient(host="h", port=65002, user="u", password="p")
        await cliente.upload("index.html", b"<html></html>")

        mock_connect.assert_awaited_once_with(
            "h", port=65002, username="u", password="p", known_hosts=None
        )
        arquivo_remoto.write.assert_awaited_once_with(b"<html></html>")


@pytest.mark.anyio
async def test_download_le_arquivo_remoto():
    with patch("app.integrations.publish.sftp_client.asyncssh.connect", new=AsyncMock()) as mock_connect:
        conn = mock_connect.return_value
        sftp = AsyncMock()
        conn.start_sftp_client = AsyncMock(return_value=sftp)
        arquivo_remoto = AsyncMock()
        arquivo_remoto.read = AsyncMock(return_value=b"conteudo atual")
        sftp.open = MagicMock()
        sftp.open.return_value.__aenter__ = AsyncMock(return_value=arquivo_remoto)
        sftp.open.return_value.__aexit__ = AsyncMock(return_value=False)

        cliente = SFTPClient(host="h", port=65002, user="u", password="p")
        conteudo = await cliente.download("sitemap.xml")

        assert conteudo == b"conteudo atual"


@pytest.mark.anyio
async def test_garantir_diretorio_cria_diretorio_remoto():
    with patch("app.integrations.publish.sftp_client.asyncssh.connect", new=AsyncMock()) as mock_connect:
        conn = mock_connect.return_value
        sftp = AsyncMock()
        conn.start_sftp_client = AsyncMock(return_value=sftp)
        sftp.makedirs = AsyncMock()

        cliente = SFTPClient(host="h", port=65002, user="u", password="p")
        await cliente.garantir_diretorio("blog/capas")

        sftp.makedirs.assert_awaited_once_with("blog/capas", exist_ok=True)
