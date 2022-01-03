# -*-* coding:UTF-8
import lxml.etree


class Plugin(Base):
    __info__ = {
        "author": "doimet",
        "references": ["https://riddler.io"],
        "desc": "riddler查询",
        "datetime": "2021-12-31"
    }

    def domain(self) -> dict:
        r = self.request(
            method='get',
            url='https://riddler.io/search',
            params={'q': f'pld:{self.target.value}'}
        )
        if r.status_code == 200:
            dom = lxml.etree.HTML(r.content)
            result = dom.xpath('//tbody/tr/td[@class="col-lg-5 col-md-5 col-sm-5"]/a[position()>1]/text()')
            return {
                'SubdomainList': [{'subdomain': _} for _ in result]
            }
