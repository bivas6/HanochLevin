from itertools import count
import os
from IPython.core.debugger import Tracer
import NamesDealer
from bs4 import BeautifulSoup
import numpy as np
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt


class Play:
    def __init__(self, file, htmp, names_dealer, labels, edges, node_colors, metric):
        if file is None:
            raise 'NO FILE'
        else:
            self.names_dealer = names_dealer
            self.imp_const = 4 if metric == 'proportional' else 40
            self.con_const = 1 if metric == 'proportional' else 0.5
            self.labels = labels
            self.edges = edges
            self.node_colors = node_colors
            self.metric = metric
            self.htmp = htmp
            self.html = file
            self.get_name()
            self.parse()
            self.unify()
            self.metrics()
            self.imp_bar_f = self.get_imp_bar()
    
    def get_result_dir_name(self):
        dir = './result' + '_' + self.metric
        dir += '_colorfulNodes' if self.node_colors == 'with_colors' else '_1colorNodes'
        dir += '_allLabels' if self.labels == 'all_labels' else '_impLabels'
        dir += '_allEdges' if self.edges == 'all_edges' else '_impEdges'
        return dir+'/'
        
    def get_imp_bar(self):
        imp = []
        for char in self.importency:
            imp.append(self.importency[char])
        imp.sort()
        return imp[int((len(imp)-1) * 0.25)]
        
    def get_name(self):
        f = open(self.html, "r", encoding='utf8')
        soup = BeautifulSoup(f, 'html.parser')
        f.close()
        #print(soup.prettify())
        i =  soup.title.string.index('|')
        self.name = soup.title.string[:i-1]
    
    def parse(self):
        g = open(self.html, "r", encoding='utf8').read()
        self.htmp.feed(str(g))
        self.characters = self.htmp.chars
        if '' in self.characters:
            self.characters.remove('')
        self.scenes = self.htmp.scenes
        self.n_characters = len(self.characters)
        #print(self.characters)
    
    def unify(self): ## in case that same charcter use different names, unify them to the detailed one.  הנסיכה >> הנסיכה של מונקו 
        self.characters = self.names_dealer.unify(self.characters)          
        self.n_characters = len(self.characters)
        #print(self.characters)
          
    def find_index(self, char):
        for i in range(self.n_characters):
            if self.names_dealer.can_unify(self.characters[i], char):
                return i
        return -1
        
    def find_real_char(self, char):
        i = self.find_index(char)
        if i == -1:
            return None
        return self.characters[i]
    
    def metrics(self):
        self.do_metric(self.metric == 'basic')
     
    def do_metric(self, basic):
        importency = {}
        connections = np.zeros((self.n_characters, self.n_characters))
        for sc in range(len(self.scenes)):
            for char in self.scenes[sc]:
                to_add = 1 if basic else self.scenes[sc][char]
                if not self.names_dealer.more_then_one(char):
                    self.add_for_spec_char(char, connections, importency, to_add, sc)
                else:
                    for w in char.split('_'):
                        self.add_for_spec_char(w, connections, importency, to_add, sc)

        self.connections = connections
        self.importency = importency
        #print(importency)

    def add_for_spec_char(self, char, connections, importency, to_add, sc):
        real_char = self.find_real_char(char)
        if real_char == None:
            return
        importency[real_char] =  importency.get(real_char, 0) + to_add
        for k in self.scenes[sc]:
            if not k == char:
                i = self.find_index(real_char)
                j = self.find_index(k)
                if i<0 or j<0 or i == j:
                    continue
                connections[i][j] += 1

    def con_bar(self, u, v):
        return self.G[u][v]['weight'] >= self.con_bar_f or self.edges == 'all_edges'
    
    def imp_bar(self, char):
        return self.importency[char] >= self.imp_bar_f or self.n_characters < 10 or self.labels == 'all_labels'
    
    def graph(self):
        G = nx.Graph()
        for char in self.importency:
            G.add_node(char)
        connections = []
        for i in range(self.n_characters):
            for j in range(i+1, self.n_characters):
                if not self.connections[i][j] == 0 and self.characters[i] in G.nodes() and self.characters[j] in G.nodes():
                    G.add_edge(self.characters[i], self.characters[j], weight=self.connections[i][j])
                    connections.append(self.connections[i][j])
        self.G = G
        connections.sort()
        if len(connections) > 0:
            self.con_bar_f = connections[int((len(connections)-1)*0.25)]
        else:
            self.con_bar_f = 0
        
    def get_node_colors(self):
        if self.node_colors == 'with_colors':
            return [self.importency[n]*4 for n in self.G.nodes()]
        return 'steelblue'
    
    def draw_graph(self):
        G = self.G
        pos = nx.spring_layout(G)
        colors = self.get_node_colors()
        labels = {n: self.names_dealer.print_format(n)  if self.imp_bar(n) else '' for n in G.nodes()}
        nodes_sizes = [(self.importency[n]+1)*self.imp_const for n in self.G.nodes()]
        edges_sizes = [self.G[u][v]['weight']*self.con_const if self.con_bar(u,v) else 0 for u,v in self.G.edges()]
        plt.figure(figsize=(8, 8))
        plt.subplots_adjust()
        plt.axis('off')
        #print(edges_sizes)
        nx.draw_networkx_nodes(G,pos,
                            nodelist=G.nodes(),
                            node_color=colors,
                            node_size=nodes_sizes,
                            cmap=plt.cm.summer)
        nx.draw_networkx_edges(G,pos,
                           with_labels=False,
                           edge_color="red",
                           width=edges_sizes
                        )
        nx.draw_networkx_labels(G,pos, labels)
        filename = self.get_result_dir_name()
        filename += self.name
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        plt.savefig(filename)
        plt.close("all")
