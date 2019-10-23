'''
Created By : Kaustubh Pandey
Roll : S20160010041
UG - 4  CSE
'''
import numpy as np
from simplex2 import simplex
from simplex2 import find_neg

'''
1. Find dual and a lambda (a feasible solution)
2. Form set P and formualte ARP; optimize ARP, if y==0 stop
3. If min val of ARP is +ve obtain u0 from ARD
4. Update lambda by finding epsilon
5. Update the table and repeat the steps until y==0 
'''
#returns true if all the values in last row are strictly positive
def is_pos(table):
    lr = len(table[:,0])
    m = min(table[lr-1,:-1])
    if m>0:
       return True
    return False

def findDual(A,C):
	m=np.concatenate((A,C),axis=0)
	return np.transpose(m)

def findInitialLambda(n):
	return np.array([np.zeros(n)])

def Tableau(A,C,B,lamb):
	num_const = A.shape[0]
	part = np.concatenate((A,np.identity(num_const)),axis=1)
	m=np.concatenate((part,np.transpose(B)),axis=1)
	red = np.sum(m,axis=0)
	for i in range(len(red)):
		if(red[i]==1):
			red[i]=0
		else:
			red[i]=-red[i]
	m=np.concatenate((m,np.array([red])),axis=0)
	last = C-np.matmul(lamb,A)
	last = np.concatenate((last,np.array([np.ones(num_const+1)])),axis=1)
	m=np.concatenate((m,last),axis=0)
	return m

def check_col(col):
	count=0
	flag=1
	for i in col:
		if(i==1):
			count+=1
		elif(i!=0):
			flag=0
			break
	if(count==1 and flag==1):
		return True
	return False

def find_single_one_col(table):
	#neglect last two rows
	a=[]
	for i in range(table.shape[1]):
		if(check_col(table[:-2,i])):
			a.append(i)
	return a
# a : list of indices that are basis
def find_u(table,num,num_const):
	u=[]
	# a=find_single_one_col(table)
	# print(a,num,num_const)
	a = list(range(num,num+num_const))
	for i in a:
		u.append(1-table[-2,i])
	return np.array([u])
def find_epsilon(table,u,num_const):
	A=table[:-2,:-(num_const+1)]
	pro = np.matmul(u,A)
	return min(np.array([table[-1,:pro.shape[1]]])/pro)
'''
num : number of variables
num_const : number of constraints
C : original cost
table : tableau
'''
def ARP_ARD(table,C,lamb,num,num_const):
	while(True):
		#print(find_neg(table))
		if find_neg(table) is not None:
			table=simplex(table)
		#print('$',table)
		if(is_pos(table)):
			#ARD
			u=find_u(table,num,num_const)
			epsilon = min(find_epsilon(table,u,num_const))
			lamb = lamb + epsilon*u
			#print(lamb)
			#update last row
			for i in range(num):
				col=np.array(table[:-2,i])
				table[-1,i]=C[0,i]-np.matmul(lamb,col)
			#print(table)
		else:
			#x and lambda are optimal
			#if num_const basis cols between index in [0,num)
			count=0
			for i in range(num):
				if(check_col(table[:,i])):
					count+=1
			if(count==num_const):
				print("Exit")
				break
	return table
#return index of row or None
def basis(col):
	if(min(col)==0 and sum(col)==1):
		for i in range(len(col)):
			if(col[i]==1):
				return i
	return None
def extract_output(table,C,num):
	res=[]
	for i in range(num):
		col = table[:,i]
		row = basis(col)
		if row is not None:
			res.append(table[row,-1])
		else:
			res.append(0)
	val={}
	result=0
	for i in range(C.shape[1]):
		result += C[0,i]*res[i]
		val['x'+str(i+1)]=res[i]
	val['min'] = result
	return val

if __name__ == "__main__":
	'''
	Sample:
	A=np.array([[1,1,2],[2,1,3]])
	C=np.array([[2,1,4]])
	B=np.array([[3,5]])
	'''
	'''
	Assuming minimization problem in standard form
	To maximize, enter the C values multiplied with -1
	'''
	# A=np.array([[1,1,2],[2,1,3]])
	# C=np.array([[2,1,4]])
	# B=np.array([[3,5]])
	# num = C.shape[1]
	# num_const = B.shape[1]
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
	C=np.array([temp])
	lamb=findInitialLambda(B.shape[1])
	table= Tableau(A,C,B,lamb)
	#print(table)
	table=ARP_ARD(table,C,lamb,num,num_const)
	print(extract_output(table,C,num))


'''
Created By : Kaustubh Pandey
Roll : S20160010041
UG - 4  CSE
'''