# Torium-Alerts

General description of project can be found here:
[TORIUM-Torium-generalinfo-280123-0718.pdf](https://github.com/ArtCie/Torium-Alerts/files/10526562/TORIUM-Torium-generalinfo-280123-0718.pdf)

This repository consist of external tool built for managing Torium Backend architecture. Torium-Alerts is a Python base Lambda function which is execute by AWS EventBridge event each 5 minutes. System goes through Cloud resources and filter them for any error messages:
a) Lambda logs
b) EB logs
c) EB health logs
d) EB access logs
e) RDS Database logs
f) in addition - system executes each Lambda function to check if it's accessible + if there was any error during Lambda function set up. 
System collects logs and sends them to Discord channel - admin is notified about errors.

Basic architecture flow:

<img width="636" alt="Screenshot 2023-01-28 at 08 33 19" src="https://user-images.githubusercontent.com/72509444/215253417-2bb02246-ec32-46d5-97a7-432c012b1fe8.png">

Project requirements:

```
boto3==1.26.14
requests==2.24.0
urllib3==1.25.9
```
