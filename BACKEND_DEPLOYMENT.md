# Matrix Pentesting Backend - Complete Deployment Guide

## 📋 System Architecture

The backend system consists of:
- **FastAPI Backend Server** - REST API and WebSocket server
- **Task Manager** - Asynchronous task execution and management  
- **Module Integration** - 21+ pentesting modules
- **Frontend Integration** - Matrix UI connector
- **Real-time Updates** - WebSocket for live task status

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Install Python packages
pip install --break-system-packages fastapi uvicorn aiohttp websockets pydantic

# Or use requirements file
pip install --break-system-packages -r backend_requirements.txt
```

### 2. Start Backend Server

```bash
# Basic startup
python backend_server.py

# With custom options
python backend_server.py --host 0.0.0.0 --port 8000 --reload

# Production mode with multiple workers
python backend_server.py --host 0.0.0.0 --port 8000 --workers 4
```

### 3. Verify Installation

```bash
# Check API health
curl http://localhost:8000/health

# View API documentation
open http://localhost:8000/docs
```

## 📦 Requirements File

Create `backend_requirements.txt`:

```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
aiohttp==3.9.0
websockets==12.0
python-multipart==0.0.6
rich==13.7.0
click==8.1.7
questionary==2.0.1
pyfiglet==1.0.2
```

## 🔧 Configuration

### Environment Variables

```bash
# API Configuration
export API_HOST="0.0.0.0"
export API_PORT="8000"
export API_WORKERS="4"

# Security
export CORS_ORIGINS="http://localhost:3000,http://localhost:8080"
export API_KEY="your-secret-api-key"

# Module Configuration
export OUTPUT_DIR="/path/to/output"
export LOG_LEVEL="INFO"

# API Keys for modules
export SHODAN_API_KEY="your-shodan-key"
export VIRUSTOTAL_API_KEY="your-vt-key"
```

### Configuration File

Create `backend_config.json`:

```json
{
  "api": {
    "host": "0.0.0.0",
    "port": 8000,
    "workers": 4,
    "reload": false
  },
  "cors": {
    "origins": ["*"],
    "allow_credentials": true,
    "allow_methods": ["*"],
    "allow_headers": ["*"]
  },
  "task_manager": {
    "max_workers": 10,
    "task_timeout": 3600,
    "cleanup_interval": 300
  },
  "modules": {
    "output_dir": "./output",
    "logs_dir": "./logs",
    "reports_dir": "./reports"
  }
}
```

## 🎯 API Endpoints

### Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information |
| `/health` | GET | Health check |
| `/docs` | GET | Interactive API documentation |
| `/modules` | GET | List available modules |
| `/execute` | POST | Execute pentesting task |
| `/task/{task_id}` | GET | Get task results |
| `/tasks` | GET | List all tasks |
| `/task/{task_id}` | DELETE | Cancel task |
| `/batch` | POST | Execute batch tasks |
| `/export/{task_id}` | GET | Export results |
| `/ws` | WebSocket | Real-time updates |

### Test Types

Available test types for `/execute` endpoint:

1. **network_scan** - Network scanning and enumeration
2. **reconnaissance** - Information gathering
3. **vulnerability_scan** - Vulnerability assessment
4. **web_test** - Web application testing
5. **exploitation** - Exploit execution
6. **payload_generation** - Payload creation
7. **mobile_test** - Mobile app analysis
8. **wireless_test** - Wi-Fi security testing
9. **cloud_assessment** - Cloud infrastructure audit
10. **iot_analysis** - IoT/firmware analysis
11. **social_engineering** - Social engineering campaigns
12. **ai_analysis** - AI-powered analysis
13. **service_analysis** - Service identification
14. **report_generation** - Report creation

## 🔌 Frontend Integration

### JavaScript/TypeScript Example

```javascript
// Connect to backend
const API_URL = 'http://localhost:8000';
const WS_URL = 'ws://localhost:8000/ws';

// Execute scan
async function executeScan(testType, target, parameters = {}) {
    const response = await fetch(`${API_URL}/execute`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            test_type: testType,
            target: target,
            parameters: parameters,
            async_execution: true
        })
    });
    
    return await response.json();
}

// WebSocket connection for real-time updates
const ws = new WebSocket(WS_URL);

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    
    if (data.event === 'task_completed') {
        console.log('Task completed:', data.task_id);
        // Update UI with results
        updateMatrixUI(data.results);
    }
};

// Example: Network scan
async function performNetworkScan(target) {
    const result = await executeScan('network_scan', target, {
        mode: 'external'
    });
    
    console.log('Scan started:', result.task_id);
    
    // Poll for results or wait for WebSocket notification
    const taskResult = await waitForTask(result.task_id);
    return taskResult;
}
```

### Python Integration Example

```python
import asyncio
from matrix_frontend_integration import MatrixBackendClient, MatrixUIConnector

async def integrate_with_matrix_ui():
    # Initialize client
    client = MatrixBackendClient()
    await client.connect()
    
    # Connect WebSocket
    await client.connect_websocket()
    
    # Create UI connector
    ui_connector = MatrixUIConnector(client)
    
    # Handle UI request
    ui_request = {
        "target": "192.168.1.0/24",
        "mode": "internal"
    }
    
    result = await ui_connector.handle_ui_request("network_scan", ui_request)
    
    # Wait for completion
    if "task_id" in result:
        final_result = await client.wait_for_task(result["task_id"])
        formatted = ui_connector.format_for_matrix_ui(final_result)
        return formatted
    
    return result

