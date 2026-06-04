# Testing vForth Tutorials with the Emulator

This guide explains how to use the interactive REPL to load and test the vForth tutorials.

## Quick Start

1. Start the interactive REPL:
   ```bash
   python emu/interactive_test.py
   ```

2. You'll see the Forth prompt:
   ```
   forth>
   ```

3. Load a tutorial file:
   ```
   forth> INCLUDE tutorial/001-stack-basics.f
   ```

4. You should see the tutorial banner:
   ```
   --- Tutorial 001: stack basics loaded.
       Type NEWTASK to unload.
   ```

5. Follow the instructions in the tutorial and try the examples:
   ```
   forth> 42 .
   42

   forth> 3 4 +  .
   7
   ```

6. To unload the tutorial and reload it:
   ```
   forth> NEWTASK
   ```

7. To exit the REPL:
   ```
   forth> quit
   ```

## Available Tutorials (in recommended order)

| File | Topic | Difficulty |
|------|-------|------------|
| `001-stack-basics.f` | Stack operations, basic arithmetic | Beginner |
| `002-stack-ops.f` | Stack manipulation (DUP, DROP, SWAP, etc.) | Beginner |
| `003-output.f` | Output formatting (., .S, CR, etc.) | Beginner |
| `004-numeric-bases.f` | Hex, binary, decimal number bases | Beginner |
| `005-defining-words.f` | Creating your own words with `:` | Beginner |
| `006-control-flow.f` | IF/THEN/ELSE conditionals | Beginner |
| `007-loops.f` | DO/LOOP, BEGIN/UNTIL, REPEAT | Beginner |
| `008-memory.f` | Memory access (!, @, ALLOT) | Intermediate |
| `009-strings.f` | String handling | Intermediate |
| `010-create-does.f` | CREATE...DOES> data structures | Intermediate |

## REPL Commands

While in the interactive REPL, you can use these debugging commands:

- `<word> ...` — Execute Forth words/code
- `reset` — Reinitialize the emulator
- `status` — Show CPU state (registers, PC, instruction count)
- `memory ADDR LEN` — Dump memory (both hex)
- `stack` — Show data stack contents
- `help` — Show available commands
- `quit` — Exit the REPL

## Example Session

```
=== vForth Interactive Emulator (Phase B) ===
Loading binaries...

[OK] Binaries loaded
[OK] Cold start at PC=$639A

Type Forth words and press Enter
Commands: 'quit' to exit, 'reset' to reinit, 'status' for CPU state

forth> INCLUDE tutorial/001-stack-basics.f

--- Tutorial 001: stack basics loaded.
    Type NEWTASK to unload.

forth> 42 .
42
forth> 3 4 +  .
7
forth> 10 3 - .
7
forth> 22 7 /MOD . .
1 3
forth> status
PC=$5449  BC=$0002  DE=$D398  HL=$0007  SP=$D2F8
IX=$639A  A=$00
Instructions executed: 1234567

forth> quit
Exiting...
Test complete
```

## Implementation Details

### How INCLUDE Works

1. **File opening**: `OPEN< filename` returns a file handle
2. **Line reading**: `F_GETLINE` reads one line at a time into BLOCK 1
3. **Interpretation**: Each line is interpreted via the `INTERPRET` word
4. **Loop**: Repeats until end-of-file

### Tutorial Structure

Each tutorial file:
- Starts with `MARKER NEWTASK` to enable reloading
- Has a load banner via `.( ... )`
- Contains numbered sections with examples
- Defines demonstration words (usually prefixed with `.`)
- Ends with optional commented-out test block

### Expected Output

When you load a tutorial, you should see:
```
CR (blank line)
--- Tutorial NNN: title loaded.
    Type NEWTASK to unload.
```

This output comes from the `.( )` (print on load) directives in the tutorial file.

## Troubleshooting

### "File not found" error
- Check that the tutorial file exists in `tutorial/` directory
- Use the full path: `INCLUDE tutorial/001-stack-basics.f`
- Verify no typos in the filename

### Emulator hangs
- Press Ctrl+C to interrupt
- Type `reset` to reinitialize
- Check that the command wasn't waiting for more input

### Stack overflow / underflow
- Type `stack` to inspect the current stack state
- Type `reset` to clear and start fresh
- Some tutorials intentionally demonstrate error conditions

### Output formatting issues
- If output looks garbled, the character encoding may be mismatched
- Tutorials use 7-bit ASCII only
- Check that your terminal/console supports ASCII output

## Performance Notes

The emulator runs at approximately **1.2 million instructions/second** on modern hardware.
Long-running tutorials should complete in a few seconds. If a tutorial takes >10 seconds,
it may be stuck in an infinite loop.

## Advanced: Session Recording

You can record your tutorial session to a transcript file:

```python
# In interactive_test.py, before starting the REPL:
emu.start_session_recording("tutorial_session.txt")
# ... interact with tutorials ...
emu.stop_session_recording()
```

The transcript file will contain timestamped records of all input and output.
