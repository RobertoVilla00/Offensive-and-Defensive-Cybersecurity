import angr
import claripy


proj = angr.Project('./keycheck_baby',auto_load_libs=False)

chars = [claripy.BVS('c%d' % i, 8) for i in range(31)] # 31 bytes)
newline_char = claripy.BVV(b'\n')  # 1 byte for newline
input_str = claripy.Concat(*chars + [newline_char])
stdin_stream = angr.SimFileStream(name='stdin',content=input_str)
initial_state = proj.factory.entry_state(stdin=stdin_stream, add_options={angr.options.LAZY_SOLVES})
initial_state.options.add(angr.options.SYMBOL_FILL_UNCONSTRAINED_MEMORY)

for c in chars: # make sure all chars are printable
 initial_state.solver.add(c >= 0x20, c <= 0x7e)


simgr = proj.factory.simulation_manager(initial_state)


to_find = [0x40145b] 
#to_avoid = [0x400e73]
simgr.explore(find=to_find)

if simgr.found:
    print(simgr.found[0].posix.dumps(0))

else: 
    print("ciao") 