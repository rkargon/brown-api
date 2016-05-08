#!/usr/bin/python

import argparse
from datetime import datetime
import re

from brown_api import BrownAPISession

# TODO move this to ~/.brownrc or something...
CLIENT_ID = "7574545c-6b5f-4ea9-8c20-999910e90171"


def main(service_type, laundry_room=None):
    """
    Display information about Brown's laundry or dining services.
    :param service_type: either "laundry" or "dining"
    :param laundry_room: A pattern to match to the name of a laundry room.
    """
    sess = BrownAPISession(client_id=CLIENT_ID)

    # TODO test unavailable machines
    if service_type == "laundry":
        laundry_service(sess, laundry_room)
    elif service_type == "dining":
        print sess.get_dining_menu(sess.RATTY), "\n"
        print sess.get_dining_hours(sess.VDUB), "\n"
        print sess.find_food("scrambled"), "\n"
        pass


def laundry_service(session, laundry_room=None):
    """
    Print the status of laundry machines in a set of rooms whose names match a certain pattern
    :param session: A BrownAPISession object to connect to the Brown API.
    :param laundry_room: A piece of text that should match to a set of rooms. Case Insensitive, no regexes / wildcards.
    e.g. "hark" would match to rooms in Harkness House.
    """
    all_rooms = session.list_laundry_rooms()['results']
    if laundry_room is not None:
        matched_rooms = filter(lambda r: re.search(re.escape(laundry_room), r['name'], re.IGNORECASE), all_rooms)
    else:
        matched_rooms = all_rooms

    # prompt the user to continue if more than 10 rooms are matched, to prevent excessive requests.
    if len(matched_rooms) > 10:
        conf = raw_input("You're getting data for more than 10 rooms. Continue? [y/n]: ")
        if conf != "y":
            return

    for r in matched_rooms:
        print "Room:", r['name']
        machines = session.list_laundry_machines(r['id'], get_status=True)['results']
        machines.sort(key=lambda m: int(m['id']))
        for m in machines:
            print_machine_info(m)
        print


def print_machine_info(m):
    """
    Print the status of a specific laundry machine.
    The output is: "<ID>. <TYPE>: <AVAILABILITY/TIME REMAINING> <MESSAGE, IF ANY>"
    :param m: JSON representing an individual laundry machine, returned by the Brown API
    """
    type_str = BrownAPISession.get_laundry_machine_nicename(m['type'])
    avail_str = "AVAILABLE" if m['avail'] else "%d mins remaining" % m['time_remaining']
 
    msg_str = "(%s)" % m['message'] if m['message'] is not None else ""
    print "%d. %s: %s %s" % (int(m['id']), type_str, avail_str, msg_str)


if __name__ == '__main__':
    """
    Parse command line arguments, and execute corresponding commands
    """

    parser = argparse.ArgumentParser(description='A set of tools using the Brown API')
    parser.add_argument("service", choices=["dining", "laundry"], help="the type of service requested.")
    parser.add_argument("-r", "--room", help="string used to match to the name of a laundry room.")
    args = parser.parse_args()

    main(service_type=args.service, laundry_room=args.room)
