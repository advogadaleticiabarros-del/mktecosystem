from app.config import Settings


def test_settings_tem_campos_sftp_do_blog_com_defaults_vazios():
    s = Settings(_env_file=None)
    assert s.BLOG_SFTP_HOST == ""
    assert s.BLOG_SFTP_PORT == 22
    assert s.BLOG_SFTP_USER == ""
    assert s.BLOG_SFTP_PASSWORD == ""
    assert s.BLOG_SFTP_PATH == ""
