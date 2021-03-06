import supriya.assets.synthdefs
import supriya.realtime
import uqbar.strings


def test_allocate_synthdef(server):
    synthdef = supriya.assets.synthdefs.test
    synth_a = supriya.realtime.Synth(synthdef=synthdef)
    assert not synthdef.is_allocated
    assert not synth_a.is_allocated
    assert synth_a.node_id is None
    assert synth_a not in server
    with server.osc_io.capture() as transcript:
        synth_a.allocate()
    assert list(transcript) == [
        ('S', supriya.osc.OscMessage(5, bytearray(synthdef.compile()), supriya.osc.OscMessage(9, 'test', 1000, 0, 1))),
        ('R', supriya.osc.OscMessage('/n_go', 1000, 1, -1, -1, 0)),
        ('R', supriya.osc.OscMessage('/done', '/d_recv')),
        ]
    assert synthdef.is_allocated
    assert synth_a.node_id == 1000
    assert server[1000] is synth_a
    assert synth_a in server
    server_state = str(server.query_remote_nodes(include_controls=True))
    assert server_state == uqbar.strings.normalize('''
        NODE TREE 0 group
            1 group
                1000 test
                    amplitude: 1.0, frequency: 440.0
        ''')
    assert str(server.query_local_nodes(include_controls=True)) == server_state


def test_no_reallocate_synthdef(server):
    synthdef = supriya.assets.synthdefs.test
    supriya.realtime.Synth(synthdef=synthdef).allocate()
    # SynthDef won't be allocated again
    synth_b = supriya.realtime.Synth(synthdef=synthdef)
    assert not synth_b.is_allocated
    assert synth_b.node_id is None
    assert synth_b not in server
    with server.osc_io.capture() as transcript:
        synth_b.allocate()
    assert list(transcript) == [
        ('S', supriya.osc.OscMessage(9, 'test', 1001, 0, 1)),
        ('R', supriya.osc.OscMessage('/n_go', 1001, 1, -1, 1000, 0)),
        ]
    assert synthdef.is_allocated
    assert synth_b.node_id == 1001
    assert server[1001] is synth_b
    assert synth_b in server
    server_state = str(server.query_remote_nodes(include_controls=True))
    assert server_state == uqbar.strings.normalize('''
        NODE TREE 0 group
            1 group
                1001 test
                    amplitude: 1.0, frequency: 440.0
                1000 test
                    amplitude: 1.0, frequency: 440.0
        ''')
    assert str(server.query_local_nodes(include_controls=True)) == server_state


def test_replace(server):
    synthdef = supriya.assets.synthdefs.test
    synth_a = supriya.realtime.Synth()
    synth_b = supriya.realtime.Synth(synthdef=synthdef)
    synth_a.allocate()
    assert synth_a.node_id == 1000
    assert server[1000] is synth_a
    assert synth_a in server
    assert synth_a.is_allocated
    assert not synthdef.is_allocated
    assert not synth_b.is_allocated
    assert synth_b.node_id is None
    assert synth_b not in server
    server_state = str(server.query_remote_nodes(include_controls=True))
    assert server_state == uqbar.strings.normalize('''
        NODE TREE 0 group
            1 group
                1000 default
                    out: 0.0, amplitude: 0.1, frequency: 440.0, gate: 1.0, pan: 0.5
        ''')
    with server.osc_io.capture() as transcript:
        synth_b.allocate(
            add_action='replace',
            target_node=synth_a,
            )
    assert list(transcript) == [
        ('S', supriya.osc.OscMessage(5, bytearray(synthdef.compile()), supriya.osc.OscMessage(9, 'test', 1001, 4, 1000))),
        ('R', supriya.osc.OscMessage('/n_go', 1001, 1, -1, -1, 0)),
        ('R', supriya.osc.OscMessage('/done', '/d_recv')),
        ]
    server_state = str(server.query_remote_nodes(include_controls=True))
    assert server_state == uqbar.strings.normalize('''
        NODE TREE 0 group
            1 group
                1001 test
                    amplitude: 1.0, frequency: 440.0
        ''')
    assert synth_a.node_id is None
    assert synth_a not in server
    assert not synth_a.is_allocated
    assert server[1000] is None
    assert synth_b.node_id == 1001
    assert server[1001] is synth_b
    assert synth_b in server
    assert synth_b.is_allocated


