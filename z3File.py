from z3 import *

s = Optimize()

# Variable declaration
A_6_7_R1 = Int("A_6_7_R1")
A_6_7_R2 = Int("A_6_7_R2")
A_7_7_R1 = Int("A_7_7_R1")
A_7_7_R2 = Int("A_7_7_R2")

V_R1 = Int("V_R1")
V_R2 = Int("V_R2")

d_0_R1  = Int("d_0_R1")
d_0_R2  = Int("d_0_R2")
d_1_R1  = Int("d_1_R1")
d_1_R2  = Int("d_1_R2")
d_2_R1  = Int("d_2_R1")
d_2_R2  = Int("d_2_R2")

d_6_7_0_R1 = Int("d_6_7_0_R1")
d_6_7_1_R1 = Int("d_6_7_1_R1")
d_6_7_2_R1 = Int("d_6_7_2_R1")
d_6_7_0_R2 = Int("d_6_7_0_R2")
d_6_7_1_R2 = Int("d_6_7_1_R2")
d_6_7_2_R2 = Int("d_6_7_2_R2")
d_7_7_0_R1 = Int("d_7_7_0_R1")
d_7_7_1_R1 = Int("d_7_7_1_R1")
d_7_7_2_R1 = Int("d_7_7_2_R1")
d_7_7_0_R2 = Int("d_7_7_0_R2")
d_7_7_1_R2 = Int("d_7_7_1_R2")
d_7_7_2_R2 = Int("d_7_7_2_R2")

# Number of cells in the mixture filled with Rt reagent
s.add(And(A_6_7_R1>=0, A_6_7_R1<=1, A_6_7_R2>=0, A_6_7_R2<=1))
s.add(And(A_7_7_R1>=0, A_7_7_R1<=1, A_7_7_R2>=0, A_7_7_R2<=1))

s.add(A_6_7_R1 + A_7_7_R1 == V_R1)
s.add(A_6_7_R2 + A_7_7_R2 == V_R2)

# If a cell is filled with reagent Rt then no reagent Rk where k != t can be filled in that cell.
s.add(A_6_7_R1 + A_6_7_R2 == 1)
s.add(A_7_7_R1 + A_7_7_R2 == 1)

# To get traceability and connectivity.
s.add(If(And(A_6_7_R1 == 1, A_7_7_R1 == 0), (d_6_7_0_R1 == 1), (d_6_7_0_R1 == 0)))
s.add(If(And(A_7_7_R1 == 1, A_6_7_R1 == 0), (d_7_7_0_R1 == 1), (d_7_7_0_R1 == 0)))
s.add(If(And(A_6_7_R2 == 1, A_7_7_R2 == 0), (d_6_7_0_R2 == 1), (d_6_7_0_R2 == 0)))
s.add(If(And(A_7_7_R2 == 1, A_6_7_R2 == 0), (d_7_7_0_R2 == 1), (d_7_7_0_R2 == 0)))
s.add(If(And(A_6_7_R1 == 1, A_7_7_R1 == 1), (d_6_7_1_R1 == 1), (d_6_7_1_R1 == 0)))
s.add(If(And(A_7_7_R1 == 1, A_6_7_R1 == 1), (d_7_7_1_R1 == 1), (d_7_7_1_R1 == 0)))
s.add(If(And(A_6_7_R2 == 1, A_7_7_R2 == 1), (d_6_7_1_R2 == 1), (d_6_7_1_R2 == 0)))
s.add(If(And(A_7_7_R2 == 1, A_6_7_R2 == 1), (d_7_7_1_R2 == 1), (d_7_7_1_R2 == 0)))

s.add(d_6_7_0_R1 + d_7_7_0_R1 == d_0_R1)
s.add(d_6_7_1_R1 + d_7_7_1_R1 == d_1_R1)
s.add(d_6_7_2_R1 + d_7_7_2_R1 == d_2_R1)
s.add(d_6_7_0_R2 + d_7_7_0_R2 == d_0_R2)
s.add(d_6_7_1_R2 + d_7_7_1_R2 == d_1_R2)
s.add(d_6_7_2_R2 + d_7_7_2_R2 == d_2_R2)

s.add(Implies(V_R1 == 1, And(d_0_R1 == 1, d_1_R1 == 0, d_2_R1 == 0)))
s.add(Implies(V_R1 == 2, And(d_0_R1 == 0, d_1_R1 == 2, d_2_R1 == 0)))
s.add(Implies(V_R1 == 3, And(d_0_R1 == 0, d_1_R1 == 2, d_2_R1 == 1)))
s.add(Implies(V_R1 == 4, And(d_0_R1 == 0, d_1_R1 == 0, d_2_R1 == 4)))
s.add(Implies(V_R2 == 1, And(d_0_R2 == 1, d_1_R2 == 0, d_2_R2 == 0)))
s.add(Implies(V_R2 == 2, And(d_0_R2 == 0, d_1_R2 == 2, d_2_R2 == 0)))
s.add(Implies(V_R2 == 3, And(d_0_R2 == 0, d_1_R2 == 2, d_2_R2 == 1)))
s.add(Implies(V_R2 == 4, And(d_0_R2 == 0, d_1_R2 == 0, d_2_R2 == 4)))

s.add(And(V_R1 == 1, V_R2 == 1))

if s.check() == unsat:
	print("Not possible to create traceable graph for all reagents")
else:
	fp = open('output0.txt','w')
	values = s.model()
	if values[A_6_7_R1] == 1:
		fp.write("6,7,R1\n")
	if values[A_6_7_R2] == 1:
		fp.write("6,7,R2\n")
	if values[A_7_7_R1] == 1:
		fp.write("7,7,R1\n")
	if values[A_7_7_R2] == 1:
		fp.write("7,7,R2\n")
