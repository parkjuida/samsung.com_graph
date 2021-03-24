from html.parser import HTMLParser


class SamsungDotComHTMLParser(HTMLParser):
    next_page = []

    def error(self, message):
        pass

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            attributes = dict(attrs)
            href = attributes.get("href", "")
            klass = attributes.get("class", "")
            an_ca = attributes.get("an-ca", "")
            an_ac = attributes.get("an-ac", "")
            an_la = attributes.get("an-la", "")

            if "tv" in href:
                self.next_page.append({
                    "href": href,
                    "class": klass,
                    "an_ac": an_ac,
                    "an_ca": an_ca,
                    "an_la": an_la,
                })
