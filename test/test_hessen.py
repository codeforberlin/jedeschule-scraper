import unittest

from scrapy.http import HtmlResponse, Request

from jedeschule.spiders.hessen import HessenSpider


DETAILS_URL = "https://schul-db.bildung.hessen.de/schul_db.html/details/?school_no={}"


def details_page(marker: str) -> str:
    return f"""
<html><body><main>
<div class="col-md-9 col-lg-9">
Gymnasium (Oberstufe)
</div>
<pre>
Toni-Sender-Oberstufe
Voltastraße 1a
60486 Frankfurt am Main
</pre>
<pre><a href="tel:+49 69 21245800">+49 69 21245800</a></pre>
<iframe src="https://www.openstreetmap.org/export/embed.html?bbox=0&amp;marker={marker}&amp;layer=mapnik"></iframe>
</main></body></html>
"""


class TestHessenSpider(unittest.TestCase):
    def _parse(self, school_no: str, marker: str) -> dict:
        url = DETAILS_URL.format(school_no)
        response = HtmlResponse(
            url=url,
            body=details_page(marker).encode("utf-8"),
            encoding="utf-8",
            request=Request(url),
        )
        return next(HessenSpider().parse_details(response))

    def test_coordinates_are_extracted(self):
        school = self._parse("4405", "50.116549,8.641518")
        self.assertEqual(school["latitude"], 50.116549)
        self.assertEqual(school["longitude"], 8.641518)

    def test_minus_one_placeholder_is_filtered(self):
        school = self._parse("9642", "-1.0,-1.0")
        self.assertIsNone(school["latitude"])
        self.assertIsNone(school["longitude"])

    def test_zero_placeholder_is_filtered(self):
        school = self._parse("4405", "0.0,0.0")
        self.assertIsNone(school["latitude"])
        self.assertIsNone(school["longitude"])
        self.assertEqual(HessenSpider.normalize(school)["id"], "HE-4405")


if __name__ == "__main__":
    unittest.main()
