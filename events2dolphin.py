"""
events2dolphin - Converts a "CTS Start list" set of files from Hy-Tek Meet
Manager into an event list for the CTS Dolphin system.
"""

# events2dolphin - https://github.com/JohnStrunk/events2dolphin
# Copyright (C) 2020 - John D. Strunk
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import copy
import re
import sys
from typing import List, NamedTuple, NoReturn, Optional, Tuple

class Event(NamedTuple):
    """
    Event represents a swimming event.
    """
    event_number: int
    event_name: str
    num_heats: int

def filename(path: str) -> str:
    """
    Return just the filename from a full pathname.

    Examples:
    >>> filename("/my/full/path.name")
    'path.name'
    """
    m = re.match(r"^.*[\\/]([^\\/]+)$", path)
    if m:
        return m.group(1)
    return ""

def key_exit(rc: int) -> NoReturn:
    input("Press RETURN to exit...")
    sys.exit(rc)

def usage() -> None:
    print(
        f"""
        Usage:
        {filename(sys.argv[0])} <file1.scb> ...

        This program converts CTS scoreboard start lists into a CSV file of
        events for the CTS Dolphin software.

        Instructions:
        1) Export a start list for CTS scoreboards.
           - In Hy-Tek Meet Manager, go to:
             File > Export > Start Lists for Scoreboard > Start Lists for CTS
           - Choose an output folder and the desired session.
           - This will write a set of *.scb files to the chosen directory,
             one per event in the session.
        2) Use this program to generate the Dolphin event CSV.
           - Open the folder from above and select all the *.scb files.
           - Drag the files (all at once) onto this executable.
           - This program will write a file: dolphin_events_X-Y.csv,
             where X and Y are the first and last event numbers.
        3) Load the CSV into the Dolphin software.
           - In the Dolphin software, go to the Events screen.
           - Click Load, and select the CSV from above
           - The events should appear in the table, with the name, number,
             and number of heats.
        """
    )

def parse_scb_header(header: str) -> Optional[Tuple[int, str]]:
    """
    >>> parse_scb_header("#113 GIRLS 13&O 100 BREAST")
    (113, 'GIRLS 13&O 100 BREAST')
    """
    match = re.match(r"^#(\w+)\s+(.*)$", header)
    if match:
        event_num = match.group(1)
        name = match.group(2)
        return (int(event_num), name)
    return None


def parse_scb(path: str) -> List[Event]:
    """
    Parses the contents of a CTS start list file into an Event structure.

    Parameters:
      path: String containing the full path to a ".scb" strt list file

    Returns:
      An Event corresponding to the start list file
    """
    scb = open(path, "r", encoding="utf-8", errors="ignore")
    lines = scb.readlines()
    scb.close()
    if (len(lines)-1) % 10:
        print(f"Unexpected number of lines in file: {filename}")
        return []
    heats = (len(lines)-1)//10
    header = parse_scb_header(lines[0])
    if header is None:
        print(f"Unable to parse header in file: {filename}")
        return []
    (event_num, name) = header
    return [Event(event_num, name, heats)]

def print_event_table(events: List[Event]) -> None:
    print()
    print(f"| {'Event #':>7} | {'Event name':<25} | {'Heats':>5} |")
    print("-"*(10 + 7 + 25 + 5))
    for e in events:
        print(f"| {e.event_number:>7} | {e.event_name:<25} | {e.num_heats:>5} |")
    print()

def eventlist_to_csv(events: List[Event]) -> List[str]:
    lines: List[str] = []
    for e in events:
        lines.append(f"{e.event_number},{e.event_name},{e.num_heats},1,A\n")
    return lines

def main():
    """This is the main function."""
    if len(sys.argv) < 2:
        usage()
        key_exit(1)

    files = copy.deepcopy(sys.argv)
    files.pop(0)

    events: List[Event] = []
    for f in files:
        events += parse_scb(f)

    events.sort(key=lambda e: e.event_number)
    print_event_table(events)

    csv_lines = eventlist_to_csv(events)
    outfile = f"dolphin_events_{events[0].event_number}-{events[-1].event_number}.csv"
    csv = open(outfile, "w")
    csv.writelines(csv_lines)
    csv.close()
    print(f"Wrote events to: {outfile}")
    key_exit(0)

if __name__ == "__main__":
    main()
