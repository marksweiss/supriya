# -*- encoding: utf-8 -*-
from supriya.tools.osctools.OscCallback import OscCallback


class ControlBusResponseCallback(OscCallback):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_server',
        '_response_manager',
        )

    ### INITIALIZER ###

    def __init__(self, server):
        from supriya.tools import servertools
        OscCallback.__init__(
            self,
            address_pattern='/c_(set|setn)',
            procedure=self.__call__,
            )
        assert isinstance(server, servertools.Server)
        self._server = server
        self._response_manager = server._response_manager

    ### SPECIAL METHODS ###

    def __call__(self, message):
        response = self._response_manager(message)
        bus_id = response.bus_id
        bus = self._server._control_busses.get(bus_id)
        if bus is None:
            return
        bus.handle_response(response)