# -*- coding: utf-8 -*-

########################################################################
#                                                                      #
# python-OBD: A python OBD-II serial module derived from pyobd         #
#                                                                      #
# Copyright 2004 Donour Sizemore (donour@uchicago.edu)                 #
# Copyright 2009 Secons Ltd. (www.obdtester.com)                       #
# Copyright 2009 Peter J. Creath                                       #
# Copyright 2016 Brendan Whitfield (brendan-w.com)                     #
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
import logging
from .OBDResponse import OBDResponse
from .obd import OBD

logger = logging.getLogger(__name__)


class Async(OBD):
    """
        Class representing an OBD-II connection with it's assorted commands/sensors
        Specialized for asynchronous value reporting.
    """

    def __init__(self, portstr=None, baudrate=None, protocol=None, fast=True,
                 timeout=0.1):
        super(Async, self).__init__(portstr, baudrate, protocol, fast,
                                    timeout)
        self.__commands    = {} # key = OBDCommand, value = Response
        self.__callbacks   = {} # key = OBDCommand, value = list of Functions
        self.__thread      = None
        self.__running     = False
        self.__was_running = False # used with __enter__() and __exit__()


    @property
    def running(self):
        return self.__running


    def start(self):
        """ Starts the async update loop """
        if not self.is_connected():
            logger.info("Async thread not started because no connection was made")
            return

        if len(self.__commands) == 0:
            logger.info("Async thread not started because no commands were registered")
            return

        if self.__thread is None:
            logger.info("Starting async thread")
            self.__running = True
            self.__thread = threading.Thread(target=self.run)
            self.__thread.daemon = True
            self.__thread.start()


    def stop(self):
        """ Stops the async update loop """
        if self.__thread is not None:
            logger.info("Stopping async thread...")
            self.__running = False
            self.__thread.join()
            self.__thread = None
            logger.info("Async thread stopped")


    def paused(self):
        """
            A stub function for semantic purposes only
            enables code such as:

            with connection.paused() as was_running
                ...
        """
        return self


    def __enter__(self):
        """
            pauses the async loop,
            while recording the old state
        """
        self.__was_running = self.__running
        self.stop()
        return self.__was_running


    def __exit__(self, exc_type, exc_value, traceback):
        """
            resumes the update loop if it was running
            when __enter__ was called
        """
        if not self.__running and self.__was_running:
            self.start()

        return False # don't suppress any exceptions


    def close(self):
        """ Closes the connection """
        self.stop()
        super(Async, self).close()


    def watch(self, c, callback=None, force=False):
        """
            Subscribes the given command for continuous updating. Once subscribed,
            query() will return that command's latest value. Optional callbacks can
            be given, which will be fired upon every new value.
        """

        # the dict shouldn't be changed while the daemon thread is iterating
        if self.__running:
            logger.warning("Can't watch() while running, please use stop()")
        else:

            if not force and not self.test_cmd(c):
                # self.test_cmd() will print warnings
                return

            # new command being watched, store the command
            if c not in self.__commands:
                logger.info("Watching command: %s" % str(c))
                self.__commands[c] = OBDResponse() # give it an initial value
                self.__callbacks[c] = [] # create an empty list

            # if a callback was given, push it
            if hasattr(callback, "__call__") and (callback not in self.__callbacks[c]):
                logger.info("subscribing callback for command: %s" % str(c))
                self.__callbacks[c].append(callback)


    def unwatch(self, c, callback=None):
        """
            Unsubscribes a specific command (and optionally, a specific callback)
            from being updated. If no callback is specified, all callbacks for
            that command are dropped.
        """

        # the dict shouldn't be changed while the daemon thread is iterating
        if self.__running:
            logger.warning("Can't unwatch() while running, please use stop()")
        else:
            logger.info("Unwatching command: %s" % str(c))

            if c in self.__commands:
                # if a callback was specified, only remove the callback
                if hasattr(callback, "__call__") and (callback in self.__callbacks[c]):
                    self.__callbacks[c].remove(callback)

                    # if no more callbacks are left, remove the command entirely
                    if len(self.__callbacks[c]) == 0:
                        self.__commands.pop(c, None)
                else:
                    # no callback was specified, pop everything
                    self.__callbacks.pop(c, None)
                    self.__commands.pop(c, None)


    def unwatch_all(self):
        """ Unsubscribes all commands and callbacks from being updated """

        # the dict shouldn't be changed while the daemon thread is iterating
        if self.__running:
            logger.warning("Can't unwatch_all() while running, please use stop()")
        else:
            logger.info("Unwatching all")
            self.__commands  = {}
            self.__callbacks = {}


    def query(self, c):
        """
            Non-blocking query().
            Only commands that have been watch()ed will return valid responses
        """

        if c in self.__commands:
            return self.__commands[c]
        else:
            return OBDResponse()


    def run(self):
        """ Daemon thread """

        # loop until the stop signal is recieved
        while self.__running:

            if len(self.__commands) > 0:
                # loop over the requested commands, send, and collect the response
                for c in self.__commands:

                    # force, since commands are checked for support in watch()
                    r = super(Async, self).query(c, force=True)

                    # store the response
                    self.__commands[c] = r

                    # fire the callbacks, if there are any
                    for callback in self.__callbacks[c]:
                        callback(r)

            else:
                time.sleep(0.25) # idle
