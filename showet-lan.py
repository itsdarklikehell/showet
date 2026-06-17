#!/usr/bin/env python3
"""
Showet LAN Multiplayer Synchronization
Synchronized playback across multiple devices for demo parties
"""

import socket
import threading
import time
import json
from dataclasses import dataclass
from typing import Dict, List, Optional
import struct

@dataclass
class SyncPacket:
    """Network synchronization packet for demo playback"""
    timestamp: float
    demo_id: int
    platform: str
    playback_state: str  # play, pause, stop
    frame_count: int = 0

class ShowetLAN:
    """LAN-based synchronized demo viewing"""
    
    BROADCAST_PORT = 8767
    BROADCAST_INTERVAL = 0.016  # 60Hz sync
    
    def __init__(self, platform: str, demo_id: int):
        self.platform = platform
        self.demo_id = demo_id
        self.is_host = False
        self.is_client = False
        self.peers: Dict[str, SyncPacket] = {}
        self.sync_thread = None
        self.socket = None
    
    def start_host(self):
        """Start as synchronization host"""
        self.is_host = True
        
        # UDP socket for broadcasting
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.socket.bind(('', 0))
        
        # Start sync thread
        self.sync_thread = threading.Thread(target=self._broadcast_loop, daemon=True)
        self.sync_thread.start()
        
        print(f"📡 LAN Sync Host started for {self.platform} demo #{self.demo_id}")
    
    def join_host(self, host_ip: str = None):
        """Join as client to sync host"""
        self.is_client = True
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('', self.BROADCAST_PORT))
        
        # Start receive thread
        self.sync_thread = threading.Thread(target=self._receive_loop, daemon=True)
        self.sync_thread.start()
        
        print(f"🔗 LAN Sync Client started, listening on port {self.BROADCAST_PORT}")
    
    def _broadcast_loop(self):
        """Broadcast sync packets to all peers (HOST)"""
        while self.is_host and self.socket:
            packet = SyncPacket(
                timestamp=time.time(),
                demo_id=self.demo_id,
                platform=self.platform,
                playback_state="playing",
                frame_count=int(time.time() * 60) % 1000
            )
            
            data = json.dumps({
                't': packet.timestamp,
                'd': packet.demo_id,
                'p': packet.platform,
                's': packet.playback_state,
                'f': packet.frame_count
            }).encode()
            
            try:
                self.socket.sendto(data, ('<broadcast>', self.BROADCAST_PORT))
            except:
                break
            
            time.sleep(self.BROADCAST_INTERVAL)
    
    def _receive_loop(self):
        """Receive sync packets from host (CLIENT)"""
        while self.is_client and self.socket:
            try:
                data, addr = self.socket.recvfrom(1024)
                sync = json.loads(data.decode())
                
                # Process sync - would connect to emulator playback
                self._apply_sync(SyncPacket(
                    timestamp=sync.get('t', 0),
                    demo_id=sync.get('d', 0),
                    platform=sync.get('p', ''),
                    playback_state=sync.get('s', 'idle'),
                    frame_count=sync.get('f', 0)
                ))
            except:
                continue
    
    def _apply_sync(self, packet: SyncPacket):
        """Apply received sync state to local playback"""
        # This would interface with the actual emulator
        print(f"⏱️ Sync: {packet.playback_state} at t={packet.timestamp:.2f}s, frame {packet.frame_count}")
    
    def stop(self):
        """Stop LAN synchronization"""
        self.is_host = False
        self.is_client = False
        if self.socket:
            self.socket.close()
        print("🛑 LAN Sync stopped")

# CLI utility
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python3 showet-lan.py <host|join> <platform> [demo_id]")
        print("Example: python3 showet-lan.py host commodore_64 12345")
        sys.exit(1)
    
    mode = sys.argv[1]
    platform = sys.argv[2]
    demo_id = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    
    lan = ShowetLAN(platform, demo_id)
    
    if mode == "host":
        lan.start_host()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            lan.stop()
    elif mode == "join":
        lan.join_host()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            lan.stop()
    else:
        print(f"Unknown mode: {mode}")