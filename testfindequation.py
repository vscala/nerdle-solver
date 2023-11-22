from findequation import *

def input_gen(stream):
	def mock_input(*args, **kwargs):
		return next(stream)
	return mock_input

def result_gen():
	results = []
	def mock_print(*args, **kwargs):
		results.append((args, kwargs))
	return mock_print, results
	
def test_search(user_input, include_macro = False):
	mock_print, results = result_gen()
	start_search(input_gen((inp for inp in user_input)), mock_print, include_macro)
	return [result[0][0] for result in results]
	
def macro_test_A():
	user_input = [
		"10", 
		"1???????=? /897", 
		"1????+?)=? 0*#$", 
		"1????+?)=? +23", 
		"14-(?+4)=? 5",
		"14-(?+4)=?"
	]
	results = test_search(user_input, True)
	print(results)

def micro_test_A():
	user_input = [
		"5", 
		"???=? 1+3", 
		"2*4=8"
	]
	results = test_search(user_input)
	print(results)

def micro_test_B():
	user_input = [
		"6", 
		"?????? 2*50", 
		"?????? +4-",
		"18/3=6"
	]
	results = test_search(user_input)
	print(results)

def micro_test_C():
	user_input = [
		"6", 
		"11??=? *50+438/6", 
		"11-?=?"
	]
	results = test_search(user_input)
	print(results)

micro_test_A()
micro_test_B()
micro_test_C()
macro_test_A()