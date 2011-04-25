Directions:
===========

Install ZeroMQ:

For Ubuntu Linux

    $ apt-get install zeromq-bin libzmq-dev libzmq0

For Arch Linux

    $ pacman -S zeromq

Build your virtualenv:

    $ cd zeromq-chat
    $ virtualenv --no-site-packages env
    $ source env/bin/activate

Install neccesary packages:

    $ pip install -r requirements.txt 

Run:
    
    $ python run.py

Point your browser to localhost:8080

Notes:
=====

You may need to install from a PPA if your version of Ubuntu does
not carray libzmq >= 2.10. Such as:
    
    sudo add-apt-repository ppa:chris-lea/zeromq
