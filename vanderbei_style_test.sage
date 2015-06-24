# '''
# Loading this file on sage will test the notations for vanderbei 
# style and original style for primial, dual and auxiliary problems.
# All examples are obtained from http://doc.sagemath.org/html/en/reference/numerical/sage/numerical/interactive_simplex_method.html#sage.numerical.interactive_simplex_method.LPDictionary

# '''

# vanderbei style 
# Example obtained from sage website
A = (
[1, 1],
[3, 1],
[1, 0],
) 
b = (1000, 1500, 500)
c = (10, 5)
'''can add argument to objective
like P = InteractiveLPProblemStandardForm(A, b, c, style="vanderbei", objective = "a")
'''
P = InteractiveLPProblemStandardForm(A, b, c, style="vanderbei")

# Primal
D = P.initial_dictionary()
view(D)
D = P.final_dictionary()	
view(D)

# Dual
'''can add argument to objective
DP = P.dual(objective = "b")
'''
DP = P.dual()
DP = DP.standard_form()
DPSF_initial = DP.initial_dictionary()	
view(DPSF_initial)
DPSF = DP.final_dictionary()
view(DPSF)

# Auxiliary Problem 
# Example obtained from the examples on sage website)
A = ([1, 1], [3, 1], [-1, -1])
b = (1000, 1500, -400)
c = (10, 5)
P = InteractiveLPProblemStandardForm(A, b, c, style = "vanderbei")
'''can add argument to objective
AP = P.auxiliary_problem("aux")
'''
AP = P.auxiliary_problem()
D = AP.initial_dictionary()
view(D)

D.enter(0)
D.leave("w3")
D.update()
view(D)

D.enter("x1")
D.leave(0)
D.update()
view(D)

D.is_optimal()
D.objective_value()
D = P.feasible_dictionary(D)
view(D)


# ##################### 
#original style
A = (
[1, 1],
[3, 1],
[1, 0],
) 
b = (1000, 1500, 500)
c = (10, 5)
P = InteractiveLPProblemStandardForm(A, b, c)

# Primal
D = P.initial_dictionary()
view(D)
D = P.final_dictionary()	
view(D)

# # Dual
DP = P.dual(objective = "P")
DP = DP.standard_form()
DPSF_initial = DP.initial_dictionary()	
view(DPSF_initial)
DPSF = DP.final_dictionary()
view(DPSF)

# Auxiliary Problem 
# Example obtained from the examples on sage website)
A = ([1, 1], [3, 1], [-1, -1])
b = (1000, 1500, -400)
c = (10, 5)
P = InteractiveLPProblemStandardForm(A, b, c)
AP = P.auxiliary_problem()
D = AP.initial_dictionary()
view(D)

D.enter(0)
D.leave(5)
D.update()
view(D)

D.enter(1)
D.leave(0)
D.update()
view(D)

D.is_optimal()
D.objective_value()
D = P.feasible_dictionary(D)
view(D)


###############################
#self-defined objective variable
# vanderbei style 
# Example obtained from sage website
A = (
[1, 1],
[3, 1],
[1, 0],
) 
b = (1000, 1500, 500)
c = (10, 5)
P = InteractiveLPProblemStandardForm(A, b, c, style = "vanderbei", objective="a")

# Primal
D = P.initial_dictionary()
view(D)
D = P.final_dictionary()	
view(D)

# Dual
DP = P.dual(objective="dual")
DP = DP.standard_form()
DPSF_initial = DP.initial_dictionary()	
view(DPSF_initial)
DPSF = DP.final_dictionary()
view(DPSF)

# Auxiliary Problem 
# Example obtained from the examples on sage website)
A = ([1, 1], [3, 1], [-1, -1])
b = (1000, 1500, -400)
c = (10, 5)
P = InteractiveLPProblemStandardForm(A, b, c, style="vanderbei", objective="b")
AP = P.auxiliary_problem(objective="aux")
D = AP.initial_dictionary()
view(D)

D.enter(0)
D.leave("w3")
D.update()
view(D)

D.enter("x1")
D.leave(0)
D.update()
view(D)

D.is_optimal()
D.objective_value()
D = P.feasible_dictionary(D)
view(D)


# ##################### 
#original style
A = (
[1, 1],
[3, 1],
[1, 0],
) 
b = (1000, 1500, 500)
c = (10, 5)
P = InteractiveLPProblemStandardForm(A, b, c)

# Primal
D = P.initial_dictionary()
view(D)
D = P.final_dictionary()	
view(D)

# # Dual
DP = P.dual()
DP = DP.standard_form()
DPSF_initial = DP.initial_dictionary()	
view(DPSF_initial)
DPSF = DP.final_dictionary()
view(DPSF)

# Auxiliary Problem 
# Example obtained from the examples on sage website)
A = ([1, 1], [3, 1], [-1, -1])
b = (1000, 1500, -400)
c = (10, 5)
P = InteractiveLPProblemStandardForm(A, b, c)
AP = P.auxiliary_problem()
D = AP.initial_dictionary()
view(D)

D.enter(0)
D.leave("w3")
D.update()
view(D)

D.enter("x1")
D.leave(0)
D.update()
view(D)

D.is_optimal()
D.objective_value()
D = P.feasible_dictionary(D)
view(D)
