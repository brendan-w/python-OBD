
########################################################################
#                                                                      #
# python-OBD: A python OBD-II serial module derived from pyobd         #
#                                                                      #
# Copyright 2004 Donour Sizemore (donour@uchicago.edu)                 #
# Copyright 2009 Secons Ltd. (www.obdtester.com)                       #
# Copyright 2009 Peter J. Creath                                       #
# Copyright 2015 Brendan Whitfield (bcw7044@rit.edu)                   #
#                                                                      #
########################################################################
#                                                                      #
# async.py                                                             #
#                                                                      #
# This file is part of python-OBD (a derivative of pyOBD)              #
#                                                                      #
# python-OBD is free software: you can redistribute it and/or modify   #
# it under the terms of the GNU General Public License as published by #
# the Free Software Foundation, either version 2 of the License, or    #
# (at your option) any later version.                                  #
#                                                                      #
# python-OBD is distributed in the hope that it will be useful,        #
# but WITHOUT ANY WARRANTY; without even the implied warranty of       #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the        #
# GNU General Public License for more details.                         #
#                                                                      #
# You should have received a copy of the GNU General Public License    #
# along with python-OBD.  If not, see <http://www.gnu.org/licenses/>.  #
#                                                                      #
########################################################################

import time
import threading
from .utils import Response
from .debug import debug
from . import OBD


class Async(OBD):

    """ subclass representing an OBD-II connection """

    def __init__(self, portstr=None, baudrate=38400):
        super(Async, self).__init__(portstr, baudrate)
        self.commands = {}  # key = OBDCommand, value = Response
        self.callbacks = {}  # key = OBDCommand, value = list of Functions
        self.thread = None
        self.running = False

    def start(self):
        if self.is_connected():
            debug("Starting async thread")
            self.running = True
            self.thread = threading.Thread(target=self.run)
            self.thread.daemon = True
            self.thread.start()
        else:
            debug("Async thread not started because no connection was made")

    def stop(self):
        if self.thread is not None:
            debug("Stopping async thread...")
            self.running = False
            self.thread.join()
            self.thread = None
            debug("Async thread stopped")

    def close(self):
        self.stop()
        super(Async, self).close()

    def watch(self, c, callback=None, force=False):

        # the dict shouldn't be changed while the daemon thread is iterating
        if self.running:
            debug("Can't watch() while running, please use stop()", True)
        else:

            if not (self.supports(c) or force):
                debug("'%s' is not supported" % str(c), True)
                return

            # new command being watched, store the command
            if c not in self.commands:
                debug("Watching command: %s" % str(c))
                self.commands[c] = Response()  # give it an initial value
                self.callbacks[c] = []  # create an empty list

            # if a callback was given, push it
            if hasattr(callback, "__call__") and (callback not in self.callbacks[c]):
                debug("subscribing callback for command: %s" % str(c))
                self.callbacks[c].append(callback)

    def unwatch(self, c, callback=None):

        # the dict shouldn't be changed while the daemon thread is iterating
        if self.running:
            debug("Can't unwatch() while running, please use stop()", True)
        else:
            debug("Unwatching command: %s" % str(c))

            if c in self.commands:
                # if a callback was specified, only remove the callback
                if hasattr(callback, "__call__") and (callback in self.callbacks[c]):
                    self.callbacks[c].remove(callback)

                    # if no more callbacks are left, remove the command
                    # entirely
                    if len(self.callbacks[c]) == 0:
                        self.commands.pop(c, None)
                else:
                    # no callback was specified, pop everything
                    self.callbacks.pop(c, None)
                    self.commands.pop(c, None)

    def unwatch_all(self):

        # the dict shouldn't be changed while the daemon thread is iterating
        if self.running:
            debug("Can't unwatch_all() while running, please use stop()", True)
        else:
            debug("Unwatching all")
            self.commands = {}
            self.callbacks = {}

    def query(self, c):
        if c in self.commands:
            return self.commands[c]
        else:
            return Response()

    def run(self):
        """ Daemon thread """

        # loop until the stop signal is recieved
        while self.running:

            if len(self.commands) > 0:
                # loop over the requested commands, send, and collect the
                # response
                for c in self.commands:
                    r = self.send(c)

                    # store the response
                    self.commands[c] = r

                    # fire the callbacks, if there are any
                    for callback in self.callbacks[c]:
                        callback(r)

            else:
                time.sleep(1)  # idle
