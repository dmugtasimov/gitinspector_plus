#!/usr/bin/python
# coding: utf-8
#
# Copyright © 2012 Ejwa Software. All rights reserved.
#
# This file is part of gitinspector.
#
# gitinspector is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# gitinspector is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with gitinspector. If not, see <http://www.gnu.org/licenses/>.

import blame
import changes
import extensions
import filtering
import getopt
import help
import metrics
import missing
import os
import sys
import terminal
import timeline
import version

class Runner:
	def __init__(self):
		self.hard = False
		self.include_metrics = False
		self.list_file_types = False
		self.repo = "."
		self.tda367 = False
		self.timeline = False
		self.useweeks = False

	def output(self):
		terminal.skip_escapes(not sys.stdout.isatty())
		previous_directory = os.getcwd()
		os.chdir(self.repo)
		changes.output(self.hard)

		if changes.get(self.hard).get_commits():
			blame.output(self.hard)

			if self.timeline:
				timeline.output(changes.get(self.hard), self.useweeks)

			if self.include_metrics:
				metrics.output()

			missing.output()
			filtering.output()

			if self.list_file_types:
				extensions.output()

		os.chdir(previous_directory)

if __name__ == "__main__":
	__run__ = Runner()

	try:
		__opts__, __args__ = getopt.gnu_getopt(sys.argv[1:], "cf:hHlmTwx:", ["checkout-missing", "exclude=", "file-types=",
		                                                     "hard", "help", "list-file-types", "metrics","tda367", "timeline",
		                                                     "version"])
	except getopt.error, msg:
		print sys.argv[0], "\b:", msg
		print "Try `", sys.argv[0], "--help' for more information."
		sys.exit(2)
	for o, a in __opts__:
		if o in("-c", "--checkout-missing"):
			missing.set_checkout_missing(True)
		elif o in("-h", "--help"):
			help.output()
			sys.exit(0)
		elif o in("-f", "--file-types"):
			extensions.define(a)
		elif o in("-H", "--hard"):
			__run__.hard = True
		elif o in("-l", "--list-file-types"):
			__run__.list_file_types = True
		elif o in("-m", "--metrics"):
			__run__.include_metrics = True
		elif o in("--version"):
			version.output()
			sys.exit(0)
		elif o in("--tda367"):
			__run__.include_metrics = True
			__run__.list_file_types = True
			__run__.tda367 = True
			__run__.timeline = True
			__run__.useweeks = True
		elif o in("-T", "--timeline"):
			__run__.timeline = True
		elif o in("-w"):
			__run__.useweeks = True
		elif o in("-x", "--exclude"):
			filtering.add(a)
	for arg in __args__:
		__run__.repo = arg

	__run__.output()
