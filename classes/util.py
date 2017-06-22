import os
import csv

class CompletedLog():
    def __init__(self, filename, fieldnames, keyfield):
        self.filename = filename
        self.fieldnames = fieldnames
        self.keyfield = keyfield
        self.skip_list = set()
        self.fh = None
        self.writer = None

        # open filename, if it exists, and read completed files into list
        completed_items = []
        if not os.path.isfile(self.filename):
            with open(self.filename, 'w', 1) as fh:
                writer = csv.DictWriter(fh, fieldnames=self.fieldnames)
                writer.writeheader()
        else:
            with open(self.filename, 'r', 1) as fh:
                reader = csv.DictReader(fh)

                # check the validity of the map file data
                if not reader.fieldnames == fieldnames:
                    raise Exception('Fieldnames in {0} do not match expected fieldnames'.format(filename))

                # read the data from the existing file
                for row in reader:
                    self.skip_list.add(row[self.keyfield])

    def get_writer(self):
        if self.fh is None:
            self.fh = open(self.filename, 'a', 1)
        if self.writer is None:
            self.writer = csv.DictWriter(self.fh, fieldnames=self.fieldnames)
        return self.writer

    def writerow(self, row):
        self.get_writer().writerow(row)
        self.skip_list.add(row[self.keyfield])

    def __contains__(self, other):
        return other in self.skip_list

    def __len__(self):
        return len(self.skip_list)

    def __del__(self):
        if self.fh is not None:
            self.fh.close()
