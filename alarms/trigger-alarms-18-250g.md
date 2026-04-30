# Artisan Alarm: trigger-alarms-18-250g

| # | On | Phase | Offset | Guard | NegGuard | Source | Cond | Temp° | Action | Beep | Label |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | ✓ | CHARGE | 00:04 | — | — | BT | below | 140 | Pop-up message | ✓ | 140 Ready Charge 250gm (A18) |
| 2 | ✓ | CHARGE | 00:02 | — | — | Time | above | — | Set Fan | ✓ | 30 # soak |
| 3 | ✓ | CHARGE | 00:07 | — | — | Time | above | — | Set Burner | ✓ | 30  # soak |
| 4 | ✓ | CHARGE | 00:15 | — | — | Time | above | — | Set Burner | ✓ | 75 # convection |
| 5 | ✓ | CHARGE | 00:30 | — | — | Time | above | — | Set Fan | ✓ | 60 # convection |
| 6 | ✓ | TP | 01:30 | — | — | Time | above | — | Set Burner | ✓ | 70 |
| 7 | ✓ | TP | 02:00 | — | — | Time | above | — | Set Burner | ✓ | 65 |
| 8 | ✓ | TP | 02:15 | — | — | Time | above | — | Set Fan | ✓ | 70 |
| 9 | ✓ | TP | 02:30 | — | — | Time | above | — | Set Burner | ✓ | 65 |
| 10 | ✓ | DRY END | 00:30 | — | — | Time | above | — | Set Burner | ✓ | 60 |
| 11 | ✓ | DRY END | 01:00 | — | — | BT | below | 170 | Set Burner | ✓ | 60 |
| 12 | ✓ | DRY END | 01:45 | — | — | Time | above | — | Set Burner | ✓ | 55 |
| 13 | ✓ | DRY END | 02:15 | — | — | Time | above | — | Set Fan | ✓ | 80 |
| 14 | ✓ | FC START | 01:00 | — | — | Time | above | — | Set Burner | ✓ | 55 # dont stall FC |
| 15 | ✓ | FC START | 01:30 | — | — | Time | above | — | Pop-up message | ✓ | Drop around 10:30, by 188+ |
| 16 | ✓ | FC START | 02:30 | — | — | Time | above | — | Set Burner | ✓ | 45 # late devel |
| 17 | ✓ | DROP | 00:01 | — | — | Time | above | — | Set Burner | ✓ | 0 |
| 18 | ✓ | DROP | 00:10 | — | — | Time | above | — | Set Fan | ✓ | 100 |
| 19 | ✓ | COOL END | 00:15 | — | — | Time | above | — | Set Burner | ✓ | 20 # BTB |
| 20 | ✓ | COOL END | 00:20 | — | — | Time | above | — | Set Fan | ✓ | 30 # BTB |
