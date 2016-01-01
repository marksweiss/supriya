# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class SessionObject(SupriyaObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_session',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        session,
        ):
        from supriya.tools import nrttools
        assert isinstance(session, nrttools.Session)
        self._session = session

    ### PUBLIC PROPERTIES ###

    @property
    def session(self):
        return self._session