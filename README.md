# cdk-fargate-hello

This project demonstrates a containerized application deployed using AWS Fargate and managed via AWS CDK in Python.

- The application logic resides in the `src/hello_api` directory.
- The infrastructure is defined in the `src/infra` directory.

---

## **Getting Started**

### **1. Prerequisites**

Before working with this project, ensure the following tools are installed and configured:

1. **Python**:
   - Install Python 3.7 or higher.
   - Verify the installation:

     ```bash
     python --version
     ```

2. **AWS CLI**:
   - Install the AWS CLI and configure credentials for your AWS account:

     ```bash
     aws configure
     ```

3. **npm (Node.js)**:
   - Install Node.js, which includes npm.
     - [Download and install Node.js](https://nodejs.org/).
   - Verify the installation:

     ```bash
     npm --version
     ```

4. **AWS CDK Toolkit**:
   - Install the AWS CDK CLI globally:

     ```bash
     npm install -g aws-cdk
     ```

   - Verify the installation:

     ```bash
     cdk --version
     ```

5. **Docker**:
   - Ensure Docker is installed and running to build container images for the application.
     - Verify Docker:

       ```bash
       docker --version
       ```

---

## **Project Structure**

```plaintext
.
├── LICENSE                       # License for the project
├── NOTES.txt                     # Miscellaneous notes for the project
├── README.md                     # This file
└── src
    ├── hello_api                 # Application logic and Dockerfile
    │   ├── config.py
    │   ├── Dockerfile
    │   ├── requirements.txt
    │   └── server.py
    └── infra
        └── infra                 # Infrastructure code (AWS CDK)
            ├── app.py
            ├── infra_stack.py
            └── __init__.py
```

---

## **License**

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.
