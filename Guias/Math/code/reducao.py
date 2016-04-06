# -*- coding: utf-8 -*-

from numpy import *
from numpy.linalg import *

#a is a numpy matrix
def print_matriz(a,n):
	for i in range(0,n):
		st = ''
		for j in range(0,n):
			st += ('%7.2f' % a[i,j])
			if (j != n - 1):
				st += ' '
		print(st)
	print()

def generateA(n, b, d, e, tau, taul):
	L = (-tau) * eye(n)
	L[0][0] = (-taul)
	M = zeros((n,n))
	for k in range(0,n):
		M[k][k] = -2*b[k] if k != 0 else -b[k]
		if k != n-1:
			M[k+1][k] = d[k+1]
			M[k][k+1] = e[k] if k != 0 else b[k]
	A = vstack((hstack((zeros((n,n)),eye(n))),hstack((M,L))))
	return matrix(A)

def generateB(n, eN):
	B = zeros((2*n,1))
	B[2*n-1] = e[n-1]
	return matrix(B)

def generateC(n):
	C = zeros((1,2*n))
	C[0] = 1
	return matrix(C)

def getReducedSystem(A,B,C):
	eig_A,T = eig(A)	# eig_A são os autovalores de A, e T é a matriz de autovetores
	T_inv = matrix(inv(T))
	A_M = T_inv * A * T
	B_M = T_inv * B
	C_M = C * T
	C_M_diag = zeros((2*n,2*n), complex)
	for i in range(0,2*n):
		C_M_diag[i][i] = C_M[0,i]

def main():
	n = 6
	tau = 0.2426	# tau do barbante
	taul = 0.1133	# tau da bolinha
	ms = 0.0006		# massa linear do barbante (kg/m)
	mb = 0.00015	# massa da bolinha (kg)
	g = 9.807		# aceleração da gravidade (m/s^2)
	L = 0.82		# Comprimento total do barbante (m)
	l = L/n			# distância entre dois pontos de discretização
	T0 = mb*g		# Tração no ponto 0 (logo acima da bolinha) - considerando peso da bolinha (N)

	b = zeros((n,1))
	c = g/(2*l)
	d = zeros((n,1))
	e = zeros((n,1))
	b[0] = g/((n-1)*l)
	for k in range(2,n+1):
		b[k-1] = (T0 + ms*g*(k-1)*l)/(ms*l**2)
		d[k-1] = b[k-1] - c
		e[k-1] = b[k-1] + c

	# b = [1,2,3,4,5,6]
	# d = [0,0.2,0.3,0.4,0.5,0.6] # Teste
	# e = [0,12,13,14,15,16]

	A = generateA(n, b, d, e, tau, taul)
	print_matriz(A,2*n)

if __name__ == "__main__":
	main()