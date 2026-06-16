#!/usr/bin/env python3
"""Show upcoming demoscene parties from the terminal.

Usage:
    showet-parties
"""

from party_calendar import get_upcoming_parties, format_countdown


def main() -> int:
    """Display upcoming demoparty calendar."""
    parties = get_upcoming_parties(180)  # Next 6 months
    
    print("🎮 UPCOMING DEMOPARTIES")
    print("=" * 50)
    
    for party in parties[:5]:
        countdown = format_countdown(party)
        print(f"\n{party['name']}")
        print(f"  📅 {party['date']}")
        print(f"  📍 {party['location']}")
        print(f"  ⏰ {countdown}")
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())