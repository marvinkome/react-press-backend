#!usr/bin/env python
import os
from app import create_app, db, socket, migrate
from app.model import User, Post, Comment, CommentReply, Clap, Tags, Notification
from flask_script import Manager, Shell, Server
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
    from flask_migrate import upgrade
    
    # migrate database to latest revision
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

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('runserver', Server('0.0.0.0'))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    try:
        manager.run()
    except AssertionError:
        pass