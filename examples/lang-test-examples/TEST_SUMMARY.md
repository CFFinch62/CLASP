# CLASP Logo Language Compliance Report

| Test File                      | Status | Error |
|--------------------------------|--------|-------|
| test_01_data_constructors.logo | PASS   | None  |
| test_02_data_selectors.logo    | PASS   | None  |
| test_03_predicates.logo        | PASS   | None  |
| test_04_arithmetic.logo        | FAIL   |  File <string>, line 7 print sum 3 5 ^ Logo error:  File <string>, line 7 print sum 3                |
| test_05_trig_math.logo         | FAIL   |  File <string>, line 20   ^ Unexpected end of line error: The end of the line was not expected       |
| test_06_logic_bitwise.logo     | FAIL   |  File <string>, line 20 print bitand 5 3  ; 101 & 011 = 001 (1) ^ Logo error:                        |
| test_07_control_flow.logo      | FAIL   |  File <string>, line 41 ]   ^ Unexpected end of code block error: Not enough arguments provided to c |
| test_08_procedures_scope.logo  | PASS   | None  | 
| test_09_io.logo                | FAIL   |  File <string>, line 15   ^ Unexpected end of line error: The end of the line was not expected       |
| test_10_turtle_advanced.logo   | FAIL   |  File <string>, line 13 label [Starting Advanced Graphics Test] ^ Name not found error: I don't      |


Test	        Status	Note
01, 02, 03, 08	PASS	Core data structures and procedures work perfectly
04 (Arithmetic)	FAIL	sum parsing issue
05, 06, 09	    FAIL	Syntax/parsing issues with specific commands
07 (Control)	FAIL	catch/throw argument handling
10 (Graphics)	FAIL	Missing label command