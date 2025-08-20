#!/usr/bin/env python3
"""
Matrix Pentesting Backend Server
Comprehensive backend API for all pentesting operations
"""

import os
import sys
import asyncio
import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from concurrent.futures import ThreadPoolExecutor
import logging

# FastAPI and async components
from fastapi import FastAPI, HTTPException, BackgroundTasks, WebSocket, WebSocketDisconnect, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, Field, validator
import uvicorn

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

# Import all pentesting modules
from src.module_manager import get_module_manager
from src.reconnaissance import ReconnaissanceModule
from src.vulnerability_scanner import VulnerabilityScanner
from src.service_analyzer import ServiceAnalyzer
from src.exploit_module import ExploitModule
from src.payload_generator import PayloadGenerator
from src.network_assessor import NetworkAssessor
from src.web_assessor import WebAssessor
from src.mobile_assessor import MobileAssessor
from src.wireless_assessor import WirelessAssessor
from src.cloud_assessor import CloudAssessor
from src.iot_assessor import IoTAssessor
from src.social_engineering import SocialEngineer
from src.report_generator import ReportGenerator
from src.agentic_ai import AgenticPentestAI
from src.config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('backend_server.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Matrix Pentesting Backend API",
    description="Comprehensive backend for cybersecurity pentesting operations",
    version="2.0.0"
)

# Configure CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Thread pool for async execution
executor = ThreadPoolExecutor(max_workers=10)

# Active tasks storage
active_tasks: Dict[str, Dict[str, Any]] = {}

# WebSocket connections for real-time updates
active_connections: List[WebSocket] = []


# ============= Pydantic Models =============

class PentestRequest(BaseModel):
    """Base request model for pentesting operations"""
    test_type: str = Field(..., description="Type of pentest to perform")
    target: str = Field(..., description="Target for testing (IP/Domain/URL/File)")
    parameters: Dict[str, Any] = Field(default={}, description="Additional parameters")
    async_execution: bool = Field(default=False, description="Execute asynchronously")
    
    @validator('test_type')
    def validate_test_type(cls, v):
        valid_types = [
            'network_scan', 'reconnaissance', 'vulnerability_scan',
            'web_test', 'exploitation', 'payload_generation',
            'mobile_test', 'wireless_test', 'cloud_assessment',
            'iot_analysis', 'social_engineering', 'ai_analysis',
            'service_analysis', 'report_generation'
        ]
        if v not in valid_types:
            raise ValueError(f"Invalid test type. Must be one of: {valid_types}")
        return v


class TaskResponse(BaseModel):
    """Response model for task creation"""
    task_id: str
    status: str
    message: str
    estimated_time: Optional[int] = None


class ResultResponse(BaseModel):
    """Response model for task results"""
    task_id: str
    status: str
    test_type: str
    target: str
    results: Dict[str, Any]
    timestamp: str
    execution_time: float


class ModuleInfo(BaseModel):
    """Information about available modules"""
    name: str
    category: str
    description: str
    methods: List[str]
    requires_root: bool
    requires_api_keys: List[str]


# ============= Task Management =============

