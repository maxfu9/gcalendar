# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"module_name": "Gcalendar",
			"color": "#f5f5f5",
			"icon": "octicon octicon-git-compare",
			"type": "module",
			"label": _("Google Calendar")
		}
	]
