# Infra Module

The `infra` directory contains the AWS CDK codebase for defining and managing the cloud infrastructure of the **CDK Fargate Hello Project**. This project leverages AWS Fargate to deploy a containerized application in a scalable, serverless environment. Core resources include a VPC, ECS Cluster, and Fargate Service.

---

## **Structure**

The `infra` module consists of the following files:

```plaintext
infra/
└──| infra
   ├── __init__.py        # Marks the directory as a Python module
   ├── app.py             # Entry point for the CDK application
   └── infra_stack.py     # AWS Fargate stack definition
```

### **File Descriptions**

- **`app.py`**:
  - Entry point for the AWS CDK application.
  - Instantiates the `FargateStack` class and synthesizes it into a CloudFormation template.

- **`fargate_stack.py`**:
  - Defines the AWS Fargate stack, including resources such as:
    - **VPC**: Public and private subnets for networking.
    - **ECS Cluster**: Cluster for running containerized workloads.
    - **Fargate Service**: Serverless deployment for the application.

- **`__init__.py`**:
  - Marks the `infra` directory as a Python module to enable imports.

---

## **Getting Started**

### **Prerequisites**

1. **Python Environment**:
   - Ensure Python 3.7 or higher is installed.
   - Activate your virtual environment:

     **Linux/macOS**:

     ```bash
     source .venv/bin/activate
     ```

     **Windows**:

     ```cmd
     .venv\Scripts\activate
     ```

---

## **How to Use**

**Note:** The following steps are only required when setting up the `infra` directory for the first time (steps 1 to 3). The CDK environment has already been bootstrapped separately.

1. **Create the Directory**:
   Navigate to the project root and create the `infra` directory:

   ```bash
   mkdir -p src/infra
   cd src/infra
   ```

2. **Initialize the CDK Project**:
   Set up the directory as a CDK project:

   ```bash
   cdk init app --language python
   ```

3. **Add Required Files**:
   Add the `app.py`, `fargate_stack.py`, and `__init__.py` files to define your infrastructure as described in the structure above.

4. **Install Dependencies**:
   Ensure all required Python packages are installed. From the `src/infra` directory, run:

   ```bash
   python -m pip install -r requirements.txt
   ```

5. **Synthesize the Stack**:
   Run this command from the `src/infra` directory to generate the CloudFormation template from the CDK code:

   ```bash
   cdk synth
   ```

6. **Deploy the Stack**:
   Deploy the stack to your AWS account:

   ```bash
   cdk deploy
   ```

7. **Destroy the Stack**:
   To clean up and remove the resources:

   ```bash
   cdk destroy
   ```

---

## **Key Features**

- **VPC**:
  - A Virtual Private Cloud with public and private subnets to host the ECS cluster and tasks.

- **ECS Cluster**:
  - A cluster to manage containerized workloads.

- **Fargate Service**:
  - A service that deploys the `hello_api` containerized application using AWS Fargate.

---

## **Troubleshooting**

1. **CDK Bootstrap Issues**:
   - Ensure AWS CLI is configured and the account/region has the required permissions.

2. **Deployment Errors**:
   - Check the CloudFormation console for detailed error logs and event histories.

3. **Dependency Issues**:
   - Ensure all required Python packages are installed in the virtual environment.

---

## **Testing the Deployment**

After deploying, verify the application:

1. Access the Fargate Service endpoint through the ECS console or load balancer URL.
2. Check ECS task logs for any application errors.

---

## **License**

This project is licensed under the MIT License. See the [LICENSE](../../LICENSE) file for details.
