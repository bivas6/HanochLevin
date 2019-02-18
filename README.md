# HanochLevin
Social networks in Hanoch Levin Plays 


I case that you got a tsv file with all the plays html code named hanochlevin.tsv:
  put the python code and the tsv file in the same directory and run python main.py.
  
   you can run it with the options:
   
   

"""
options:
    
    ## param labels ##
    To set every node to got a label: python main.py labels=all_labels (default)
    To set only important (upper 75%) nodes got a label: python main.py labels=important
    
    ## param edges ##
    every edge drawn: python main.py edges=all_edges
    only important (upper 75%) edges get drawn: python main.py edges=important (default)
    nodes with colors: python main.py nodes_color=with_colors
    all nodes have same color: nodes_color=one_color
    
    ## param metric ##
    metric options:
        basic: character importency = scene the character appears in / number of scene
               characters connection = scenes the characters appears together / number of scene (default)
               python main.py metric=basic
               
               
        proportional: character importency = character talk in the scene / the total talks in the scene
                      characters connection = scenes the characters appears together / number of scene
                python main.py metric=proportional
"""
