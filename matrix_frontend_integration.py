#!/usr/bin/env python3
"""
Matrix UI Frontend Integration
Connects the Matrix-style UI with the backend API
"""

import asyncio
import aiohttp
import websockets
import json
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class BackendConfig:
    """Backend connection configuration"""
    api_url: str = "http://localhost:8000"
    ws_url: str = "ws://localhost:8000/ws"
    timeout: int = 30
    retry_attempts: int = 3


class MatrixBackendClient:
    """Client for interacting with the Matrix Pentesting Backend"""
    
    def __init__(self, config: BackendConfig = None):
        """Initialize the backend client
        
        Args:
            config: Backend configuration
        """
        self.config = config or BackendConfig()
        self.session: Optional[aiohttp.ClientSession] = None
        self.ws_connection = None
        self.callbacks: Dict[str, List[Callable]] = {}
        
    async def __aenter__(self):
        """Async context manager entry"""
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.disconnect()
    
    async def connect(self):
        """Establish connection to backend"""
        if not self.session:
            self.session = aiohttp.ClientSession()
        
        # Test connection
        try:
            async with self.session.get(f"{self.config.api_url}/health") as resp:
                if resp.status != 200:
                    raise ConnectionError(f"Backend not healthy: {resp.status}")
                data = await resp.json()
                logger.info(f"Connected to backend: {data}")
        except Exception as e:
            logger.error(f"Failed to connect to backend: {e}")
            raise
    
    async def disconnect(self):
        """Close connections"""
        if self.ws_connection:
            await self.ws_connection.close()
        if self.session:
            await self.session.close()
    
    async def connect_websocket(self):
        """Connect to WebSocket for real-time updates"""
        try:
            self.ws_connection = await websockets.connect(self.config.ws_url)
            
            # Start listening for messages
            asyncio.create_task(self._listen_websocket())
            
            logger.info("WebSocket connected")
            return True
        except Exception as e:
            logger.error(f"WebSocket connection failed: {e}")
            return False
    
    async def _listen_websocket(self):
        """Listen for WebSocket messages"""
        try:
            async for message in self.ws_connection:
                data = json.loads(message)
                await self._handle_ws_message(data)
        except websockets.exceptions.ConnectionClosed:
            logger.info("WebSocket connection closed")
        except Exception as e:
            logger.error(f"WebSocket error: {e}")
    
    async def _handle_ws_message(self, data: Dict[str, Any]):
        """Handle incoming WebSocket message
        
        Args:
            data: Message data
        """
        event = data.get("event")
        
        # Trigger callbacks for this event
        if event in self.callbacks:
            for callback in self.callbacks[event]:
                try:
                    await callback(data)
                except Exception as e:
                    logger.error(f"Callback error for {event}: {e}")
    
    def on_event(self, event: str, callback: Callable):
        """Register event callback
        
        Args:
            event: Event name
            callback: Async callback function
        """
        if event not in self.callbacks:
            self.callbacks[event] = []
        self.callbacks[event].append(callback)
    
    # ============= API Methods =============
    
    async def get_modules(self, category: Optional[str] = None) -> List[Dict]:
        """Get available modules
        
        Args:
            category: Filter by category
            
        Returns:
            List of module information
        """
        params = {}
        if category:
            params["category"] = category
        
        async with self.session.get(
            f"{self.config.api_url}/modules",
            params=params
        ) as resp:
            return await resp.json()
    
    async def execute_scan(
        self,
        test_type: str,
        target: str,
        parameters: Dict[str, Any] = None,
        async_execution: bool = True
    ) -> Dict[str, Any]:
        """Execute a pentesting scan
        
        Args:
            test_type: Type of test to perform
            target: Target for testing
            parameters: Additional parameters
            async_execution: Execute asynchronously
            
        Returns:
            Task response
        """
        payload = {
            "test_type": test_type,
            "target": target,
            "parameters": parameters or {},
            "async_execution": async_execution
        }
        
        async with self.session.post(
            f"{self.config.api_url}/execute",
            json=payload
        ) as resp:
            return await resp.json()
    
    async def get_task_result(self, task_id: str) -> Dict[str, Any]:
        """Get task results
        
        Args:
            task_id: Task ID
            
        Returns:
            Task results
        """
        async with self.session.get(
            f"{self.config.api_url}/task/{task_id}"
        ) as resp:
            if resp.status == 202:
                # Task still running
                return {"status": "running"}
            elif resp.status == 404:
                return {"status": "not_found"}
            else:
                return await resp.json()
    
    async def list_tasks(
        self,
        status: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict]:
        """List tasks
        
        Args:
            status: Filter by status
            limit: Maximum number of tasks
            
        Returns:
            List of tasks
        """
        params = {"limit": limit}
        if status:
            params["status"] = status
        
        async with self.session.get(
            f"{self.config.api_url}/tasks",
            params=params
        ) as resp:
            return await resp.json()
    
    async def cancel_task(self, task_id: str) -> Dict[str, Any]:
        """Cancel a task
        
        Args:
            task_id: Task ID
            
        Returns:
            Cancellation result
        """
        async with self.session.delete(
            f"{self.config.api_url}/task/{task_id}"
        ) as resp:
            return await resp.json()
    
    async def execute_batch(
        self,
        requests: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Execute multiple scans in batch
        
        Args:
            requests: List of scan requests
            
        Returns:
            Batch execution result
        """
        async with self.session.post(
            f"{self.config.api_url}/batch",
            json=requests
        ) as resp:
            return await resp.json()
    
    async def export_results(
        self,
        task_id: str,
        format: str = "json"
    ) -> bytes:
        """Export task results
        
        Args:
            task_id: Task ID
            format: Export format (json, html, pdf)
            
        Returns:
            Exported data
        """
        async with self.session.get(
            f"{self.config.api_url}/export/{task_id}",
            params={"format": format}
        ) as resp:
            return await resp.read()
    
    # ============= Convenience Methods =============
    
    async def quick_scan(self, target: str) -> Dict[str, Any]:
        """Perform a quick reconnaissance scan
        
        Args:
            target: Target to scan
            
        Returns:
            Scan results
        """
        result = await self.execute_scan(
            test_type="reconnaissance",
            target=target,
            async_execution=False
        )
        
        if result.get("status") == "completed":
            task_id = result.get("task_id")
            return await self.get_task_result(task_id)
        
        return result
    
    async def vulnerability_assessment(
        self,
        target: str,
        scan_type: str = "quick"
    ) -> Dict[str, Any]:
        """Perform vulnerability assessment
        
        Args:
            target: Target to scan
            scan_type: Type of scan (quick/comprehensive)
            
        Returns:
            Assessment results
        """
        return await self.execute_scan(
            test_type="vulnerability_scan",
            target=target,
            parameters={"scan_type": scan_type}
        )
    
    async def web_application_test(
        self,
        url: str,
        tools: List[str] = None
    ) -> Dict[str, Any]:
        """Test web application security
        
        Args:
            url: Target URL
            tools: Tools to use
            
        Returns:
            Test results
        """
        return await self.execute_scan(
            test_type="web_test",
            target=url,
            parameters={"tools": tools or ["nuclei", "nikto"]}
        )
    
    async def generate_payloads(
        self,
        payload_type: str,
        platform: str,
        options: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Generate exploitation payloads
        
        Args:
            payload_type: Type of payload
            platform: Target platform
            options: Additional options
            
        Returns:
            Generated payloads
        """
        return await self.execute_scan(
            test_type="payload_generation",
            target=platform,
            parameters={
                "payload_type": payload_type,
                "platform": platform,
                "options": options or {}
            }
        )
    
    async def wait_for_task(
        self,
        task_id: str,
        timeout: int = 300,
        poll_interval: int = 2
    ) -> Dict[str, Any]:
        """Wait for task completion
        
        Args:
            task_id: Task ID
            timeout: Maximum wait time in seconds
            poll_interval: Polling interval in seconds
            
        Returns:
            Task results
        """
        start_time = asyncio.get_event_loop().time()
        
        while (asyncio.get_event_loop().time() - start_time) < timeout:
            result = await self.get_task_result(task_id)
            
            if result.get("status") not in ["running", "pending"]:
                return result
            
            await asyncio.sleep(poll_interval)
        
        raise TimeoutError(f"Task {task_id} did not complete within {timeout} seconds")


class MatrixUIConnector:
    """Connector for Matrix UI to backend integration"""
    
    def __init__(self, backend_client: MatrixBackendClient):
        """Initialize UI connector
        
        Args:
            backend_client: Backend client instance
        """
        self.client = backend_client
        self.active_scans: Dict[str, Dict] = {}
        
    async def handle_ui_request(self, request_type: str, data: Dict) -> Dict:
        """Handle request from Matrix UI
        
        Args:
            request_type: Type of request
            data: Request data
            
        Returns:
            Response data for UI
        """
        handlers = {
            "network_scan": self._handle_network_scan,
            "web_test": self._handle_web_test,
            "vulnerability_scan": self._handle_vuln_scan,
            "exploitation": self._handle_exploitation,
            "mobile_test": self._handle_mobile_test,
            "wireless_scan": self._handle_wireless_scan,
            "cloud_assessment": self._handle_cloud_assessment,
            "iot_analysis": self._handle_iot_analysis,
            "ai_analysis": self._handle_ai_analysis,
            "report_generation": self._handle_report_generation
        }
        
        handler = handlers.get(request_type)
        if not handler:
            return {"error": f"Unknown request type: {request_type}"}
        
        try:
            return await handler(data)
        except Exception as e:
            logger.error(f"Error handling {request_type}: {e}")
            return {"error": str(e)}
    
    async def _handle_network_scan(self, data: Dict) -> Dict:
        """Handle network scanning request"""
        target = data.get("target")
        if not target:
            return {"error": "Target required"}
        
        # Start reconnaissance and network scan
        recon_task = await self.client.execute_scan(
            test_type="reconnaissance",
            target=target,
            async_execution=True
        )
        
        network_task = await self.client.execute_scan(
            test_type="network_scan",
            target=target,
            parameters={"mode": data.get("mode", "external")},
            async_execution=True
        )
        
        return {
            "status": "started",
            "tasks": {
                "reconnaissance": recon_task["task_id"],
                "network_scan": network_task["task_id"]
            },
            "message": "Network scanning initiated"
        }
    
    async def _handle_web_test(self, data: Dict) -> Dict:
        """Handle web application testing request"""
        url = data.get("url")
        if not url:
            return {"error": "URL required"}
        
        task = await self.client.web_application_test(
            url=url,
            tools=data.get("tools")
        )
        
        return {
            "status": "started",
            "task_id": task["task_id"],
            "message": "Web application testing initiated"
        }
    
    async def _handle_vuln_scan(self, data: Dict) -> Dict:
        """Handle vulnerability scanning request"""
        target = data.get("target")
        if not target:
            return {"error": "Target required"}
        
        task = await self.client.vulnerability_assessment(
            target=target,
            scan_type=data.get("scan_type", "quick")
        )
        
        return {
            "status": "started",
            "task_id": task["task_id"],
            "message": "Vulnerability scanning initiated"
        }
    
    async def _handle_exploitation(self, data: Dict) -> Dict:
        """Handle exploitation request"""
        action = data.get("action")
        
        if action == "generate_payload":
            result = await self.client.generate_payloads(
                payload_type=data.get("payload_type", "reverse_shell"),
                platform=data.get("platform", "linux"),
                options=data.get("options", {})
            )
            return result
        
        elif action == "exploit":
            task = await self.client.execute_scan(
                test_type="exploitation",
                target=data.get("target"),
                parameters={"vulnerability": data.get("vulnerability")},
                async_execution=True
            )
            return {
                "status": "started",
                "task_id": task["task_id"],
                "message": "Exploitation attempt initiated"
            }
        
        return {"error": "Invalid exploitation action"}
    
    async def _handle_mobile_test(self, data: Dict) -> Dict:
        """Handle mobile application testing"""
        apk_path = data.get("apk_path")
        if not apk_path:
            return {"error": "APK path required"}
        
        task = await self.client.execute_scan(
            test_type="mobile_test",
            target=apk_path,
            async_execution=True
        )
        
        return {
            "status": "started",
            "task_id": task["task_id"],
            "message": "Mobile app analysis initiated"
        }
    
    async def _handle_wireless_scan(self, data: Dict) -> Dict:
        """Handle wireless network scanning"""
        task = await self.client.execute_scan(
            test_type="wireless_test",
            target=data.get("interface", "wlan0"),
            parameters={
                "action": data.get("action", "scan"),
                "bssid": data.get("bssid"),
                "channel": data.get("channel")
            },
            async_execution=True
        )
        
        return {
            "status": "started",
            "task_id": task["task_id"],
            "message": "Wireless scanning initiated"
        }
    
    async def _handle_cloud_assessment(self, data: Dict) -> Dict:
        """Handle cloud infrastructure assessment"""
        task = await self.client.execute_scan(
            test_type="cloud_assessment",
            target=data.get("provider", "aws"),
            parameters={
                "provider": data.get("provider", "aws"),
                "profile": data.get("profile")
            },
            async_execution=True
        )
        
        return {
            "status": "started",
            "task_id": task["task_id"],
            "message": "Cloud assessment initiated"
        }
    
    async def _handle_iot_analysis(self, data: Dict) -> Dict:
        """Handle IoT/firmware analysis"""
        firmware_path = data.get("firmware_path")
        if not firmware_path:
            return {"error": "Firmware path required"}
        
        task = await self.client.execute_scan(
            test_type="iot_analysis",
            target=firmware_path,
            async_execution=True
        )
        
        return {
            "status": "started",
            "task_id": task["task_id"],
            "message": "IoT analysis initiated"
        }
    
    async def _handle_ai_analysis(self, data: Dict) -> Dict:
        """Handle AI-powered analysis"""
        task = await self.client.execute_scan(
            test_type="ai_analysis",
            target=data.get("target", ""),
            parameters={"request": data.get("request", "")},
            async_execution=True
        )
        
        return {
            "status": "started",
            "task_id": task["task_id"],
            "message": "AI analysis initiated"
        }
    
    async def _handle_report_generation(self, data: Dict) -> Dict:
        """Handle report generation"""
        task = await self.client.execute_scan(
            test_type="report_generation",
            target=data.get("target", ""),
            parameters={
                "recon_data": data.get("recon_data", {}),
                "vuln_data": data.get("vuln_data", {}),
                "exploit_data": data.get("exploit_data", {})
            },
            async_execution=False
        )
        
        return task
    
    def format_for_matrix_ui(self, results: Dict) -> Dict:
        """Format backend results for Matrix UI display
        
        Args:
            results: Raw backend results
            
        Returns:
            Formatted results for UI
        """
        formatted = {
            "timestamp": datetime.now().isoformat(),
            "status": results.get("status", "unknown"),
            "matrix_data": []
        }
        
        # Convert results to Matrix-style display format
        if "summary" in results:
            for key, value in results["summary"].items():
                formatted["matrix_data"].append({
                    "type": "info",
                    "label": key.replace("_", " ").title(),
                    "value": str(value),
                    "color": self._get_color_for_value(key, value)
                })
        
        if "vulnerabilities" in results:
            for vuln in results["vulnerabilities"][:10]:
                formatted["matrix_data"].append({
                    "type": "vulnerability",
                    "severity": vuln.get("severity", "info"),
                    "name": vuln.get("name", "Unknown"),
                    "description": vuln.get("description", ""),
                    "color": self._get_severity_color(vuln.get("severity"))
                })
        
        if "details" in results:
            formatted["details"] = results["details"]
        
        return formatted
    
    def _get_color_for_value(self, key: str, value: Any) -> str:
        """Get color for value display"""
        if "critical" in key.lower():
            return "#ff0000"
        elif "high" in key.lower():
            return "#ff8800"
        elif "medium" in key.lower():
            return "#ffff00"
        elif "low" in key.lower():
            return "#00ff00"
        else:
            return "#00ffff"
    
    def _get_severity_color(self, severity: str) -> str:
        """Get color for severity level"""
        colors = {
            "critical": "#ff0000",
            "high": "#ff8800",
            "medium": "#ffff00",
            "low": "#88ff00",
            "info": "#00ffff"
        }
        return colors.get(severity.lower(), "#ffffff")


# Example usage for Matrix UI integration
async def main():
    """Example usage"""
    config = BackendConfig()
    
    async with MatrixBackendClient(config) as client:
        # Connect WebSocket for real-time updates
        await client.connect_websocket()
        
        # Register event handlers
        async def on_task_completed(data):
            print(f"Task completed: {data}")
        
        client.on_event("task_completed", on_task_completed)
        
        # Create UI connector
        ui_connector = MatrixUIConnector(client)
        
        # Example: Handle UI request for network scan
        ui_request = {
            "target": "example.com",
            "mode": "external"
        }
        
        result = await ui_connector.handle_ui_request("network_scan", ui_request)
        print(f"Scan started: {result}")
        
        # Wait for results
        if "tasks" in result:
            for task_name, task_id in result["tasks"].items():
                final_result = await client.wait_for_task(task_id)
                formatted = ui_connector.format_for_matrix_ui(final_result)
                print(f"{task_name} results: {formatted}")


if __name__ == "__main__":
    asyncio.run(main())
