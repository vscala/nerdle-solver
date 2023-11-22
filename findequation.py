from isvalidequation import *
from heapq import *
import sys

def heuristic_eq_strength(eq: str) -> int:
	return len(set(eq))

def better(eq1: str, eq2: str) -> bool:
	return heuristic_eq_strength(eq1) > heuristic_eq_strength(eq2)

def estimated_mx_eq_str(cur) -> int:
	return max_cover(cur) # could maybe do better?

def max_cover(sets):
	sets = [s.copy() for s in sets]
	selected_elements = set()
	sorted_sets = sorted(sets, key=lambda s: len(s), reverse=True)
	for current_set in sorted_sets:
		try:
			element = next(element for element in current_set if element not in selected_elements)
			selected_elements.add(element)
			for other_set in sets:
				other_set.discard(element)
		except:
			continue
	return len(selected_elements)

# Give up after a good enough best guess has been found and traversal count is high
GIVE_UP = True
def find_best_guess(cur) -> str:
	heap = [(0, 0, "")]
	best = ""
	mx_eq_strength = estimated_mx_eq_str(cur)
	count = 0
	while heap:
		_, i, peq = heappop(heap)
		count += 1
		if GIVE_UP and heuristic_eq_strength(best) >= mx_eq_strength - max(0, len(str(count)) - 4):
			return best
		if not is_valid_partial_equation(peq):
			continue
		if i == len(cur):
			if better(peq, best):
				if not is_valid_equation(peq):
					continue
				if heuristic_eq_strength(peq) >= mx_eq_strength:
					return peq
				best = peq
			continue
		for char in cur[i]:
			new_peq = peq + char
			heappush(heap, (-heuristic_eq_strength(new_peq), i + 1, new_peq))
	return best

best_first_guess = {
	5: "1+2=3",
	6: "2*5=10",
	7: "2*+5=10",
	8: "2-6/+3=0",
	9: "1*+20/4=5",
	10: "16/8+9-4=7",
	11: "1234567*0=0",
	12: "12345678*0=0",
	13: "123456789*0=0",
	14: "(12345678)*0=0"
}

def search(input_function, output_function, length, cur, guess):
	for i, v in enumerate(guess):
		cur[i].discard(v)
	output_function(guess)
	try:
		inp = input_function('Type pattern and new bad chars (eg. "1+?=? 12"): ').split()
	except:
		return
	if len(inp) == 2:
		pattern, bad_chars = inp
		bad_chars = set(bad_chars)
		if "=" in pattern:
			bad_chars.add("=")
	else:
		pattern = inp[0]
		bad_chars = set()
	for i, v in enumerate(pattern):
		cur[i] -= bad_chars
		if v != "?":
			cur[i] = set(v)
	guess = find_best_guess(cur)
	search(input_function, output_function, length, cur, guess)

def start_search(input_function, output_function, include_macro = False):
	length = int(input_function('Type guessing length: '))
	chars = CHARSET if include_macro else CHARSET - MACROSET
	cur = [chars.copy() for _ in range(length)]
	guess = best_first_guess[length]
	search(input_function, output_function, length, cur, guess)

if __name__ == "__main__":
	print("Using", ["micro", "macro"]["macro" in sys.argv], "char set")
	start_search(input, print, "macro" in sys.argv)
