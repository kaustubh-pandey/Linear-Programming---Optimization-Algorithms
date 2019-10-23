'''
Created By : Kaustubh Pandey
Roll : S20160010041
UG - 4  CSE
'''
import numpy as np
def iter_next(tableau):
    m = min(tableau[:-1,-1])
    if(m<0):
        return True
    return False

def iter(tableau):
    lr = len(tableau[:,0])
    m = min(tableau[lr-1,:-1])
    if(m<0):
        return True
    return False

def find_neg_r(tableau):
    lc = len(tableau[0,:])
    m = min(tableau[:-1,lc-1])
    n = None
    if(m<=0):
        n = np.where(tableau[:-1,lc-1] == m)[0][0]
    return n

#returns column index of negative element in bottom row
def find_neg(tableau):
    lr = len(tableau[:,0])
    m = min(tableau[lr-1,:-1])
    n = None
    if(m<=0):
        n = np.where(tableau[lr-1,:-1] == m)[0][0]
    return n

def find_piv_r(tableau):
        total = []
        r = find_neg_r(tableau)
        row = tableau[r,:-1]
        m = min(row)
        c = np.where(row == m)[0][0]
        col = tableau[:-1,c]
        for i, b in zip(col,tableau[:-1,-1]):
            if i**2>0 and b/i>0:
                total.append(b/i)
            else:
                total.append(999999)
        index = total.index(min(total))
        return [index,c]

def find_piv(tableau):
    if iter(tableau):
        total = []
        n = find_neg(tableau)
        for i,b in zip(tableau[:-1,n],tableau[:-1,-1]):
            if i!=0 and b/i >0 and i**2>0:
                total.append(b/i)
            else:
                total.append(999999)
        index = total.index(min(total))
        return [index,n]

def convert_min(tableau):
    tableau[-1,:-2] = [-1*i for i in tableau[-1,:-2]]
    tableau[-1,-1] = -1*tableau[-1,-1]
    return tableau

def gen_var(tableau):
    lc = len(tableau[0,:])
    lr = len(tableau[:,0])
    var = lc - lr
    v = []
    for i in range(var):
        v.append('x'+str(i+1))
    return v

def pivot(row,col,tableau):
    lr = len(tableau[:,0])
    lc = len(tableau[0,:])
    t = np.zeros((lr,lc))
    pr = tableau[row,:]
    if tableau[row,col]**2>0:
        e = 1/tableau[row,col]
        r = pr*e
        for i in range(len(tableau[:,col])):
            k = tableau[i,:]
            c = tableau[i,col]
            if list(k) == list(pr):
                continue
            else:
                t[i,:] = list(k-r*c)
        t[row,:] = list(r)
        return t
    else:
        print('Cannot pivot on this element.')

# solves maximization problem for optimal solution, returns dictionary w/ keys x1,x2...xn and max.
def maxz(tableau, output='summary'):
    while iter_next(tableau)==True:
        tableau = pivot(find_piv_r(tableau)[0],find_piv_r(tableau)[1],tableau)
    while iter(tableau)==True:
        tableau = pivot(find_piv(tableau)[0],find_piv(tableau)[1],tableau)

    lc = len(tableau[0,:])
    lr = len(tableau[:,0])
    var = lc - lr
    i = 0
    val = {}
    for i in range(var):
        col = tableau[:,i]
        s = sum(col)
        m = max(col)
        if float(s) == float(m):
            loc = np.where(col == m)[0][0]
            val[gen_var(tableau)[i]] = tableau[loc,-1]
        else:
            val[gen_var(tableau)[i]] = 0
    val['max'] = tableau[-1,-1]
    if output == 'tableau':
        return tableau
    else:
        return val

# solves minimization problems for optimal solution, returns dictionary w/ keys x1,x2...xn and min.
def minz(tableau, output='summary'):
    tableau = convert_min(tableau)
    while iter_next(tableau)==True:
        tableau = pivot(find_piv_r(tableau)[0],find_piv_r(tableau)[1],tableau)
    while iter(tableau)==True:
        tableau = pivot(find_piv(tableau)[0],find_piv(tableau)[1],tableau)

    lc = len(tableau[0,:])
    lr = len(tableau[:,0])
    var = lc - lr
    i = 0
    val = {}
    for i in range(var):
        col = tableau[:,i]
        s = sum(col)
        m = max(col)
        if float(s) == float(m):
            loc = np.where(col == m)[0][0]
            val[gen_var(tableau)[i]] = tableau[loc,-1]
        else:
            val[gen_var(tableau)[i]] = 0
    val['min'] = tableau[-1,-1]*-1
    if output == 'tableau':
        return tableau
    else:
        return val

def simplex(tableau):
    return maxz(tableau,output="tableau")

def simplexWrapper(A,C,B):
    m=np.concatenate((A,np.identity(B.shape[1])),axis=1)
    #add a column of zero
    #m=np.concatenate((m,np.transpose(np.array([np.zeros(B.shape[1])]))),axis=1)
    m=np.concatenate((m,np.transpose(B)),axis=1)
    c=np.concatenate((C,np.array([np.zeros(B.shape[1]+1)])),axis=1)
    #c=np.concatenate((C,np.array([np.zeros(B.shape[1])])),axis=1)
    #c=np.concatenate((c,np.array([[1,0]])),axis=1)
    m=np.concatenate((m,c),axis=0)
    print(minz(m))

if __name__ == "__main__":
    # A=np.array([[-2,-5],[3,-5],[8,3],[-9,7]])
    # B=np.array([[-30,-5,85,42]])
    # C=np.array([[-2,-7]])
    print("Enter the number of variables")
    num = int(input())
    print("Enter the number of constraints")
    num_const = int(input())
    print("Enter the matrix A:")
    A=[]
    for i in range(num_const):
        temp = list(map(float,input().split()))
        A.append(temp)
    A=np.array(A)
    print("Enter the vector B (space separated): Example: 4 5 1")
    temp=list(map(float,input().split()))
    B=np.array([temp])
    print("Enter the vector C (space separated): Example: 4 5 1")
    temp=list(map(float,input().split()))
    C=np.array([temp])*(-1)
    simplexWrapper(A,C,B)

'''
Created By : Kaustubh Pandey
Roll : S20160010041
UG - 4  CSE
'''