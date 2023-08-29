from behave import *


@given(u'User got navigated to webpage')
def step_impl(context):
    print("user got navigated")


@when(u'User entered username as "{username}" and password as "{password}" into seachbox field')
def step_impl(context,username,password):
    print("user entered valid username "+username+" and password "+password+" ")


@when(u'User clicked on search button')
def step_impl(context):
    print("user clicked on search button")


@then(u'Valid product should get displayed')
def step_impl(context):
    print("products get displayed")
