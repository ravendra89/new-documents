resource "datadog_dashboard" "azure_monitoring" {
  title       = local.name_prefix
  description = "Datadog Dashboard For Client ${var.client_name}"
  layout_type = "ordered"
  tags        = ["team:teamname"]

# Pingdom Uptime
  widget {
    timeseries_definition {
      title       = "Pingdom Uptime"
      show_legend = true
      request {
        q             = "avg:pingdom.uptime{${lower(var.client_name)}} by {check}"
        display_type = "line"
      }
    }
  }

# App Services Health Check Status
widget {
  timeseries_definition {
    title       = "App Services Health Check Status"
    show_legend = true
    request {
      q            = "avg:azure.app_services.health_check_status{subscription_name:${var.subscription_name},monitoring:datadog} by {name}"
      display_type = "line"
    }
  }
}

# App Services Response Time
widget {
  timeseries_definition {
    title       = "App Services Response Time"
    show_legend = true
    request {
      q            = "avg:azure.app_services.response_time{subscription_name:${var.subscription_name},monitoring:datadog} by {name}"
      display_type = "line"
    }
  }
}

# App Services High Request Count
  widget {
    timeseries_definition {
      title       = "App Services High Request Count"
      show_legend = true
      request {
        q            = "sum:azure.app_services.requests{subscription_name:${var.subscription_name},monitoring:datadog} by {name}.as_count()"
        display_type = "line"
      }
    }
  }

# App Service Plan Instance Count
  widget {
    timeseries_definition {
      title       = "App Service Plan instance count"
      show_legend = true
      request {
        q            = "avg:azure.web_serverfarms.current_instance_count{subscription_name:${var.subscription_name},monitoring:datadog} by {name}"
        display_type = "line"
      }
    }
  }

# App Services HTTP 5xx Errors
  widget {
    timeseries_definition {
      title       = "App Services HTTP 5xx Errors"
      show_legend = true
      request {
        q            = "sum:azure.app_services.http5xx{subscription_name:${var.subscription_name},monitoring:datadog} by {name}.as_count()"
        display_type = "line"
      }
    }
  }

# App Service Plan CPU Usage
  widget {
    timeseries_definition {
      title       = "App Service Plan CPU Usage"
      show_legend = true
      request {
        q            = "avg:azure.web_serverfarms.cpu_percentage{subscription_name:${var.subscription_name},monitoring:datadog} by {name}"
        display_type = "line"
      }
    }
  }

# App Service Plan Memory Usage
  widget {
    timeseries_definition {
      title       = "App Service Plan Memory Usage"
      show_legend = true
      request {
        q            = "avg:azure.web_serverfarms.memory_percentage{subscription_name:${var.subscription_name},monitoring:datadog} by {name}"
        display_type = "line"
      }
    }
  }

# Azure SQL Database CPU Usage
  widget {
    timeseries_definition {
      title       = "Azure SQL Database CPU Usage"
      show_legend = true
      request {
        q            = "max:azure.sql_servers_databases.cpu_percent{subscription_name:${var.subscription_name},monitoring:datadog} by {name}"
        display_type = "line"
      }
    }
  }

# Azure SQL Database Storage Usage
  widget {
    timeseries_definition {
      title       = "Azure SQL Database Storage Usage"
      show_legend = true
      request {
        q            = "avg:azure.sql_servers_databases.storage_percent{subscription_name:${var.subscription_name},monitoring:datadog} by {name}"
        display_type = "line"
      }
    }
  }

# Azure SQL Elastic Pool CPU Usage
  widget {
    timeseries_definition {
      title       = "Azure SQL Elastic Pool CPU Usage"
      show_legend = true
      request {
        q            = "max:azure.sql_servers_elasticpools.cpu_percent{subscription_name:${var.subscription_name},monitoring:datadog} by {name}"
        display_type = "line"
      }
    }
  }

# Azure SQL Elastic Pool Memory Usage
  widget {
    timeseries_definition {
      title       = "Azure SQL Elastic Pool Memory Usage"
      show_legend = true
      request {
        q            = "avg:azure.sql_servers_elasticpools.sql_instance_memory_percent{subscription_name:${var.subscription_name},monitoring:datadog} by {name}"
        display_type = "line"
      }
    }
  }

# Azure SQL Elastic Pool Storage Usage
  widget {
    timeseries_definition {
      title       = "Azure SQL Elastic Pool Storage Usage"
      show_legend = true
      request {
        q            = "avg:azure.sql_servers_elasticpools.storage_percent{subscription_name:${var.subscription_name},monitoring:datadog} by {name}"
        display_type = "line"
      }
    }
  }
# Azure VM Availability Count
widget {
  timeseries_definition {
    title       = "Azure VM Availability Count"
    show_legend = true
    request {
      q            = "sum:azure.vm.vm_availability_metric_preview{subscription_name:${var.subscription_name},monitoring:datadog} by {host}.as_count()"
      display_type = "line"
    }
  }
}

# Azure VM CPU Usage
widget {
  timeseries_definition {
    title       = "Azure VM CPU Usage"
    show_legend = true
    request {
      q            = "avg:azure.vm.percentage_cpu{subscription_name:${var.subscription_name},monitoring:datadog} by {host}"
      display_type = "line"
    }
  }
}

# Azure VM Available Memory
widget {
  timeseries_definition {
    title       = "Azure VM Available Memory"
    show_legend = true
    request {
      q            = "avg:azure.vm.available_memory_percentage{subscription_name:${var.subscription_name},monitoring:datadog} by {host}"
      display_type = "line"
    }
  }
}

# Azure VM Disk Usage
widget {
  timeseries_definition {
    title       = "Azure VM Disk Usage"
    show_legend = true
    request {
      q            = "avg:system.disk.in_use{subscription_name:${var.subscription_name},monitoring:datadog} by {host,device}"
      display_type = "line"
    }
  }
}

# Azure Redis Cache CPU Usage
widget {
  timeseries_definition {
    title       = "Azure Redis Cache CPU Usage"
    show_legend = true
    request {
      q            = "avg:azure.cache_redis.percent_processor_time{subscription_name:${var.subscription_name},monitoring:datadog} by {name}"
      display_type = "line"
    }
  }
}

# Azure Redis Cache Memory Usage
widget {
  timeseries_definition {
    title       = "Azure Redis Cache Memory Usage"
    show_legend = true
    request {
      q            = "avg:azure.cache_redis.usedmemorypercentage{subscription_name:${var.subscription_name},monitoring:datadog} by {name}"
      display_type = "line"
    }
  }
  }
}

