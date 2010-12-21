from cheese_emporium import app
import pkg_resources
import optparse
import sys

def main():
    usage = "usage: %prog [options]"
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-d', '--debug',
                      help='Run in debug mode',
                      dest='debug',
                      action='store_true',
                      default=False)
    options, args = parser.parse_args(sys.argv)
    print "FILE ROOT: " + app.config['FILE_ROOT']
    print "STATIC: " + pkg_resources.resource_filename(app.config['CHEESE'], 'cheese_emporium/static')
    app.run(debug=options.debug)


def make_app(global_conf, settings=None, fileroot=None):
    """
    paste compatible make app
    """
    if settings is not None:
        app.config.from_pyfile(settings)
        
    if fileroot is not None:
        app.config['FILE_ROOT'] = fileroot

    return app.wsgi_app


if __name__ == "__main__":
    print "Running single thread test emporium\n"
    main()
