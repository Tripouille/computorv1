import sys
import re

class expression:
	def __init__(self, value):
		self.x = [0, 0, 0]
		i = 0
		while i < len(value):
			is_negative = False
			if value[i] in ['+', '-']:
				is_negative = value[i] == '-'
				i += 1
			if i + 2 > len(value):
				sys.exit("Invalid expression")
			v = float(value[i])
			if value[i + 1] != '*' or len(value[i + 2]) != 3 or value[i + 2][:2] != 'X^':
				sys.exit("Invalid expression")
			x = int(value[i + 2][2])
			if x < 0 or x > 2:
				sys.exit("Unsupported polynomial degree")
			self.x[x] = -v if is_negative else v
			i += 3

	def display(self):
		print(f'{self.x[0]:g} * X^0', end="")
		print(" + " if self.x[1] >= 0 else " - ", end="")
		print(f'{abs(self.x[1]):g} * X^1', end="")
		print(" + " if self.x[2] >= 0 else " - ", end="")
		print(f'{abs(self.x[2]):g} * X^2', end="")
	
	def get_degree(self):
		for i in range(2, -1, -1):
			if self.x[i] != 0:
				return (i)

def reduce_equation(left, right):
	for i in range(3):
		left.x[i] -= right.x[i] if right.x[i] > 0 else right.x[i]
	return (left)

if len(sys.argv) != 2:
	sys.exit("usage: python computor.py equation")

values = re.split(" +", sys.argv[1])
try:
	equal_pos = values.index("=")
except ValueError:
	sys.exit("Missing = operand")
left, right = values[:equal_pos], values[equal_pos + 1:]
if not len(left) or not len(right):
	sys.exit("Invalid expression")
left_expression = expression(left)
if not (len(right) == 1 and int(right[0]) == 0):
	left_expression = reduce_equation(left_expression, expression(right))
print("Reduced form: ", end=''); left_expression.display(); print(" = 0")
print(f'Polynomial degree: {left_expression.get_degree()}')