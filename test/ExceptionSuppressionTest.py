__author__ = 'User'


import SolarisUtils.ExceptionSuppression as es


class ExceptionSuppressionTest:
    exceptions_counter = 0

def exception_thrower(no, exception = Exception):
    if ExceptionSuppressionTest.exceptions_counter < no:
        ExceptionSuppressionTest.exceptions_counter+=1
        raise exception("An exception is raised for " + str(ExceptionSuppressionTest.exceptions_counter)+" time.")

def reset_counter():
    ExceptionSuppressionTest.exceptions_counter = 0




if __name__ == '__main__':

    # check static methods:

    # check no exception is raised without global exception counting
    try:
        reset_counter()
        es.suppress_exceptions(5, exception_thrower,(2,))
        reset_counter()
        es.suppress_exceptions(5, exception_thrower,(4,))
        reset_counter()
        es.suppress_exceptions(5, exception_thrower,(5,))
    except Exception as e:
        print "FAIL: The test of static method without global counting has failed. An exception has not been suppresed:"
        print "\t"+e.message
    else:
        print "OK: The test of static method without global counting has passed for exception suppressing."

    # check exception is raised without global exception counting
    try:
        reset_counter()
        es.suppress_exceptions(5, exception_thrower,(8,))
    except Exception as e:
        print "OK: The test of static method without global counting has been passed. An exception has not been suppresed:"
        print "\t"+e.message
    else:
        print "FAIL: The test of static method without global counting has failed for raising exception." \
              "\tNo exception re-raised even there were more than limited number of exceptions raised."

    # check no exception is raised with global exception counting
    es.reset_global_counter()
    try:
        reset_counter()
        es.suppress_exceptions(5, exception_thrower,(2,), (Exception,), 5)
        reset_counter()
        es.suppress_exceptions(5, exception_thrower,(4,), (Exception,), 6)
        reset_counter()
        es.suppress_exceptions(5, exception_thrower,(5,), (Exception,), 11)
    except Exception as e:
        print "FAIL: The test of static method with global counting has failed. An exception has not been suppresed:"
        print "\t"+e.message
    else:
        print "OK: The test of static method with global counting has passed for exception suppressing."

    # check exception is raised with global exception counting
    try:
        reset_counter()
        es.suppress_exceptions(10, exception_thrower,(8,), (Exception,), 18)
    except Exception as e:
        print "OK: The test of static method with global counting has been passed. An exception has not been suppresed:"
        print "\t"+e.message
        print "\tWhereas globally it was "+str(es.ExceptionSuppresser.global_counter)+" times raised with global limit set to 18."
    else:
        print "FAIL: The test of static method with global counting has failed for raising exception." \
              "\tNo exception re-raised even there were more than limited number of exceptions raised."

