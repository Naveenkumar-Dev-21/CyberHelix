#!/usr/bin/env python3
"""
Automated Security Assessment Framework
For authorized testing in controlled environments only
"""

import os
import sys
import json
import subprocess
import argparse
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('security_assessment.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SecurityAssessmentFramework:
    def __init__(self, target, output_dir="./reports"):
        """
        Initialize the security assessment framework
        
        Args:
            target: Target IP or hostname (must be authorized)
            output_dir: Directory for storing reports
        """
        self.target = target
        self.output_dir = output_dir
        self.results = {}
        self.authorized = False
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
    def verify_authorization(self):
        """
        Verify that testing is authorized
        This should check against a whitelist or authorization database
        """
        logger.warning("=" * 50)
        logger.warning("SECURITY ASSESSMENT AUTHORIZATION CHECK")
        logger.warning("=" * 50)
        logger.warning("This tool should only be used on systems you own or")
        logger.warning("have explicit written authorization to test.")
        logger.warning("=" * 50)
        
        # In production, this would check against an authorization database
        # For now, we'll require explicit confirmation
        response = input(f"Do you have written authorization to test {self.target}? (yes/no): ")
        
        if response.lower() != 'yes':
            logger.error("Testing aborted - no authorization confirmed")
            sys.exit(1)
            
        self.authorized = True
        logger.info(f"Authorization confirmed for testing {self.target}")
        
    def network_discovery(self):
        """
        Perform network discovery using nmap (basic scan only)
        """
        if not self.authorized:
            logger.error("Authorization required before scanning")
            return
            
        logger.info(f"Starting network discovery for {self.target}")
        
        try:
            # Basic service detection without aggressive scanning
            nmap_cmd = [
                "nmap",
                "-sV",  # Service version detection
                "-sC",  # Default scripts (safe)
                "-O",   # OS detection
                "--open",  # Only show open ports
                "-oX", f"{self.output_dir}/nmap_scan.xml",  # XML output
                "-oN", f"{self.output_dir}/nmap_scan.txt",  # Normal output
                self.target
            ]
            
            logger.info(f"Running: {' '.join(nmap_cmd)}")
            result = subprocess.run(nmap_cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info("Network discovery completed successfully")
                self.results['network_discovery'] = {
                    'status': 'completed',
                    'output_file': f"{self.output_dir}/nmap_scan.txt"
                }
            else:
                logger.error(f"Network discovery failed: {result.stderr}")
                self.results['network_discovery'] = {
                    'status': 'failed',
                    'error': result.stderr
                }
                
        except FileNotFoundError:
            logger.error("nmap not found. Please install nmap first.")
            self.results['network_discovery'] = {
                'status': 'error',
                'error': 'nmap not installed'
            }
        except Exception as e:
            logger.error(f"Error during network discovery: {str(e)}")
            self.results['network_discovery'] = {
                'status': 'error',
                'error': str(e)
            }
            
    def vulnerability_scanning(self):
        """
        Perform vulnerability scanning using OpenVAS or similar
        """
        if not self.authorized:
            logger.error("Authorization required before scanning")
            return
            
        logger.info(f"Starting vulnerability scanning for {self.target}")
        
        # Check for common vulnerabilities using nmap scripts
        try:
            vuln_scan_cmd = [
                "nmap",
                "--script", "vuln",  # Vulnerability scripts
                "-oX", f"{self.output_dir}/vuln_scan.xml",
                "-oN", f"{self.output_dir}/vuln_scan.txt",
                self.target
            ]
            
            logger.info(f"Running vulnerability scan...")
            result = subprocess.run(vuln_scan_cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                logger.info("Vulnerability scanning completed")
                self.results['vulnerability_scan'] = {
                    'status': 'completed',
                    'output_file': f"{self.output_dir}/vuln_scan.txt"
                }
            else:
                logger.warning(f"Vulnerability scan had issues: {result.stderr}")
                self.results['vulnerability_scan'] = {
                    'status': 'partial',
                    'warning': result.stderr
                }
                
        except subprocess.TimeoutExpired:
            logger.warning("Vulnerability scan timed out")
            self.results['vulnerability_scan'] = {
                'status': 'timeout',
                'error': 'Scan timed out after 5 minutes'
            }
        except Exception as e:
            logger.error(f"Error during vulnerability scanning: {str(e)}")
            self.results['vulnerability_scan'] = {
                'status': 'error',
                'error': str(e)
            }
            
    def web_application_scanning(self):
        """
        Perform web application scanning if web services are detected
        """
        if not self.authorized:
            logger.error("Authorization required before scanning")
            return
            
        logger.info("Checking for web applications...")
        
        # Check if common web ports are open
        web_ports = ['80', '443', '8080', '8443']
        
        try:
            # Quick check for web services
            for port in web_ports:
                check_cmd = [
                    "curl",
                    "-s",
                    "-o", "/dev/null",
                    "-w", "%{http_code}",
                    f"http://{self.target}:{port}",
                    "--connect-timeout", "5"
                ]
                
                result = subprocess.run(check_cmd, capture_output=True, text=True)
                
                if result.stdout and result.stdout != "000":
                    logger.info(f"Web service detected on port {port}")
                    
                    # Run nikto for web vulnerability scanning
                    nikto_cmd = [
                        "nikto",
                        "-h", f"{self.target}:{port}",
                        "-o", f"{self.output_dir}/nikto_port_{port}.txt",
                        "-Format", "txt"
                    ]
                    
                    logger.info(f"Running web application scan on port {port}...")
                    nikto_result = subprocess.run(nikto_cmd, capture_output=True, text=True, timeout=300)
                    
                    if nikto_result.returncode == 0:
                        logger.info(f"Web scan completed for port {port}")
                        
        except FileNotFoundError as e:
            logger.warning(f"Required tool not found: {str(e)}")
        except Exception as e:
            logger.error(f"Error during web application scanning: {str(e)}")
            
    def ssl_tls_assessment(self):
        """
        Assess SSL/TLS configuration
        """
        if not self.authorized:
            logger.error("Authorization required before scanning")
            return
            
        logger.info("Starting SSL/TLS assessment...")
        
        try:
            # Use testssl.sh or sslscan if available
            ssl_cmd = [
                "sslscan",
                "--no-colour",
                f"{self.target}:443"
            ]
            
            result = subprocess.run(ssl_cmd, capture_output=True, text=True, timeout=60)
            
            with open(f"{self.output_dir}/ssl_assessment.txt", "w") as f:
                f.write(result.stdout)
                
            logger.info("SSL/TLS assessment completed")
            self.results['ssl_assessment'] = {
                'status': 'completed',
                'output_file': f"{self.output_dir}/ssl_assessment.txt"
            }
            
        except FileNotFoundError:
            logger.warning("sslscan not found, skipping SSL/TLS assessment")
            self.results['ssl_assessment'] = {
                'status': 'skipped',
                'reason': 'sslscan not installed'
            }
        except Exception as e:
            logger.error(f"Error during SSL/TLS assessment: {str(e)}")
            self.results['ssl_assessment'] = {
                'status': 'error',
                'error': str(e)
            }
            
    def generate_report(self):
        """
        Generate a comprehensive report of all findings
        """
        logger.info("Generating assessment report...")
        
        report = {
            'target': self.target,
            'timestamp': datetime.now().isoformat(),
            'assessment_results': self.results,
            'report_files': os.listdir(self.output_dir)
        }
        
        # Save JSON report
        report_file = f"{self.output_dir}/assessment_report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
            
        logger.info(f"Report saved to {report_file}")
        
        # Generate HTML report
        self.generate_html_report(report)
        
    def generate_html_report(self, report_data):
        """
        Generate an HTML report for better readability
        """
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Security Assessment Report - {self.target}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #333; }}
                h2 {{ color: #666; border-bottom: 1px solid #ccc; }}
                .section {{ margin: 20px 0; padding: 10px; background: #f5f5f5; }}
                .status-completed {{ color: green; }}
                .status-failed {{ color: red; }}
                .status-error {{ color: orange; }}
                .warning {{ background: #fff3cd; padding: 10px; border-left: 4px solid #ffc107; }}
            </style>
        </head>
        <body>
            <h1>Security Assessment Report</h1>
            <div class="section">
                <h2>Assessment Details</h2>
                <p><strong>Target:</strong> {report_data['target']}</p>
                <p><strong>Timestamp:</strong> {report_data['timestamp']}</p>
            </div>
            
            <div class="section">
                <h2>Assessment Results</h2>
                <ul>
        """
        
        for module, result in report_data['assessment_results'].items():
            status_class = f"status-{result.get('status', 'unknown')}"
            html_content += f"""
                <li>
                    <strong>{module.replace('_', ' ').title()}:</strong> 
                    <span class="{status_class}">{result.get('status', 'unknown')}</span>
                    {f" - {result.get('output_file', '')}" if 'output_file' in result else ""}
                </li>
            """
            
        html_content += """
                </ul>
            </div>
            
            <div class="warning">
                <p><strong>Important:</strong> This report is for authorized security assessment only. 
                Do not use this information for unauthorized access or malicious purposes.</p>
            </div>
        </body>
        </html>
        """
        
        html_file = f"{self.output_dir}/assessment_report.html"
        with open(html_file, 'w') as f:
            f.write(html_content)
            
        logger.info(f"HTML report saved to {html_file}")
        
    def run_assessment(self):
        """
        Run the complete security assessment
        """
        logger.info("=" * 50)
        logger.info("STARTING SECURITY ASSESSMENT FRAMEWORK")
        logger.info("=" * 50)
        
        # Step 1: Verify authorization
        self.verify_authorization()
        
        # Step 2: Network discovery
        self.network_discovery()
        
        # Step 3: Vulnerability scanning
        self.vulnerability_scanning()
        
        # Step 4: Web application scanning
        self.web_application_scanning()
        
        # Step 5: SSL/TLS assessment
        self.ssl_tls_assessment()
        
        # Step 6: Generate report
        self.generate_report()
        
        logger.info("=" * 50)
        logger.info("ASSESSMENT COMPLETED")
        logger.info(f"Reports saved to: {self.output_dir}")
        logger.info("=" * 50)

def main():
    parser = argparse.ArgumentParser(
        description="Automated Security Assessment Framework (Authorized Testing Only)"
    )
    parser.add_argument(
        "target",
        help="Target IP address or hostname (must be authorized)"
    )
    parser.add_argument(
        "--output",
        "-o",
        default="./reports",
        help="Output directory for reports (default: ./reports)"
    )
    
    args = parser.parse_args()
    
    # Create and run assessment
    framework = SecurityAssessmentFramework(args.target, args.output)
    framework.run_assessment()

if __name__ == "__main__":
    main()
