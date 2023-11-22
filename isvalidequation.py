from collections import Counter
import warnings

PARANSET = set('()')
UNARYSET = set('+-')
POSTUNARYSET = set('#$')
BINARYSET = set('+-*/=')
NUMSET = set('0123456789')
MACROSET = PARANSET | POSTUNARYSET
CHARSET = BINARYSET | UNARYSET | NUMSET | MACROSET

REPLACE = {
	"=" : "==",
	"#" : "**2",
	"$" : "**3"
}

def eval_supress(eq: str) -> bool:
	try:
		warnings.filterwarnings("ignore", category=SyntaxWarning, module="<string>")
		res = eval(eq)
		warnings.resetwarnings()
		return res
	except:
		warnings.resetwarnings()
		return False

def is_valid_partial_equation(peq: str) -> bool:
	peq = peq.replace(" ", "").strip()
	if not peq:
		return True
	multiset = Counter(peq)
	if multiset["="] > 1:
		return False
	if multiset.keys() - CHARSET:
		return False
	if peq[0] not in (UNARYSET | NUMSET | set('(')):
		return False
	if "()" in peq:
		return False
	if "=" in multiset:
		left, right = peq.split("=")
		if not left:
			return False
		if left[-1] not in (NUMSET | POSTUNARYSET | set(')')):
			return False
		return is_valid_partial_equation(left) and is_valid_partial_equation(right)
	consecutive_ops = None
	for v in peq:
		if v in BINARYSET:
			if not consecutive_ops:
				consecutive_ops = 1
			elif consecutive_ops == 1 and v in UNARYSET:
				consecutive_ops = 2
			else:
				return False
		else:
			consecutive_ops = None
	return True

def is_valid_equation(eq: str) -> bool:
	if eq.count("=") != 1:
		return False
	if not is_valid_partial_equation(eq):
		return False
	for op in REPLACE:
		eq = eq.replace(op, REPLACE[op])
	return eval_supress(eq)
	
if __name__ == "__main__":
	def assert_valid(eq: str):
		for i in range(len(eq)+1):
			print("asserting", eq[:i], "is a valid partial equation")
			assert is_valid_partial_equation(eq[:i])
		print("asserting", eq, "is a valid equation")
		assert is_valid_equation(eq)
		
	assert_valid("1 + -1 = 0")
	assert_valid("5$=125")
	assert_valid("5#=25")
