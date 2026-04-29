# Artisan Alarm: trigger-alarms-10-200g

| # | On | Phase | Offset | Guard | NegGuard | Source | Cond | Temp° | Action | Beep | Label |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | ✓ | CHARGE | 00:08 | — | — | BT | below | 150 | Pop-up message | ✓ | 150 Ready Charge 200gm |
| 2 | ✓ | CHARGE | 00:02 | — | — | Time | above | — | Set Fan | ✓ | 30 # soak |
| 3 | ✓ | CHARGE | 00:07 | — | — | Time | above | — | Set Burner | ✓ | 30  # soak |
| 4 | ✓ | CHARGE | 00:45 | — | — | Time | above | — | Set Burner | ✓ | 65 # convection |
| 5 | ✓ | CHARGE | 00:55 | — | — | Time | above | — | Set Fan | ✓ | 60 # convection |
| 6 | ✓ | TP | 00:15 | — | — | Time | above | — | Set Burner | ✓ | 65 |
| 7 | ✓ | TP | 01:00 | — | — | Time | above | — | Set Burner | ✓ | 60 |
| 8 | ✓ | TP | 01:30 | — | — | Time | above | — | Set Fan | ✓ | 70 |
| 9 | ✓ | DRY END | 00:15 | — | — | Time | above | — | Set Burner | ✓ | 55 |
| 10 | ✓ | DRY END | 01:00 | — | — | Time | above | — | Set Burner | ✓ | 50 |
| 11 | ✓ | FC START | 00:30 | — | — | Time | above | — | Set Fan | ✓ | 80 |
| 12 | ✓ | FC START | 00:45 | — | — | Time | above | — | Set Burner | ✓ | 50 # afraid to stall with 45 |
| 13 | ✓ | FC START | 01:30 | — | — | Time | above | — | Pop-up message | ✓ | Drop around 10:30, by 187C |
| 14 | ✓ | DROP | 00:01 | — | — | Time | above | — | Set Burner | ✓ | 0 |
| 15 | ✓ | DROP | 00:10 | — | — | Time | above | — | Set Fan | ✓ | 100 |
| 16 | ✓ | COOL END | 00:15 | — | — | Time | above | — | Set Burner | ✓ | 20 # BTB |
| 17 | ✓ | COOL END | 00:20 | — | — | Time | above | — | Set Fan | ✓ | 30 # BTB |