class TaskManager:
    """Manages pentesting task execution"""
    
    def __init__(self):
        self.module_manager = get_module_manager()
        self.tasks = {}
        
    async def execute_task(self, task_id: str, request: PentestRequest):
        """Execute a pentesting task"""
        try:
            # Update task status
            self.update_task_status(task_id, "running", {"progress": 0})
            
            # Route to appropriate handler
            result = await self.route_request(request)
            
            # Update task with results
            self.update_task_status(task_id, "completed", {
                "results": result,
                "completed_at": datetime.now().isoformat()
            })
            
            # Send WebSocket notification
            await self.notify_clients({
                "event": "task_completed",
                "task_id": task_id,
                "results": result
            })
            
            return result
            
        except Exception as e:
            logger.error(f"Task {task_id} failed: {e}")
            self.update_task_status(task_id, "failed", {"error": str(e)})
            
            await self.notify_clients({
                "event": "task_failed",
                "task_id": task_id,
                "error": str(e)
            })
            
            raise
    
    async def route_request(self, request: PentestRequest) -> Dict[str, Any]:
        """Route request to appropriate module"""
        
        handlers = {
            'network_scan': self.handle_network_scan,
            'reconnaissance': self.handle_reconnaissance,
            'vulnerability_scan': self.handle_vulnerability_scan,
            'web_test': self.handle_web_test,
            'exploitation': self.handle_exploitation,
            'payload_generation': self.handle_payload_generation,
            'mobile_test': self.handle_mobile_test,
            'wireless_test': self.handle_wireless_test,
            'cloud_assessment': self.handle_cloud_assessment,
            'iot_analysis': self.handle_iot_analysis,
            'social_engineering': self.handle_social_engineering,
            'ai_analysis': self.handle_ai_analysis,
            'service_analysis': self.handle_service_analysis,
            'report_generation': self.handle_report_generation
        }
        
        handler = handlers.get(request.test_type)
        if not handler:
            raise ValueError(f"Unknown test type: {request.test_type}")
        
        # Execute in thread pool for non-blocking
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            executor,
            handler,
            request.target,
            request.parameters
        )
        
        return self.filter_results(result, request)
    
    def filter_results(self, results: Dict[str, Any], request: PentestRequest) -> Dict[str, Any]:
        """Filter results to only include relevant data based on user input"""
        filtered = {
            "target": request.target,
            "test_type": request.test_type,
            "timestamp": datetime.now().isoformat(),
            "summary": {}
        }
        
        # Extract only the most relevant information
        if request.test_type == 'reconnaissance':
            filtered["summary"] = {
                "subdomains": len(results.get("subdomains", [])),
                "open_ports": self._extract_ports(results),
                "technologies": results.get("technologies", [])[:5],
                "emails": len(results.get("osint_data", {}).get("emails", [])),
                "key_findings": self._extract_key_findings(results)
            }
            filtered["details"] = {
                "subdomains": results.get("subdomains", [])[:10],
                "ports": self._extract_ports(results, detailed=True)
            }
            
        elif request.test_type == 'vulnerability_scan':
            filtered["summary"] = {
                "total_vulnerabilities": results.get("summary", {}).get("total_vulnerabilities", 0),
                "critical": results.get("summary", {}).get("severity_breakdown", {}).get("critical", 0),
                "high": results.get("summary", {}).get("severity_breakdown", {}).get("high", 0),
                "top_vulnerabilities": self._extract_top_vulnerabilities(results)
            }
            filtered["vulnerabilities"] = self._extract_top_vulnerabilities(results, limit=10)
            
        elif request.test_type == 'web_test':
            filtered["summary"] = {
                "security_headers": results.get("security_headers", {}),
                "vulnerabilities_found": len(results.get("vulnerabilities", [])),
                "forms_detected": len(results.get("forms", [])),
                "cookies_analyzed": len(results.get("cookies", []))
            }
            filtered["critical_findings"] = results.get("vulnerabilities", [])[:5]
            
        else:
            # Generic filtering for other types
            filtered["summary"] = self._create_generic_summary(results)
            filtered["key_data"] = self._extract_key_data(results)
        
        return filtered
    
    def _extract_ports(self, results: Dict, detailed: bool = False) -> Union[int, List[Dict]]:
        """Extract port information from scan results"""
        ports = []
        nmap_scan = results.get("nmap_scan", {})
        
        for host, host_data in nmap_scan.get("hosts", {}).items():
            for protocol, port_list in host_data.get("protocols", {}).items():
                for port, port_info in port_list.items():
                    if detailed:
                        ports.append({
                            "port": port,
                            "service": port_info.get("service", "unknown"),
                            "state": port_info.get("state", "open")
                        })
                    else:
                        ports.append(port)
        
        return ports if detailed else len(ports)
    
    def _extract_key_findings(self, results: Dict) -> List[str]:
        """Extract key findings from results"""
        findings = []
        
        if results.get("subdomains"):
            findings.append(f"Found {len(results['subdomains'])} subdomains")
        
        if results.get("nmap_scan", {}).get("hosts"):
            findings.append(f"Discovered {len(results['nmap_scan']['hosts'])} hosts")
        
        if results.get("osint_data", {}).get("emails"):
            findings.append(f"Found {len(results['osint_data']['emails'])} email addresses")
        
        return findings[:5]
    
    def _extract_top_vulnerabilities(self, results: Dict, limit: int = 5) -> List[Dict]:
        """Extract top vulnerabilities from scan results"""
        vulns = []
        
        for source in ['nuclei_results', 'nikto_results', 'sqlmap_results']:
            if source in results:
                for vuln in results[source][:limit]:
                    vulns.append({
                        "name": vuln.get("name", "Unknown"),
                        "severity": vuln.get("severity", "info"),
                        "description": vuln.get("description", "")[:100]
                    })
        
        return vulns[:limit]
    
    def _create_generic_summary(self, results: Dict) -> Dict:
        """Create a generic summary for any result type"""
        summary = {
            "total_items": len(results) if isinstance(results, (list, dict)) else 1,
            "data_types": list(results.keys()) if isinstance(results, dict) else ["list"],
            "status": "completed"
        }
        return summary
    
    def _extract_key_data(self, results: Dict) -> Any:
        """Extract key data from generic results"""
        if isinstance(results, dict):
            # Return first 5 key-value pairs
            return dict(list(results.items())[:5])
        elif isinstance(results, list):
            # Return first 5 items
            return results[:5]
        else:
            return results
    
    def update_task_status(self, task_id: str, status: str, data: Dict = None):
        """Update task status"""
        if task_id not in active_tasks:
            active_tasks[task_id] = {}
        
        active_tasks[task_id].update({
            "status": status,
            "updated_at": datetime.now().isoformat(),
            **(data or {})
        })
    
    async def notify_clients(self, message: Dict):
        """Send WebSocket notifications to connected clients"""
        for connection in active_connections:
            try:
                await connection.send_json(message)
            except:
                # Remove dead connections
                active_connections.remove(connection)
    
    # ============= Module Handlers =============
    
    def handle_reconnaissance(self, target: str, params: Dict) -> Dict:
        """Handle reconnaissance requests"""
        recon = ReconnaissanceModule()
        return recon.scan_target(target)
    
    def handle_network_scan(self, target: str, params: Dict) -> Dict:
        """Handle network scanning requests"""
        assessor = NetworkAssessor()
        mode = params.get("mode", "external")
        return assessor.scan(target, mode)
    
    def handle_vulnerability_scan(self, target: str, params: Dict) -> Dict:
        """Handle vulnerability scanning requests"""
        scanner = VulnerabilityScanner()
        scan_type = params.get("scan_type", "quick")
        return scanner.scan_target(target, scan_type)
    
    def handle_web_test(self, target: str, params: Dict) -> Dict:
        """Handle web application testing"""
        assessor = WebAssessor()
        tools = params.get("tools", ["nuclei", "nikto"])
        return assessor.scan(target, tools=tools)
    
    def handle_exploitation(self, target: str, params: Dict) -> Dict:
        """Handle exploitation requests"""
        exploit = ExploitModule()
        vulnerability = params.get("vulnerability", {})
        return exploit.exploit_vulnerability(target, vulnerability)
    
    def handle_payload_generation(self, target: str, params: Dict) -> Dict:
        """Handle payload generation requests"""
        generator = PayloadGenerator()
        payload_type = params.get("payload_type", "reverse_shell")
        platform = params.get("platform", "linux")
        options = params.get("options", {})
        
        return {
            "payloads": generator.generate_custom_payloads(payload_type, platform, options),
            "recommendations": generator.generate_recommendations(None, [])
        }
    
    def handle_mobile_test(self, target: str, params: Dict) -> Dict:
        """Handle mobile application testing"""
        assessor = MobileAssessor()
        
        if target.endswith('.apk'):
            return assessor.analyze_apk(target)
        else:
            return {"error": "Please provide an APK file path"}
    
    def handle_wireless_test(self, target: str, params: Dict) -> Dict:
        """Handle wireless network testing"""
        assessor = WirelessAssessor()
        interface = params.get("interface", "wlan0")
        
        if params.get("action") == "scan":
            return assessor.scan_wifi(interface)
        elif params.get("action") == "capture":
            bssid = params.get("bssid")
            channel = params.get("channel")
            return assessor.capture_handshake(interface, bssid, channel)
        else:
            return assessor.scan_wifi(interface)
    
    def handle_cloud_assessment(self, target: str, params: Dict) -> Dict:
        """Handle cloud infrastructure assessment"""
        assessor = CloudAssessor()
        provider = params.get("provider", "aws")
        profile = params.get("profile")
        
        if provider == "aws":
            return assessor.scout_aws(profile)
        else:
            return {"error": f"Provider {provider} not yet supported"}
    
    def handle_iot_analysis(self, target: str, params: Dict) -> Dict:
        """Handle IoT and firmware analysis"""
        assessor = IoTAssessor()
        return assessor.analyze_firmware(target)
    
    def handle_social_engineering(self, target: str, params: Dict) -> Dict:
        """Handle social engineering campaign planning"""
        engineer = SocialEngineer()
        campaign = params.get("campaign", "phishing")
        sender = params.get("sender", "security@example.com")
        return engineer.plan_phishing(campaign, sender, target)
    
    def handle_ai_analysis(self, target: str, params: Dict) -> Dict:
        """Handle AI-powered analysis"""
        try:
            ai = AgenticPentestAI()
            request = params.get("request", f"Analyze {target}")
            return ai.process_request(request)
        except Exception as e:
            return {"error": f"AI analysis failed: {e}"}
    
    def handle_service_analysis(self, target: str, params: Dict) -> Dict:
        """Handle service analysis"""
        analyzer = ServiceAnalyzer()
        ports = params.get("ports", {})
        return analyzer.analyze_services(target, ports)
    
    def handle_report_generation(self, target: str, params: Dict) -> Dict:
        """Handle report generation"""
        generator = ReportGenerator()
        
        # Gather data from previous scans if available
        recon_data = params.get("recon_data", {})
        vuln_data = params.get("vuln_data", {})
        exploit_data = params.get("exploit_data", {})
        
        report = generator.generate_comprehensive_report(
            target, recon_data, vuln_data, exploit_data
        )
        
        # Save report
        output_dir = Path(Config.OUTPUT_DIR)
        report_file = generator.save_json_report(report, output_dir)
        
        return {
            "report": report,
            "file_path": str(report_file)
        }