# Run integration
asyncio.run(integrate_with_matrix_ui())
```

## 🔐 Security Considerations

### Authentication (Optional)

Add API key authentication:

```python
# In backend_server.py
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")

@app.post("/execute")
async def execute_pentest(
    request: PentestRequest,
    api_key: str = Depends(api_key_header)
):
    if api_key != os.getenv("API_KEY"):
        raise HTTPException(status_code=403, detail="Invalid API key")
    # ... rest of the function
```

### Rate Limiting

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/execute")
@limiter.limit("10/minute")
async def execute_pentest(request: Request, ...):
    # ... function implementation
```

### HTTPS Configuration

For production, use HTTPS:

```bash
# Generate SSL certificate
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365

# Run with SSL
uvicorn backend_server:app --host 0.0.0.0 --port 8000 \
    --ssl-keyfile=./key.pem --ssl-certfile=./cert.pem
```

## 📊 Monitoring

### Logging

All operations are logged to `backend_server.log`:

```bash
# View logs
tail -f backend_server.log

# Filter by level
grep ERROR backend_server.log
grep "task_id" backend_server.log
```

### Metrics Endpoint

Add Prometheus metrics:

```python
from prometheus_client import Counter, Histogram, generate_latest

# Add metrics
task_counter = Counter('pentest_tasks_total', 'Total pentesting tasks')
task_duration = Histogram('pentest_task_duration_seconds', 'Task duration')

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")
```

## 🐳 Docker Deployment

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    nmap \
    nikto \
    && rm -rf /var/lib/apt/lists/*

# Copy application
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r backend_requirements.txt

# Expose port
EXPOSE 8000

# Run server
CMD ["python", "backend_server.py", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - API_KEY=${API_KEY}
      - SHODAN_API_KEY=${SHODAN_API_KEY}
      - VIRUSTOTAL_API_KEY=${VIRUSTOTAL_API_KEY}
    volumes:
      - ./output:/app/output
      - ./logs:/app/logs
    restart: unless-stopped
    
  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
    
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - backend
```

## 🔄 Production Deployment

### Systemd Service

Create `/etc/systemd/system/pentest-backend.service`:

```ini
[Unit]
Description=Matrix Pentesting Backend
After=network.target

[Service]
Type=exec
User=pentest
WorkingDirectory=/opt/pentesting-backend
Environment="PATH=/usr/local/bin:/usr/bin"
ExecStart=/usr/bin/python3 /opt/pentesting-backend/backend_server.py --host 0.0.0.0 --port 8000 --workers 4
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Nginx Reverse Proxy

```nginx
server {
    listen 80;
    server_name pentest-api.example.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /ws {
        proxy_pass http://127.0.0.1:8000/ws;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
    }
}
```

## 🧪 Testing

### Unit Tests

```python
# test_backend.py
import pytest
from httpx import AsyncClient
from backend_server import app

@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

@pytest.mark.asyncio
async def test_execute_scan():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/execute", json={
            "test_type": "reconnaissance",
            "target": "example.com",
            "async_execution": False
        })
        assert response.status_code == 200
        assert "task_id" in response.json()
```

### Load Testing

```bash
# Install locust
pip install locust

# Run load test
locust -f load_test.py --host=http://localhost:8000
```

## 📈 Performance Optimization

### Caching

Add Redis caching for repeated scans:

```python
import redis
import json

redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

def cache_result(key: str, data: dict, ttl: int = 3600):
    redis_client.setex(key, ttl, json.dumps(data))

def get_cached_result(key: str):
    data = redis_client.get(key)
    return json.loads(data) if data else None
```

### Database Storage

For persistent storage, add database support:

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://user:password@localhost/pentestdb"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

## 🆘 Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Find process using port
   lsof -i :8000
   # Kill process
   kill -9 <PID>
   ```

2. **Module import errors**
   ```bash
   # Verify Python path
   python -c "import sys; print(sys.path)"
   # Add to PYTHONPATH
   export PYTHONPATH=/path/to/project:$PYTHONPATH
   ```

3. **Permission errors**
   ```bash
   # Some modules require root
   sudo python backend_server.py
   ```

4. **WebSocket connection failed**
   - Check firewall settings
   - Verify CORS configuration
   - Ensure WebSocket upgrade headers are passed through proxy

## 📚 API Usage Examples

### cURL Examples

```bash
# List modules
curl http://localhost:8000/modules

# Execute reconnaissance
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{
    "test_type": "reconnaissance",
    "target": "example.com",
    "async_execution": true
  }'

# Get task result
curl http://localhost:8000/task/<task_id>

# Export results
curl http://localhost:8000/export/<task_id>?format=html -o report.html
```

## 📝 Assumptions

1. **Python 3.8+** is installed
2. **Pentesting tools** are installed (nmap, nikto, etc.)
3. **Network access** for scanning targets
4. **File system permissions** for output directories
5. **API keys** configured for certain modules

## 🔗 Integration Points

- **Matrix UI**: WebSocket for real-time updates
- **CLI Interface**: Direct module execution
- **External Tools**: System command execution
- **Reporting**: JSON/HTML export
- **Storage**: File system and optional database

## 📞 Support

For issues or questions:
1. Check API documentation at `/docs`
2. Review logs in `backend_server.log`
3. Test individual modules via CLI
4. Verify network connectivity
5. Ensure all dependencies are installed

---

**Note**: This backend is designed for authorized security testing only. Always ensure you have permission before scanning any systems.