def test_settings(server):
    group = supriya.realtime.Group().allocate()
    synth_a = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    synth_a.allocate(target_node=group)
    synth_b = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    synth_b.allocate(target_node=group)
    server_state = str(server.query_remote_nodes(include_controls=True))
    assert server_state == uqbar.strings.normalize('''
        NODE TREE 0 group
            1 group
                1000 group
                    1002 test
                        amplitude: 1.0, frequency: 440.0
                    1001 test
                        amplitude: 1.0, frequency: 440.0
        ''')
    assert synth_a['frequency'] == 440.0
    assert synth_a['amplitude'] == 1.0
    assert synth_b['frequency'] == 440.0
    assert synth_b['amplitude'] == 1.0
    synth_a['frequency'] = 443
    synth_a['amplitude'] = 0.5
    server_state = str(server.query_remote_nodes(include_controls=True))
    assert server_state == uqbar.strings.normalize('''
        NODE TREE 0 group
            1 group
                1000 group
                    1002 test
                        amplitude: 1.0, frequency: 440.0
                    1001 test
                        amplitude: 0.5, frequency: 443.0
        ''')
    assert synth_a['frequency'] == 443.0
    assert synth_a['amplitude'] == 0.5
    assert synth_b['frequency'] == 440.0
    assert synth_b['amplitude'] == 1.0
    synth_b.controls['frequency', 'amplitude'] = 441, 0.25
    server_state = str(server.query_remote_nodes(include_controls=True))
    assert server_state == uqbar.strings.normalize('''
        NODE TREE 0 group
            1 group
                1000 group
                    1002 test
                        amplitude: 0.25, frequency: 441.0
                    1001 test
                        amplitude: 0.5, frequency: 443.0
        ''')
    assert synth_a['frequency'] == 443.0
    assert synth_a['amplitude'] == 0.5
    assert synth_b['frequency'] == 441.0
    assert synth_b['amplitude'] == 0.25
    bus_a = supriya.realtime.Bus(calculation_rate='control').allocate()
    bus_b = supriya.realtime.Bus(calculation_rate='audio').allocate()
    synth_a['frequency'] = bus_a
    synth_b['amplitude'] = bus_b
    server_state = str(server.query_remote_nodes(include_controls=True))
    assert server_state == uqbar.strings.normalize('''
        NODE TREE 0 group
            1 group
                1000 group
                    1002 test
                        amplitude: a16, frequency: 441.0
                    1001 test
                        amplitude: 0.5, frequency: c0
        ''')
    assert synth_a['frequency'] == bus_a
    assert synth_a['amplitude'] == 0.5
    assert synth_b['frequency'] == 441.0
    assert synth_b['amplitude'] == bus_b


def test_mapping(server):
    synthdef = supriya.assets.synthdefs.test.allocate()
    synth = supriya.realtime.Synth(synthdef=synthdef)
    synth['frequency'] = 443
    synth['amplitude'] = 0.5
    assert synth['frequency'] == 443
    assert synth['amplitude'] == 0.5
    # Allocate and verify messaging and server state
    with server.osc_io.capture() as transcript:
        synth.allocate()
    assert list(transcript) == [
        ('S', supriya.osc.OscMessage(9, 'test', 1000, 0, 1, 'amplitude', 0.5, 'frequency', 443.0)),
        ('R', supriya.osc.OscMessage('/n_go', 1000, 1, -1, -1, 0)),
        ]
    server_state = str(server.query_remote_nodes(include_controls=True))
    assert server_state == uqbar.strings.normalize('''
        NODE TREE 0 group
            1 group
                1000 test
                    amplitude: 0.5, frequency: 443.0
        ''')
    # Free and verify post-free state
    synth.free()
    assert synth['frequency'] == 443
    assert synth['amplitude'] == 0.5
    # Map controls to buses
    control_bus = supriya.realtime.Bus(0, calculation_rate='control').allocate()
    audio_bus = supriya.realtime.Bus(0, calculation_rate='audio').allocate()
    synth['frequency'] = control_bus
    synth['amplitude'] = audio_bus
    assert synth['frequency'] == control_bus
    assert synth['amplitude'] == audio_bus
    # Allocate and verify messaging and server state
    with server.osc_io.capture() as transcript:
        synth.allocate()
    assert list(transcript) == [
        ('S', supriya.osc.OscBundle(
            contents=(
                supriya.osc.OscMessage(9, 'test', 1001, 0, 1),
                supriya.osc.OscMessage(60, 1001, 'amplitude', 0),
                supriya.osc.OscMessage(14, 1001, 'frequency', 0),
                supriya.osc.OscMessage(52, 0),
            ),
        )),
        ('R', supriya.osc.OscMessage('/n_end', 1000, 1, -1, -1, 0)),
        ('R', supriya.osc.OscMessage('/n_go', 1001, 1, -1, -1, 0)),
        ('R', supriya.osc.OscMessage('/synced', 0)),
        ]
    server_state = str(server.query_remote_nodes(include_controls=True))
    assert server_state == uqbar.strings.normalize('''
        NODE TREE 0 group
            1 group
                1001 test
                    amplitude: a0, frequency: c0
        ''')
    # Free and verify post-free state
    synth.free()
    assert synth['frequency'] == control_bus
    assert synth['amplitude'] == audio_bus
