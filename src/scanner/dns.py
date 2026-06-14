"""
DNS Enumeration Scanner Module
"""

import socket
import dns.resolver
import dns.zone
import dns.name
from typing import List, Dict, Optional
from dataclasses import dataclass

from src.utils.logger import logger, color_logger


@dataclass
class DNSRecord:
    """DNS record information"""
    name: str
    record_type: str
    value: str
    ttl: int = 0


class DNSScanner:
    """DNS enumeration and reconnaissance"""
    
    def __init__(self, timeout: int = 5):
        self.timeout = timeout
        self.resolver = dns.resolver.Resolver()
        self.resolver.lifetime = timeout
    
    def get_dns_records(self, domain: str, record_type: str = 'A') -> List[DNSRecord]:
        """Get DNS records for domain"""
        records = []
        
        try:
            color_logger.info(f"Querying {record_type} records for {domain}", "DNS")
            answers = self.resolver.resolve(domain, record_type)
            
            for rdata in answers:
                record = DNSRecord(
                    name=domain,
                    record_type=record_type,
                    value=str(rdata),
                    ttl=answers.rrset.ttl
                )
                records.append(record)
                color_logger.success(f"{record_type}: {rdata}", "DNS")
        
        except dns.resolver.NXDOMAIN:
            logger.warning(f"Domain {domain} not found")
        except dns.exception.Timeout:
            logger.warning(f"DNS query timeout for {domain}")
        except Exception as e:
            logger.error(f"Error querying DNS: {e}")
        
        return records
    
    def enumerate_dns_records(self, domain: str) -> Dict[str, List[DNSRecord]]:
        """Enumerate all common DNS record types"""
        color_logger.info(f"Starting DNS enumeration for {domain}", "DNSENUM")
        
        record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME', 'SOA', 'SRV']
        results = {}
        
        for record_type in record_types:
            records = self.get_dns_records(domain, record_type)
            if records:
                results[record_type] = records
        
        return results
    
    def find_subdomains_dns(self, domain: str, wordlist: List[str] = None) -> List[str]:
        """Enumerate subdomains using DNS queries"""
        color_logger.info(f"Enumerating subdomains for {domain}", "SUBDOM")
        
        if wordlist is None:
            wordlist = self._get_default_wordlist()
        
        subdomains = []
        
        for subdomain in wordlist:
            full_domain = f"{subdomain}.{domain}"
            try:
                self.resolver.resolve(full_domain, 'A')
                subdomains.append(full_domain)
                color_logger.success(f"Found subdomain: {full_domain}", "SUBDOM")
            except (dns.resolver.NXDOMAIN, dns.exception.Timeout, Exception):
                pass
        
        return subdomains
    
    def zone_transfer(self, domain: str, nameserver: str = None) -> List[DNSRecord]:
        """Attempt DNS zone transfer"""
        color_logger.info(f"Attempting zone transfer for {domain}", "ZONE")
        
        records = []
        
        try:
            # Get nameserver if not provided
            if nameserver is None:
                ns_records = self.get_dns_records(domain, 'NS')
                if not ns_records:
                    return []
                nameserver = ns_records[0].value
            
            # Attempt zone transfer
            zone = dns.zone.from_xfr(dns.query.xfr(nameserver, domain))
            
            for name, node in zone.items():
                for rdataset in node:
                    for rdata in rdataset:
                        record = DNSRecord(
                            name=str(name.derelativize(zone.origin)),
                            record_type=dns.rdatatype.to_text(rdataset.rdtype),
                            value=str(rdata),
                            ttl=rdataset.ttl
                        )
                        records.append(record)
                        color_logger.success(f"Zone record: {name} -> {rdata}", "ZONE")
        
        except Exception as e:
            color_logger.warning(f"Zone transfer failed (expected): {e}", "ZONE")
        
        return records
    
    def reverse_dns_lookup(self, ip: str) -> Optional[str]:
        """Reverse DNS lookup"""
        try:
            hostname, _, _ = socket.gethostbyaddr(ip)
            color_logger.success(f"Reverse DNS: {ip} -> {hostname}", "RDNS")
            return hostname
        except (socket.herror, socket.gaierror):
            return None
    
    def check_dns_security(self, domain: str) -> Dict[str, bool]:
        """Check DNS security features"""
        color_logger.info(f"Checking DNS security for {domain}", "DNSSEC")
        
        security = {
            'dnssec': False,
            'caa_record': False,
        }
        
        try:
            # Check DNSSEC
            response = self.resolver.resolve(domain, 'A')
            security['dnssec'] = response.response.flags & 0x0020 != 0
            
            # Check CAA records
            try:
                self.resolver.resolve(domain, 'CAA')
                security['caa_record'] = True
            except:
                pass
        
        except Exception as e:
            logger.error(f"DNS security check failed: {e}")
        
        return security
    
    def _get_default_wordlist(self) -> List[str]:
        """Get default subdomain wordlist"""
        return [
            'www', 'mail', 'ftp', 'admin', 'test', 'dev', 'staging',
            'api', 'app', 'static', 'cdn', 'ns', 'ns1', 'vpn',
            'server', 'backup', 'db', 'database', 'old', 'new',
            'blog', 'shop', 'forum', 'wiki', 'download',
        ]
