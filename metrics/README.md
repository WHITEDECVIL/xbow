# XBOW Metrics Directory

This directory contains performance metrics, analytics, and statistical data from XBOW scan operations.

## Metrics Files

### Performance Metrics
- `scan_performance_[timestamp].json` - Per-scan performance data
- `aggregate_performance.json` - Aggregated performance statistics
- `bottleneck_analysis.json` - Performance bottleneck identification

### Scan Statistics
- `scan_statistics_[timestamp].json` - Per-scan statistics
- `vulnerability_statistics.json` - Vulnerability trend analysis
- `scan_duration_stats.json` - Scan duration analytics

### Resource Metrics
- `cpu_usage_[timestamp].json` - CPU utilization during scans
- `memory_usage_[timestamp].json` - Memory usage patterns
- `network_traffic_[timestamp].json` - Network bandwidth metrics

### Trend Analysis
- `weekly_trends.json` - Weekly aggregated metrics
- `monthly_trends.json` - Monthly aggregated metrics
- `vulnerability_trends.json` - Vulnerability discovery trends

## Metrics Format

```json
{
  "timestamp": "2026-03-03T14:23:45Z",
  "scan_id": "scan_20260303_142345",
  "metrics": {
    "total_duration_seconds": 1234,
    "scan_rate_targets_per_second": 42.3,
    "total_hosts_scanned": 512,
    "total_ports_scanned": 524288,
    "vulnerabilities_found": 47,
    "avg_response_time_ms": 234.5,
    "cpu_usage_percent": 65.4,
    "memory_usage_mb": 512.3,
    "success_rate_percent": 98.7
  }
}
```

## Retention Policy

- Raw metrics: 90 days
- Weekly aggregates: 1 year
- Monthly aggregates: 3 years
- Archive: 7 years (for compliance)

## Analysis Tools

Metrics can be analyzed using:
- Statistical tools (mean, median, std dev)
- Time-series analysis
- Trend detection
- Anomaly detection
- Comparative analysis

