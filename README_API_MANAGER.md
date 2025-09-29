# 🚀 Robust OpenRouter API Key Management System

This system provides a bulletproof solution for managing multiple OpenRouter API keys with automatic failover, intelligent retry logic, and seamless user experience.

## ✨ Features

### 🔄 **Automatic Failover**
- Seamlessly switches between API keys when one fails
- Intelligent key selection based on performance metrics
- No user-facing delays or errors when keys fail

### 🛡️ **Circuit Breaker Pattern**
- Automatically disables failing keys to prevent cascading failures
- Configurable failure thresholds and timeout periods
- Automatic recovery when keys become healthy again

### ⚡ **Response Caching**
- Reduces API calls by caching identical requests
- Configurable cache TTL (Time To Live)
- Automatic cache cleanup of expired entries

### 📊 **Performance Monitoring**
- Tracks success rates for each API key
- Monitors response times and failure patterns
- Comprehensive statistics and health metrics

### 🔍 **Rate Limit Handling**
- Detects rate limiting and automatically switches keys
- Respects `Retry-After` headers from API responses
- Predictive rate limit avoidance

### 🎯 **Smart Retry Logic**
- Exponential backoff with jitter to avoid thundering herd
- Configurable retry attempts and timeouts
- Different handling for different types of failures

## 🏗️ System Architecture

```
┌─────────────────┐    ┌─────────────────────┐    ┌─────────────────┐
│   Discord Bot   │───▶│ RobustAPIManager    │───▶│  OpenRouter API │
│   (app.py)      │    │ (api_manager.py)    │    │                 │
└─────────────────┘    └─────────────────────┘    └─────────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Performance Stats  │
                    │  • Success rates    │
                    │  • Response times   │
                    │  • Failure counts   │
                    │  • Circuit states   │
                    └─────────────────────┘
```

## 🛠️ Configuration

The system is configured in your Discord bot with these parameters:

```python
self.api_manager = RobustOpenRouterManager(
    api_keys=OPENROUTER_API_KEYS,           # List of your API keys
    model=OPENROUTER_MODEL,                 # Model to use
    cache_ttl=300,                          # Cache for 5 minutes
    circuit_breaker_threshold=3,            # Open circuit after 3 failures
    circuit_breaker_timeout=60,             # 1 minute timeout
    max_retries=3,                          # Try up to 3 times
    request_timeout=30                      # 30 second timeout per request
)
```

### Configuration Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `cache_ttl` | 300 | Cache lifetime in seconds |
| `circuit_breaker_threshold` | 3 | Failures before opening circuit |
| `circuit_breaker_timeout` | 60 | Circuit open time in seconds |
| `max_retries` | 3 | Maximum retry attempts |
| `request_timeout` | 30 | Request timeout in seconds |

## 📝 Usage

### Basic Usage in Discord Commands

```python
# Make a robust API request
response = await bot.api_manager.make_request(
    messages=messages,
    use_cache=True,
    max_tokens=1000
)
```

### Admin Commands

The system includes these admin-only Discord commands:

- `/api_stats` - View comprehensive API performance statistics
- `/reset_api` - Reset circuit breakers for all API keys
- `/clear_cache` - Clear the response cache

## 📊 Monitoring and Statistics

### API Key States

- **🟢 Healthy**: Key is working normally
- **⏳ Rate Limited**: Key has hit rate limits
- **❌ Failed**: Key has experienced failures
- **🚫 Circuit Open**: Key is temporarily disabled due to failures

### Performance Metrics

- **Success Rate**: Percentage of successful requests
- **Average Response Time**: Mean response time for the key
- **Consecutive Failures**: Number of recent failures in a row
- **Total Requests**: Total number of requests made with this key

## 🔧 Error Handling

The system handles multiple types of errors:

### Network Errors
- Connection timeouts
- DNS resolution failures
- SSL certificate errors

### API Errors
- Rate limiting (HTTP 429)
- Authentication failures (HTTP 401)
- Server errors (HTTP 5xx)
- Invalid requests (HTTP 4xx)

### Retry Strategy
1. **First failure**: Immediate retry with next key
2. **Second failure**: 2-second delay + retry
3. **Third failure**: 4-second delay + retry
4. **All keys failed**: Return error to user

## 🚀 Benefits

### For Users
- **Zero downtime**: Automatic failover means users never see API failures
- **Fast responses**: Caching makes common queries instant
- **Reliable service**: Multiple backups ensure high availability

### For Administrators
- **Full visibility**: Comprehensive monitoring of API performance
- **Easy management**: Simple admin commands for maintenance
- **Cost optimization**: Caching reduces API usage and costs

### For Developers
- **Simple integration**: Drop-in replacement for basic API calls
- **Async-first**: Built for modern Python async/await patterns
- **Extensible**: Easy to customize for different use cases

## 🧪 Testing

Run the test script to verify everything works:

```bash
python test_api_manager.py
```

This will test:
- Basic API requests
- Caching functionality
- Concurrent request handling
- Error handling with invalid keys
- Performance statistics

## 📁 Files

- `api_manager.py` - Core robust API manager
- `app.py` - Updated Discord bot with integrated manager
- `test_api_manager.py` - Test script for verification
- `README_API_MANAGER.md` - This documentation

## 🔐 Security

- API keys are never logged or exposed in error messages
- All sensitive data is handled securely
- Circuit breaker prevents API key abuse
- Rate limiting respects API provider limits

## 🚦 Status Indicators

The system provides visual status indicators in Discord:

- ✅ **All systems healthy**
- 🟡 **Some keys rate limited but system operational**
- 🔴 **Multiple failures detected**
- 🚫 **Critical: All keys unavailable**

This robust system ensures your Discord bot provides a seamless experience for users while efficiently managing multiple API keys behind the scenes!
