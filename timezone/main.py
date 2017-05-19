#-*-coding: utf-8-*-
"""
Main application file the timezone lookup server
"""
import logging
import os
import sys
import ujson as json

from flask import Flask, request, current_app

from timezone_finder import TimezoneFinder

# Gunicorn, by default, will search for the 'application' name, so use it
# for convenience
application = Flask('timezone')
# Set up logging on the application
handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(logging.Formatter(
    '%(asctime)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
))
application.logger.addHandler(handler)
application.logger.setLevel('DEBUG')

timezone_finder = TimezoneFinder()

@application.route('/timezone/')
def timezone():
    """Return a timezone name for the given latitude and longitude"""
    if not (request.args.get('lon') and request.args['lat']):
        # Make an error response and return it
        response = current_app.make_response(json.dumps({'reason': 'Missing lat/lon in request parameters'}))
        response.status_code = 400
        response.content_type = "application/json"
        return response

    timezone_name = timezone_finder.timezone_lookup(lon=request.args['lon'], lat=request.args['lat'])
    response = current_app.make_response(json.dumps({'tz': timezone_name}))
    response.content_type = "application/json"
    return response

# Useful for debugging problems in your API; works with pdb.set_trace()
if __name__ == '__main__':
    from wsgiref import simple_server

    httpd = simple_server.make_server('127.0.0.1', 8000, application)
    httpd.serve_forever()
