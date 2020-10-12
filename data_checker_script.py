import xml.etree.ElementTree as ET


def data_parser():
    path = "data/dataset/nysk.xml"

    with open(path, "r", encoding="utf-8") as f:
        doc = ET.ElementTree(file=f)

    r = doc.getroot()
    print(len(r))

    for item in r:
        news_id = item.findtext('docid')
        source = item.findtext('source')
        url = item.findtext('url')
        title = item.findtext('title')
        summary = item.findtext('summary')
        text = item.findtext('text')

        print(f"{news_id} -- {title}")


if __name__ == "__main__":
    data_parser()