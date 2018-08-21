#!/usr/bin/env python3

import sys
import dateutil.parser as dp
#from lxml import etree as et
import xml.etree.ElementTree as et
sys.path.append('.')

from logger.utils import formats
from logger.utils import das_record
from logger.transforms.transform import Transform

#####################################################################
class ParseXMLTransform(Transform):
    """foo."""

    def __init__(self):
        pass

    def transform(self, xmlRecord):
        """Parse the SUDS XML Datagram into openRVDAS DASRecord."""
        tree = et.fromstring(xmlRecord)
        if tree is None:
            return None

        else:
            # Get the Board element attributes
            for elem in tree.iterfind("Board"):
                ATTRIBS = elem.attrib
                INDEX = ATTRIBS["Index"]
                STATUS = ATTRIBS["Status"]
                LOCATION = ATTRIBS["Location"]
                MAC = ATTRIBS["MAC"]
                IP = ATTRIBS["IP"]
                FIRMWARE = ATTRIBS["FirmwareRev"]
                CHANNEL = ATTRIBS["Channel"]

            # Get the Device element attributes
            for elem in tree.iterfind("Device"):
                ATTRIBS = elem.attrib
                NAME = ATTRIBS["Name"]
                MAKE = ATTRIBS["Make"]
                MODEL = ATTRIBS["Model"]

            # Get the Start Date and Time and format as float
            for elem in tree.iterfind("Data/Timestamp/Finish/Date"):
                startDATE = elem.text

            for elem in tree.iterfind("Data/Timestamp/Finish/Time"):
                startTIME = elem.text

            ISO8601string = startDATE+'T'+startTIME+'Z'
            EPOCHtime = int(dp.parse(ISO8601string).strftime('%s'))

            # Get the Signal Values (this is probably all we really needed..)
            for elem in tree.iterfind("Data/Signal"):
                ATTRIBS = elem.attrib
                SIGNAL = elem.text

            signal_data = SIGNAL.encode('ascii', 'ignore')

            dRecord = das_record.DASRecord(data_id=NAME,
                                           message_type='OSU_SUDS',
                                           timestamp=EPOCHtime,
                                           fields={"SIGNAL": SIGNAL},
                                           metadata={"MAKE":MAKE, "MODEL":MODEL})
            # return signal_data
            return dRecord
