################################################################################
# Module: network-interface
################################################################################

resource "aws_network_interface" "eni" {

  subnet_id       = var.subnet_id
  security_groups = var.security_group_ids
  private_ips     = var.private_ips

  tags = merge(var.tags, {
    Name = "${var.project}-${var.environment}-eni"
  })
}

resource "aws_eip" "eni_eip" {

  count = var.create_eip ? 1 : 0

  domain            = "vpc"
  network_interface = aws_network_interface.eni.id

  depends_on = [aws_network_interface.eni]
}