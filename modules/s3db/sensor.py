# -*- coding: utf-8 -*-
"""
This is just a commented template to copy/paste from when implementing
new models. Be sure you replace this docstring by something more
appropriate, e.g. a short module description and a license statement.

The module prefix is the same as the filename (without the ".py"), in this
case "skeleton". Remember to always add an import statement for your module
to:

models/00_tables.py

like:

import eden.skeleton

(Yeah - not this one of course :P it's just an example)
"""

# mandatory __all__ statement:
#
# - all classes in the name list will be initialized with the
#   module prefix as only parameter. Subclasses of S3Model
#   support this automatically, and run the model() method
#   if the module is enabled in deployment_settings, otherwise
#   the default() method.
#
# - all other names in the name list will be added to response.s3
#   if their names start with the module prefix plus underscore
#
__all__ = ("S3SensorModel",
          )

# The following import statements are needed in almost every model
# (you may need more than this in your particular case). To
# import classes from s3, use from + relative path like below
#
import json

from gluon import *

from ..s3 import *
from s3dal import Row
from s3layouts import S3PopupLink

# =============================================================================
# Define a new class as subclass of S3Model
# => you can define multiple of these classes within the same module, each
#    of them will be initialized only when one of the declared names gets
#    requested from s3db
# => remember to list all model classes in __all__, otherwise they won't ever
#    be loaded.
#
class S3SensorModel(S3Model):

    # Declare all the names this model can auto-load, i.e. all tablenames
    # and all response.s3 names which are defined here. If you omit the "names"
    # variable, then this class will serve as a fallback model for this module
    # in case a requested name cannot be found in one of the other model classes
    #
    names = ("sensor_sensor_station",
    "sensor_registry",
    # "sensor_property"
    )

    # Define a function model() which takes no parameters (except self):
    def model(self):

        # You will most likely need (at least) these:
        db = current.db
        T = current.T
        s3db = current.s3db
        location_id = self.gis_location_id

        # This one may be useful:
        settings = current.deployment_settings
        crud_strings = current.response.s3.crud_strings
        # define_table = self.define_table
        # float_represent = IS_FLOAT_AMOUNT.represent
        # int_represent = IS_INT_AMOUNT.represent


        # Now define your table(s),
        # -> always use self.define_table instead of db.define_table, this
        #    makes sure the table won't be re-defined if it's already in db
        # -> use s3_meta_fields to include meta fields (not s3_meta_fields!),
        #    of course this needs the s3 assignment above
        tablename = "sensor_sensor_station"
        self.define_table(tablename,
        # super_link("track_id", "sit_trackable"),
        Field("description",
        notnull=True,
        label = T("Description"),
        ),
        Field("aprs_id",
        notnull=False,
        label = T("APRS ID"),
        ),
        location_id(
        widget = S3LocationSelector(show_address = False,
        show_postcode = False,
        show_latlon = True,
        ),
        ),
        s3_comments(),
        *s3_meta_fields())

        represent = S3Represent(lookup=tablename,
            fields=["description"],
            translate=True)
        sensor_sensor_station_id = S3ReusableField("sensor_sensor_station_id", "reference %s" % tablename,
            label = T("sensor_sensor_station"),
            ondelete = "RESTRICT",
            represent = represent,
            requires = IS_EMPTY_OR(
            IS_ONE_OF(db,
            "sensor_sensor_station.id",
            represent,)),
        )

        crud_strings[tablename] = Storage(
        label_create = T("Create Sensor Station"),
        title_display = T("Sensor Station Details"),
        title_list = T("Sensor Stations"),
        title_update = T("Edit Sensor Station"),
        title_upload = T("Import Sensor Stations"),
        label_list_button = T("List Sensor Stations"),
        label_delete_button = T("Delete Sensor Station"),
        msg_record_created = T("Sensor Station added"),
        msg_record_modified = T("Sensor Station updated"),
        msg_record_deleted = T("Sensor Station removed"),
        msg_list_empty = T("No Sensor Stations currently registered")
        )

        self.configure(tablename,
        context = {"location": "sensor_sensor_station_id$location_id"},
        )

        tablename = "sensor_sensor_station_registry"
        self.define_table(tablename,
        sensor_sensor_station_id(),
        location_id(
        widget = S3LocationSelector(show_address = False,
        show_postcode = False,
        show_latlon = True,
        )),
        s3_comments(),
        *s3_meta_fields())

        type_represent = S3Represent(lookup=tablename,
            fields=["created_on"],
            translate=True)
        s3db.add_components("sensor_sensor_station",
                    sensor_sensor_station_registry = "sensor_sensor_station_id")

        return dict(sensor_sensor_station_id = sensor_sensor_station_id,)


    # def sensor_represent(id):
    #
    #     if not id:
    #         # Don't do a DB lookup if we have no id
    #         # Instead return a consistenct representation of a null value
    #         return current.messages["NONE"]
    #
    #     # Your function may need to access tables. If a table isn't defined
    #     # at the point when this function gets called, then this:
    #     s3db = current.s3db
    #     table = s3db.sensor_table
    #     # will load the table. This is the same function as self.table described in
    #     # the model class except that "self" is not available here, so you need to
    #     # use the class instance as reference instead
    #
    #     db = current.db
    #     query = (table.id == id)
    #     record = db(query).select(table.name,
    #     limitby=(0, 1)).first()
    #     try:
    #         # Try faster than If for the common case where it works
    #         return record.name
    #     except:
    #     # Data inconsistency error!
    #         return current.messages.UNKNOWN_OPT

    # END =========================================================================
