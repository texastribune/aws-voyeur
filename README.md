Quick n dirty CLI for checking ec2 inventory

Specifically design for my own personal workflow.

Here Be Dragons
---------------

If you're doing something serious, you should look into these better
alternatives:

* https://github.com/DrGonzo65/ec2-cli-tools - very similar package that lets
  you glob
* https://github.com/mattrobenolt/ec2 - lets you query instances using django-
  orm-like syntax
* awscli - official aws cli


If you're still here, here's the deal: This is a CLI for querying aws for what
instances are running and display them in a table with the same columns I have
enabled in the web interface. You can sort by specifying the headers:

    voyeur name
    voyeur launch_time
    voyeur environment

You can filter similarily like:

    voyeur environment=production

Or go crazy (show production foo sites ordered by launch time):

    voyeur environment=production site=foo launch_time

I picked the columns and names so that line lengths are under 120 columns;
which is how wide my terminal is.


But Wait, There's More
----------------------

If you make the first argument `elb` or `rds`, you can list your elastic load
balancers and databases too. You can also do add `ec2` if you like being
consistent.


Example
-------

### List EC2

```bash
name                   environment    site     ip              private_ip      launch_time    id
---------------------  -------------  -------  --------------  --------------  -------------  ----------
hodor-weg              prod           groot    54.85.94.132    10.0.0.2        2014-06-17     i-27fghb69
groot-elasticsearch    prod           hodor                    10.0.0.1        2014-08-08     i-abcdcaz7
```


### List ELB

```bash
$ voyeur elb
name     dns_name                                     pool  created_time
-------  -------------------------------------------  ------  ------------------------
groot    groot-1529220.us-east-1.elb.amazonaws.com         3  2012-02-03T01:41:02.930Z
hodor    hodor-4545272.us-east-1.elb.amazonaws.com         2  2014-03-08T06:15:53.610Z
```

### List RDS

```bash
$ voyeur rds
id          uri
----------  -------------------------------------------------------------------------------
groot-db    postgres://iamgroot@groot-db.cya8ag0rj.us-east-1.rds.amazonaws.com:5432/groot
hodor-db    postgres://iamgroot@hodor-db.cya8ag0rj.us-east-1.rds.amazonaws.com:5432/groot
```


## Installation

    pip install https://github.com/texastribune/ec2-voyeur/archive/master.tar.gz

## Usage

Configure boto following [the official instructions](http://boto.readthedocs.org/en/latest/boto_config_tut.html).

A basic configuration would just involve setting the `AWS_ACCESS_KEY_ID`,
`AWS_SECRET_ACCESS_KEY` environment variables.


## AWS IAM Policy

This library requires the Describe* permissions. You can use use the "Read Only
Access" policy template, or you can make your own with at least these
permissions:

```json
{
  "Statement": [
    {
      "Action": [
        "ec2:Describe*",
        "elasticloadbalancing:Describe*",
        "rds:Describe*"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
```
