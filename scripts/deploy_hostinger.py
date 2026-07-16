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
    print("Deploy concluído.")


if __name__ == "__main__":
    main()
