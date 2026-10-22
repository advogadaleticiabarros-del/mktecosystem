import asyncssh


class SFTPClient:
    def __init__(self, host: str, port: int, user: str, password: str) -> None:
        self._host = host
        self._port = port
        self._user = user
        self._password = password
        self._conn = None
        self._sftp = None

    async def _ensure_conn(self) -> None:
        if self._conn is None:
            self._conn = await asyncssh.connect(
                self._host,
                port=self._port,
                username=self._user,
                password=self._password,
                known_hosts=None,
            )
            self._sftp = await self._conn.start_sftp_client()

    async def upload(self, caminho_remoto: str, conteudo: bytes) -> None:
        await self._ensure_conn()
        async with self._sftp.open(caminho_remoto, "wb") as arquivo:
            await arquivo.write(conteudo)

    async def garantir_diretorio(self, caminho_remoto: str) -> None:
        await self._ensure_conn()
        await self._sftp.makedirs(caminho_remoto, exist_ok=True)

    async def download(self, caminho_remoto: str) -> bytes:
        await self._ensure_conn()
        async with self._sftp.open(caminho_remoto, "rb") as arquivo:
            return await arquivo.read()

    async def listar_recursivo(self, caminho_remoto: str, sufixo: str, profundidade: int = 3) -> list[str]:
        """Caminhos (relativos a `caminho_remoto`) dos arquivos terminados em `sufixo`."""
        await self._ensure_conn()
        achados: list[str] = []

        async def andar(pasta: str, relativo: str, nivel: int) -> None:
            for entrada in await self._sftp.readdir(pasta):
                nome = entrada.filename
                if nome in (".", "..") or nome.startswith("."):
                    continue
                if entrada.attrs.type == 2:  # diretório
                    if nivel < profundidade:
                        await andar(f"{pasta.rstrip('/')}/{nome}", f"{relativo}{nome}/", nivel + 1)
                elif nome.endswith(sufixo):
                    achados.append(f"{relativo}{nome}")

        await andar(caminho_remoto, "", 0)
        return sorted(achados)

    async def close(self) -> None:
        if self._conn is not None:
            self._conn.close()
            await self._conn.wait_closed()
            self._conn = None
            self._sftp = None
