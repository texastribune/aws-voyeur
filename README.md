Quick n dirty CLI for checking ec2 inventory

Specifically design for my own personal workflow.

If you're doing something serious, you should look into these better
alternatives:

* https://github.com/DrGonzo65/ec2-cli-tools - very similar package that lets
  you glob
* https://github.com/mattrobenolt/ec2 - lets you query instances using django-
  orm-like syntax
* awscli - official aws cli


If you're still here, here's the deal: This is a CLI for querying ec2 for what
instances are running and display them in a table with the same columns I have
enabled in the web interface. You can sort by specifying the headers:

    voyeur name
    voyeur launch_time
    voyeur environment

You can filter similarily like:

    voyeur environment=production

Or go crazy (show production foo sites ordered by launch time):

    voyeru environment=production site=foo launch_time

## Installation

    pip install https://github.com/texastribune/ec2-voyeur/archive/master.tar.gz

## Usage

Configure boto following [the official instructions](http://boto.readthedocs.org/en/latest/boto_config_tut.html).

A basic configuration would just involve setting the `AWS_ACCESS_KEY_ID`,
`AWS_SECRET_ACCESS_KEY` environment variables.
