from scrapy.dupefilters import RFPDupeFilter
import os

class CustomURLFilter(RFPDupeFilter):
    def request_seen(self, request):
        fp = request.url
        if fp in self.fingerprints:
            return True
        self.fingerprints.add(fp)
        if self.file:
            self.file.write(fp + os.linesep)
        return False