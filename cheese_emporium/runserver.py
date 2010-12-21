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

if __name__ == "__main__":
    main()
