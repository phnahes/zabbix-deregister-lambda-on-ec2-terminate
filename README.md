# zabbix-deregister-lambda-on-ec2-terminate
Deregister Ec2 Instance from Zabbix API when EC2 Terminate
  

## CloudWatch Event

Use:

* Service Name: EC2
* Event Type: EC2 Instance State-change Notification
* Specific state(s): terminated
* Any instance

* Event Pattern Preview

```
{
  "source": [
    "aws.ec2"
  ],
  "detail-type": [
    "EC2 Instance State-change Notification"
  ],
  "detail": {
    "state": [
      "terminated"
    ]
  }
}
```

So call a Lambda Function (target)


## Lambda Function

Import lambda function and Library, changing the vars bellow:


```
server =
username = 
password =
```

### Extras

Variable such as: 
```st_disabled``` and ```st_enabled``` define how script will work, enabling or disabling hosts on Zabbix Server. 

To work fine, change "state" on "Specific State" to running.

## Security

### IAM Role and Policy

On lambda function, create a role to execute function:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:*:*:*"
        },
        {
            "Action": "ec2:*",
            "Effect": "Allow",
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": "cloudwatch:*",
            "Resource": "*"
        }
    ]
}
```

## Lambda Configurations

You will need configure a VPC and a Subnet that yours Zabbix Server be to access.

 
