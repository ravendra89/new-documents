resource "aws_instance" "main" {

  ami           = var.ami_id
  instance_type = var.instance_type
  key_name      = var.key_name

  network_interface {
    network_interface_id = var.eni_id
    device_index         = 0
  }

  root_block_device {
    volume_size = var.root_volume_size
    volume_type = "gp3"
  }

  user_data = var.user_data

  tags = merge(var.tags, {
    Name = "${var.project}-${var.environment}-${var.name_suffix}"
  })
}

resource "aws_ebs_volume" "extra" {

  count = length(var.extra_ebs_volumes)

  availability_zone = aws_instance.main.availability_zone
  size              = var.extra_ebs_volumes[count.index]

  tags = merge(var.tags, {
    Name = "${var.project}-extra-ebs-${count.index + 1}"
  })
}

resource "aws_volume_attachment" "extra_attach" {

  count = length(var.extra_ebs_volumes)

  device_name = "/dev/sd${element(["f","g","h"], count.index)}"
  volume_id   = aws_ebs_volume.extra[count.index].id
  instance_id = aws_instance.main.id
}