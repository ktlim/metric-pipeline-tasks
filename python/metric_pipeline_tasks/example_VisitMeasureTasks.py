import astropy.units as u
from lsst.pipe.base import Struct, Task
from lsst.pex.config import Config
from lsst.verify import Measurement

#Currently this is a placeholder until additional per-visit measurements are added.
class StarFracTask(Task):
    ConfigClass = Config
    _DefaultName = "starFracTask"

    def run(self, catalog, metric_name):
        self.log.info(f"Measuring {metric_name}")
        if not catalog.isContiguous():
            catalog = catalog.copy(deep=True)
        good_extended = catalog.get('base_ClassificationExtendedness_value')[~catalog.get('base_ClassificationExtendedness_flag')]
        n_gals = sum(good_extended)
        frac = 100*(len(good_extended) - n_gals)/len(good_extended)
        meas = Measurement("starFrac", frac * u.percent)
        return Struct(measurement=meas)