# Artisan Alarm: trigger-alarms-07-200g

| # | On | Phase | Offset | Guard | NegGuard | Source | Cond | Temp° | Action | Beep | Label |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | ✓ | CHARGE | 00:08 | — | — | BT | below | 130 | Pop-up message | ✓ | 130 Ready Charge |
| 2 | ✓ | CHARGE | 00:02 | — | — | Time | above | — | Set Fan | ✓ | 50 |
| 3 | ✓ | CHARGE | 00:05 | — | — | Time | above | — | Set Burner | ✓ | 40  # soak |
| 4 | ✓ | CHARGE | 00:20 | — | — | Time | above | — | Set Burner | ✓ | 70 |
| 5 | ✓ | CHARGE | 00:30 | — | — | Time | above | — | Set Fan | ✓ | 60 |
| 6 | ✓ | CHARGE | 01:30 | — | — | Time | above | — | Set Burner | ✓ | 65 |
| 7 | ✗ | CHARGE | 01:45 | — | — | Time | above | — | Set Fan | ✓ | 70 |
| 8 | ✗ | CHARGE | 02:15 | — | — | Time | above | — | Set Burner | ✓ | 55 |
| 9 | ✗ | CHARGE | 02:30 | — | — | Time | above | — | Set Fan | ✓ | 70 |
| 10 | ✗ | FC START | 01:15 | — | — | Time | above | — | Set Burner | ✓ | 45 |
| 11 | ✗ | FC START | 01:30 | — | — | Time | above | — | Set Fan | ✓ | 70 |
| 12 | ✗ | FC START | 02:00 | — | — | Time | above | — | Set Burner | ✓ | 50 |
| 13 | ✓ | CHARGE | 10:00 | — | — | Time | above | — | Pop-up message | ✓ | Drop by 10:30 |
| 14 | ✓ | DROP | 00:01 | — | — | Time | above | — | Set Burner | ✓ | 0 |
| 15 | ✓ | DROP | 00:02 | — | — | Time | above | — | Set Fan | ✓ | 100 |
