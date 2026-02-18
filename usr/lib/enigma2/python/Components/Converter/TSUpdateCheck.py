# -*- coding: utf-8 -*-
from Components.Converter.Converter import Converter
from Components.Element import cached
from Components.config import config

class TSUpdateCheck(Converter, object):
    """
    Converter for showing whether updates are available and/or how many.
    Safe against missing config.plugins.TSUpdater.* keys.
    Usage in skin:
        <converter type="TSUpdateCheck">PackageCount</converter>
    """
    PKGCOUNT = 0

    def __init__(self, type):
        Converter.__init__(self, type)
        # Normalize type (keep only "PackageCount" for now)
        self.type = self.PKGCOUNT if str(type).lower() == 'packagecount' else self.PKGCOUNT

    # --------- helpers ---------
    def _updates_available_value(self, default=0):
        """
        Safely read config.plugins.TSUpdater.UpdateAvailable.value as int.
        Returns 'default' if any part is missing or invalid.
        """
        try:
            return int(getattr(getattr(config.plugins, 'TSUpdater'), 'UpdateAvailable').value)
        except Exception:
            return default

    # --------- boolean property (for ConditionalRenderers etc.) ---------
    @cached
    def getBoolean(self):
        val = self._updates_available_value(0)
        return True if val > 0 else False

    boolean = property(getBoolean)

    # --------- text property (for Labels etc.) ---------
    @cached
    def getText(self):
        if self.type == self.PKGCOUNT:
            val = self._updates_available_value(0)
            if val > 0:
                return '%d' % val
        return ''

    text = property(getText)
