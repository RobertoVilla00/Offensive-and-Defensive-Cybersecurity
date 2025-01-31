import angr
import claripy

proj = angr.Project('./revmem', auto_load_libs=False)

# Crea l'argomento simbolico con vincoli sui singoli caratteri
argv = ['./revmem']
chars = [claripy.BVS('c%d' % i, 8) for i in range(33)] # 33 bytes
input_str = claripy.Concat(*chars + [claripy.BVV(b'\n')]) # + \n
argv.append(input_str)
initial_state = proj.factory.entry_state(args=argv,add_options={angr.options.LAZY_SOLVES})
#initial_state.options.add(angr.options.SYMBOL_FILL_UNCONSTRAINED_MEMORY)


for i in range(33):
    initial_state.solver.add(chars[i] == ord("flag{this_was_a_bit_more_complex}"[i]))

for c in chars: # make sure all chars are printable
 initial_state.solver.add(c >= 0x20, c <= 0x7e)
 
simgr = proj.factory.simulation_manager(initial_state)

to_avoid=[0x40134b, 0x401247, 0x40124c]
simgr.explore(find=0x401376,avoid=to_avoid)  # esplora fino a target_function_address evitando l'altro indirizzo di puts
if simgr.found:
    found = simgr.found[0]
    print(found.solver.eval(argv[1], cast_to=bytes))  # eval
