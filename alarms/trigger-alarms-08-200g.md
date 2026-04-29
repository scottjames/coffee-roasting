# Artisan Alarm: trigger-alarms-08-200g

| # | On | Phase | Offset | Guard | NegGuard | Source | Cond | Temp° | Action | Beep | Label |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | ✓ | CHARGE | 00:08 | — | — | BT | below | 150 | Pop-up message | ✓ | 150 Ready Charge |
| 2 | ✓ | CHARGE | 00:02 | — | — | Time | above | — | Set Fan | ✓ | 50 # soak |
| 3 | ✓ | CHARGE | 00:07 | — | — | Time | above | — | Set Burner | ✓ | 40  # soak |
| 4 | ✓ | CHARGE | 00:25 | — | — | Time | above | — | Set Burner | ✓ | 75 # convection |
| 5 | ✓ | CHARGE | 00:30 | — | — | Time | above | — | Set Fan | ✓ | 70 # convection |
| 6 | ✓ | TP | 00:07 | — | — | Time | above | — | Set Burner | ✓ | 65 |
| 7 | ✓ | TP | 00:30 | — | — | Time | above | — | Set Burner | ✓ | 60 |
| 8 | ✓ | TP | 01:00 | — | — | Time | above | — | Set Fan | ✓ | 80 |
| 9 | ✓ | DRY END | 00:07 | — | — | Time | above | — | Set Burner | ✓ | 55 |
| 10 | ✓ | FC START | 01:00 | — | — | Time | above | — | Set Burner | ✓ | 50 |
| 11 | ✓ | FC START | 01:30 | — | — | Time | above | — | Pop-up message | ✓ | Drop around 10:30 |
| 12 | ✓ | DROP | 00:01 | — | — | Time | above | — | Set Burner | ✓ | 0 |
| 13 | ✓ | DROP | 00:02 | — | — | Time | above | — | Set Fan | ✓ | 100 |
