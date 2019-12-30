#!/usr/bin/bash

aws autoscaling execute-policy --auto-scaling-group-name 'Notifon Example Group' --policy-name 'Scale Up' --honor-cooldown
