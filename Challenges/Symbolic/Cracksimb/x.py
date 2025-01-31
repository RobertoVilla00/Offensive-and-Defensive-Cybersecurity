import angr
import claripy

proj = angr.Project('./cracksymb',auto_load_libs=False)

chars = [claripy.BVS('c%d' % i, 8) for i in range(23)] # 20 bytes)
newline_char = claripy.BVV(b'\n')  # 1 byte for newline
input_str = claripy.Concat(*chars + [newline_char])
stdin_stream = angr.SimFileStream(name='stdin', content=input_str, has_end=False)
initial_state = proj.factory.entry_state(stdin=stdin_stream, add_options={angr.options.LAZY_SOLVES})
for c in chars: # make sure all chars are printable
 initial_state.solver.add(c >= 0x20, c <= 0x7e)
simgr = proj.factory.simulation_manager(initial_state)



to_find = [0x4033c2, 0x403370] # 0x403370 non necessario
to_avoid = [0x4033d0,0x403369,0x40317c,0x402f79,0x402d77,0x402b7c,0x40297c,0x402781,0x402576,0x402379,0x402181,0x401f7d,0x401d7a,0x401b6d,0x401978,0x40177f,0x401592,0x40139d,0x4011af,0x400fac,0x400da6,0x400bad,0x4009ac]
simgr.explore(find=to_find, avoid=to_avoid)

if simgr.found:
 print(simgr.found[0].posix.dumps(0))

else: 
    print("ciao") 


# con to_avoid funziona, ma sembra più lento rispetto ad usare solo to_find    