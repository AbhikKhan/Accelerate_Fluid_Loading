from tree import *
from utility import *
from ntm_helper import *
from genMix import *
from hda import *
from ntm import *
from PIL import Image
from findfpandseq2 import *

#<<<<<<<<<<<<<<<<===========================>>>>>>>>>>>>>>>>>>>>>>.
def getHeight(root):
    if root == None:
        return 0
    height = 0
    for child in root.children:
        height = max(height, getHeight(child)+1)

    return height


#ratioList = [22,14,14,14]
#factorList = [4,4,4]

#ratioList = [102,26,2,2,124]
#factorList = [4,4,4,4]
 
#ratioList = [19,15,15,15]
#factorList = [4,4,4]

#ratioList = [300,499,225]
#factorList = [4,4,4,4,4]
 
 
# ratioList = [9,26,29]
# factorList = [4,4,4]

# ratioList = [56,113,87]
# factorList = [4,4,4,4]

#ratioList = [25, 123, 108]
#factorList = [4,4,4,4]
 
#ratioList = [27,25,57,69,78]
#factorList = [4,4,4,4]

#---------------------------------------------------
# ratioList = [57,28,6,6,6,3,150]
# factorList = [4,4,4,4]
# 
# ratioList = [102,26,3,3,122]
# factorList = [4,4,4,4]
# 
# ratioList = [26,15,51,26,5,5,1,127]
# factorList = [4,4,4,4]

# ratioList = [180,26,26,5,5,14]
# factorList = [4,4,4,4]

#ratioList = [4,6,10,14,22,26,174]
#factorList = [4,4,4,4]
# 
#ratioList = [56,113,87]
#factorList = [4,4,4,4]
# 
# ratioList = [128,122,6]
# factorList = [4,4,4,4]


# ratioList = [9,26,29]
# factorList = [4,4,4]


#ratioList = [22,14,14,14]
#factorList = [4,4,4]


# C:\MTP\Newfolder\5.Codes\NTM
######################################################################
mixture1 =[(1,90) ,(2,90), (3,76)]
mixture2 =[(1,19) ,(2,15), (3,15), (4,15)]##--
# mixture3 =[(1,300),(2,499),(3,225)]
mixture3 =[(1,102),(2,26),(3,33),(4,122)]
mixture4 =[(1,27),(2,25),(3,57),(4,69),(5,78)]
# mixture5 =[(1,4),(2,6),(3,10),(4,14),(5,22),(6,26),(7,174)]
# mixture6 =[(1,40),(2,60),(3,10),(4,14),(5,22),(6,2),(7,174)]
mixture7 =[(1,30),(2,24),(3,155),(4,38),(5,9)]
mixture8 =[(1,228), (2,36), (3,259), (4,98), (5,403)]
# [180,26,26,5,5,14]

######################################################################





# mix=mixture2                 #[(1, 43), (2, 435), (3, 79), (4, 217), (5, 250)]

######################################genmix
# root1=(genMix(mixture1,4))
# root2=(genMix(mixture2,4))

# root3=(genMix(mix,4))###

# root4=(genMix(mixture4,4))
# l = leftistTree((root3))
# l=ntm(l)
# viewTree(root3)
# image = Image.open('output.png')
# image.show()

######################################hda
# viewTree(hda(root))
# viewTree((root))
#image = Image.open('output.png')
#image.show()

######################################NTM
# l = leftistTree((root3))
# info = place360((l),[0,0],t=[1])
# info1 = ntm(hda(root1))
# info2 = ntm(hda(root2))
# info3 = ntm(hda(root3))
# info4 = ntm(hda(root4))

file_path = 'RATIOS_1.txt'
import ast
with open(file_path, 'r') as file:
    line = file.readline()
    c=0
    while line:
        c=c+1
        print(c)
        dir="frames2"
        # import os
        # for f in os.listdir(dir):# CLEAR THE FOLDER
        #     os.remove(os.path.join(dir, f))
        # print(line)
        # import subprocess
        # import os
        # import signal
        # p=subprocess.Popen(['python','findfpandseq2.py'])
        # p.terminate()
        # p.wait()
        
        
        
        mix=ast.literal_eval(line)
        print(mix)
        root3=(genMix(mix,4))
        
        lft = leftistTree(root3) 
        height = getHeight(lft)
        # lft = ((root3))
        # # r=createGraphFromPydot(leftFactoredTree)
        treelist=getNodesEdges(lft)


        # viewTree(lft)
        # image = Image.open('output.png')##
        # image.show()
        footprint(treelist, mix)
        find_seq(height)
        line = file.readline()
        if c ==  2000:     #1000-240-62-41-59-14:     # 1000-240:
            break

# lft = leftistTree(hda(root3))##
# r=createGraphFromPydot(leftFactoredTree)
# treelist=getNodesEdges(lft)##
# 

# viewTree(lft)##
# image = Image.open('output.png')##
# image.show()
# footprint(treelist,mix)##
# find_seq()##
# leftFactoredTree = leftistTree(hda(root2))
# viewTree(leftFactoredTree)
# image = Image.open('output.png')
# image.show()
# leftFactoredTree = leftistTree((root3))
# viewTree(leftFactoredTree)
# image = Image.open('output.png')
# image.show()
# leftFactoredTree = leftistTree(hda(root4))
# viewTree(leftFactoredTree)
# image = Image.open('output.png')
# image.show()


# visualize_placement(info)
# visualize_placement(info2)
# visualize_placement(info3)
# visualize_placement(info4)
# =============================================================================
# import turtle
# skk = turtle.Turtle()

# for i in range(4):
#  	skk.forward(50)
#  	skk.right(90)
 	
# turtle.done()
# =============================================================================

