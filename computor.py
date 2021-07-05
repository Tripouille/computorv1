import sys
import re
import math
from fractions import Fraction

class Polynome:
	def __init__(self, string):
		self.x = [0, 0, 0]
		i = 0
		string_len = len(string)
		re_number = re.compile("^[-+]{0,1}\d+(\.\d+){0,1}")
		while i < string_len:
			x = 0
			match = re_number.match(string[i:])
			if string[i] == 'X' or string[i:i+2] == "+X" or string[i:i+2] == "-X":
				value = 1.0 if not string[i:i+2] == "-X" else -1.0
				i += 1 if not string[i] == 'X' else 0
			else:
				if match is None: sys.exit("Error: expecting number but found: " + string[i:])
				match_end = match.end()
				value = float(string[i:i + match_end])
				i += match_end
			if i < string_len and string[i] == '*':
				i += 1
				if not i < string_len or string[i] != 'X': sys.exit("Error: expecting X.")
			if i < string_len and string[i] == 'X':
				x = 1
				i += 1
				if i < string_len and string[i] == '^':
					i += 1
					if not i < string_len or string[i] not in ['0', '1', '2']:
						sys.exit("Error: expecting ^ + value in ['0', '1', '2'].")
					x = int(string[i])
					i += 1
			if i < string_len and string[i] not in ['+', '-']: sys.exit("Error: expecting operand but found: " + string[i])
			self.x[x] += value

	def display(self):
		if self.x[0] != 0:
			print(f"{self.x[0]:g} ", end="")
		if self.x[1] != 0:
			if self.x[0] != 0: print("+ " if self.x[1] >= 0 else "- ", end="")
			elif self.x[1] < 0: print("-", end='')
			print(f"{abs(self.x[1]):g}X ", end="") if abs(self.x[1]) != 1.0 else print("X ", end='')
		if self.x[2] != 0:
			if self.x[0] != 0 or self.x[1] != 0: print("+ " if self.x[2] >= 0 else "- ", end="")
			elif self.x[2] < 0: print("-", end='')
			print(f"{abs(self.x[2]):g}X^2 ", end="") if abs(self.x[2]) != 1.0 else print("X^2 ", end='')
		if self.x[0] == 0 and self.x[1] == 0 and self.x[2] == 0: print("0 ", end='')

	def get_degree(self):
		for i in range(2, -1, -1):
			if self.x[i] != 0:
				return (i)

def reduce_polynome(left, right):
	for i in range(3):
		left.x[i] -= right.x[i]
	return (left)

def get_discriminant(polynome):
	return (polynome.x[1] ** 2 - 4 * polynome.x[0] * polynome.x[2])

def solve_second_degree(p):
	discriminant = get_discriminant(p)
	print(f"Discriminant: {discriminant}")
	if discriminant > 0:
		print("Discriminant is strictly positive, the two solutions are:")
		squareroot_discriminant = math.sqrt(discriminant)
		print(format_solution((-p.x[1] + squareroot_discriminant) / (2 * p.x[2])))
		print(format_solution((-p.x[1] - squareroot_discriminant) / (2 * p.x[2])))
	elif discriminant == 0:
		print(f"The solution is: \n{format_solution(-p.x[1] / (2 * p.x[2]))}")
	else:
		print("Discriminant is strictly negative, there is no solution.")

def solve_one_degree(p):
	print(f"The solution is: \n{format_solution(-p.x[0] / p.x[1])}")

def format_solution(solution):
	if (solution.as_integer_ratio()[1] <= 100):
		return (Fraction(solution))
	return (solution)

#Main
if len(sys.argv) != 2:
	sys.exit("usage: python computor.py equation")

expression = sys.argv[1].replace(' ', '')
try: equal_pos = expression.index('=')
except ValueError: sys.exit("Error: Missing = operand.")
left_string, right_string = expression[:equal_pos], expression[equal_pos + 1:]
if not len(left_string) or not len(right_string): sys.exit("Error: Invalid equation")

left_polynome = reduce_polynome(Polynome(left_string), Polynome(right_string))
print("Reduced form: ", end=''); left_polynome.display(); print("= 0")
degree = left_polynome.get_degree()
print(f'Polynomial degree: {degree}')
if degree == 2:
	solve_second_degree(left_polynome)
elif degree == 1:
	solve_one_degree(left_polynome)
elif degree == 0:
	print("The solution is: \n0") if left_polynome.x[0] == 0 else print("There is no solution.")
else:
	print("The solution is: \nAll real numbers.")
