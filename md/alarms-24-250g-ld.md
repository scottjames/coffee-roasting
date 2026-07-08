# Artisan Alarm: alarms-24-250g-ld

| # | On | Phase | Offset | Guard | NegGuard | Source | Cond | Temp° | Action | Beep | Label |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | ✓ | CHARGE | 00:00 | — | — | BT | below | 130 | Pop-up message | ✓ | 130 Ready Charge 250gm (A24) LD |
| 2 | ✓ | CHARGE | 00:02 | — | — | Time | above | — | Set Fan | ✓ | 30 # soak |
| 3 | ✓ | CHARGE | 00:03 | — | — | Time | above | — | Set Burner | ✓ | 60  # |
| 4 | ✓ | CHARGE | 00:20 | — | — | Time | above | — | Set Burner | ✓ | 80 # convection |
| 5 | ✓ | CHARGE | 00:25 | — | — | Time | above | — | Set Fan | ✓ | 60 # convection |
| 6 | ✓ | TP | 01:15 | — | — | Time | above | — | Set Burner | ✓ | 75 |
| 7 | ✓ | TP | 02:00 | — | — | Time | above | — | Set Burner | ✓ | 70 |
| 8 | ✓ | TP | 02:20 | — | — | Time | above | — | Set Fan | ✓ | 70 |
| 9 | ✓ | TP | 02:40 | — | — | Time | above | — | Set Burner | ✓ | 65 |
| 10 | ✓ | TP | 03:30 | — | — | Time | above | — | Set Burner | ✓ | 60 # lower B60 earlier |
| 11 | ✗ | TP | 04:00 | — | — | Time | above | — | Set Fan | ✓ | 80 # no |
| 12 | ✗ | DRY END | 00:10 | — | — | Time | above | — | Set Burner | ✓ | 65 # no |
| 13 | ✗ | DRY END | 00:30 | — | — | Time | above | — | Set Burner | ✓ | 60 # no |
| 14 | ✓ | DRY END | 02:30 | — | — | Time | Cond(3) | — | Set Burner | ✓ | 55 # pre-FC |
| 15 | ✓ | FC START | 00:45 | — | — | Time | above | — | Set Burner | ✓ | 50  # dont stall FC |
| 16 | ✓ | FC START | 01:00 | — | — | Time | above | — | Pop-up message | ✓ | Drop around 1:30 devel by 194+ (avoid FLICK) |
| 17 | ✓ | FC START | 01:10 | — | — | Time | above | — | Set Burner | ✓ | 45 # late devel avoid ashy |
| 18 | ✓ | FC END | 00:05 | — | — | Time | above | — | Set Burner | ✓ | 40 # late devel avoid ashy |
| 19 | ✓ | DROP | 00:01 | — | — | Time | above | — | Set Burner | ✓ | 0 |
| 20 | ✓ | DROP | 00:10 | — | — | Time | above | — | Set Fan | ✓ | 100 |
| 21 | ✓ | COOL END | 00:15 | — | — | Time | above | — | Set Burner | ✓ | 20 # BTB |
| 22 | ✓ | COOL END | 00:20 | — | — | Time | above | — | Set Fan | ✓ | 30 # BTB |
