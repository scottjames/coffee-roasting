# Artisan Alarm: trigger-alarms-brazil-200g

| # | On | Phase | Offset | Guard | NegGuard | Source | Cond | Temp° | Action | Beep | Label |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | ✓ | CHARGE | 00:02 | — | — | Time | below | 500 | Set Burner | ✗ | 0 # soak |
| 2 | ✓ | CHARGE | 00:05 | — | — | Time | below | 500 | Set Fan | ✗ | 20 # soak |
| 3 | ✓ | CHARGE | 01:30 | — | — | Time | below | 500 | Set Burner | ✗ | 60 |
| 4 | ✓ | CHARGE | 01:35 | — | — | Time | below | 500 | Set Fan | ✗ | 50 |
| 5 | ✓ | CHARGE | 00:00 | — | — | BT | below | 130 | Set Burner | ✗ | 40 |
| 6 | ✓ | CHARGE | 00:00 | — | — | BT | below | 130 | Set Fan | ✗ | 70 |
| 7 | ✓ | CHARGE | 00:00 | — | — | BT | below | 165 | Set Burner | ✗ |  |
| 8 | ✓ | CHARGE | 00:00 | — | — | BT | below | 165 | Set Burner | ✗ |  |
| 9 | ✓ | FC START | 00:10 | — | — | Time | below | — | Set Burner | ✗ | 20 |
| 10 | ✓ | FC START | 00:15 | — | — | Time | below | — | Set Burner | ✗ | 80 |
| 11 | ✓ | CHARGE | 00:00 | — | — | BT | below | 182 | Pop-up message | ✓ | "DROP NOW" |
| 12 | ✓ | DROP | 00:01 | — | — | Time | below | — | Set Burner | ✗ | 0 |
| 13 | ✓ | DROP | 00:05 | — | — | Time | below | — | Set Fan | ✗ | 100 |
| 14 | ✓ | DROP | 00:05 | — | — | Time | below | — | Set Fan | ✗ | 100 |
