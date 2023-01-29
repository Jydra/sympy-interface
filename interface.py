##SYMBOLIC COMPUTATION FRAMEWORK
from sympy import symbols, sin, cos, sqrt, Eq, expand, simplify, collect, solve, lambdify, pprint, latex
from sympy.simplify.fu import *
from IPython.display import display, Latex

def verbose_output(obj : list, eq, n, prec = 2):
  """Displays verbose output for various symbolic computation commands from a list of operations
  
  :param obj: a list where obj[0] contains an instruction, and the rest of the arguments supply information required
  :type obj: list
  :param eq: a sympy equation to print in LaTeX
  :type obj: sympy.core.relational.Equality
  :param n: the current index of the operation to be performed in the op list
  :type n: int
  :param prec: the precision of numeric values in the verbose output, defaults to 2
  :type prec: int, optional
  """
  latex_string = r"\text{Step " + str(n+1) + ": "
  if obj[0] == "expand":
    latex_string += r"Expand equation}"
  elif obj[0] == "collect_lhs":
    latex_string += "Collect all }" + latex(obj[1]) + r" \text{ on LHS}"
  elif obj[0] == "collect_rhs":
    latex_string += "Collect all }" + latex(obj[1]) + r" \text{ on RHS}"
  elif obj[0] == "simplify":
    latex_string += "Simplify equation}"
  elif obj[0] == "pythag_id":
    latex_string += "Apply the Pythagorean identity}"
  elif obj[0] == "trig_split_args":
    latex_string += "Split compound arguments in trig functions}"
  elif obj[0] == "to_lhs":
    latex_string += "Move all terms to LHS}"
  elif obj[0] == "to_rhs":
    latex_string += "Move all terms to RHS}"
  elif obj[0] == "solve":
    if len(obj) == 2:
      latex_string += "Solve equation for }" + latex(obj[1])
    if len(obj) == 3:
      latex_string += "Solve equation for } " + latex(obj[1]) +r" \text{ and select solution \#}" + str(obj[2]+1)
  elif obj[0] == "var_expand":
    latex_string += "Expand the variables: }" + r"\text{, }".join([latex(i) for i in obj[2]])
  elif obj[0] == "var_set":
    latex_string += "Set the variables: }" + r"\text{, }".join([latex(i)+"="+latex(obj[1][i].rhs.evalf(prec)) for i in obj[2]])
  elif obj[0] == "var_collect":
    latex_string += "Collect into the variables: }" + r"\text{, }".join(latex(i) for i in obj[2])
  elif obj[0] == "init":
    latex_string+= "Begin with }"
  display(Latex(latex_string))
  print ("\n")
  display(Latex(latex(eq)))
  print ("\n\n")

def exec_op (n:int, op:list, eq, is_verbose = False, prec = 2):
  """Executes an operation on an equation object

  :param n: An integer describing what operation is currently being executed
  :param type: int
  :param op: A list containing the operation and necessary arguments for the operation
  :param type: list
  :param eq: The equation to be manipulated
  :param type: sympy.core.relational.Eq
  :param is_verbose: If verbose output is required
  :param type: bool, optional
  :param prec: The precision of numerals in the verbose output LaTeX
  :param type: int, optional
  :return: The manipulated equation
  :rtype: sympy.core.relational.Eq
  """
  if op[n][0] == "expand":
    eq = eq.expand()
  elif op[n][0] == "collect_lhs":
    eq = Eq(collect(eq.lhs,op[n][1]),eq.rhs)
  elif op[n][0] == "collect_rhs":
    eq = Eq(eq.lhs,collect(eq.rhs,op[n][1]))
  elif op[n][0] == "simplify":
    eq = eq.simplify()
  elif op[n][0] == "pythag_id":
    eq = TR5(eq)
  elif op[n][0] == "trig_split_args":
    eq = TR10(eq)
  elif op[n][0] == "to_lhs":
    eq = Eq(eq.lhs - eq.rhs,0)
  elif op[n][0] == "to_rhs":
    eq = Eq(0, eq.rhs-eq.lhs)
  elif op[n][0] == "solve":
    if len(op[n]) == 2:
      eq = Eq(op[n][1], solve(eq,op[n][1]))
    elif len(op[n]) == 3:
      eq = Eq(op[n][1], solve(eq,op[n][1])[op[n][2]])
  elif op[n][0] == "var_expand" or op[n][0] == "var_set":
    for i in op[n][2]:
      eq = eq.subs(op[n][1][i].lhs,op[n][1][i].rhs)
  elif op[n][0] == "var_collect":
    for i in op[n][2]:
      eq = eq.subs(op[n][1][i].rhs,op[n][1][i].lhs)
  elif op[n][0] == "init":
    eq = eq
  else:
    print(op[n][0] + " is unsupported in exec_Op()")
  if is_verbose:
    verbose_output(op[n], eq, n, prec)
  return eq
