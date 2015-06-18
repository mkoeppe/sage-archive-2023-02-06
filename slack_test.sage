A = (
[1, 1],
[3, 1],
[1, 0],
) 
b = (1000, 1500, 500)
c = (10, 5)
P = InteractiveLPProblem(A, b, c)
D = P.initial_dictionary()	
view(D)