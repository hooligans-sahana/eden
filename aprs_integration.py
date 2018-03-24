import aprslib

def callback(packet):
    parsed_packet = aprslib.parse(packet)
    print packet
    if parsed_packet['from'] in aprs_names:
        create_gis_location(parsed_packet)

def create_gis_location(packet):
    if packet.has_key('weather'):
        print "============================================="
        sensor_station = db(s3db.sensor_sensor_station.aprs_id == packet['from']).select().first()
        sensor_station_location = db(s3db.gis_location.id == sensor_station.location_id).select().first()
        sensor_station_location.update_record(lat=packet['latitude'], lon=packet['longitude'])
        location = s3db.gis_location.insert(lat=packet['latitude'], lon=packet['longitude'])
        registry = s3db.sensor_sensor_station_registry.insert(location_id = location.id,
        sensor_sensor_station_id = sensor_station.id)
        for name, value in packet['weather'].items():
            s3db.sensor_property.insert(sensor_sensor_station_registry_id=registry.id,name=name, value=value)
    else:
        track_id =  db(s3db.vehicle_vehicle.aprs_id == packet['from']).select(
        join=db.sit_trackable.on((s3db.vehicle_vehicle.asset_id == s3db.asset_asset.id)
        & (s3db.asset_asset.track_id == s3db.sit_trackable.id))).first().sit_trackable.id
        location_id = s3db.gis_location.insert(lat=packet['latitude'], lon=packet['longitude'])
        print packet
        prsence_id = s3db.sit_presence.insert(timestmp = datetime.datetime.utcnow(),track_id = track_id, location_id = location_id)
    s3db.commit()

AIS = aprslib.IS("pu1rgs", "21942", host="brazil.aprs2.net", port="14579")
aprs_names = [field.aprs_id for field in
list(db(s3db.vehicle_vehicle.aprs_id != None).select(s3db.vehicle_vehicle.aprs_id)) + list(db(s3db.sensor_sensor_station.aprs_id != None).select(s3db.sensor_sensor_station.aprs_id)) ]
print aprs_names
AIS.connect()
AIS.consumer(callback, raw=True)
