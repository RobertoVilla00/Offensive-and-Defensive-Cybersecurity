import angr
import claripy
#import logging
#logging.getLogger("angr").setLevel(logging.DEBUG)

proj = angr.Project('./crackme', auto_load_libs=False)

# Crea l'argomento simbolico con vincoli sui singoli caratteri
argv = ['./crackme']
chars = [claripy.BVS('c%d' % i, 8) for i in range(36)] # 33 bytes
input_str = claripy.Concat(*chars + [claripy.BVV(b'\n')]) # + \n
argv.append(input_str)
initial_state = proj.factory.entry_state(args=argv,add_options={angr.options.LAZY_SOLVES})
#initial_state.options.add(angr.options.SYMBOL_FILL_UNCONSTRAINED_MEMORY)



for c in chars: # make sure all chars are printable
 initial_state.solver.add(c >= 0x20, c <= 0x7e)
 
simgr = proj.factory.simulation_manager(initial_state)


#to_avoid=[0x40134b, 0x401247, 0x40124c]
to_find=[0x401845]
simgr.explore(find=to_find)  # esplora fino a target_function_address evitando l'altro indirizzo di puts


if simgr.found:
    found = simgr.found[0]
    print(found.solver.eval(argv[1], cast_to=bytes))  # eval
