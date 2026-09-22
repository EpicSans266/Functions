from tokenize import TokenError

from sympy import Abs, E, I, S, cos, diff, exp, log, oo, parse_expr, pi, sin, solveset, sqrt, symbols, tan
from sympy.calculus.util import continuous_domain, function_range


x = symbols("x", real=True)


def is_injective(function):
	"""Проверяет инъективность функции на всей вещественной оси."""
	if continuous_domain(function, x, S.Reals) != S.Reals:
		return False

	derivative = diff(function, x)
	negative_values = solveset(derivative < 0, x, domain=S.Reals)
	positive_values = solveset(derivative > 0, x, domain=S.Reals)
	zero_values = solveset(derivative, x, domain=S.Reals)

	return (
		(negative_values == S.EmptySet or positive_values == S.EmptySet)
		and zero_values.is_FiniteSet
	)


def is_surjective(function):
	"""Проверяет сюръективность функции из R в R."""
	if continuous_domain(function, x, S.Reals) != S.Reals:
		return False

	try:
		return function_range(function, x, S.Reals) == S.Reals
	except NotImplementedError:
		return False


def is_bijective(function):
	return is_injective(function) and is_surjective(function)


def read_function(prompt):
	expression = input(prompt)
	allowed_symbols = {
		"x": x,
		"sin": sin,
		"cos": cos,
		"tan": tan,
		"exp": exp,
		"log": log,
		"sqrt": sqrt,
		"Abs": Abs,
		"pi": pi,
		"E": E,
	}
	return parse_expr(expression, local_dict=allowed_symbols)


try:
	function = read_function(
		"Введите функцию f(x), например x**2 или 2*x + 1: "
	)
	if function.has(I, oo, -oo) or function.free_symbols - {x}:
		raise ValueError

	injective = is_injective(function)
	surjective = is_surjective(function)

	if injective:
		print("Функция инъективна на множестве R")
	else:
		print("Функция не является инъективной на множестве R")

	if surjective:
		print("Функция сюръективна на множестве R")
	else:
		print("Функция не является сюръективной на множестве R")

	if injective and surjective:
		print("Функция биективна на множестве R")
	else:
		print("Функция не является биективной на множестве R")

	second_function = read_function(
		"Введите функцию g(x) для композиции f(g(x)): "
	)
	if second_function.has(I, oo, -oo) or second_function.free_symbols - {x}:
		raise ValueError

	print("Композиция f(g(x)) =", function.subs(x, second_function))
except (TokenError, ValueError, TypeError, SyntaxError, NotImplementedError):
	print("Не удалось распознать функцию или проверить её свойства")
