import gdp
# Input/output class. Identifies the gcl_name and parameter_name for each input or output.
class ioClass(object):
    def __init__(self, nameStr = "", paramName = "", lagVal = 0):
        if nameStr == "":
            raise ValueError ("GCL name must be provided.")
        if paramName == "":
            raise ValueError ("JSON parameter name must be provided.")
        # Log name in GDP
        self.gclName = gdp.GDP_NAME(nameStr)
        # Assume that GCL already exists and create the GCL handle
        self.gclHandle = gdp.GDP_GCL(self.gclName, gdp.GDP_MODE_RO)
        # JSON parameter name to be used in each log record
        self.param = paramName
        # Lag from the current record. Can be used to implement time series functions.
        self.lag = lagVal

    def printTester(self):
        print self.gcl, self.param, self.lag
