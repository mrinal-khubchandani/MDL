import numpy as np
import cvxpy as cp
import json 
import os

states = np.zeros(60,dtype=float)
path = './outputs'
try:  
    os.mkdir(path)  
except OSError as error:  
    x=0

for i in range(60):
    sta = int(i%3)        #sta represents stamina/50
    y = int((i%12)/3)   #y represents arrows
    z = int(i/12)       #z represents health/25
    
    if z == 0:
        states[i] = 1   #noop

    elif sta == 0:
        states[i] = 1   #recharge
    
    elif y == 0 and sta == 2:
        states[i] = 1   #dodge
    
    elif sta == 2 or y == 0:
        states[i] = 2   #dodge + shoot,dodge + recharge
        
    else:
        states[i] = 3   #all

n = int(np.sum(states))
actions = np.zeros(n,dtype=int)
left = int(states[0])
cur = 0
corre = np.zeros(n,dtype=int)
for i in range(n):
    
    corre[i] = cur
    sta = int(cur%3)        #sta represents stamina/50
    y = int((cur%12)/3)     #y represents arrows
    z = int(cur/12)         #z represents health/25

    # print(cur,i,z,y,sta)
    if z == 0:                              #will noop
        actions[i] = 1

        #now z!=0

    elif sta == 0:                            #will recharge
        actions[i] = 4
                            
        # now z!=0 and sta!=0

    elif y == 0 and sta == 2:                 #will dodge
        actions[i] = 3

    elif y == 0 and left == 2:              #will dodge
        actions[i] = 3

    elif y == 0 and left == 1:              #will recharge
        actions[i] = 4
    
        #now sta!=0 and y!=0 and z!=0
    elif sta == 2 and left == 2:              #will shoot
        actions[i] = 2
    
    elif sta == 2 and left == 1 and y != 3:   #will dodge
        actions[i] = 3
    
    elif sta == 2 and left == 1 and y == 3:              #will dodge
        actions[i] = 3


        #now sta==1 and y!=0 and z!=0'''
    else:
        if left == 3:                       #will shoot
            actions[i] = 2
        
        elif left == 2 and y != 3 and sta == 1:            #will dodge
            actions[i] = 3
        
        elif left == 2 and y == 3 and sta == 1:            #will dodge
            actions[i] = 3

        elif left == 2 and sta == 2 and y != 3:           #will dodge
            actions[i] = 3
        
        elif left == 2 and sta == 2 and y == 3:                     #will dodge
            actions[i] = 3

        else:                               #will recharge
            actions[i] = 4

    left = left-1
    if left == 0 and cur != 59:
        cur = cur+1
        left = int(states[cur])

A = []

for i in range(60):
    temp = []
    for j in range(n):
        temp.append(0.0)
    A.append(temp)

A_mat = np.array(A).transpose()

R = np.zeros((n,1))

for i in range(n):
    if actions[i] != 1:
        R[i] = -5

R = R.transpose()
alpha = np.zeros((60,1))
alpha[59] = 1

cur = 0
left = int(states[0])


