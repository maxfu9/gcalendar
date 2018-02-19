#!/usr/bin/env python
# -*- coding: utf-8 -*-
import frappe

def pre_process(events):
	event = {
		'summary': events["summary"],
		'start_datetime': events["start"]["dateTime"],
		'end_datetime': events["end"]["dateTime"]
	}

	if 'description' in events:
		event.update({'description': events["description"]})
	else:
		event.update({'description': ""})
	return event
