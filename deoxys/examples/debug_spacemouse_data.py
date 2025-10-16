#!/usr/bin/env python3
"""Debug script to inspect SpaceMouse raw HID data packets."""

import argparse
import time
import hid

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--vendor-id", type=int, default=9583)
    parser.add_argument("--product-id", type=int, default=50741)
    parser.add_argument("--samples", type=int, default=100, help="Number of packets to capture")
    args = parser.parse_args()

    print(f"Opening SpaceMouse device (VID: {hex(args.vendor_id)}, PID: {hex(args.product_id)})")
    device = hid.device()
    device.open(args.vendor_id, args.product_id)
    
    print(f"Manufacturer: {device.get_manufacturer_string()}")
    print(f"Product: {device.get_product_string()}")
    print("\nCapturing HID packets... Move the SpaceMouse and press buttons!")
    print("=" * 80)
    
    packet_stats = {}
    sample_count = 0
    
    while sample_count < args.samples:
        d = device.read(64, timeout_ms=100)  # Read up to 64 bytes with timeout
        if d is not None and len(d) > 0:
            sample_count += 1
            pkt_type = d[0]
            pkt_len = len(d)
            
            # Track packet type statistics
            key = (pkt_type, pkt_len)
            if key not in packet_stats:
                packet_stats[key] = {"count": 0, "sample": list(d)}
            packet_stats[key]["count"] += 1
            
            # Print first few samples of each type
            if packet_stats[key]["count"] <= 3:
                print(f"[{sample_count:4d}] Type: {pkt_type:2d} | Len: {pkt_len:2d} | Data: {list(d[:min(16, pkt_len)])}")
    
    print("=" * 80)
    print("\nPacket Statistics:")
    print("-" * 80)
    for (pkt_type, pkt_len), info in sorted(packet_stats.items()):
        print(f"Type {pkt_type:2d} | Length {pkt_len:2d} | Count: {info['count']:4d} | Sample: {info['sample'][:16]}")
    
    print("\n" + "=" * 80)
    print("Analysis:")
    print("-" * 80)
    
    # Check for 6-DOF sensor packets
    dof_packets = [(t, l, i) for (t, l), i in packet_stats.items() if t == 1]
    if dof_packets:
        for pkt_type, pkt_len, info in dof_packets:
            print(f"✓ 6-DOF sensor packets (type 1) detected with length {pkt_len}")
            if pkt_len < 13:
                print(f"  ⚠ WARNING: Packet length {pkt_len} < 13 (code expects 13+)")
                print(f"     This will cause IndexError in spacemouse.py line 227-229")
    
    # Check for button packets
    btn_packets = [(t, l, i) for (t, l), i in packet_stats.items() if t == 3]
    if btn_packets:
        for pkt_type, pkt_len, info in btn_packets:
            print(f"✓ Button packets (type 3) detected with length {pkt_len}")
    
    device.close()
    print("=" * 80)

if __name__ == "__main__":
    main()

