# Artisan Alarm: trigger-alarms-6-190g

| # | On | Phase | Offset | Guard | NegGuard | Source | Cond | Temp° | Action | Beep | Label |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | ✓ | CHARGE | 00:08 | — | — | BT | below | 120 | Pop-up message | ✓ | 120 Ready Charge |
| 2 | ✓ | CHARGE | 00:02 | — | — | Time | above | — | Set Fan | ✓ | 40 |
| 3 | ✓ | CHARGE | 00:05 | — | — | Time | above | — | Set Burner | ✓ | 30  # soak |
| 4 | ✓ | CHARGE | 00:30 | — | — | Time | above | — | Set Burner | ✓ | 65 |
| 5 | ✓ | CHARGE | 00:30 | — | — | Time | above | — | Set Fan | ✓ | 50 |
| 6 | ✓ | CHARGE | 01:00 | — | — | Time | above | — | Set Burner | ✓ | 60 |
| 7 | ✓ | CHARGE | 01:30 | — | — | Time | above | — | Set Burner | ✓ | 55 |
| 8 | ✓ | CHARGE | 01:45 | — | — | Time | above | — | Set Fan | ✓ | 60 |
| 9 | ✓ | CHARGE | 02:00 | — | — | Time | above | — | Set Burner | ✓ | 50 |
| 10 | ✓ | CHARGE | 02:30 | — | — | Time | above | — | Set Fan | ✓ | 70 |
| 11 | ✗ | FC START | 01:15 | — | — | Time | above | — | Set Burner | ✓ | 45 |
| 12 | ✗ | FC START | 01:30 | — | — | Time | above | — | Set Fan | ✓ | 70 |
| 13 | ✗ | FC START | 02:00 | — | — | Time | above | — | Set Burner | ✓ | 50 |
| 14 | ✓ | CHARGE | 10:00 | — | — | Time | above | — | Pop-up message | ✓ | Drop by 10:30 |
| 15 | ✓ | DROP | 00:01 | — | — | Time | above | — | Set Burner | ✓ | 0 |
| 16 | ✓ | DROP | 00:02 | — | — | Time | above | — | Set Fan | ✓ | 100 |
