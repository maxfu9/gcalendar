from __future__ import unicode_literals
import frappe
from frappe.data_migration.doctype.data_migration_connector.connectors.base import BaseConnection
import googleapiclient.discovery
import google.oauth2.credentials
from googleapiclient.errors import HttpError
import time
from datetime import datetime
import pytz

class CalendarConnector(BaseConnection):
	def __init__(self, connector):
		self.connector = connector
		settings = frappe.get_doc("GCalendar Settings", None)

		self.account = frappe.get_doc("GCalendar Account", "chdecultot@dokos.io")

		self.credentials_dict = {
			'token': self.account.get_password(fieldname='session_token', raise_exception=False),
			'refresh_token': self.account.get_password(fieldname='refresh_token', raise_exception=False),
			'token_uri': 'https://www.googleapis.com/oauth2/v4/token',
			'client_id': settings.client_id,
			'client_secret': settings.get_password(fieldname='client_secret', raise_exception=False),
			'scopes':'https://www.googleapis.com/auth/calendar'
			}

		self.name_field = 'id'

		self.credentials = google.oauth2.credentials.Credentials(**self.credentials_dict)
		self.gcalendar = googleapiclient.discovery.build('calendar', 'v3', credentials=self.credentials)

		self.check_remote_calendar()

	def check_remote_calendar(self):
		def _create_calendar():
			calendar = {
				'summary': self.account.calendar_name,
				'timeZone': 'Europe/Paris'
			}
			try:
				created_calendar = self.gcalendar.calendars().insert(body=calendar).execute()
				frappe.db.set_value("GCalendar Account", self.account.name, "gcalendar_id", created_calendar["id"])
			except Exception:
				frappe.log_error(frappe.get_traceback())
		try:
			if self.account.gcalendar_id is not None:
				calendar = self.gcalendar.calendars().get(calendarId=self.account.gcalendar_id).execute()
			else:
				_create_calendar()
		except HttpError as err:
			if err.resp.status in [403, 500, 503]:
				time.sleep(5)
			elif err.resp.status in [404]:
				_create_calendar()
			else: raise


	def get(self, remote_objectname, fields=None, filters=None, start=0, page_length=10):
		return self.get_events(remote_objectname, filters, page_length)

	def insert(self, doctype, doc):
		if doctype == 'Events':
			if doc["start_datetime"] >= datetime.now():
				try:
					doctype = "Event"
					return self.insert_events(doctype, doc)
				except Exception:
					frappe.log_error(frappe.get_traceback(), "GCalendar Synchronization Error")


	def update(self, doctype, doc, migration_id):
		if doctype == 'Events':
			if doc["start_datetime"] >= datetime.now():
				try:
					doctype = "Event"
					return self.update_events(doctype, doc, migration_id)
				except Exception:
					frappe.log_error(frappe.get_traceback(), "GCalendar Synchronization Error")

	def delete(self, doctype, migration_id):
		if doctype == 'Events':
			try:
				return self.delete_events(migration_id)
			except Exception:
				frappe.log_error(frappe.get_traceback(), "GCalendar Synchronization Error")

	def get_events(self, remote_objectname, filters, page_length):
		page_token = None
		results = []
		while True:
			events = self.gcalendar.events().list(calendarId=self.account.gcalendar_id, maxResults=page_length, singleEvents=True, orderBy='startTime').execute()
			for event in events['items']:
				results.append(event)

		 	page_token = events.get('nextPageToken')
			if not page_token:
				break
		return list(results)

	def insert_events(self, doctype, doc):
		event = {
			'summary': doc.summary,
			'description': doc.description
		}

		dates = self.return_dates(doc)
		event.update(dates)

		if doc.repeat_this_event != 0:
			recurrence = self.return_recurrence(doctype, doc)
			if not not recurrence:
				event.update({"recurrence": ["RRULE:" + str(recurrence)]})

		try:
			remote_event = self.gcalendar.events().insert(calendarId=self.account.gcalendar_id, body=event).execute()
			return {self.name_field: remote_event["id"]}
		except Exception:
			frappe.log_error(frappe.get_traceback(), "GCalendar Synchronization Error")

	def update_events(self, doctype, doc, migration_id):
		event = self.gcalendar.events().get(calendarId=self.account.gcalendar_id, eventId=migration_id).execute()
		event = {
			'summary': doc.summary,
			'description': doc.description
		}

		if doc.event_type == "Cancel":
			event.update({"status": "cancelled"})

		dates = self.return_dates(doc)
		event.update(dates)

		if doc.repeat_this_event != 0:
			recurrence = self.return_recurrence(doctype, doc)
			if not not recurrence:
				event.update({"recurrence": ["RRULE:" + str(recurrence)]})

		try:
			updated_event = self.gcalendar.events().update(calendarId=self.account.gcalendar_id, eventId=migration_id, body=event).execute()
			return {self.name_field: updated_event["id"]}
		except Exception as e:
			frappe.log_error(e, "GCalendar Synchronization Error")

	def delete_events(self, migration_id):
		try:
			self.gcalendar.events().delete(calendarId=self.account.gcalendar_id, eventId=migration_id).execute()
		except HttpError as err:
			if err.resp.status in [410]:
				pass

	def return_dates(self, doc):
		timezone = frappe.db.get_value("System Settings", None, "time_zone")
		tz = pytz.timezone(timezone)
		if doc.all_day == 1:
			return {
						'start': {
							'date': doc.start_datetime.date().isoformat(),
							'timeZone': timezone,
						},
						'end': {
							'date': doc.start_datetime.date().isoformat(),
							'timeZone': timezone,
						}
					}
		else:
			return {
						'start': {
							'dateTime': doc.start_datetime.isoformat(),
							'timeZone': timezone,
						},
						'end': {
							'dateTime': doc.end_datetime.isoformat(),
							'timeZone': timezone,
						}
					}

	def return_recurrence(self, doctype, doc):
		#TODO: Ajust recurrence for special dates
		e = frappe.get_doc(doctype, doc.name)
		if e.repeat_till is not None:
			timezone = frappe.db.get_value("System Settings", None, "time_zone")
			end_date = datetime.combine(e.repeat_till, datetime.min.time()).strftime('UNTIL=%Y%m%dT%H%M%SZ')
		else:
			end_date = None

		day = []
		if e.repeat_on == "Every Day":
			if e.monday is not None:
				day.append("MO")
			if e.tuesday is not None:
				day.append("TU")
			if e.wednesday is not None:
				day.append("WE")
			if e.thursday is not None:
				day.append("TH")
			if e.friday is not None:
				day.append("FR")
			if e.saturday is not None:
				day.append("SA")
			if e.sunday is not None:
				day.append("SU")

			day = "BYDAY=" + ",".join(str(d) for d in day)
			frequency = "FREQ=DAILY"

		elif e.repeat_on == "Every Week":
			frequency = "FREQ=WEEKLY"
		elif e.repeat_on == "Every Month":
			frequency = "FREQ=MONTHLY"
		elif e.repeat_on == "Every Year":
			frequency = "FREQ=YEARLY"
		else:
			return None

		wst = "WKST=SU"

		elements = [frequency, end_date, wst, day]

		return ";".join(str(e) for e in elements if e is not None and not not e)
