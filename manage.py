#!usr/bin/env python
import os
from app import create_app, db
from app.model import User, Post, Comment, CommentReply
from flask_script import Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand

app = create_app('default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(
        app=app, 
        db=db, 
        User=User, 
        Post=Post,
        Comment=Comment,
        CommentReply=CommentReply
    )

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('runserver', Server(host='192.168.43.200', port=5000))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    try:
        manager.run()
    except AssertionError:
        pass