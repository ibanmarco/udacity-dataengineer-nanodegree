data "aws_availability_zones" "available" {
  state = "available"
}

####################################################################
# Bastion host

resource "aws_security_group" "bastion_sg" {
  name   = "${var.project}-bastion-sg"
  vpc_id = var.vpc_id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    description = "SSH access"
    cidr_blocks = [var.cidr_ssh]
  }

  ingress {
    from_port   = 8888
    to_port     = 8888
    protocol    = "tcp"
    description = "Jupyter Notebook access"
    cidr_blocks = [var.cidr_ssh]
  }

  ingress {
    from_port   = 18080
    to_port     = 18080
    protocol    = "tcp"
    description = "Spark History"
    cidr_blocks = [var.cidr_ssh]
  }

  ingress {
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    description = "PostgreSL access"
    cidr_blocks = [var.cidr_ssh]
  }

  ingress {
    from_port   = 5439
    to_port     = 5439
    protocol    = "tcp"
    description = "Redshift access"
    cidr_blocks = [var.cidr_ssh]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}


resource "aws_instance" "bastion" {
  ami               = var.ec2_ami
  availability_zone = data.aws_availability_zones.available.names[0]
  ebs_optimized     = var.ec2_ebs_optimized
  instance_type     = var.ec2_instance_type
  key_name          = "${lower(var.project)}-accesskey"
  monitoring        = var.ec2_monitoring
  subnet_id         = var.public_subnet_id

  vpc_security_group_ids = [
    "${aws_security_group.bastion_sg.id}",
  ]

  tags = {
    Name = "${var.project}-bastion"
  }
}

resource "aws_eip_association" "eip_assoc" {
  instance_id   = aws_instance.bastion.id
  allocation_id = aws_eip.bastion.id
}

resource "aws_eip" "bastion" {
  vpc = true
}
