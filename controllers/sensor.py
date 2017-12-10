
def sensor_station():
    return s3_rest_controller(rheader = sensor_station_rheader)

def sensor_station_gis():
    T = current.T
    s3db = current.s3db
    request = current.request
    s3 = current.response.s3
    settings = current.deployment_settings

    # Get default organisation_id
    req_vars = request.vars
    resourcename = "sensor_sensor_station"
    table = s3db.sensor_sensor_station
    # Pre-processor
    def prep(r):
        # Location Filter
        s3db.gis_location_filter(r)

        if r.representation == "plain":
            # Map popups want less clutter
            table.obsolete.readable = False

        elif r.representation == "geojson":
            marker_fn = s3db.get_config("org_office", "marker_fn")
            if marker_fn:
                # Load these models now as they'll be needed when we encode
                mtable = s3db.gis_marker

        return True
    s3.prep = prep


    output = current.rest_controller(resourcename=resourcename)
    return output

def sensor_station_rheader(r, tabs=[]):
    """ Resource Header for sensor station """

    if r.representation == "html":
        record = r.record
        if record:

            T = current.T
            s3db = current.s3db
            s3 = current.response.s3


            tabs = [(T("Sensor station"), None),
                    (T("Registers"), "sensor_station_registry"),
                    ]
            rheader_tabs = s3_rheader_tabs(r, tabs)

            table = r.table
            ltable = s3db.asset_log
            rheader = DIV(TABLE(TR(TH("%s: " % table.description.label),
                                   record.description,
                                   TH("%s: " % table.aprs_id.label),
                                   table.aprs_id)
                                ),
                          rheader_tabs)
            return rheader
    return None
