import sys
import re

class equation:
	def __init__(self):
		self.x = [0, 0, 0]
	def display(self):
		print(self.x)
		#if self.x[0] != 0:
			#print(f'{self.x[0]:g }')
			#print(str(self.x[0]) + " * X^" + str(0))

def parse_equation(value):
	e = equation()
	i = 0
	while i < len(value):
		is_negative = False
		if value[i] in ['+', '-']:
			is_negative = value[i] == '-'
			i += 1
		if i + 2 > len(value):
			sys.exit("Invalid equation")
		v = float(value[i])
		if value[i + 1] != '*' or len(value[i + 2]) != 3 or value[i + 2][:2] != 'X^':
			sys.exit("Invalid equation")
		x = int(value[i + 2][2])
		if x < 0 or x > 2:
			sys.exit("Unsupported polynomial degree")
		e.x[x] = -v if is_negative else v
		i += 3
	return (e)

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

left_equation = parse_equation(left)
left_equation.display()
right_equation = parse_equation(right)
right_equation.display()
left_reduce = reduce_equation(left_equation, right_equation)
left_reduce.display()