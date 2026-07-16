"""Mirror a local static export directory to Hostinger over SFTP.

Used by .github/workflows/deploy-frontend.yml. Connects with a short
timeout and clear error reporting (no silent hangs like the lftp
subprocess approach this replaces), and removes remote files/dirs
that no longer exist locally so Next.js's content-hashed build
artifacts don't accumulate forever.
"""
import os
import stat
import sys

import paramiko

LOCAL_DIR = "apps/web/out"


def upload_dir(sftp: paramiko.SFTPClient, local_dir: str, remote_dir: str) -> None:
    try:
        sftp.mkdir(remote_dir)
    except OSError:
        pass  # already exists

    local_entries = set(os.listdir(local_dir))

    try:
        remote_entries = {a.filename: a for a in sftp.listdir_attr(remote_dir)}
    except FileNotFoundError:
        remote_entries = {}

    for name, attr in remote_entries.items():
        if name not in local_entries:
            remote_path = f"{remote_dir}/{name}"
            if stat.S_ISDIR(attr.st_mode):
                remove_remote_dir(sftp, remote_path)
            else:
                sftp.remove(remote_path)
            print(f"  removido (obsoleto): {remote_path}")

    for entry in sorted(local_entries):
        local_path = os.path.join(local_dir, entry)
        remote_path = f"{remote_dir}/{entry}"
        if os.path.isdir(local_path):
            upload_dir(sftp, local_path, remote_path)
        else:
            sftp.put(local_path, remote_path)
            print(f"  enviado: {remote_path}")


def remove_remote_dir(sftp: paramiko.SFTPClient, remote_dir: str) -> None:
    for attr in sftp.listdir_attr(remote_dir):
        full = f"{remote_dir}/{attr.filename}"
        if stat.S_ISDIR(attr.st_mode):
            remove_remote_dir(sftp, full)
        else:
            sftp.remove(full)
    sftp.rmdir(remote_dir)


def verify_landmark(host: str, port: int, user: str, password: str, remote_path: str) -> None:
    """Re-connect fresh and byte-compare one real file against the server.

    Found by hand on 2026-07-16: multiple GitHub Actions runs printed
    "enviado" for every file and exited 0, but the live site kept serving
    stale content for over two hours — sftp.put() reported success while
    Hostinger silently didn't persist the write, for reasons never
    confirmed (suspected flaky handling of GitHub's shared runner IPs).
    A fresh connection + real byte comparison is the only way to catch
    that failure mode instead of trusting the upload loop's own reports.
    """
    landmark = "login/index.html"
    local_file = os.path.join(LOCAL_DIR, landmark)
    with open(local_file, "rb") as f:
        local_bytes = f.read()

    transport = paramiko.Transport((host, port))
    transport.banner_timeout = 20
    transport.connect(username=user, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)
    try:
        with sftp.open(f"{remote_path}/{landmark}", "rb") as f:
            remote_bytes = f.read()
    finally:
        sftp.close()
        transport.close()

    if remote_bytes != local_bytes:
        print(
            f"FALHA NA VERIFICAÇÃO: {landmark} no servidor não bate com o "
            f"arquivo local ({len(remote_bytes)} bytes remotos vs "
            f"{len(local_bytes)} bytes locais). O upload reportou sucesso "
            "mas não persistiu de verdade — rode o deploy de novo.",
            file=sys.stderr,
        )
        sys.exit(1)
    print(f"Verificação ok: {landmark} no servidor bate byte a byte com o build local.")


def main() -> None:
    host = os.environ["HOSTINGER_SFTP_HOST"]
    port = int(os.environ["HOSTINGER_SFTP_PORT"])
    user = os.environ["HOSTINGER_SFTP_USER"]
    password = os.environ["HOSTINGER_SFTP_PASSWORD"]
    remote_path = os.environ["HOSTINGER_REMOTE_PATH"]

    print(f"Conectando em {host}:{port} como {user}...")
    transport = paramiko.Transport((host, port))
    transport.banner_timeout = 20
    try:
        transport.connect(username=user, password=password)
    except Exception as exc:
        print(f"FALHA ao conectar/autenticar: {type(exc).__name__}: {exc}", file=sys.stderr)
        sys.exit(1)

    print("Conectado. Sincronizando arquivos...")
    sftp = paramiko.SFTPClient.from_transport(transport)
    upload_dir(sftp, LOCAL_DIR, remote_path)
    sftp.close()
    transport.close()
    print("Deploy concluído. Verificando...")

    verify_landmark(host, port, user, password, remote_path)


if __name__ == "__main__":
    main()
