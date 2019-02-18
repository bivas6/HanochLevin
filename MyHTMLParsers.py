import urllib.request
from html.parser import HTMLParser
import NamesDealer

class MyHtmlParser(HTMLParser):
 
    def __init__(self):
        HTMLParser.__init__(self)
        self.scenes = {0: {}}
        self.num_words = 0
        self.sc_num = 0
        self.chars = []
        self.rec_char = False
        self.speaks = False
        self.speaker = ''
        self.rec_speaker = False
        self.rec_url = False
        self.saw_h3 = False
        self.saw_main = False
    
    def handle_starttag(self, tag, attrs):
        
        if tag == 'h2': ## usually represent scene
            self.end_scene()
            self.sc_num += 1
            self.scenes[self.sc_num] = {}
            self.rec_url = True
        
        if tag == 'a' and self.rec_url: ## if the sceenes in another page
            for attr in attrs:
                if attr[0] == 'href':
                    self.rec_url = False
                    url = attr[1]
                    sc = urllib.request.urlopen(url).read().decode('utf8')
                    htmp2 = MyHTMLParser2()
                    htmp2.feed(sc)
                    self.parsers_union(htmp2)
                    break
            
        if tag == 'h3':
            self.saw_h3 = True 
            if self.saw_main:
                 return
            self.end_scene()
            self.sc_num += 1
            self.scenes[self.sc_num] = {}
 
        if tag == 'big':
            self.rec_speaker = True
        
        if tag == 'small':
            self.rec_speaker = False
    
    def parsers_union(self, parser): ## in case that another parser parse scene of this play, take the data
        for char in parser.chars:
            if not char in self.chars:
                self.chars.append(char)
        for char in parser.scenes:
             self.scenes[self.sc_num][char] = self.scenes[self.sc_num].get(char, 0) + parser.scenes[char]
        
    def end_scene(self): 
        if self.num_words > 0:
            for char in self.scenes[self.sc_num]:
                self.scenes[self.sc_num][char] /= self.num_words ## take the proprtional part of the talking
            self.num_words = 0

    def handle_endtag(self, tag):
        if tag == 'big' and not self.rec_char:
            self.speaks = True
        if tag == 'main':
            self.saw_main = True
            if self.saw_h3:
                return
        
    def handle_data(self, data):
        if self.rec_char:
            self.chars.append(NamesDealer.no_nikkud(data))
            self.rec_char = False
        if self.rec_speaker:
            self.speaker = NamesDealer.no_nikkud(data)
            if self.speaker not in self.chars:
                self.chars.append(self.speaker)
            try:
                self.scenes[self.sc_num][self.speaker] += 1
            except:
                self.scenes[self.sc_num][self.speaker] = 1
            self.rec_speaker = False
        if self.speaks:
            #if self.speaker == '':
             #   print(data)
            data = data.split(' ')
            self.scenes[self.sc_num][self.speaker] = self.scenes[self.sc_num].get(self.speaker, 0) + len(data)
            self.num_words += len(data)
            self.apeaks = False
  


# In[5]:


class MyHTMLParser2(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.scenes = {}
        self.num_words = 0
        self.chars = []
        self.speaks = False
        self.speaker = ''
        self.rec_speaker = False
        self.ignore = False

    def handle_starttag(self, tag, attrs):

        if tag == 'h3':
            self.end_scene()
            return

        if tag == 'big':
            self.rec_speaker = True

        if tag == 'small':
            self.ignore = True

    def end_scene(self):
        if self.num_words > 0:
            for char in self.scenes:
                self.scenes[char] /= self.num_words
            self.num_words = 0

    def handle_endtag(self, tag):
        if tag == 'big':
            self.speaks = True
        if tag == 'small':
            self.ignore = False
    
    def handle_data(self, data):
        if self.rec_speaker:
            self.speaker = NamesDealer.no_nikkud(data)
            if self.speaker not in self.chars:
                self.chars.append(self.speaker)
            try:
                self.scenes[self.speaker] += 1
            except:
                self.scenes[self.speaker] = 1
            self.rec_speaker = False
        if self.speaks and not self.ignore:
            data = data.split(' ')
            self.scenes[self.speaker] = self.scenes.get(self.speaker, 0) + len(data)
            self.num_words += len(data)
            self.apeaks = False
            
