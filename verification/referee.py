"""
CheckiOReferee is a base referee for checking you code.
	arguments:
		tests -- the dict contains tests in the specific structure.
			You can find an example in tests.py.
		cover_code -- is a wrapper for the user function and additional operations before give data
			in the user function. You can use some predefined codes from checkio.referee.cover_codes
		checker -- is replacement for the default checking of an user function result. If given, then
			instead simple "==" will be using the checker function which return tuple with result
			(false or true) and some additional info (some message).
			You can use some predefined codes from checkio.referee.checkers
		add_allowed_modules -- additional module which will be allowed for your task.
		add_close_builtins -- some closed builtin words, as example, if you want, you can close "eval"
		remove_allowed_modules -- close standard library modules, as example "math"

checkio.referee.checkers
	checkers.float_comparison -- Checking function fabric for check result with float numbers.
		Syntax: checkers.float_comparison(digits) -- where "digits" is a quantity of significant
			digits after coma.

checkio.referee.cover_codes
	cover_codes.unwrap_args -- Your "input" from test can be given as a list. if you want unwrap this
		before user function calling, then using this function. For example: if your test's input
		is [2, 2] and you use this cover_code, then user function will be called as checkio(2, 2)
	cover_codes.unwrap_kwargs -- the same as unwrap_kwargs, but unwrap dict.

"""

from checkio.signals import ON_CONNECT
from checkio import api
from checkio.referees.io import CheckiOReferee
from checkio.referees import cover_codes
from checkio.referees import checkers

from tests import TESTS

import marshal

if isinstance(__builtins__,dict):
	compile=__builtins__['compile']
else:
	compile=__builtins__.compile

class CheckiORefereeGolf(CheckiOReferee):
	def __init__(self, max_length, **kwargs):
		self.max_length = max_length
		super().__init__(**kwargs)
	def check_code(self, codestring):
		codestring = codestring.replace("\r\n","\n")
		codestring = codestring.replace("\r","\n")
		codestring = codestring.rstrip()
		try:
			return len( marshal.dumps(compile(codestring,'','exec')) )
		except SyntaxError as detail:
			import traceback
			lines = traceback.format_exception_only(SyntaxError, detail)
			return "\n".join(lines)
	def check_current_test(self, data):
		if self.inspector:
			inspector_result, inspector_result_addon = self.inspector(self.code, self.runner)
			self.inspector = None
			self.current_test["inspector_result_addon"] = inspector_result_addon
			if not inspector_result:
				self.current_test["inspector_fail"] = True
				api.request_write_ext(self.current_test)
				return api.fail(0, inspector_result_addon)
		user_result = data['result']
		check_result = self.check_user_answer(user_result)
		self.current_test["result"], self.current_test["result_addon"] = check_result
		api.request_write_ext(self.current_test)
		if not self.current_test["result"]:
			return api.fail(self.current_step, self.get_current_test_fullname())
		if self.next_step():
			self.test_current_step()
		else:
			if self.next_env():
				self.restart_env()
			else:
				# all tests passed. now check code size.
				code_len = self.check_code(self.code)
				if isinstance(code_len,str):
					message = 'Something wrong: '+code_len
					self.current_test["inspector_result_addon"] = message
					self.current_test["inspector_fail"] = True
					api.request_write_ext(self.current_test)
					return api.fail(0, message)
				if code_len >= self.max_length:
					message = "Your code is correct, but this code compiles too long ({}) for any points".format(code_len)
					self.current_test["inspector_result_addon"] = message
					self.current_test["inspector_fail"] = True
					api.request_write_ext(self.current_test)
					return api.fail(0, message)
				else:
					api.success(self.max_length - code_len)

api.add_listener(
	ON_CONNECT,
	CheckiORefereeGolf(
		tests=TESTS,
		max_length=1000,
		cover_code={
			'python-27': cover_codes.unwrap_args,
			'python-3': cover_codes.unwrap_args
		},
		function_name="fibgolf",
	).on_ready)
