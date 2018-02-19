# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Google Calendar"),
			"items": [
				{
					"type": "doctype",
					"name": "GCalendar Settings",
					"description": _("Google Calendar Settings"),
				},
				{
					"type": "doctype",
					"name": "GCalendar Account",
					"description": _("Google Calendar Account"),
				}
				]
		}
	]
