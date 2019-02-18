import sys
import codecs
from bs4 import BeautifulSoup
import os
import errno
import NamesDealer
import csv
import Play
import MyHTMLParsers



def main(argv):
    maxInt = sys.maxsize
    decrement = True

    while decrement:
        # decrease the maxInt value by factor 10 
        # as long as the OverflowError occurs.

        decrement = False
        try:
            csv.field_size_limit(maxInt)
        except OverflowError:
            maxInt = int(maxInt/10)
            decrement = True
    names = []
    dir = './plays/'

    with open('hanochlevin.tsv', encoding="utf8") as fd:
        rd = csv.DictReader(fd, delimiter="\t", quotechar='"')
        for row in rd:
            name = row['play'].replace(' ', '_')+'.html'
            filename = dir + name
            if not os.path.exists(os.path.dirname(filename)):
                try:
                    os.makedirs(os.path.dirname(filename))
                except OSError as exc: # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise
            f = open(filename, "w", encoding='utf8')
            f.write(row['html'])
            f.close()
            names.append(name)

    labels = 'all_labels'
    edges = 'important'
    node_colors = 'one_color'
    metric = 'basic'
    
    for arg in argv:
        o,a = arg.split('=')
        if o == 'labels':
            labels = a
        elif o == 'edges':
            edges = a
        elif o == 'node_colors':
            node_colors = a
        elif o == 'metric':
            metric = a
            
    names_dealer = NamesDealer.NamesDealer()

    for name in names: 
        htmp = MyHTMLParsers.MyHtmlParser()
        dirname = dir + name
        play = Play.Play(dirname, htmp, names_dealer, labels, edges, node_colors, metric)
        play.graph()
        play.draw_graph()



if __name__ == '__main__':
    main(sys.argv[1:])


