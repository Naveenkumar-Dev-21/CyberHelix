#!/usr/bin/env python3
"""
Modular Security Assessment Framework
Enhanced version with multiple assessment modules
For authorized testing in controlled environments only
"""

import os
import sys
import yaml
import json
import subprocess
import threading
import queue
import time
from datetime import datetime
from typing import Dict, List, Optional
import logging
import ipaddress
import socket

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(name)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AssessmentModule:
    """Base class for assessment modules"""
    
    def __init__(self, target: str, config: dict):
        self.target = target
        self.config = config
        self.results = {}
        
    def run(self) -> dict:
        """Run the assessment module"""
        raise NotImplementedError("Subclasses must implement run method")
        
    def is_enabled(self) -> bool:
        """Check if module is enabled in configuration"""
        return self.config.get('enabled', True)

class NetworkDiscoveryModule(AssessmentModule):
    """Network discovery and port scanning module"""
    
    def run(self) -> dict:
        if not self.is_enabled():
            return {'status': 'skipped', 'reason': 'Module disabled'}
            
        logger.info(f"Running network discovery on {self.target}")
        
        try:
            # Prepare nmap command with configuration options
            nmap_options = self.config.get('options', ['-sV', '-sC'])
            timeout = self.config.get('timeout', 300)
            
            cmd = ['nmap'] + nmap_options + [
                '-oX', f"reports/nmap_{self.target}.xml",
                '-oN', f"reports/nmap_{self.target}.txt",
                self.target
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            
            if result.returncode == 0:
                # Parse results
                return {
                    'status': 'completed',
                    'open_ports': self._parse_nmap_output(result.stdout),
                    'output_file': f"reports/nmap_{self.target}.txt"
                }
            else:
                return {'status': 'failed', 'error': result.stderr}
                
        except subprocess.TimeoutExpired:
            return {'status': 'timeout', 'error': f'Scan timed out after {timeout} seconds'}
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
            
    def _parse_nmap_output(self, output: str) -> List[dict]:
        """Parse nmap output to extract open ports"""
        ports = []
        for line in output.split('\n'):
            if '/tcp' in line and 'open' in line:
                parts = line.split()
                if len(parts) >= 3:
                    port_info = {
                        'port': parts[0].split('/')[0],
                        'state': parts[1],
                        'service': parts[2] if len(parts) > 2 else 'unknown'
                    }
                    ports.append(port_info)
        return ports

class VulnerabilityScanModule(AssessmentModule):
    """Vulnerability scanning module"""
    
    def run(self) -> dict:
        if not self.is_enabled():
            return {'status': 'skipped', 'reason': 'Module disabled'}
            
        logger.info(f"Running vulnerability scan on {self.target}")
        
        vulnerabilities = []
        scan_types = self.config.get('scan_types', ['vuln', 'safe'])
        timeout = self.config.get('timeout', 600)
        
        for scan_type in scan_types:
            try:
                cmd = [
                    'nmap',
                    '--script', scan_type,
                    '-oN', f"reports/vuln_{scan_type}_{self.target}.txt",
                    self.target
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
                
                if result.returncode == 0:
                    # Parse for vulnerabilities
                    vulns = self._parse_vulnerabilities(result.stdout)
                    vulnerabilities.extend(vulns)
                    
            except Exception as e:
                logger.error(f"Error in {scan_type} scan: {str(e)}")
                
        return {
            'status': 'completed',
            'vulnerabilities_found': len(vulnerabilities),
            'vulnerabilities': vulnerabilities[:10],  # Top 10 for summary
            'output_file': f"reports/vuln_*_{self.target}.txt"
        }
        
    def _parse_vulnerabilities(self, output: str) -> List[dict]:
        """Parse vulnerability scan output"""
        vulnerabilities = []
        
        vuln_keywords = ['VULNERABLE', 'vulnerability', 'CVE-', 'OSVDB-']
        
        for line in output.split('\n'):
            for keyword in vuln_keywords:
                if keyword in line:
                    vulnerabilities.append({
                        'type': keyword,
                        'description': line.strip()
                    })
                    break
                    
        return vulnerabilities

class WebApplicationModule(AssessmentModule):
    """Web application scanning module"""
    
    def run(self) -> dict:
        if not self.is_enabled():
            return {'status': 'skipped', 'reason': 'Module disabled'}
            
        logger.info(f"Running web application scan on {self.target}")
        
        web_ports = self.config.get('ports', [80, 443, 8080, 8443])
        results = {}
        
        for port in web_ports:
            if self._check_web_service(port):
                logger.info(f"Web service detected on port {port}")
                
                # Run different web scanning tools based on configuration
                if self.config.get('tools', {}).get('nikto', True):
                    results[f'port_{port}'] = self._run_nikto(port)
                    
                if self.config.get('tools', {}).get('dirb', False):
                    results[f'dirb_{port}'] = self._run_dirb(port)
                    
        return {
            'status': 'completed',
            'web_services': list(results.keys()),
            'scan_results': results
        }
        
    def _check_web_service(self, port: int) -> bool:
        """Check if a web service is running on the given port"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((self.target, port))
            sock.close()
            return result == 0
        except:
            return False
            
    def _run_nikto(self, port: int) -> dict:
        """Run Nikto web scanner"""
        try:
            cmd = [
                'nikto',
                '-h', f"{self.target}:{port}",
                '-o', f"reports/nikto_{self.target}_{port}.txt",
                '-Format', 'txt',
                '-timeout', '30'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                return {'status': 'completed', 'findings': self._parse_nikto(result.stdout)}
            else:
                return {'status': 'failed', 'error': 'Nikto scan failed'}
                
        except FileNotFoundError:
            return {'status': 'error', 'error': 'Nikto not installed'}
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
            
    def _parse_nikto(self, output: str) -> int:
        """Parse Nikto output for findings count"""
        findings = 0
        for line in output.split('\n'):
            if line.startswith('+'):
                findings += 1
        return findings
        
    def _run_dirb(self, port: int) -> dict:
        """Run directory bruteforce scan"""
        # Implementation for dirb scanning
        return {'status': 'not_implemented'}

class SSLAssessmentModule(AssessmentModule):
    """SSL/TLS configuration assessment module"""
    
    def run(self) -> dict:
        if not self.is_enabled():
            return {'status': 'skipped', 'reason': 'Module disabled'}
            
        logger.info(f"Running SSL/TLS assessment on {self.target}")
        
        ssl_ports = self.config.get('ports', [443, 8443])
        results = {}
        
        for port in ssl_ports:
            if self._check_ssl_service(port):
                results[f'port_{port}'] = self._assess_ssl(port)
                
        return {
            'status': 'completed',
            'ssl_services': list(results.keys()),
            'assessment_results': results
        }
        
    def _check_ssl_service(self, port: int) -> bool:
        """Check if SSL/TLS service is running"""
        try:
            import ssl
            context = ssl.create_default_context()
            with socket.create_connection((self.target, port), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=self.target) as ssock:
                    return True
        except:
            return False
            
    def _assess_ssl(self, port: int) -> dict:
        """Assess SSL/TLS configuration"""
        try:
            cmd = [
                'sslscan',
                '--no-colour',
                f'{self.target}:{port}'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                return {
                    'status': 'completed',
                    'weak_ciphers': self._check_weak_ciphers(result.stdout),
                    'certificate_issues': self._check_cert_issues(result.stdout)
                }
            else:
                # Fallback to openssl if sslscan is not available
                return self._assess_with_openssl(port)
                
        except FileNotFoundError:
            return self._assess_with_openssl(port)
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
            
    def _assess_with_openssl(self, port: int) -> dict:
        """Fallback SSL assessment using openssl"""
        try:
            cmd = [
                'openssl', 's_client',
                '-connect', f'{self.target}:{port}',
                '-servername', self.target
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10, input='')
            
            return {
                'status': 'completed',
                'method': 'openssl',
                'certificate_valid': 'Verify return code: 0' in result.stdout
            }
        except:
            return {'status': 'error', 'error': 'SSL assessment failed'}
            
    def _check_weak_ciphers(self, output: str) -> List[str]:
        """Check for weak ciphers in SSL scan output"""
        weak_ciphers = []
        weak_keywords = ['RC4', 'DES', 'MD5', 'NULL', 'EXPORT', 'anon']
        
        for line in output.split('\n'):
            for keyword in weak_keywords:
                if keyword in line and 'Accepted' in line:
                    weak_ciphers.append(line.strip())
                    
        return weak_ciphers
        
    def _check_cert_issues(self, output: str) -> List[str]:
        """Check for certificate issues"""
        issues = []
        
        if 'expired' in output.lower():
            issues.append('Certificate expired')
        if 'self-signed' in output.lower():
            issues.append('Self-signed certificate')
        if 'mismatch' in output.lower():
            issues.append('Hostname mismatch')
            
        return issues

class DNSEnumerationModule(AssessmentModule):
    """DNS enumeration module"""
    
    def run(self) -> dict:
        if not self.is_enabled():
            return {'status': 'skipped', 'reason': 'Module disabled'}
            
        logger.info(f"Running DNS enumeration on {self.target}")
        
        results = {
            'dns_records': self._enumerate_dns_records(),
            'subdomains': self._enumerate_subdomains(),
            'zone_transfer': self._check_zone_transfer()
        }
        
        return {
            'status': 'completed',
            'findings': results
        }
        
    def _enumerate_dns_records(self) -> dict:
        """Enumerate DNS records"""
        records = {}
        record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA']
        
        for record_type in record_types:
            try:
                cmd = ['dig', '+short', record_type, self.target]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                
                if result.stdout.strip():
                    records[record_type] = result.stdout.strip().split('\n')
                    
            except Exception as e:
                logger.debug(f"Error querying {record_type} records: {str(e)}")
                
        return records
        
    def _enumerate_subdomains(self) -> List[str]:
        """Basic subdomain enumeration"""
        common_subdomains = [
            'www', 'mail', 'ftp', 'admin', 'test', 'dev',
            'staging', 'api', 'mobile', 'secure', 'vpn'
        ]
        
        found_subdomains = []
        
        for subdomain in common_subdomains:
            try:
                target = f"{subdomain}.{self.target}"
                socket.gethostbyname(target)
                found_subdomains.append(target)
            except:
                pass
                
        return found_subdomains
        
    def _check_zone_transfer(self) -> dict:
        """Check for DNS zone transfer vulnerability"""
        try:
            # Get NS records first
            cmd = ['dig', '+short', 'NS', self.target]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if not result.stdout:
                return {'vulnerable': False, 'reason': 'No NS records found'}
                
            ns_servers = result.stdout.strip().split('\n')
            
            for ns in ns_servers:
                # Try zone transfer
                cmd = ['dig', 'AXFR', f'@{ns.strip(".")}', self.target]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
                
                if 'Transfer failed' not in result.stdout and result.returncode == 0:
                    return {'vulnerable': True, 'ns_server': ns}
                    
            return {'vulnerable': False, 'reason': 'Zone transfer not allowed'}
            
        except Exception as e:
            return {'vulnerable': False, 'error': str(e)}

class ModularSecurityAssessment:
    """Main orchestrator for modular security assessment"""
    
    def __init__(self, target: str, config_file: str = "config.yaml"):
        self.target = target
        self.config = self._load_config(config_file)
        self.modules = []
        self.results = {}
        
        # Create reports directory
        os.makedirs("reports", exist_ok=True)
        
        # Initialize modules
        self._initialize_modules()
        
    def _load_config(self, config_file: str) -> dict:
        """Load configuration from YAML file"""
        try:
            with open(config_file, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.warning(f"Config file {config_file} not found, using defaults")
            return self._get_default_config()
        except Exception as e:
            logger.error(f"Error loading config: {str(e)}")
            return self._get_default_config()
            
    def _get_default_config(self) -> dict:
        """Return default configuration"""
        return {
            'modules': {
                'network_discovery': {'enabled': True},
                'vulnerability_scanning': {'enabled': True},
                'web_application': {'enabled': True},
                'ssl_assessment': {'enabled': True},
                'dns_enumeration': {'enabled': True}
            },
            'safe_mode': {
                'no_exploits': True,
                'no_aggressive': True
            }
        }
        
    def _initialize_modules(self):
        """Initialize assessment modules based on configuration"""
        module_classes = {
            'network_discovery': NetworkDiscoveryModule,
            'vulnerability_scanning': VulnerabilityScanModule,
            'web_application': WebApplicationModule,
            'ssl_assessment': SSLAssessmentModule,
            'dns_enumeration': DNSEnumerationModule
        }
        
        for module_name, module_class in module_classes.items():
            if module_name in self.config.get('modules', {}):
                module_config = self.config['modules'][module_name]
                module = module_class(self.target, module_config)
                self.modules.append((module_name, module))
                
    def verify_authorization(self) -> bool:
        """Verify that the target is authorized for testing"""
        authorized_targets = self.config.get('authorization', {}).get('authorized_targets', [])
        
        # Check if target is in authorized list
        for authorized in authorized_targets:
            try:
                # Check if it's a network range
                if '/' in authorized:
                    network = ipaddress.ip_network(authorized, strict=False)
                    target_ip = ipaddress.ip_address(socket.gethostbyname(self.target))
                    if target_ip in network:
                        return True
                # Check exact match
                elif authorized == self.target:
                    return True
            except:
                pass
                
        # If require_confirmation is set, ask user
        if self.config.get('authorization', {}).get('require_confirmation', True):
            logger.warning("=" * 60)
            logger.warning("AUTHORIZATION REQUIRED")
            logger.warning("=" * 60)
            logger.warning(f"Target: {self.target}")
            logger.warning("This assessment tool should only be used on systems")
            logger.warning("you own or have explicit written authorization to test.")
            logger.warning("=" * 60)
            
            response = input("Do you have authorization to test this target? (yes/no): ")
            return response.lower() == 'yes'
            
        return False
        
    def run_assessment(self):
        """Run all enabled assessment modules"""
        
        if not self.verify_authorization():
            logger.error("Assessment aborted - no authorization")
            sys.exit(1)
            
        logger.info("=" * 60)
        logger.info("STARTING MODULAR SECURITY ASSESSMENT")
        logger.info(f"Target: {self.target}")
        logger.info(f"Modules: {len(self.modules)}")
        logger.info("=" * 60)
        
        # Run modules based on performance settings
        max_parallel = self.config.get('performance', {}).get('max_parallel_scans', 3)
        scan_delay = self.config.get('performance', {}).get('scan_delay', 2)
        
        for module_name, module in self.modules:
            logger.info(f"\n[*] Running module: {module_name}")
            
            try:
                result = module.run()
                self.results[module_name] = result
                logger.info(f"[+] {module_name} completed with status: {result.get('status')}")
                
                # Delay between scans
                time.sleep(scan_delay)
                
            except Exception as e:
                logger.error(f"[-] Error in {module_name}: {str(e)}")
                self.results[module_name] = {'status': 'error', 'error': str(e)}
                
        # Generate report
        self._generate_report()
        
    def _generate_report(self):
        """Generate comprehensive assessment report"""
        timestamp = datetime.now().isoformat()
        
        report = {
            'assessment_info': {
                'target': self.target,
                'timestamp': timestamp,
                'modules_run': len(self.modules),
                'configuration': self.config.get('safe_mode', {})
            },
            'results': self.results,
            'summary': self._generate_summary()
        }
        
        # Save JSON report
        report_file = f"reports/assessment_{self.target}_{timestamp.split('T')[0]}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
            
        logger.info("=" * 60)
        logger.info("ASSESSMENT COMPLETED")
        logger.info(f"Report saved to: {report_file}")
        logger.info("=" * 60)
        
        # Print summary
        self._print_summary()
        
    def _generate_summary(self) -> dict:
        """Generate assessment summary"""
        summary = {
            'total_modules': len(self.modules),
            'completed': sum(1 for r in self.results.values() if r.get('status') == 'completed'),
            'failed': sum(1 for r in self.results.values() if r.get('status') in ['failed', 'error']),
            'skipped': sum(1 for r in self.results.values() if r.get('status') == 'skipped'),
            'key_findings': []
        }
        
        # Extract key findings
        if 'vulnerability_scanning' in self.results:
            vuln_count = self.results['vulnerability_scanning'].get('vulnerabilities_found', 0)
            if vuln_count > 0:
                summary['key_findings'].append(f"{vuln_count} potential vulnerabilities found")
                
        if 'network_discovery' in self.results:
            ports = self.results['network_discovery'].get('open_ports', [])
            if ports:
                summary['key_findings'].append(f"{len(ports)} open ports discovered")
                
        if 'ssl_assessment' in self.results:
            for port_result in self.results['ssl_assessment'].get('assessment_results', {}).values():
                if port_result.get('weak_ciphers'):
                    summary['key_findings'].append("Weak SSL/TLS ciphers detected")
                    break
                    
        return summary
        
    def _print_summary(self):
        """Print assessment summary to console"""
        summary = self._generate_summary()
        
        print("\n" + "=" * 60)
        print("ASSESSMENT SUMMARY")
        print("=" * 60)
        print(f"Target: {self.target}")
        print(f"Modules Run: {summary['total_modules']}")
        print(f"Completed: {summary['completed']}")
        print(f"Failed: {summary['failed']}")
        print(f"Skipped: {summary['skipped']}")
        
        if summary['key_findings']:
            print("\nKey Findings:")
            for finding in summary['key_findings']:
                print(f"  - {finding}")
                
        print("=" * 60)

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Modular Security Assessment Framework (Authorized Testing Only)"
    )
    parser.add_argument("target", help="Target IP address or hostname")
    parser.add_argument("--config", "-c", default="config.yaml", help="Configuration file")
    
    args = parser.parse_args()
    
    assessment = ModularSecurityAssessment(args.target, args.config)
    assessment.run_assessment()

if __name__ == "__main__":
    main()
