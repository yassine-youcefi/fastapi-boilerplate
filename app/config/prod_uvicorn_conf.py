# Logging configuration
log_level = "warning"  # Minimized log level to avoid verbosity
access_log = False  # Disabling access logs in production to reduce I/O
error_log = True  # Enable error logs to capture any issues

# Performance settings
workers = 4
reload = False  # Disable hot-reloading in production

# Timeout settings
timeout_keep_alive = 5  # Seconds before closing idle connections

# Network settings
host = "0.0.0.0"  # Bind to all interfaces for external access (common in production)
port = 8000  # Default port, adjust if necessary