for i in range(n):
                            #cur = 12z + 3y + sta
    sta = int(cur%3)        #sta represents stamina/50
    y = int((cur%12)/3)     #y represents arrows
    z = int(cur/12)         #z represents health/25


    if z == 0:                              #will noop
        A_mat[i][i] = 1

        #now z!=0

    elif sta == 0:                            #will recharge
        A_mat[i][cur] = 0.8
        A_mat[i][cur+1] = -0.8
                            
        # now z!=0 and sta!=0

    elif y == 0 and sta == 2:                 #will dodge
        A_mat[i][cur] = 1
        A_mat[i][cur+2] = -0.64
        A_mat[i][cur-1] = -0.16
        A_mat[i][cur+1] = -0.16
        A_mat[i][cur-2] = -0.04

    elif y == 0 and left == 2:              #will dodge
        A_mat[i][cur] = 1
        A_mat[i][cur+2] = -0.8
        A_mat[i][cur-1] = -0.2

    elif y == 0 and left == 1:              #will recharge
        A_mat[i][cur] = 0.8
        A_mat[i][cur+1] = -0.8
    
        #now sta!=0 and y!=0 and z!=0
    elif sta == 2 and left == 2:              #will shoot
        A_mat[i][cur] = 1
        A_mat[i][cur-16] = -0.5
        A_mat[i][cur-4] = -0.5
    
    elif sta == 2 and left == 1 and y != 3:   #will dodge
        A_mat[i][cur] = 1
        A_mat[i][cur+2] = -0.64
        A_mat[i][cur-1] = -0.16
        A_mat[i][cur+1] = -0.16
        A_mat[i][cur-2] = -0.04
    
    elif sta == 2 and left == 1 and y == 3:              #will dodge

        A_mat[i][cur] = 1
        A_mat[i][cur-1] = -0.8
        A_mat[i][cur-2] = -0.2


        #now sta==1 and y!=0 and z!=0'''
    else:
        if left == 3:                       #will shoot

            A_mat[i][cur] = 1
            A_mat[i][cur-16] = -0.5
            A_mat[i][cur-4] = -0.5
        
        elif left == 2 and y != 3 and sta == 1:            #will dodge
            A_mat[i][cur] = 1
            A_mat[i][cur+2] = -0.8
            A_mat[i][cur-1] = -0.2
        
        elif left == 2 and y == 3 and sta == 1:            #will dodge
            A_mat[i][cur] = 1
            A_mat[i][cur-1] = -1

        elif left == 2 and sta == 2 and y != 3:           #will dodge
            print(i)
            A_mat[i][cur] = 1
            A_mat[i][cur+2] = -0.64
            A_mat[i][cur-1] = -0.16
            A_mat[i][cur+1] = -0.16
            A_mat[i][cur-2] = -0.04
        
        elif left == 2 and sta == 2 and y == 3:                     #will dodge
            print(i)
            A_mat[i][cur] = 1
            A_mat[i][cur-1] = -0.8
            A_mat[i][cur-2] = -0.2

        else:                               #will recharge
            A_mat[i][cur] = 0.8
            A_mat[i][cur+1] = -0.8

    left = left-1
    if left == 0 and cur != 59:
        cur = cur+1
        left = int(states[cur])

A_mat = A_mat.transpose()
fd = open('matrixA.txt','w+')
for i in range(60):
    for j in range(n):
        print("%.3f"%A_mat[i][j] + ",",end=" ",file=fd)
    fd.write("\n")
fd.close()


x = cp.Variable(shape=(n,1), name="x")
constraints = [cp.matmul(A_mat, x) == alpha, x>=0]
objective = cp.Maximize(cp.sum(R*x))
problem = cp.Problem(objective, constraints)

solution = problem.solve()
print(solution)
print(x.value)
X_array = x.value

des = np.zeros((60,1),dtype=int)

cur = 0
poli = []
for i in range(60):
    count = int(states[i])
    maxi = X_array[cur]
    opti = 0
    for i in range(count):
        if X_array[cur+i] > maxi:
            maxi = X_array[cur+i]
            opti = i
    
    stat = cur + opti
    oristat = corre[stat]
    act = actions[stat]
    cur = cur + count

    sta = int(oristat%3)        #sta represents stamina/50
    y = int((oristat%12)/3)     #y represents arrows
    z = int(oristat/12)         #z represents health/25

    lis = [z,y,sta]
    action_taken = "NOOP"

    if act == 2:
        action_taken = "SHOOT"
    
    if act == 3:
        action_taken = "DODGE"
    
    if act == 4:
        action_taken = "RECHARGE"
    
    temp = [lis,action_taken]
    poli.append(temp)

R_temp = []
R = R.transpose()
for i in range(n):
    x1 = float(R[i])
    R_temp.append(x1)
alpha_temp = []
for i in range(60):
    x1 = float(alpha[i])
    alpha_temp.append(x1)
x_te = []
for i in range(n):
    x1 = float(X_array[i])
    x_te.append(x1)
print(poli)
dict1 = {
    "a": [],
    "r": [],
    "x": [],
    "alpha": [],
    "policy": [],
    "objective": solution
}
dict1["a"] = A_mat.tolist()
dict1["r"] = R_temp
dict1["x"] = x_te
dict1["alpha"] = alpha_temp
dict1["policy"] = poli

  
out_file = open("outputs/output.json", "w") 
  
json.dump(dict1, out_file,indent=4) 
  
out_file.close() 