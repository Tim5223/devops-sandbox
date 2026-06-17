# ── Virtual Cloud Network (VCN) ───────────────────────────────
resource "oci_core_vcn" "sandbox_vcn" {
  compartment_id = var.compartment_ocid
  cidr_block     = "10.0.0.0/16"
  display_name   = "devops-sandbox-vcn"
  dns_label      = "sandboxvcn"
}

# ── Internet Gateway ──────────────────────────────────────────
resource "oci_core_internet_gateway" "sandbox_igw" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.sandbox_vcn.id
  display_name   = "devops-sandbox-igw"
  enabled        = true
}

# ── Route Table ───────────────────────────────────────────────
resource "oci_core_route_table" "sandbox_rt" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.sandbox_vcn.id
  display_name   = "devops-sandbox-rt"

  route_rules {
    destination       = "0.0.0.0/0"
    network_entity_id = oci_core_internet_gateway.sandbox_igw.id
  }
}

# ── Security List (Firewall Rules) ────────────────────────────
resource "oci_core_security_list" "sandbox_sl" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.sandbox_vcn.id
  display_name   = "devops-sandbox-sl"

  # Allow all outbound traffic
  egress_security_rules {
    destination = "0.0.0.0/0"
    protocol    = "all"
  }

  # Allow SSH (port 22)
  ingress_security_rules {
    protocol = "6" # TCP
    source   = "0.0.0.0/0"
    tcp_options {
      min = 22
      max = 22
    }
  }

  # Allow FastAPI (port 8000)
  ingress_security_rules {
    protocol = "6"
    source   = "0.0.0.0/0"
    tcp_options {
      min = 8000
      max = 8000
    }
  }

  # Allow pgAdmin (port 5050)
  ingress_security_rules {
    protocol = "6"
    source   = "0.0.0.0/0"
    tcp_options {
      min = 5050
      max = 5050
    }
  }

  # Allow PostgreSQL (port 5432)
  ingress_security_rules {
    protocol = "6"
    source   = "0.0.0.0/0"
    tcp_options {
      min = 5432
      max = 5432
    }
  }

  # Allow ICMP (ping)
  ingress_security_rules {
    protocol = "1" # ICMP
    source   = "0.0.0.0/0"
  }
}

# ── Subnet ────────────────────────────────────────────────────
resource "oci_core_subnet" "sandbox_subnet" {
  compartment_id    = var.compartment_ocid
  vcn_id            = oci_core_vcn.sandbox_vcn.id
  cidr_block        = "10.0.1.0/24"
  display_name      = "devops-sandbox-subnet"
  dns_label         = "sandboxsubnet"
  route_table_id    = oci_core_route_table.sandbox_rt.id
  security_list_ids = [oci_core_security_list.sandbox_sl.id]
}
