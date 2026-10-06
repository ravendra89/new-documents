module "vpc" {
  source = "./modules/vpc"

  project              = var.project
  environment          = var.environment
  tags                 = var.tags
  vpc_cidr             = var.vpc_cidr
  availability_zones   = var.availability_zones
  public_subnet_cidrs  = var.public_subnet_cidrs
  private_subnet_cidrs = var.private_subnet_cidrs
  enable_nat_gateway   = var.enable_nat_gateway
}

module "sg" {
  source = "./modules/security-group"

  project     = var.project
  environment = var.environment
  tags        = var.tags
  vpc_id      = module.vpc.vpc_id      # runtime

  # All port values come from tfvars
  ssh_port         = var.ssh_port
  http_port        = var.http_port
  https_port       = var.https_port
  app_port         = var.app_port
  ssh_allowed_cidr = var.ssh_allowed_cidr
  vpc_cidr         = var.vpc_cidr
}

module "eni" {
  source = "./modules/network-interface"

  project            = var.project
  environment        = var.environment
  tags               = var.tags
  subnet_id          = module.vpc.public_subnet_1_id  # runtime
  security_group_ids = [module.sg.sg_id]              # runtime
  private_ips        = var.eni_private_ips
  create_eip         = var.create_eip
}

module "ec2" {
  source = "./modules/ec2"

  project                    = var.project
  environment                = var.environment
  tags                       = var.tags
  name_suffix                = var.name_suffix
  ami_id                     = var.ami_id
  instance_type              = var.instance_type
  key_name                   = var.key_name
  eni_id                     = module.eni.eni_id       # runtime
  root_volume_size           = var.root_volume_size
  extra_ebs_volumes          = var.extra_ebs_volumes
  user_data = file("${path.module}/user_data.sh")
}