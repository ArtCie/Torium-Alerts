# Torium-Alerts

### General project description can be found here:
[TORIUM-Torium-generalinfo-280123-0718.pdf](https://github.com/ArtCie/Torium-Alerts/files/10526562/TORIUM-Torium-generalinfo-280123-0718.pdf)

This repository consist of external tool built for managing Torium Backend architecture. Torium-Alerts is a Python base Lambda function which is execute by AWS EventBridge event each 5 minutes. System goes through Cloud resources and filter them for any error messages:

a) Lambda logs

b) EB logs

c) EB health logs

d) EB access logs

e) RDS Database logs

f) in addition - system executes each Lambda function to check if it's accessible + if there was any error during Lambda function set up. 
System collects logs and sends them to Discord channel - admin is notified about errors.

### Basic architecture flow:

<img width="636" alt="Screenshot 2023-01-28 at 08 33 19" src="https://user-images.githubusercontent.com/72509444/215253417-2bb02246-ec32-46d5-97a7-432c012b1fe8.png">

### Project requirements:

```
boto3==1.26.14
requests==2.24.0
urllib3==1.25.9
```

### Example Discord notifications:

#### API error
<img width="542" alt="Screenshot 2023-01-28 at 10 11 52" src="https://user-images.githubusercontent.com/72509444/215257671-3e74d6dd-61ee-4c34-893e-ca1085dfe083.png">

#### API health error
<img width="281" alt="Screenshot 2023-01-28 at 10 12 22" src="https://user-images.githubusercontent.com/72509444/215257688-51be7355-a0ed-40fd-a58a-ef147bcbbbae.png">

#### API access error
<img width="477" alt="Screenshot 2023-01-28 at 10 12 57" src="https://user-images.githubusercontent.com/72509444/215257714-3bc629c7-73f9-4ca4-9d6d-2d482beee358.png">

#### Lambda error
<img width="555" alt="Screenshot 2023-01-28 at 10 13 27" src="https://user-images.githubusercontent.com/72509444/215257732-4dcdb997-7a49-44f1-8277-cefe4c405e74.png">

#### Awaking Lambda check
<img width="355" alt="Screenshot 2023-01-28 at 10 13 48" src="https://user-images.githubusercontent.com/72509444/215257745-5ad88ac1-5d43-4511-ad43-9803dcac9ea0.png">

#### Database Error
<img width="534" alt="Screenshot 2023-01-28 at 10 14 12" src="https://user-images.githubusercontent.com/72509444/215257807-615d0497-b825-4bde-a2c5-5cb660225b34.png">
