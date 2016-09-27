from bs4 import BeautifulSoup
import json
import sys
import re

class dataset:
    def __init__(self):
        self.dataTree = None
        if len(sys.argv)>1:
            self.dataTree = BeautifulSoup(open(sys.argv[1]), "html.parser")
        else:
            self.dataTree = BeautifulSoup(input(), "html.parser")
        self.header = dict()
        self.data = dict()
        self.design = list()
        self.year_regex = re.compile("Fallzahlen für das Jahr (?P<year>[0-9]{4}):")

    def processHeader(self, table):
        """Saves metadata and appends the current ID to design list
        """
        metadata = dict()
        for idx,row in enumerate(table.tbody.find_all('tr')):
            cell_id = row.find_all('td')[0].text.strip()
            cell_id = cell_id.strip(":")
            cell_res = row.find_all('td')[1].text.strip()
            metadata[cell_id] = cell_res
        self.header[metadata["Lokalisation"]] = metadata
        self.design.append(metadata["Lokalisation"])

    def processData(self, table, id=None):
        if id is None:
            id = len(self.design) - 1
        currentYear = "NA"
        self.data[self.design[id]] = dict()
        for row in table.tbody.find_all("tr"):
            if row.td.has_attr('colspan'):
                try:
                    year = self.year_regex.match(row.text)
                    currentYear = year.group("year")
                except:
                    currentYear = "NA"
                self.data[self.design[id]][currentYear] =  dict()
            else:
                cells = row.find_all("td")
                age = "NA"
                for idx, cell in enumerate(cells):
                    value = cell.text.strip()
                    print(idx, value)
                    if idx == 0:
                        age = value.replace("\u00a0","")
                        self.data[self.design[id]][currentYear][age] = list()
                    else:
                        value = value.replace(".","")
                        value = value.replace("-", "0")
                        value = int(value)
                        self.data[self.design[id]][currentYear][age].append(value)
        pass

    def export_json(self):
        filename = input("Output filename (auto suffix: data.json, design.json, meta.json):")
        with open("{}data.json".format(filename), "w") as f:
            f.write(json.dumps(self.data))
        with open("{}design.json".format(filename), "w") as f:
            f.write(json.dumps(self.design))
        with open("{}meta.json".format(filename), "w") as f:
            f.write(json.dumps(self.header))

        pass


    def parse(self):
        for table in self.dataTree.find_all(name="table", attrs={}, recursive=True, text=None, limit=None):
            if table["id"] == "resheader":
                self.processHeader(table)
            elif table["id"] == "datatab":
                self.processData(table)
            else:
                print("Found table that is neither header nor data table.")
        pass


if __name__ == '__main__':
    d = dataset()
    d.parse()
    d.export_json()
