import unittest

from scrapy.http import TextResponse

from jedeschule.spiders.schleswig_holstein import SchleswigHolsteinSpider


class TestSchleswigHolsteinAddress(unittest.TestCase):
    csv_response = (
        "id\tname\tcity\tzipcode\tstreet\thouse_number\ttelephone\tfax\temail\twebsite\tlongitude\tlatitude\tagency_number\tmain_school_type\tschool_type\n"
        "9099793\tGoethe-Gemeinschaftsschule, Gemeinschaftsschule der Landeshauptstadt Kiel in Kiel\tKiel\t24118\tWestring 358\t\t+49 431 26042850\t+49 431 26042869\tGoethe-gemeinschaftsschule.kiel@schule.landsh.de\thttps://www.ggs-kiel.de\t10.125675992206988\t54.33448298508549\t0707060\t1024\t1024\n"
        "9099810\tGemeinschaftsschule am Hamberg, Gemeinschaftsschule des Amtes Burg-St. Michaelisdonn in Burg\tBurg (Dithmarschen)\t25712\tAm Sportplatz\t21\t+49 4825 2569\t+49 4825 9166\tGemeinschaftsschule-am-Hamberg.Burg@schule.landsh.de\t\t9.251399129181406\t54.00221251297963\t0707200\t1024\t1024\n"
    )

    def _parse(self):
        spider = SchleswigHolsteinSpider()
        response = TextResponse(
            url=SchleswigHolsteinSpider.base_url,
            body=self.csv_response.encode("utf-8"),
            encoding="utf-8",
        )
        return [spider.normalize(item) for item in spider.parse(response)]

    def test_house_number_is_appended_to_street(self):
        schools = self._parse()
        self.assertEqual(schools[1]["id"], "SH-9099810")
        self.assertEqual(schools[1]["address"], "Am Sportplatz 21")

    def test_house_number_already_in_street_is_kept(self):
        schools = self._parse()
        self.assertEqual(schools[0]["id"], "SH-9099793")
        self.assertEqual(schools[0]["address"], "Westring 358")


if __name__ == "__main__":
    unittest.main()
