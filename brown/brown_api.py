#!/usr/bin/python
import json

import urllib2


class BrownAPISession:
    # TODO error handling

    ROOT_URL = "https://api.students.brown.edu"
    LAUNDRY_URL = ROOT_URL + "/laundry/rooms"
    DINING_URL = ROOT_URL + "/dining"

    def __init__(self, client_id):
        """
        Create a Brown API Session with a certain client ID
        :param client_id: THe given client ID
        """
        self.client_id = client_id

    # RAW API #

    # Dining

    # names of possible eateries
    RATTY = "ratty"
    VDUB = "vdub"
    EATERIES = [RATTY, VDUB]

    def get_dining_menu(self, eatery, dt=None):
        url = self.DINING_URL + "/menu"
        if dt is not None:
            return self.get_json_from_url(url, eatery=eatery, year=dt.year, month=dt.month, hour=dt.hour,
                                          minute=dt.minute)
        else:
            return self.get_json_from_url(url, eatery=eatery)

    def get_dining_hours(self, eatery, dt=None):
        url = self.DINING_URL + "/hours"
        if dt is not None:
            return self.get_json_from_url(url, eatery=eatery, year=dt.year, month=dt.month)
        else:
            return self.get_json_from_url(url, eatery=eatery)

    def find_food(self, food):
        url = self.DINING_URL + "/find"
        return self.get_json_from_url(url, food=urllib2.quote(food, safe=''))

    def find_open_eateries(self, dt=None):
        url = self.DINING_URL + "/open"
        if dt is not None:
            return self.get_json_from_url(url, year=dt.year, month=dt.month, hour=dt.hour,
                                          minute=dt.minute)
        else:
            return self.get_json_from_url(url)

    def find_all_food_ever_served(self, eatery):
        url = self.DINING_URL + "/all_food"
        return self.get_json_from_url(url, eatery=eatery)

    # Laundry

    # names for types of machines in the laundry services.
    CARD_READER = "Card Reader"
    DRYER = "Dryer"
    SINK = "Sink"
    WASHER = "Washer"
    WASHER_N_DRYER = "Washer & Dryer"
    LAUNDRY_MACHINE_TYPES = {
        '1cardReader': CARD_READER,
        '1dblDry': DRYER,
        '1sink': SINK,
        'cardReader': CARD_READER,
        'dblDry': DRYER,
        'dry': DRYER,
        'sink': SINK,
        'tableSm': "tableSm",  # what is this?
        'washFL': WASHER,
        'washNdry': WASHER_N_DRYER,
    }

    def list_laundry_rooms(self):
        return self.get_json_from_url(BrownAPISession.LAUNDRY_URL)

    def get_laundry_room_details(self, room_id):
        url = self.LAUNDRY_URL + "/%s" % room_id
        return self.get_json_from_url(url)

    def list_laundry_machines(self, room_id, get_status=False):
        url = self.LAUNDRY_URL + "/%s/machines" % room_id
        return self.get_json_from_url(url, get_status=get_status)

    def get_laundry_machine_details(self, room_id, machine_id, get_status=False):
        url = self.LAUNDRY_URL + "/%s/machines/%s" % (room_id, machine_id)
        return self.get_json_from_url(url, get_status=get_status)

    @staticmethod
    def get_laundry_machine_nicename(machine_type):
        return BrownAPISession.LAUNDRY_MACHINE_TYPES.get(machine_type, machine_type)

    def get_json_from_url(self, url, **kwargs):
        # build URL
        url = self.add_client_id(url)
        for name, value in kwargs.iteritems():
            if type(value) == bool and not value:
                continue
            else:
                url += "&%s=%s" % (name, value)

        # get JSON response from the URL
        url_obj = urllib2.urlopen(url)
        data = json.load(url_obj)
        url_obj.close()
        return data

    def add_client_id(self, url):
        return url + "?client_id=" + self.client_id
