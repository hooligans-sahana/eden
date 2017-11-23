import aprslib

def callback(packet):
  parsed_packet = aprslib.parse(packet)
  print packet
  if parsed_packet['from'] in aprs_names:
    create_gis_location(parsed_packet)

def create_gis_location(packet):
  track_id =  db(s3db.vehicle_vehicle.aprs_id == packet['from']).select(
    join=db.sit_trackable.on((s3db.vehicle_vehicle.asset_id == s3db.asset_asset.id)
    & (s3db.asset_asset.track_id == s3db.sit_trackable.id))).first().sit_trackable.id
  location_id = s3db.gis_location.insert(lat=packet['latitude'], lon=packet['longitude'])
  print packet
  prsence_id = s3db.sit_presence.insert(timestmp = datetime.datetime.utcnow(),track_id = track_id, location_id = location_id)
  s3db.commit()

AIS = aprslib.IS("pu1rgs", "21942", host="brazil.aprs2.net", port="14579")
aprs_names = [field.aprs_id for field in
  db(s3db.vehicle_vehicle.aprs_id != None).select(s3db.vehicle_vehicle.aprs_id)]
print aprs_names
AIS.connect()
AIS.consumer(callback, raw=True)