# Initialize task manager
task_manager = TaskManager()


# ============= API Endpoints =============

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "Matrix Pentesting Backend API",
        "version": "2.0.0",
        "status": "operational",
        "endpoints": [
            "/docs",
            "/modules",
            "/execute",
            "/task/{task_id}",
            "/tasks",
            "/ws"
        ]
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "active_tasks": len(active_tasks),
        "connected_clients": len(active_connections)
    }


@app.get("/modules", response_model=List[ModuleInfo])
async def get_modules(category: Optional[str] = Query(None)):
    """Get available modules and their capabilities"""
    manager = get_module_manager()
    
    modules = manager.list_modules(category)
    
    return [
        ModuleInfo(
            name=m.name,
            category=m.category,
            description=m.description,
            methods=[method["name"] for method in manager.get_module_methods(m.name)][:5],
            requires_root=m.requires_root,
            requires_api_keys=m.requires_api_keys
        )
        for m in modules
    ]


@app.post("/execute", response_model=TaskResponse)
async def execute_pentest(
    request: PentestRequest,
    background_tasks: BackgroundTasks
):
    """Execute a pentesting task"""
    # Generate task ID
    task_id = str(uuid.uuid4())
    
    # Initialize task
    active_tasks[task_id] = {
        "task_id": task_id,
        "status": "pending",
        "test_type": request.test_type,
        "target": request.target,
        "created_at": datetime.now().isoformat()
    }
    
    # Execute task
    if request.async_execution:
        # Run in background
        background_tasks.add_task(
            task_manager.execute_task,
            task_id,
            request
        )
        
        return TaskResponse(
            task_id=task_id,
            status="started",
            message="Task started in background",
            estimated_time=60
        )
    else:
        # Run synchronously
        try:
            await task_manager.execute_task(task_id, request)
            return TaskResponse(
                task_id=task_id,
                status="completed",
                message="Task completed successfully"
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


@app.get("/task/{task_id}", response_model=ResultResponse)
async def get_task_result(task_id: str):
    """Get task results"""
    if task_id not in active_tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = active_tasks[task_id]
    
    if task["status"] != "completed":
        raise HTTPException(
            status_code=202,
            detail=f"Task is {task['status']}"
        )
    
    return ResultResponse(
        task_id=task_id,
        status=task["status"],
        test_type=task["test_type"],
        target=task["target"],
        results=task.get("results", {}),
        timestamp=task["created_at"],
        execution_time=0  # Calculate from timestamps
    )


@app.get("/tasks")
async def list_tasks(
    status: Optional[str] = Query(None),
    limit: int = Query(10, le=100)
):
    """List all tasks"""
    tasks = list(active_tasks.values())
    
    if status:
        tasks = [t for t in tasks if t.get("status") == status]
    
    # Sort by creation time
    tasks.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    
    return tasks[:limit]


@app.delete("/task/{task_id}")
async def cancel_task(task_id: str):
    """Cancel a running task"""
    if task_id not in active_tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = active_tasks[task_id]
    
    if task["status"] == "running":
        task["status"] = "cancelled"
        return {"message": "Task cancelled"}
    else:
        return {"message": f"Task is {task['status']}, cannot cancel"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await websocket.accept()
    active_connections.append(websocket)
    
    try:
        # Send initial connection message
        await websocket.send_json({
            "event": "connected",
            "message": "Connected to Matrix Pentesting Backend"
        })
        
        # Keep connection alive and handle messages
        while True:
            data = await websocket.receive_text()
            
            # Handle ping/pong
            if data == "ping":
                await websocket.send_text("pong")
            else:
                # Process other messages
                try:
                    message = json.loads(data)
                    # Handle different message types
                    if message.get("type") == "subscribe":
                        task_id = message.get("task_id")
                        await websocket.send_json({
                            "event": "subscribed",
                            "task_id": task_id
                        })
                except json.JSONDecodeError:
                    await websocket.send_json({
                        "event": "error",
                        "message": "Invalid JSON"
                    })
                    
    except WebSocketDisconnect:
        active_connections.remove(websocket)


@app.post("/batch")
async def execute_batch(
    requests: List[PentestRequest],
    background_tasks: BackgroundTasks
):
    """Execute multiple pentesting tasks in batch"""
    task_ids = []
    
    for request in requests:
        task_id = str(uuid.uuid4())
        active_tasks[task_id] = {
            "task_id": task_id,
            "status": "pending",
            "test_type": request.test_type,
            "target": request.target,
            "created_at": datetime.now().isoformat()
        }
        
        background_tasks.add_task(
            task_manager.execute_task,
            task_id,
            request
        )
        
        task_ids.append(task_id)
    
    return {
        "message": f"Started {len(task_ids)} tasks",
        "task_ids": task_ids
    }


@app.get("/export/{task_id}")
async def export_results(
    task_id: str,
    format: str = Query("json", regex="^(json|html|pdf)$")
):
    """Export task results in different formats"""
    if task_id not in active_tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = active_tasks[task_id]
    
    if task["status"] != "completed":
        raise HTTPException(
            status_code=400,
            detail="Task not completed"
        )
    
    # Generate report
    generator = ReportGenerator()
    report_data = {
        "task_id": task_id,
        "target": task["target"],
        "test_type": task["test_type"],
        "results": task.get("results", {}),
        "timestamp": task["created_at"]
    }
    
    if format == "json":
        return JSONResponse(content=report_data)
    elif format == "html":
        # Generate HTML report
        html_content = generator._generate_html_content(report_data)
        return StreamingResponse(
            io.BytesIO(html_content.encode()),
            media_type="text/html",
            headers={"Content-Disposition": f"attachment; filename=report_{task_id}.html"}
        )
    else:
        raise HTTPException(status_code=501, detail="Format not implemented")


# ============= Error Handlers =============

@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"error": str(exc)}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )


# ============= Startup/Shutdown =============

@app.on_event("startup")
async def startup_event():
    """Initialize backend on startup"""
    logger.info("Matrix Pentesting Backend starting...")
    
    # Create output directories
    Config.create_output_dirs()
    
    # Initialize module manager
    manager = get_module_manager()
    logger.info(f"Loaded {len(manager.modules)} modules")
    
    logger.info("Backend ready to accept requests")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Matrix Pentesting Backend shutting down...")
    
    # Cancel all running tasks
    for task_id, task in active_tasks.items():
        if task.get("status") == "running":
            task["status"] = "cancelled"
    
    # Close WebSocket connections
    for connection in active_connections:
        await connection.close()
    
    logger.info("Shutdown complete")


# ============= Main Entry Point =============

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Matrix Pentesting Backend Server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")
    parser.add_argument("--workers", type=int, default=1, help="Number of workers")
    
    args = parser.parse_args()
    
    # Run server
    uvicorn.run(
        "backend_server:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        workers=args.workers,
        log_level="info"
    )
