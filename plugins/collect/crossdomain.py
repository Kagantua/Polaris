# -*-* coding:UTF-8
import re


class Plugin(Base):
    __info__ = {
        "author": "doimet",
        "references": ["https://www.robtex.com"],
        "desc": "crossdomain提取子域名",
        "datetime": "2022-01-01"
    }

    def domain(self) -> dict:
        with self.async_pool(max_workers=self.target.setting.asyncio, threshold=self.threshold) as execute:
            for url in [
                f'http://{self.target.value}/crossdomain.xml',
                f'http://www.{self.target.value}/crossdomain.xml',
            ]:
                execute.submit(self.task, url)
            return {'SubdomainList': execute.result()}

    async def task(self, url):
        r = await self.async_http(method='get', url=url)
        if r.status_code == 200:
            result = re.findall(rf'[\w.-]+\.{self.target.value}', r.text)
            return [{'subdomain': _} for _ in result]
