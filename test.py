#!/usr/bin/python3
#
# Bahnhofsfotos Fotoverfügbarkeit Test
# Pieter Hollants <pieter@hollants.com>
#
# Aufruf:
#   test.py de >de.csv
#   test.py cz >cz.csv
#   test.py uk >uk.csv
#   ...
#

import argparse, csv, requests, sys

parser = argparse.ArgumentParser(description="Bahnhofsfotos Fotoverfügbarkeit Test")
parser.add_argument("land", help="Zweibuchstabenkürzel des Landes, dessen Bahnhöfe überprüft werden sollen")
args = parser.parse_args()

print(f"Hole alle Bahnhöfe für {args.land} von der API...", file=sys.stderr)

r = requests.get(f"https://api.railway-stations.org/{args.land}/stations")
r.raise_for_status()

stations = sorted(r.json(), key=lambda item: str(item['id']) + ' ' + item['title'])
num_stations = len(stations)

csvwriter = csv.writer(sys.stdout)

for current_station, station in enumerate(stations, start=1):
	print(f"\rPrüfe Fotoverfügbarkeit für Bahnhof {current_station}/{num_stations}...", end="", file=sys.stderr, flush=True)
	if station["photoUrl"]:
		r = requests.get(station["photoUrl"])
		if r.status_code != 200:
			csvwriter.writerow((station["id"], station["title"], station["photoUrl"], r.status_code))
