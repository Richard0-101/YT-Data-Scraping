import luigi
import json
import requests
import datetime
import pytz
import pafy
from bs4 import BeautifulSoup
urls=["https://www.youtube.com/watch?v=LiqIQ5He7_4" ,
      "https://www.youtube.com/watch?v=lpeuIu-ZYJY" ,
      "https://www.youtube.com/watch?v=-j0dlcfekqw" ,
      "https://www.youtube.com/watch?v=2yoIPB8sowA" ,
      "https://www.youtube.com/watch?v=e8S2Pyl1aYk"
         ]
now = datetime.datetime.now()
class Time(luigi.Task):
    def requires(self):
        return []
    def output(self):
        return luigi.LocalTarget("time.txt")
    def run(self):
        with self.output().open('w') as f:
                f.write(now.strftime("%Y-%m-%d %H:%M:%S\n"))
class YTdata(luigi.Task):
    def requires(self):
        return [Time()]
    def output(self):
        return luigi.LocalTarget("YTdata.txt")
    def run(self):
        with self.input()[0].open() as fin, self.output().open('w') as fout:
            for line in fin:
                for url in urls:
                    r = BeautifulSoup(requests.get(url).text, "html.parser")
                    title = r.select_one('meta[itemprop="name"][content]')['content']
                    views=r.select_one('meta[itemprop="interactionCount"][content]')['content']
                    n = str(line.strip())
                    fout.write("{}:{}:{}\n".format(n, title, views))
                             
if __name__ == '__main__':
    luigi.run()     
