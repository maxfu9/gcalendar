# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "gcalendar"
app_title = "Gcalendar"
app_publisher = "DOKOS"
app_description = "Google Calendar Integration"
app_icon = "octicon octicon-git-compare"
app_color = "#f5f5f5"
app_email = "hello@dokos.io"
app_license = "GPLv3"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/gcalendar/css/gcalendar.css"
# app_include_js = "/assets/gcalendar/js/gcalendar.js"

# include js, css files in header of web template
# web_include_css = "/assets/gcalendar/css/gcalendar.css"
# web_include_js = "/assets/gcalendar/js/gcalendar.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "gcalendar.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "gcalendar.install.before_install"
# after_install = "gcalendar.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "gcalendar.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

scheduler_events = {
	"all": [
		"gcalendar.gcalendar.doctype.gcalendar_settings.gcalendar_settings.sync"
	],
# 	"daily": [
# 		"gcalendar.tasks.daily"
# 	],
# 	"hourly": [
# 		"gcalendar.tasks.hourly"
# 	],
# 	"weekly": [
# 		"gcalendar.tasks.weekly"
# 	]
# 	"monthly": [
# 		"gcalendar.tasks.monthly"
# 	]
}

# Testing
# -------

# before_tests = "gcalendar.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "gcalendar.event.get_events"
# }
