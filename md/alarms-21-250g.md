# Artisan Alarm: alarms-21-250g

| # | On | Phase | Offset | Guard | NegGuard | Source | Cond | Temp° | Action | Beep | Label |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | ✓ | CHARGE | 00:04 | — | — | BT | below | 130 | Pop-up message | ✓ | 130 Ready Charge 250gm (A21) |
| 2 | ✓ | CHARGE | 00:02 | — | — | Time | above | — | Set Fan | ✓ | 30 # soak |
| 3 | ✓ | CHARGE | 00:08 | — | — | Time | above | — | Set Burner | ✓ | 60  # |
| 4 | ✓ | CHARGE | 00:15 | — | — | Time | above | — | Set Burner | ✓ | 80 # convection |
| 5 | ✓ | CHARGE | 00:25 | — | — | Time | above | — | Set Fan | ✓ | 60 # convection |
| 6 | ✓ | TP | 00:30 | — | — | Time | above | — | Set Burner | ✓ | 75 |
| 7 | ✓ | TP | 01:15 | — | — | Time | above | — | Set Burner | ✓ | 70 |
| 8 | ✗ | TP | 02:00 | — | — | Time | above | — | Set Burner | ✓ | 65 # no |
| 9 | ✓ | TP | 02:30 | — | — | Time | above | — | Set Fan | ✓ | 70 |
| 10 | ✓ | TP | 03:00 | — | — | Time | above | — | Set Burner | ✓ | 65 |
| 11 | ✗ | TP | 04:00 | — | — | Time | above | — | Set Fan | ✓ | 80 # no |
| 12 | ✗ | DRY END | 00:45 | — | — | Time | above | — | Set Burner | ✓ | 65 # no |
| 13 | ✓ | DRY END | 01:30 | — | — | Time | above | — | Set Burner | ✓ | 60 # at BT 170 |
| 14 | ✓ | DRY END | 02:30 | — | — | Time | Cond(3) | — | Set Burner | ✓ | 55 |
| 15 | ✓ | FC START | 01:15 | — | — | Time | above | — | Set Burner | ✓ | 50  # dont stall FC |
| 16 | ✓ | FC START | 01:20 | — | — | Time | above | — | Pop-up message | ✓ | Drop around 10:30, by 190+ |
| 17 | ✓ | FC END | 00:05 | — | — | Time | above | — | Set Burner | ✓ | 45 # late devel |
| 18 | ✓ | DROP | 00:01 | — | — | Time | above | — | Set Burner | ✓ | 0 |
| 19 | ✓ | DROP | 00:10 | — | — | Time | above | — | Set Fan | ✓ | 100 |
| 20 | ✓ | COOL END | 00:15 | — | — | Time | above | — | Set Burner | ✓ | 20 # BTB |
| 21 | ✓ | COOL END | 00:20 | — | — | Time | above | — | Set Fan | ✓ | 30 # BTB |
