# https://code.visualstudio.com/docs/python/python-tutorial#_install-a-python-interpreter
# py -3 -m venv .venv
#.venv\scripts\activate
import math 
import timeit 
import random
######## Functions Defiitions
def ys(xn,yn,x):
  """calculate ys for given xn,yn,x"""
  L=list()
  xn2=xn*xn
  yn2=yn*yn
  QN2=xn2+yn2
  xn12=(xn+1)*(xn+1)
  PN2=xn12+yn2
  yUp2=QN2-x*x
  yDn2=PN2-(x+1)*(x+1)
  nUp=math.floor(math.sqrt(yUp2))  
  if yDn2>0:
    nDn=math.ceil(math.sqrt(yDn2))
    for i in range (nDn,nUp+1):
      L.append((x,i))
      L.append((x,-i))
  else:
    nDn=-nUp
    for i in range (nDn,nUp+1):
      L.append((x,i))
  return L
def f(xn,yn):
  """ to calculate L2 corresponding to point N with coordinates xn and yn """
  if yn==0 and xn>=0: return (xn,0)
  L=list()
  xn2=xn*xn
  yn2=yn*yn
  QN2=xn2+yn2
  nQN=math.ceil(math.sqrt(QN2))
  for x in range(xn,nQN):L=L+ys(xn,yn,x)
  L.sort(key = lambda t: t[0]*t[0]+t[1]*t[1])# sorting the list
  return L
def saveL2(k):
  """ save  lists for -k <= xn <k and -k <= yn <k """
  L2=[]
  for i in range(2*k):
    ll=[]
    for j in range(2*k): 
      l=f(i-k,j-k)
      ll.append(l)  
    L2.append(ll)
  print("L2 is saved. Example of f(40,29)=L2[50][79]:")
  l=L2[k+40][k+29]
  print(l)
  return L2
def show():
  """ print generated matrix for H<30 """
  ar=[0]*H
  ar10=[0]*H
  for i in range(H): 
    ar[i]=i%10
    ar10[i]=int((i-i%10)/10)
  print("columns:",ar10)
  print("        ",ar)
  print("...")
  for j in range(H):
    if (j<10): print("row ",j,":",arPoints[j][:H])
    else: print("row",j,":",arPoints[j][:H])
  print("...")
def FindB(Q,l):
  """ Find point B given Q, L2, and arPoints """
  if type(l[0])==type(3): l=[l]
  for e1 in l:
    e=(e1[0]+Q[0],e1[1]+Q[1])
    if e[0]>=H or e[1]>=H: continue# or e[0]<0 or e[1]<0: continue
    if arPoints[e[1]][e[0]]==1: #swapped
      return ((e[0],e[1]))
def step(P,N):
  """ find Q and B given P and N """
  Q=(P[0]+1,P[1]) 
  if arPoints[Q[1]][Q[0]]==1: 
    return [Q,Q]
  x=N[0]-Q[0]#0
  y=N[1]-Q[1]
  if x>kShift-1 or x <-kShift or y>kShift-1 or y <-kShift: 
    sys.exit("the size of saved L2 is not enough")
  l=L2[kShift+x][kShift+y]
  B=FindB(Q,l)
  return [Q,B] 
def run():
  """ for each query point, find the nearest base point """
  P=(0,n50)
  B=P
  N=P
  if display==1: print(f"{(P[1], P[0])} {(N[1],N[0])}")
  for k in range(H): 
    a=step(P,N)
    P=a[0]
    N=a[1]
    if display==1: print(f"{(P[1], P[0])} {(N[1],N[0])}")
    if P[0]==H-1:return
##############################################################################################
### function kdtree(point_list) from https://en.wikipedia.org/wiki/K-d_tree :#################
from collections import namedtuple
from operator import itemgetter
from pprint import pformat

class Node(namedtuple("Node", "location left_child right_child")):
    def __repr__(self):
        return pformat(tuple(self))
def kdtree(point_list, depth: int = 0):
    if not point_list:
        return None

    k = len(point_list[0])  # assumes all points have the same dimension
    # Select axis based on depth so that axis cycles through all valid values
    axis = depth % k

    # Sort point list by axis and choose median as pivot element
    point_list.sort(key=itemgetter(axis))
    median = len(point_list) // 2

    # Create node and construct subtrees
    return Node(
        location=point_list[median],
        left_child=kdtree(point_list[:median], depth + 1),
        right_child=kdtree(point_list[median + 1 :], depth + 1),
    )
##############################################################################################
def runTree():
  return kdtree(point_list) 
######### Main programm
if __name__ == "__main__":  
  #1) Savie the array of the lists for -50 <= xn <50 and -50 <= yn <50
  kShift=50
  L2=saveL2(kShift)

  #2) Accept user's input and generate base points
  H=int(input("Enter H:"))
  density=float(input("Enter density:"))
  point_list=[]#  for k-d tree calculations
  arPoints = [[0]*H for _ in range(H)]# for our calculations
  
  display=0 
  if H<30: display=1
  n50=math.floor(H/2) # half (50%) of H
  N=math.floor(density*H*H)
  arPoints[n50][0]=1
  point_list.append((0,n50))
  for i in range(N-1):
    x=int(math.floor(H*random.random()))
    y=int(math.floor(H*random.random()))
    point_list.append((x,y))
    arPoints[y][x]=1

  #3) measure thntime of finding the nearest neighbor for each of M query points 
  if display==1: show()
  run()
  if display!=1: #quit()
    print ("our time=",timeit.timeit(run, number=1000), " milliseconds")
    print ("k-d tree time=",100*timeit.timeit(runTree, number=10), " milliseconds")
  input("Done. Click 'Enter'")
