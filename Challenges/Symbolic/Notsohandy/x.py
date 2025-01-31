import angr
import claripy
import logging
#logging.getLogger("angr").setLevel(logging.DEBUG)
proj = angr.Project('./notsohandy', auto_load_libs=False)

def print_chars(state):
    # Recupera il valore attuale delle variabili simboliche e stampale
    current_chars = state.solver.eval(state.memory.load(state.regs.rdi, len(chars)), cast_to=bytes)
    print("Current value of chars:", current_chars)


# Crea l'argomento simbolico con vincoli sui singoli caratteri
argv = ['./notsohandy']
chars = [claripy.BVS('c%d' % i, 8) for i in range(20)] # 20 bytes
input_str = claripy.Concat(*chars + [claripy.BVV(b'\n')]) # + \n
argv.append(input_str)
initial_state = proj.factory.entry_state(args=argv,add_options={angr.options.LAZY_SOLVES})
initial_state.options.add(angr.options.ZERO_FILL_UNCONSTRAINED_MEMORY)

for c in chars: # make sure all chars are printable
 initial_state.solver.add(c >= 0x20, c <= 0x7e)

for i in range(5):
    initial_state.solver.add(chars[i] == ord("flag{"[i]))

initial_state.inspect.b('mem_write', when=angr.BP_BEFORE, action=print_chars)

simgr = proj.factory.simulation_manager(initial_state)

to_avoid=[0x40129b,0x4013d2]
simgr.explore(find=0x401422, avoid=to_avoid)  # esplora fino a target_function_address evitando l'altro indirizzo di puts
if simgr.found:
    found = simgr.found[0]
    print(found.solver.eval(argv[1], cast_to=bytes))  # eval
