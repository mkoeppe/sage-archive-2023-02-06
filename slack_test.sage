A = (
[1, 1],
[3, 1],
[1, 0],
) 
b = (1000, 1500, 500)
c = (10, 5)
P = InteractiveLPProblemStandardForm(A, b, c)
P = InteractiveLPProblemStandardForm(A, b, c, style = "vanderbei")
D = P.initial_dictionary()	
view(D)
DP = P.dual()
DP = DP.standard_form()
DPSF = DP.initial_dictionary()	
view(DPSF)