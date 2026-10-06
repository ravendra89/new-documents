output "vpc_id"             { value = aws_vpc.this.id }
output "vpc_cidr_block"     { value = aws_vpc.this.cidr_block }
output "igw_id"             { value = aws_internet_gateway.this.id }
output "public_subnet_1_id" { value = aws_subnet.public_1.id }
output "public_subnet_2_id" { value = aws_subnet.public_2.id }
output "private_subnet_1_id" { value = aws_subnet.private_1.id }
output "private_subnet_2_id" { value = aws_subnet.private_2.id }
output "nat_public_ip"      { value = aws_eip.nat.public_ip }