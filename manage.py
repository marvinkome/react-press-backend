#!usr/bin/env python
import os
from app import create_app, db, socket, migrate
from app.model import User, Post, Comment, CommentReply, Clap, Tags, Notification
from flask_script import Manager, Shell, Server as _Server, Option
from flask_migrate import Migrate, MigrateCommand


app = create_app(os.environ.get('FLASK_CONFIG') or 'default')
manager = Manager(app)

@manager.command
def profile(length=25, profile_dir=None):
    """Start the application under the code profiler."""
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length], profile_dir=profile_dir)
    app.run(host='0.0.0.1', port=5000)

@manager.command
def deploy():
    """Run deployment tasks."""
    from flask_migrate import upgrade, init, migrate
    
    # migrate database to latest revision
    init()
    migrate()
    upgrade()

@manager.command
def upgrade_db():
    """Run deployment tasks."""
    from flask_migrate import upgrade, init, migrate
    
    # migrate database to latest revision
    init()
    migrate()
    upgrade()

@manager.command
def runsocket():
    socket.run(app)

def make_shell_context():
    return dict(
        app=app, 
        db=db, 
        User=User, 
        Post=Post,
        Comment=Comment,
        CommentReply=CommentReply,
        Clap=Clap,
        Tags=Tags,
        Notification=Notification
    )

class Server(_Server):
    help = description = 'Runs the Socket.IO web server'

    def get_options(self):
        options = (
            Option('-h', '--host',
                   dest='host',
                   default=self.host),

            Option('-p', '--port',
                   dest='port',
                   type=int,
                   default=self.port),

            Option('-d', '--debug',
                   action='store_true',
                   dest='use_debugger',
                   help=('enable the Werkzeug debugger (DO NOT use in '
                         'production code)'),
                   default=self.use_debugger),
            Option('-D', '--no-debug',
                   action='store_false',
                   dest='use_debugger',
                   help='disable the Werkzeug debugger',
                   default=self.use_debugger),

            Option('-r', '--reload',
                   action='store_true',
                   dest='use_reloader',
                   help=('monitor Python files for changes (not 100%% safe '
                         'for production use)'),
                   default=self.use_reloader),
            Option('-R', '--no-reload',
                   action='store_false',
                   dest='use_reloader',
                   help='do not monitor Python files for changes',
                   default=self.use_reloader),
        )
        return options

    def __call__(self, app, host, port, use_debugger, use_reloader):
        # override the default runserver command to start a Socket.IO server
        if use_debugger is None:
            use_debugger = app.debug
            if use_debugger is None:
                use_debugger = True
        if use_reloader is None:
            use_reloader = app.debug
        socket.run(app,
                     host=host,
                     port=port,
                     debug=use_debugger,
                     use_reloader=use_reloader,
                     **self.server_options)

manager.add_command("runserver", Server())
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    try:
        manager.run()
    except AssertionError:
        pass