# ds-disco-pdf-gen-lambda

## Package Pillow dependencies with function code

Launch an EC2 with the AMI – amzn-ami-hvm-2018.03.0.20181129-x86_64-gp2 to install and package Pillow.

```bash
# SSH into the newly launched EC2
ssh -i [key-pair-name].pem ec2-user@[public-dns]

# Update yum and install Python 3.6 and pip
sudo yum update
sudo yum list | grep python3
sudo yum install python36 python36-pip
curl -O https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py --user

# Install Pillow
pip3 install Pillow --user

# Package and zip Pillow
mkdir package
cd ./.local/lib/python3.6/site-packages
mv -v PIL ~/package/
mv -v Pillow-6.2.1.dist-info ~/package/
cd ~
cd ~/package/
zip -r9 ${OLDPWD}/function.zip .

# Exit SSH and copy zip to your local
scp -i key-pair-name].pem ec2-user@[public-dns]:/home/ec2-user/function.zip ~/Desktop/
```

Finally, add the function code and files to the Pillow package zip.

## References

* https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html
* https://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html#python-package-dependencies