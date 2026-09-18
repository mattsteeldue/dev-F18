import sys; sys.path.insert(0,r'C:/zx/forth/f18/tools/vforth/emu')
import repl
repl.IDLE_INSTRS = 20_000_000
r = repl.Repl()
r.boot(); r._drain()
for l in ["INCLUDE demo/chomp-chomp.f", "", "", "", "DECIMAL HERE U. HP@ U. R0 @ U.", "HP@ U.", "HERE U."]:
    r.emu.queue_input(l); ok=r._run_to_prompt(); print(repr(r._drain()[-300:])); 
    if not ok: print("STOPPED"); break
