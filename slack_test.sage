A = (
[1, 1],
[3, 1],
[1, 0],
) 
b = (1000, 1500, 500)
c = (10, 5)
P = InteractiveLPProblemStandardForm(A, b, c, style = 'vanderbei')
P.decision_variables()
P.slack_variables()
D = P.initial_dictionary()	
view(D)