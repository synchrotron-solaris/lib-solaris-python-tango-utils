__author__ = 'User'

import PyTango
import SolarisUtils.ExceptionSuppression as es
import numpy as np
import time
from threading import Lock


class ExtendedAttributesGroup:
    global_lock = Lock()
    obsolete_attribute_read_requests = {}
    obsolete_attribute_write_requests = {}


def clear_obsolete_requests():
    '''
    It clears requests not arrived on time
    :return:
    '''
    with ExtendedAttributesGroup.global_lock:
        new_obsolete_attribute_read_requests = {}
        for ap in ExtendedAttributesGroup.obsolete_attribute_read_requests:
            left_ids = []
            for request_id in ExtendedAttributesGroup.obsolete_attribute_read_requests:
                try:
                    ap.read_reply(request_id)
                except PyTango.AsynReplyNotArrived:
                    left_ids.append(request_id)
                except:
                    pass
            if len(left_ids) > 0:
                new_obsolete_attribute_read_requests[ap] = left_ids
        ExtendedAttributesGroup.obsolete_attribute_read_requests =new_obsolete_attribute_read_requests

    with ExtendedAttributesGroup.global_lock:
        new_obsolete_attribute_write_requests = {}
        for ap in ExtendedAttributesGroup.obsolete_attribute_write_requests:
            left_ids = []
            for request_id in ExtendedAttributesGroup.obsolete_attribute_write_requests:
                try:
                    ap.read_reply(request_id)
                except PyTango.AsynReplyNotArrived:
                    left_ids.append(request_id)
                except:
                    pass
            if len(left_ids) > 0:
                new_obsolete_attribute_write_requests[ap] = left_ids
        ExtendedAttributesGroup.obsolete_attribute_write_requests =new_obsolete_attribute_write_requests


def read_attributes_parallel(attributes, wait_time=0.5, errors_limit=5):
        '''
        Read attributes in parallel
        :param attributes: list of attributes to read -(AttributePoxies)
        :param wait_time: How long to wait for responses.
        :param errors_limit: number of communication exceptions to be suppressed
        :return: dictionary of replies
        '''
        es_object = es.ExceptionSuppresser() # we will do some exception suppression
        request_ids = {}
        replies = {}

        clear_obsolete_requests() # just to do some garbage collection

        # send async read requests
        for ap in attributes:
            try:
                request_ids[ap] = es_object.suppress_exceptions(errors_limit,ap.read_async, ())
            except:
                pass

        time_counter = 0
        # read responses for request with applied timeout
        while time_counter < wait_time and len(request_ids.keys())>0:
            # just wait before each trial
            time.sleep(wait_time*0.1)
            time_counter += wait_time*0.1
            # iterate through all requests
            for ap in attributes:
                try:
                    # try to ready a reply if available for the ap proxy
                    replies[ap] = es_object.suppress_exceptions(errors_limit, ap.read_reply,
                                                                     (request_ids[ap],))
                    # if reply arrived remove request from the list
                    request_ids.pop(ap)
                except PyTango.AsynReplyNotArrived:
                    # ignore not arrived replies
                    pass

        # not arrived request is passed to be cleared in the future
        with ExtendedAttributesGroup.global_lock:
            for ap in request_ids:
                if not (ap in ExtendedAttributesGroup.obsolete_attribute_read_requests):
                    ExtendedAttributesGroup.obsolete_attribute_read_requests[ap] = []
                ExtendedAttributesGroup.obsolete_attribute_read_requests[ap].append(request_ids[ap])

        return replies


def write_attributes_parallel(attributes, values, wait_time=0.5,  errors_limit=5):
        '''
        Write attributes values in parallel.
        :param attributes: list of attributes to wrtie to -(AttributePoxies)
        :param values: list of values
        :param wait_time: how long to wait for write confirmation.
        :param errors_limit: number of communication exceptions to be suppressed
        :return: list of unconfirmed writes
        '''
        es_object = es.ExceptionSuppresser()
        request_ids = {}
        replies = {}
        clear_obsolete_requests() # just to do some garbage collection
        # send async write requests
        i=0
        for ap in attributes:
            try:
                request_ids[ap] = es_object.suppress_exceptions(errors_limit,ap.write_async, (values[i],))
            except:
                pass
            i += 1

        time_counter = 0
        # read responses for request with applied timeout
        while time_counter < wait_time and len(request_ids.keys())>0:
            # just wait before each trial
            time.sleep(wait_time*0.1)
            time_counter += wait_time*0.1
            # iterate through all requests
            for ap in attributes:
                try:
                    # try to ready a reply if available for the ap proxy
                    es_object.suppress_exceptions(errors_limit, ap.write_reply, (request_ids[ap],))
                    # if reply arrived remove request from the list
                    request_ids.pop(ap)
                except PyTango.AsynReplyNotArrived:
                    # ignore not arrived replies
                    pass

        # fill obsolete requests to be deleted in the future
        with ExtendedAttributesGroup.global_lock:
            for ap in request_ids:
                    if not (ap in ExtendedAttributesGroup.obsolete_attribute_write_requests):
                        ExtendedAttributesGroup.obsolete_attribute_write_requests[ap] = []
                    ExtendedAttributesGroup.obsolete_attribute_write_requests[ap].append(request_ids[ap])

        # return list of not confirmed writes
        return request_ids.keys()
