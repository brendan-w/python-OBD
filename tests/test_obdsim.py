
import time
import pytest
from obd import commands, Unit

# NOTE: This is purposefully tuned slightly higher than the ELM's default
#       message timeout of 200 milliseconds. This prevents us from
#       inadvertently marking the first query of an async connection as
#       null, since it may be the case that the first transaction incurs the
#       ELM's internal timeout.
STANDARD_WAIT_TIME = 0.3


@pytest.fixture(scope="module")
def obd(request):
    """provides an OBD connection object for obdsim"""
    import obd
    port = request.config.getoption("--port")
    return obd.OBD(port)


@pytest.fixture(scope="module")
def asynchronous(request):
    """provides an OBD *Async* connection object for obdsim"""
    import obd
    port = request.config.getoption("--port")
    return obd.Async(port)


def good_rpm_response(r):
    return (not r.is_null()) and \
           (r.value.u == Unit.rpm) and \
           (r.value >= 0.0 * Unit.rpm)


@pytest.mark.skipif(not pytest.config.getoption("--port"),
                    reason="needs --port=<port> to run")
def test_supports(obd):
    assert(len(obd.supported_commands) > 0)
    assert(obd.supports(commands.RPM))


@pytest.mark.skipif(not pytest.config.getoption("--port"),
                    reason="needs --port=<port> to run")
def test_rpm(obd):
    r = obd.query(commands.RPM)
    assert(good_rpm_response(r))


# Async tests

@pytest.mark.skipif(not pytest.config.getoption("--port"),
                    reason="needs --port=<port> to run")
def test_async_query(asynchronous):

    rs = []
    asynchronous.watch(commands.RPM)
    asynchronous.start()

    for i in range(5):
        time.sleep(STANDARD_WAIT_TIME)
        rs.append(asynchronous.query(commands.RPM))

    asynchronous.stop()
    asynchronous.unwatch_all()

    # make sure we got data
    assert(len(rs) > 0)
    assert(all([good_rpm_response(r) for r in rs]))


@pytest.mark.skipif(not pytest.config.getoption("--port"),
                    reason="needs --port=<port> to run")
def test_async_callback(asynchronous):

    rs = []
    asynchronous.watch(commands.RPM, callback=rs.append)
    asynchronous.start()
    time.sleep(STANDARD_WAIT_TIME)
    asynchronous.stop()
    asynchronous.unwatch_all()

    # make sure we got data
    assert(len(rs) > 0)
    assert(all([good_rpm_response(r) for r in rs]))


@pytest.mark.skipif(not pytest.config.getoption("--port"),
                    reason="needs --port=<port> to run")
def test_async_paused(asynchronous):

    assert(not asynchronous.running)
    asynchronous.watch(commands.RPM)
    asynchronous.start()
    assert(asynchronous.running)

    with asynchronous.paused() as was_running:
        assert(not asynchronous.running)
        assert(was_running)

    assert(asynchronous.running)
    asynchronous.stop()
    assert(not asynchronous.running)


@pytest.mark.skipif(not pytest.config.getoption("--port"),
                    reason="needs --port=<port> to run")
def test_async_unwatch(asynchronous):

    watched_rs = []
    unwatched_rs = []

    asynchronous.watch(commands.RPM)
    asynchronous.start()

    for i in range(5):
        time.sleep(STANDARD_WAIT_TIME)
        watched_rs.append(asynchronous.query(commands.RPM))

    with asynchronous.paused():
        asynchronous.unwatch(commands.RPM)

    for i in range(5):
        time.sleep(STANDARD_WAIT_TIME)
        unwatched_rs.append(asynchronous.query(commands.RPM))

    asynchronous.stop()

    # the watched commands
    assert(len(watched_rs) > 0)
    assert(all([good_rpm_response(r) for r in watched_rs]))

    # the unwatched commands
    assert(len(unwatched_rs) > 0)
    assert(all([r.is_null() for r in unwatched_rs]))


@pytest.mark.skipif(not pytest.config.getoption("--port"),
                    reason="needs --port=<port> to run")
def test_async_unwatch_callback(asynchronous):

    a_rs = []
    b_rs = []
    asynchronous.watch(commands.RPM, callback=a_rs.append)
    asynchronous.watch(commands.RPM, callback=b_rs.append)

    asynchronous.start()
    time.sleep(STANDARD_WAIT_TIME)

    with asynchronous.paused():
        asynchronous.unwatch(commands.RPM, callback=b_rs.append)

    time.sleep(STANDARD_WAIT_TIME)
    asynchronous.stop()
    asynchronous.unwatch_all()

    assert(all([good_rpm_response(r) for r in a_rs + b_rs]))
    assert(len(a_rs) > len(b_rs))
