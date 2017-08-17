import numpy as np

class LatexTableGenerator(object):
    def __init__(self,
                 max_height):
        self.max_height = max_height
        self.grid = [[]]
        self.entries = {}

    def update_grid(self):
        #determin how many copies is needed
        max_length = -1
        for key,entry in self.entries.iteritems():
            if max_length<len(entry["values"]):
                max_length = len(entry["values"])
        num_copies =  max_length/self.max_height
        if max_length%self.max_height != 0:
            num_copies+=1
        height = max_length/num_copies+1
            
        # generate header
        def key(k):
            return k["columns"]
        entries = sorted([e for k,e in self.entries.iteritems()],
                         key = key)
        header = [e["title"] for e in entries]
        header = header*num_copies
        self.grid = [header]+([[" - "]*(len(entries)*num_copies) for k in xrange(height)])
        
        for i,entry in enumerate(entries):
            for j,value in enumerate(entry["values"]):
                k = i+(j/height)*len(entries)
                l = j%height
                self.grid[l+1][k] = value
                    
    
        
    def add_entry(self,name,title):
        max_column = -1
        for key,entry in self.entries.iteritems():
            if max_column<entry["columns"]:
                max_column=entry["columns"]
        
        self.entries[name] = {"name":name,
                              "title":title,
                              "columns":max_column+1,
                              "depth":0,
                              "values":[]}
        

    def add_to_entry(self,name,value):
        self.entries[name]["values"].append(value)
        

    def get_latex(self):
        output="\\begin{table}[ht!]\n"
        output+="\\caption{Add your caption here}\n"
        num_sections = len(self.grid[0])/len(self.entries)
        output+="\\begin{tabular}{|"+(("|"+"c|"*len(self.entries))*num_sections)+"}\n"
        output+="\\hline"
        for row in self.grid:
            output+=("".join([" "+v+" &" for v in row]))[:-1]+"\\\\\n"
            output+="\\hline"
        output+="\n\\end{tabular}\n"
        output+="\\end{table}\n"
        return output
