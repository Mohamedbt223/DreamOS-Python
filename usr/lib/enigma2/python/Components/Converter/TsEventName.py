# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Components/Converter/TsEventName.py
# Compiled at: 2025-09-18 09:39:02
import logging
from Components.Converter.Converter import Converter
from Components.Element import cached
from enigma import eTimer
from twisted.internet.threads import deferToThread
from twisted.internet import reactor

def setup_logging():
    logger = logging.getLogger('Event_translator')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler('/tmp/evnt_translater.log')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


logger = setup_logging()
try:
    from Plugins.Extensions.EPGTranslatorLite.plugin import translatorMain
    EPG_TRANSLATOR_AVAILABLE = True
    logger.debug('EPGTranslatorLite plugin detected.')
except ImportError:
    EPG_TRANSLATOR_AVAILABLE = False
    logger.debug('EPGTranslatorLite plugin not found.')

class TsEventName(Converter, object):
    NAME = 0
    SHORT_DESCRIPTION = 1
    EXTENDED_DESCRIPTION = 2
    FULL_DESCRIPTION = 3
    ID = 4
    EventName = 5

    def __init__(self, type, session=None):
        Converter.__init__(self, type)
        self.session = session
        self._logged_no_event = False
        self._updating = False
        self._translations = {}
        self._invalidate_timer = eTimer()
        self._invalidate_timer.timeout.connect(self._invalidate)
        if type == 'Description':
            self.type = self.SHORT_DESCRIPTION
        elif type == 'ExtendedDescription':
            self.type = self.EXTENDED_DESCRIPTION
        elif type == 'FullDescription':
            self.type = self.FULL_DESCRIPTION
        elif type == 'ID':
            self.type = self.ID
        elif type == 'EventName':
            self.type = self.NAME
        else:
            self.type = self.NAME
        logger.debug('Initialized EventNameOstende with type: %s', type)
        return

    @cached
    def getText(self):
        event = self.source.event
        if event is None:
            if not self._logged_no_event:
                logger.debug('No event source found.')
                self._logged_no_event = True
            return ''
        event_id = event.getEventId()
        if self.type == self.NAME:
            return event.getEventName()
        else:
            if self.type == self.SHORT_DESCRIPTION:
                return self._getOrTranslate(event.getShortDescription(), event_id)
            else:
                if self.type == self.EXTENDED_DESCRIPTION:
                    return self._getOrTranslate(event.getExtendedDescription(), event_id)
                if self.type == self.FULL_DESCRIPTION:
                    short = event.getShortDescription()
                    extended = event.getExtendedDescription()
                    if event_id not in self._translations:
                        logger.debug('Starting full translation for event ID %s', event_id)
                        self._startTranslation(full=True, short=short, extended=extended, event_id=event_id)
                        return short or extended or ''
                    return self._translations.get(event_id, '')
                if self.type == self.ID:
                    return str(event_id)
                return

            return

    def _getOrTranslate(self, text, event_id):
        if not text:
            return ''
        if event_id not in self._translations and not self._updating:
            logger.debug('Starting translation for event ID %s', event_id)
            self._startTranslation(text=text, event_id=event_id)
        return self._translations.get(event_id, text)

    def _startTranslation(self, text=None, full=False, short=None, extended=None, event_id=None):
        if EPG_TRANSLATOR_AVAILABLE and event_id is not None:
            self._updating = True
            if full:
                deferToThread(self._translateFull, short, extended, event_id)
            else:
                deferToThread(self._translateText, text, event_id)
        else:
            logger.debug('Translation skipped: EPGTranslator not available or event_id is None')
        return

    def _translateText(self, text, event_id):
        RTL = '\\u202b'
        PDF = '\\u202c'
        try:
            try:
                logger.debug('Translating text for event ID %s: %s', event_id, text)
                event_info = (None, '', '', text, '', '', '', '')
                translator = translatorMain(text, event_info)
                translator.translateEPG(text)
                result = translator['text2'].getText().strip()
                lines = [line.strip() for line in result.splitlines() if line.strip()]
                result = ('\n').join(reversed(lines))
                result = RTL + result + PDF
                result = result.encode('utf-8')
                logger.debug('Translation result for event ID %s: %s', event_id, result)
                self._translations[event_id] = result
            except Exception as e:
                logger.error('Error translating event ID %s: %s', event_id, str(e))

        finally:
            self._updating = False
            reactor.callFromThread(self._invalidate)

        return

    def _translateFull(self, short, extended, event_id):
        RTL = '\\u202b'
        PDF = '\\u202c'
        try:
            try:
                logger.debug('Translating full description for event ID %s', event_id)
                translated_short = self._translateInline(short).strip()
                translated_extended = self._translateInline(extended).strip()
                result = ('{}\n\n{}').format(translated_short, translated_extended).strip()
                result = ('\n').join(line.strip() for line in result.splitlines() if line.strip())
                result = RTL + result + PDF
                result = result.encode('utf-8')
                logger.debug('Full translation result for event ID %s:\n%s', event_id, result)
                self._translations[event_id] = result
            except Exception as e:
                logger.error('Error in full translation for event ID %s: %s', event_id, str(e))

        finally:
            self._updating = False
            reactor.callFromThread(self._invalidate)

        return

    def _translateInline(self, text):
        if text:
            try:
                logger.debug('Inline translating: %s', text)
                event_info = (None, '', '', text, '', '', '', '')
                translator = translatorMain(text, event_info)
                translator.translateEPG(text)
                return translator['text2'].getText()
            except Exception as e:
                logger.error('Inline translation failed: %s', str(e))

        return text

    def _invalidate(self):
        logger.debug('Invalidating UI (calling self.changed)')
        self.changed((self.CHANGED_POLL,))
        return

    text = property(getText)


return
